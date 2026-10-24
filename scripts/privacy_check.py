#!/usr/bin/env python3
"""Heuristic privacy scan; semantic review is mandatory before publication."""
import argparse
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
    found = ['email address in content'] if EMAIL.search(text) else []
    found.extend(label for label, pattern in PATTERNS.items() if pattern.search(text))
    return found

def noreply(address):
    return bool(re.fullmatch(r'[A-Za-z0-9._+%-]+@users\.noreply\.github\.com', address)) or address == 'noreply' + '@github.com'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def scan(history=False, allow_commit_email=False):
    failures = []
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT)
        if '.git' in rel.parts or '__pycache__' in rel.parts or not p.is_file():
            continue
        if p.is_symlink():
            failures.append(f'{rel}: symlink requires review'); continue
        if p.name == '.env' or p.name.startswith('.env.'):
            failures.append(f'{rel}: environment file'); continue
        try:
            body = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            failures.append(f'{rel}: binary file requires separate review'); continue
        failures.extend(f'{rel}: {label}' for label in issues(body))
    if history:
        try:
            commits = git('rev-list', '--all').decode().splitlines()
            seen = set()
            for sha in commits:
                meta = git('show', '-s', '--format=%ae%x00%ce%x00%B', sha).decode()
                author, committer, message = meta.split('\x00', 2)
                if not noreply(author) or not noreply(committer):
                    if allow_commit_email:
                        print(f'NOTICE: {sha[:12]} uses a commit-email exception; owner authorization must be verified separately.')
                    else:
                        failures.append(f'{sha[:12]}: non-noreply commit identity')
                failures.extend(f'{sha[:12]} message: {label}' for label in issues(message))
                for entry in git('ls-tree', '-r', '-z', sha).split(b'\0'):
                    if not entry: continue
                    header, path = entry.split(b'\t', 1)
                    _, kind, obj = header.split()
                    if kind != b'blob' or obj in seen: continue
                    seen.add(obj)
                    raw = git('cat-file', 'blob', obj.decode())
                    try: body = raw.decode('utf-8')
                    except UnicodeDecodeError:
                        failures.append(f'{sha[:12]} historical binary requires review'); continue
                    failures.extend(f'{sha[:12]} {path.decode()}: {label}' for label in issues(body))
        except (subprocess.CalledProcessError, ValueError):
            failures.append('Git history could not be audited')
    return failures

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--history', action='store_true')
    parser.add_argument('--allow-commit-email', action='store_true', help='Only for history already verified as covered by the maintainer email exception')
    args = parser.parse_args()
    findings = scan(args.history, args.allow_commit_email)
    for finding in findings: print(f'REVIEW: {finding}')
    if findings: raise SystemExit(1)
    print('Heuristic privacy checks passed; semantic privacy review remains required.')
