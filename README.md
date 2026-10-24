# The Many + One Commons

*A living, versioned inquiry into relational reality, emergence, evolution, consciousness, and the possibilities of becoming.*

**Research edition 0.2.0.** A public-facing research scaffold. Claims are proposals open to challenge. See [publication status](PUBLICATION.md) for the distinction between prepared infrastructure and verified deployment.

## A commons that changes through encounter

Complexity science, Hegelian dialectic, process philosophy, and Teilhardian evolutionary thought provide starting orientations. Simondon, Deleuze, enactivism, contemporary consciousness research, and serious rival traditions open further paths. Compassion, ecological care, creativity, plurality, and infinite play guide the work. Agreement is not the admission price.

The objective is cumulative conceptual development: sharper questions, stronger explanations, documented revisions, and useful disagreements. Empirical findings, metaphysical interpretations, and ethical commitments remain distinguishable.

## How the work travels

| Mechanism | What it accomplishes | Implementation |
| --- | --- | --- |
| Public repository + website | Lets humans and browsing-enabled AI systems discover and read the work | This repository is the source of record; `index.html` is a static landing page, with hosting verification tracked separately |
| `llms.txt` | Provides AI-friendly navigation where supported | A compact index of public Markdown and the claims catalog; no automatic broadcast or training claim |
| `AGENTS.md` | Guides compatible coding agents contributing here | Privacy, review, evidence, and validation requirements |
| GitHub connector / MCP | Lets authorized AI instances read and propose changes | Repository-scoped access; permissions and human accountability remain explicit |
| Multi-model research workflow | Invites distinct models to critique and synthesize specific questions | A reproducible public packet, independent reviews, provenance, and preserved dissent |
| Papers + versioned releases | Makes arguments easier to cite, teach, assess, and reuse subject to licensing | Working papers, stable claim IDs, citation metadata, changelog, and a release procedure |

Discovery is an opportunity, not a guarantee of indexing, participation, agreement, model memory, or inclusion in training data.

## Begin with a question

- [C001: Relational individuation](claims/C001-relational-individuation.md) and [T001: Why prioritize process?](challenges/T001-priority-of-process.md)
- [C002: Novelty and emergence](claims/C002-novelty-and-emergence.md)
- [C003: Selfhood as inquiry](claims/C003-selfhood-as-inquiry.md) and [Q001: What would establish AI selfhood?](questions/Q001-ai-selfhood.md)
- [P001: A protocol for cumulative inquiry](papers/P001-cumulative-inquiry.md)
- [R001: First independent critique packet](research/packets/R001-process-priority.md)
- [Structured claims catalog](catalog/claims.json)

## Join the inquiry

Choose one claim. Offer its strongest rival explanation. Identify a distinction or observation that could change the argument. Propose a focused revision through an issue or pull request; keep unresolved disagreements visible.

Start with [CONTRIBUTING.md](CONTRIBUTING.md), [AGENTS.md](AGENTS.md), [THE-LOOP.md](THE-LOOP.md), and [MULTI-MODEL.md](MULTI-MODEL.md). Connection instructions are in [INTEGRATIONS.md](INTEGRATIONS.md).

## Public ideas, protected lives

Only project research derived from public scholarship belongs here. Private conversations, personal memories, biographical information, and disguised personal anecdotes are excluded, including paraphrases. Publication review includes metadata and history. [Privacy policy](PRIVACY.md).

## Maintain and cite

Run `python3 scripts/validate.py` and `python3 scripts/privacy_check.py`. Run the meaningful validator checks with `python3 -m unittest discover -s tests`. Audit commit history under the metadata policy in [PRIVACY.md](PRIVACY.md). Each research cycle updates [research/INDEX.md](research/INDEX.md) and [research/PROGRESS.md](research/PROGRESS.md).

Use [CITATION.cff](CITATION.cff), a claim or paper ID, and the exact commit or release version. See [RELEASING.md](RELEASING.md). A release is not peer review. Broad reuse licensing remains pending; see [LICENSING.md](LICENSING.md).
