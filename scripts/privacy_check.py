#!/usr/bin/env python3
"""Heuristic privacy scan; semantic review is mandatory before publication."""
import argparse
import hashlib
import os
import stat
import unicodedata
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PATTERNS = {
    'private key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'GitHub token': re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})'),
    'AWS access identifier': re.compile(r'AKIA[A-Z0-9]{16}'),
    'API secret': re.compile(r'\bsk-[A-Za-z0-9_-]{20,}'),
    'local filesystem path': re.compile(r'/(?:Users|home|workspace/scratch)/[^\s]+'),
}

def issues(text):
    text = unicodedata.normalize('NFKC', text)
    found = ['email address in content'] if EMAIL.search(text) else []
    found.extend(label for label, pattern in PATTERNS.items() if pattern.search(text))
    if any(unicodedata.category(c) == 'Cf' for c in text):
        found.append('hidden format-control character')
    return found

def noreply(address):
    return bool(re.fullmatch(r'[A-Za-z0-9._+%-]+@users\.noreply\.github\.com', address)) or address == 'noreply' + '@github.com'

MAX_BYTES = 2097152


def label(value):
    # Never print the potentially sensitive path, author name, or matched bytes.
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root,
                                   stderr=subprocess.DEVNULL, timeout=30)


def scan(history=False, root=None):
    root = Path(root or ROOT)
    failures = []

    def report(identity, reason):
        failures.append(f'item {label(identity)}: {reason}')

    def inspect(identity, text):
        for reason in issues(text):
            report(identity, reason)

    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in list(dirs):
            path = Path(directory) / name
            rel = path.relative_to(root)
            if rel == Path('.git') or name == '__pycache__':
                dirs.remove(name)
                continue
            inspect(rel, str(rel))
            if path.is_symlink():
                report(rel, 'symlink directory rejected')
                dirs.remove(name)
        for name in names:
            path = Path(directory) / name
            rel = path.relative_to(root)
            if rel == Path('.git'):
                report(rel, 'Git indirection file rejected')
                continue
            inspect(rel, str(rel))
            if name == '.env' or name.startswith('.env.'):
                report(rel, 'environment file rejected')
                continue
            try:
                fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
                with os.fdopen(fd, 'rb') as stream:
                    info = os.fstat(stream.fileno())
                    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                        report(rel, 'nonregular or oversized file rejected')
                        continue
                    raw = stream.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    report(rel, 'oversized file rejected')
                    continue
                inspect(rel, raw.decode('utf-8'))
            except (OSError, UnicodeError):
                report(rel, 'unreadable, linked or binary file rejected')
    if history:
        try:
            commits = git(root, 'rev-list', '--all').decode().splitlines()
            seen = set()
            for sha in commits:
                meta = git(root, 'show', '-s', '--format=%an%x00%ae%x00%cn%x00%ce%x00%B', sha).decode()
                author_name, author, committer_name, committer, message = meta.split('\x00', 4)
                if not noreply(author) or not noreply(committer):
                    report(sha, 'non-noreply commit identity')
                inspect(sha, author_name + '\n' + committer_name + '\n' + message)
                for entry in git(root, 'ls-tree', '-r', '-z', sha).split(b'\0'):
                    if not entry:
                        continue
                    header, path = entry.split(b'\t', 1)
                    mode, kind, obj = header.split()
                    identity = sha + ':' + path.decode('utf-8')
                    inspect(identity, path.decode('utf-8'))
                    if mode not in {b'100644', b'100755'} or kind != b'blob':
                        report(identity, 'historical nonregular entry rejected')
                        continue
                    if obj in seen:
                        continue
                    seen.add(obj)
                    if int(git(root, 'cat-file', '-s', obj.decode())) > MAX_BYTES:
                        report(identity, 'historical oversized blob rejected')
                        continue
                    raw = git(root, 'cat-file', 'blob', obj.decode())
                    try:
                        inspect(identity, raw.decode('utf-8'))
                    except UnicodeError:
                        report(identity, 'historical binary requires review')
        except (subprocess.SubprocessError, OSError, UnicodeError, ValueError):
            report('history', 'Git history could not be audited')
    return failures


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--history', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT,
                        help='Scan another checkout as data using this trusted scanner')
    args = parser.parse_args()
    if not args.root.is_dir() or args.root.is_symlink():
        raise SystemExit('Invalid scan root')
    findings = scan(args.history, args.root)
    for finding in findings:
        print(f'REVIEW: {finding}')
    if findings:
        raise SystemExit(1)
    print('Heuristic privacy checks passed; semantic privacy review remains required.')
