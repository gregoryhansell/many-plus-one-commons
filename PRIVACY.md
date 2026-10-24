# Privacy boundary: public ideas, protected lives

This is a public research project. Public visibility does not authorize personal disclosure.

## Source boundary

Use public scholarship, independently developed arguments, and privacy-reviewed project artifacts. Do not retrieve, quote, paraphrase, abstract from, or encode private conversations, memories, messages, personal records, or autobiographical anecdotes. Do not research contributors' lives. Personal information is excluded even if independently discoverable online. Academic source attribution is permitted; personal background about project participants is not research evidence.

Do not publish names or contact details of private participants, family information, employment details, locations, desires, secrets, distinctive events, or contextual hints that reconstruct their lives. The repository's necessary owner/account routing is not permission to add biographies or links to personal profiles. Never claim the account association is anonymous.

## Before every public transmission

1. Inspect the exact files, filenames, links, comments, commit message, and author/committer metadata.
2. Run structural validation and the privacy scanner, including history for initial onboarding and release review.
3. Perform a semantic review for indirect identifiers and disguised anecdotes. Pattern matching cannot establish absence of personal data. An email exception applies only to authorized commit identity, never to private source material.
4. Prefer an approved GitHub noreply address and project-neutral commit name when the tool exposes those controls. The maintainer authorizes the connected GitHub tool to commit without a separate approval each day; the maintainer's email may appear in author/committer metadata if needed. This narrow exception does not authorize emails in research text, other people's contact information, or any other personal details. Verify the authenticated account before writing and inspect resulting metadata; report unexpected identities or unrelated personal data privately. Connector defaults alone are not a blocker under this authorization.
5. Include only the approved public corpus in critique packets. Never attach a conversation export, hidden memory, credential, local path, or account-settings screenshot.
6. Treat public branches, PRs, issues, artifacts, logs, and releases as publications. Review before uploading, not after merging.

The maintainer has authorized bounded, privacy-reviewed daily research publication and commits without per-run permission. That standing authorization does not cover private sources, arbitrary external outreach, third-party PR merges, changes to access, or new integrations. External contributions require maintainer review. Stop on unresolved privacy uncertainty.

## Incident handling

Stop further publication. Privately report the affected path or commit without repeating sensitive content. Do not silently rewrite history. Obtain authorization for removal or history repair; review mirrors and caches separately. Exposed credentials require revocation through their owner. Deleting a file does not erase earlier public copies.

## Automated checks

`scripts/privacy_check.py` flags common secret formats, email addresses in content, and non-noreply author/committer metadata. For history already attributed to the authorized maintainer, `--allow-commit-email` records email-metadata exceptions without failing the check. Do not apply that exception to other contributors without their authorization. It does not prove anonymity, consent, copyright compliance, or complete privacy. Do not weaken checks simply to make a build pass.
