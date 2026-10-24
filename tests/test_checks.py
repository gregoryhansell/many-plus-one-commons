import tempfile
import unittest
from pathlib import Path
from scripts.privacy_check import issues, noreply
from scripts.validate import check_link

class PublicationChecks(unittest.TestCase):
    def test_contact_details_rejected(self):
        self.assertIn('email address in content', issues('person'+'@'+'example.org'))
    def test_local_paths_rejected(self):
        self.assertIn('local filesystem path', issues('/work'+'space/scratch/private'))
    def test_secret_patterns_rejected(self):
        self.assertIn('GitHub token', issues('gh'+'p_'+'x'*36))
        self.assertIn('AWS access identifier', issues('AK'+'IA'+'A'*16))
    def test_noreply_identity_is_not_suffix_spoofable(self):
        self.assertTrue(noreply('123+project'+'@users.noreply.github.com'))
        self.assertFalse(noreply('person'+'@example.org'))
        self.assertFalse(noreply('123+project'+'@users.noreply.github.com.invalid'))
    def test_missing_and_escaping_links_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/'README.md';source.write_text('test')
            with self.assertRaises(AssertionError): check_link(source,'missing.md',root)
            with self.assertRaises(AssertionError): check_link(source,'../escape.md',root)
            check_link(source,'README.md',root)
    def test_executable_link_rejected(self):
        with self.assertRaises(AssertionError): check_link(Path('README.md'),'javascript:alert(1)')

if __name__=='__main__': unittest.main()
