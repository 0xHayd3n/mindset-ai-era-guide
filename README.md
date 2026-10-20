# MINDSET in the AI Era Guide

**An unofficial reading companion to Jorge Garza Ulloa's _7 Pillars for MINDSET in the AI - Era_.**

This guide explains the article's seven-part framework, its workplace examples, its assumptions, and the questions a careful reader should ask. It is written for people and AI agents. **The source proposes a mindset framework; it does not experimentally validate the framework. No research experiments or implementation replications were run for this repository.**

> **Credit belongs to Jorge Garza Ulloa**, the article's sole author. The affiliation printed in the article is Research Consulting Services, University of Texas El Paso, USA; the author is also identified as the corresponding author.
>
> _American Journal of Biomedical Science & Research_ **30(1), 947-952**, article AJBSR.MS.ID.003878. Received **27 January 2026**, published **4 February 2026**. [DOI](https://doi.org/10.34297/AJBSR.2026.30.003878) · [official publisher PDF](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf)
>
> Maintained by [0xHayd3n](https://github.com/0xHayd3n), with AI assistance. This companion is independent and is not endorsed by the author or publisher.

## The idea in one minute

The article asks readers to change how they work with AI, starting with human purposes rather than the arrival of another tool. It proposes seven mutually supporting habits: investigate, adapt toward a purpose, consider the wider system, define outcomes, organize collaboration, take responsibility for consequences, and build new arrangements. Its argument is that people should shape the setting in which AI is used, rather than merely accept generated outputs. [Abstract and introduction, PDF p. 1](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=1)

That is a useful proposal to discuss, but a proposal is different from a measured effect. The article supplies no intervention study, participant sample, benchmark, causal estimate, or controlled comparison of the seven pillars. Its strong claims about uniquely human abilities should therefore be read as the author's position, not as established capability boundaries. [Evidence and limitations](docs/04-evidence-and-limitations.md)

## Start reading

| Goal | Module |
| --- | --- |
| Understand the motivation, workforce scenarios, and vocabulary | [1. Context and concepts](docs/01-context-and-concepts.md) |
| Work through curiosity, adaptation, and systems thinking | [2. Pillars 1-3](docs/02-pillars-one-to-three.md) |
| Work through outcomes, collaboration, stewardship, and building | [3. Pillars 4-7](docs/03-pillars-four-to-seven.md) |
| Separate proposals, examples, statistics, and evidence | [4. Evidence and limitations](docs/04-evidence-and-limitations.md) |
| Locate every part of the article, Figure 1, and all 13 references | [5. Complete source map](docs/05-paper-map-and-references.md) |
| Apply the framework to an original worked example and plan evaluation | [6. Exercises and application](docs/06-exercises-and-application.md) |
| Read with an AI agent | [AGENTS.md](AGENTS.md), [LLMS.txt](LLMS.txt), [paper metadata](metadata/paper.json), [claim index](metadata/claims.json) |

**Short route:** README → pillars → evidence and limitations. **Source-first route:** keep the six-page publisher PDF open beside the source map. Page links use one-based PDF pages; printed pages run from 947 to 952.

## The seven pillars at a glance

The short explanations below are this companion's paraphrases. The detailed modules preserve the article's labels and source locations.

| Pillar | Central question | Source |
| --- | --- | --- |
| Deep curiosity | Which assumptions should I investigate before accepting this output? | [p. 2](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=2) |
| Adaptation with a purpose | What lasting purpose should a change serve? | [pp. 2-3](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=2) |
| Think of wide-open on completed systems | What happens outside the immediate task boundary? | [p. 3](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=3) |
| Lead with outcomes, not tools | Which result matters, and how would we recognize it? | [p. 3](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=3) |
| Collaborate with AI as a virtual teammate | How should work and review be divided? | [p. 3](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=3) |
| Ethics and stewardship as anchors | Who bears the consequences, and who remains responsible? | [p. 4](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=4) |
| A builder's mindset | What new arrangement should we create? | [p. 4](https://biomedgrid.com/pdf/AJBSR.MS.ID.003878.pdf#page=4) |

## Evidence boundaries

The **800% job-demand increase** discussed on PDF p. 5 is a secondary statistic repeated by the author, without a dataset, sampling method, or reproducible calculation in this article. The **60% intake-time reduction in 90 days** on p. 3 is an illustrative target, not an achieved study result. Neither number validates the seven pillars. The [claim metadata](metadata/claims.json) records these distinctions; an empirical-results array is deliberately empty.

## Use this repository with an agent

Ask the agent to read [AGENTS.md](AGENTS.md) first. A useful request is:

```text
Explain pillar 3 using the source map and publisher PDF.
Give the source page, distinguish the author's position from your inference,
and identify what evidence would be needed to test the claim.
Do not describe this framework as experimentally validated.
```

The guide includes [bibliographic metadata](metadata/paper.json), a [source register](metadata/sources.json), a [claim index](metadata/claims.json), [BibTeX](references/paper.bib), and [GitHub citation metadata](CITATION.cff). Cite **Garza Ulloa (2026)** when discussing the article.

## Provenance, licensing, and maintenance

The actual attached six-page PDF was read through Library. Its complete extracted text grounded the guide. The exact official publisher PDF was also retrieved for Figure 1 inspection; its 553,454-byte size matches the attachment's recorded size. A matching size is not a byte-equality check. The public PDF's SHA-256 and this distinction are recorded in [paper metadata](metadata/paper.json).

The article states **CC BY 4.0**. Original companion material is also **CC BY 4.0**; see [attribution and scope](ATTRIBUTION.md) and [LICENSE](LICENSE). This repository contains original explanations, not the PDF, its full text, or its original figure.

Run `python scripts/validate_repository.py` to check local links, anchors, page ranges, claims, source IDs, and citation consistency. These checks assess documentation integrity, not the truth of the framework. See [VERIFICATION.md](VERIFICATION.md) and [CONTRIBUTING.md](CONTRIBUTING.md).
