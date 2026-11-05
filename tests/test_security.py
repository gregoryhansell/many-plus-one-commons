import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from becoming import runner
from scripts import privacy_check


class RunnerBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.root = self.repo / 'becoming'
        (self.root / 'approved').mkdir(parents=True)
        self.manifest = self.base / 'approval.json'
        self.root_patch = patch.object(runner, 'ROOT', self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        (self.root / 'state.json').write_text(json.dumps({'seed_question': 'Public research'}))
        self.record = {'output': {k: 'Synthetic public text' for k in runner.FIELDS}}
        (self.root / 'approved/one.json').write_text(json.dumps(self.record))
        self.digest = self.approve()

    def approve(self):
        files = {n: hashlib.sha256((self.root / n).read_bytes()).hexdigest()
                 for n in ['state.json', 'approved/one.json']}
        self.manifest.write_text(json.dumps({'version': 1, 'files': files}))
        return hashlib.sha256(self.manifest.read_bytes()).hexdigest()

    def packet(self, condition='reasons'):
        return runner.packet_for(condition, self.manifest, self.digest)

    def test_valid_manifest_and_stateless_boundary(self):
        self.assertEqual(len(self.packet()['approved_prior_public_sessions']), 1)
        self.assertEqual(self.packet('stateless')['approved_prior_public_sessions'], [])

    def test_unlisted_record_not_read(self):
        (self.root / 'approved/unlisted.json').symlink_to(self.base / 'nonexistent')
        self.assertEqual(len(self.packet()['approved_prior_public_sessions']), 1)

    def test_changed_seed_and_record_rejected(self):
        for name in ['state.json', 'approved/one.json']:
            p = self.root / name
            original = p.read_bytes()
            p.write_bytes(original + b' ')
            with self.assertRaises(ValueError):
                self.packet()
            p.write_bytes(original)

    def test_leaf_symlink_rejected_even_with_matching_digest(self):
        target = self.base / 'outside.json'
        p = self.root / 'approved/one.json'
        target.write_bytes(p.read_bytes())
        p.unlink()
        p.symlink_to(target)
        with self.assertRaises(OSError):
            self.packet()

    def test_parent_symlink_rejected(self):
        (self.root / 'approved').rename(self.base / 'outside')
        (self.root / 'approved').symlink_to(self.base / 'outside', target_is_directory=True)
        with self.assertRaises(OSError):
            self.packet()

    def test_manifest_symlink_rejected(self):
        target = self.base / 'other.json'
        self.manifest.rename(target)
        self.manifest.symlink_to(target)
        with self.assertRaises(OSError):
            self.packet()

    def test_manifest_digest_and_location_rejected(self):
        with self.assertRaises(ValueError):
            runner.packet_for('reasons', self.manifest, '0' * 64)
        inside = self.repo / 'approval.json'
        inside.write_bytes(self.manifest.read_bytes())
        with self.assertRaises(ValueError):
            runner.packet_for('reasons', inside, self.digest)

    def test_duplicate_keys_and_oversize_rejected(self):
        with self.assertRaises(ValueError):
            runner.strict_json('{"key":1,"key":2}')
        p = self.base / 'large'
        p.write_bytes(b'x' * (runner.MAX_INPUT_BYTES + 1))
        with self.assertRaises(ValueError):
            runner.safe_read(p)

    def test_path_escape_rejected_before_read(self):
        self.manifest.write_text(json.dumps({'version': 1, 'files': {
            'state.json': '0' * 64, '../outside.json': '0' * 64}}))
        self.digest = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        with self.assertRaises(ValueError):
            self.packet()

    def test_missing_approval_never_calls_model(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'synthetic'}), patch.object(runner, 'call_model') as call:
            self.assertEqual(runner.main(['--model', 'synthetic-model']), 1)
            call.assert_not_called()

    def test_dry_run_never_reads_or_calls(self):
        with patch.object(runner, 'safe_read') as read, patch.object(runner, 'call_model') as call:
            self.assertEqual(runner.main(['--dry-run']), 0)
            read.assert_not_called()
            call.assert_not_called()

    def test_redirect_rejected(self):
        with self.assertRaises(OSError):
            runner.NoRedirect().redirect_request(None, None, None, None, None, None)


class ScannerBoundary(unittest.TestCase):
    def test_sensitive_filename_is_detected_and_redacted(self):
        with tempfile.TemporaryDirectory() as d:
            name = 'person' + '@' + 'example.org.txt'
            (Path(d) / name).write_text('Ordinary public text')
            findings = privacy_check.scan(root=d)
            self.assertTrue(findings)
            self.assertNotIn(name, str(findings))
            self.assertNotIn(str(d), str(findings))

    def test_directory_and_dangling_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'repo'
            root.mkdir()
            (root / 'outside').symlink_to(Path(d), target_is_directory=True)
            (root / 'missing').symlink_to(Path(d) / 'absent')
            self.assertEqual(len(privacy_check.scan(root=root)), 2)

    def test_format_controls_rejected(self):
        self.assertIn('hidden format-control character', privacy_check.issues('public' + chr(0x202E)))

    def test_candidate_python_is_never_executed_or_imported(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            marker = root / 'executed'
            evil = "from pathlib import Path\nPath(__file__).with_name('executed').touch()\n"
            (root / 'sitecustomize.py').write_text(evil)
            (root / 'json.py').write_text(evil)
            (root / 'privacy_check.py').write_text(evil)
            scanner = Path(privacy_check.__file__).resolve()
            result = subprocess.run([sys.executable, '-I', str(scanner), '--root', str(root)],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertFalse(marker.exists())

    def test_history_filename_and_identity_name_are_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)
            git('init', '-q')
            git('config', 'user.email', '123+project' + '@users.noreply.github.com')
            git('config', 'user.name', 'person' + '@example.org')
            filename = 'private' + '@example.org.txt'
            (root / filename).write_text('public')
            git('add', '.')
            git('commit', '-qm', 'synthetic test')
            (root / filename).unlink()
            git('add', '-u')
            git('commit', '-qm', 'remove synthetic file')
            findings = privacy_check.scan(history=True, root=root)
            self.assertTrue(findings)
            self.assertNotIn(filename, str(findings))
            self.assertNotIn('person' + '@example.org', str(findings))


if __name__ == '__main__':
    unittest.main()
