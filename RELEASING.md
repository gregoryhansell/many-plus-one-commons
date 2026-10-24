# Papers, citation, and versioned releases

## Research artifacts

- Research notes: `research/notes/YYYY-MM-DD-topic.md` with a precise question and source record.
- Claims and challenges: stable IDs in the existing directories.
- Working papers: `papers/P###-title.md`, labeled with review and evidence status.
- Releases: immutable version tags plus reviewed release notes and source archives, once publication tooling is available.

## Release checklist

1. Freeze the candidate commit and review every changed artifact for privacy, attribution, rights, and factual accuracy.
2. Run `python3 scripts/validate.py`, `python3 scripts/privacy_check.py` plus a history audit under `PRIVACY.md`, and meaningful tests. Audit generated assets too.
3. Update `VERSION`, `catalog/claims.json`, `CITATION.cff`, and `CHANGELOG.md` together. Identify new arguments, revised claims, retained disagreements, and unresolved limitations.
4. Verify the target repository and author/committer identities, preferring noreply and respecting only the authorized maintainer email exception. Publish a tag and GitHub release only through authorized tooling. Never fabricate a tag, release URL, review status, or DOI.
5. Re-fetch the release and verify its commit and assets. Until that succeeds, describe the version as a prepared research edition, not a published release.
6. Archive through a service such as Zenodo only after that service is separately authorized. DOI archiving is not configured by a citation file.

## Citation

Cite The Many + One Commons contributors as a collective project attribution, the artifact title/ID, and the exact commit or verified release. `CITATION.cff` offers machine-readable project citation with a preferred generic research-corpus citation. Add article-specific metadata when a paper is ready. No personal emails or biographical author profiles are required.

## Reuse

Public reading and citation do not themselves establish a broad reuse license. See `LICENSING.md`; do not label the project CC BY or MIT until those terms have been approved and their license texts added.
