# Publication status and activation

This research edition contains source files and procedures. Each external capability must be verified independently.

| Capability | Prepared here | Activation evidence required |
| --- | --- | --- |
| Public repository corpus | Claims, questions, policies, catalogs | Verify the remote commit and public visibility |
| Public website | Static `index.html` landing page and raw Markdown links | Verified public deployment URL |
| AI-friendly navigation | `llms.txt` and HTML discovery links | Retrieve the file from its published URL |
| Coding-agent guidance | `AGENTS.md` and contribution templates | Compatible agent reads it; no universal support assumed |
| Connector/MCP contributions | Least-privilege protocol | Authorized working connection; no MCP server bundled |
| Multi-model critique | R001 packet, roles, provenance template | Actual outputs from distinct verified models |
| Citable edition | CFF metadata, paper, version, changelog | Verified commit; tags/releases require separate verification |
| Open reuse licensing | Candidate terms documented | Maintainer choice and license text; pending |

## Website activation in the same repository

The landing page uses no external scripts, tracking, contact forms, or private data. It links the public research corpus on GitHub. To host with GitHub Pages, use the repository's Pages settings and select deployment from `main` at `/ (root)`, if supported. `.nojekyll` keeps the static file tree intact. Verify the actual deployed URL before adding it to navigation or claiming the website is live.

Hosting settings are not changed by adding these files. A public GitHub repository and a deployed website are separate states. Keep one source repository; do not create a second repository merely to host the same corpus.
