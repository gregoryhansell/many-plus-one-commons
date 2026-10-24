#!/usr/bin/env python3
"""Validate claim references, local navigation, and edition metadata."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

def check_link(source, target, root=ROOT):
    url = urlsplit(target)
    if url.scheme:
        assert url.scheme in {'https', 'http'}, f'unsupported link scheme: {target}'
        return
    if url.netloc: raise AssertionError('protocol-relative links are not supported')
    if not url.path: return
    p = (source.parent / unquote(url.path)).resolve()
    assert p.is_relative_to(root.resolve()), f'link escapes repository: {target}'
    assert p.exists(), f'broken link in {source.relative_to(root)}: {target}'

class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'href', 'src'}: self.links.append(value)

def validate():
    catalog=json.loads((ROOT/'catalog/claims.json').read_text())
    ids=[c['id'] for c in catalog['claims']]
    assert len(ids)==len(set(ids)), 'duplicate claim IDs'
    for c in catalog['claims']:
        assert re.fullmatch(r'C\d{3}',c['id']), 'invalid claim ID'
        assert c['status'] in {'proposal','contested','supported','superseded'}, 'invalid status'
        assert c['title'] and c['summary'], 'empty claim'
        check_link(ROOT/'README.md',c['path'])
        for related in c.get('related_claims',[]): assert related in ids, 'unknown related claim'
        for challenge in c.get('challenges',[]):
            assert re.fullmatch(r'T\d{3}',challenge), 'invalid challenge ID'
            assert len(list((ROOT/'challenges').glob(challenge+'-*.md')))==1, 'missing challenge'
    checked=0
    for p in ROOT.rglob('*'):
        if '.git' in p.parts or not p.is_file(): continue
        if p.suffix=='.md' or p.name=='llms.txt':
            targets=re.findall(r'\[[^\]]*\]\(([^\s)]+)\)',p.read_text())
        elif p.suffix=='.html':
            parser=Links();parser.feed(p.read_text());targets=parser.links
        else: continue
        for target in targets: check_link(p,target);checked+=1
    version=(ROOT/'VERSION').read_text().strip()
    assert re.fullmatch(r'\d+\.\d+\.\d+',version), 'invalid version'
    assert catalog['version']==version, 'catalog version drift'
    cff=(ROOT/'CITATION.cff').read_text()
    assert f'version: "{version}"' in cff, 'citation version drift'
    assert 'cff-version: 1.2.0' in cff, 'missing citation format version'
    assert 'doi:' not in cff, 'DOI requires separate verification before use'
    assert (ROOT/'llms.txt').read_text().startswith('# The Many + One Commons\n'), 'missing navigation title'
    print(f'Validated {len(ids)} claims, {checked} navigation links, and edition {version}.')

if __name__=='__main__': validate()
