# Source Evaluation & SIFT Verification Playbook

A foundational guide for establishing the epistemic integrity, credibility, and provenance of web sources using lateral reading, the SIFT framework, and hierarchical source tiering.

---

## 1. The SIFT Framework for Autonomous Information Evaluation

Created by digital literacy scholar Mike Caulfield, the **SIFT** framework replaces flawed, checklist-based evaluation with four active, investigative moves:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE 4 SIFT MOVES                                │
├────────────────────────────────────────────────────────────────────────┤
│ S — STOP                    → Check initial reaction, avoid anchor bias│
│ I — INVESTIGATE THE SOURCE  → Read laterally (what do OTHERS say?)     │
│ F — FIND BETTER COVERAGE    → Locate consensus, peer review, primaries │
│ T — TRACE CLAIMS TO ORIGIN  → Strip downstream spin, locate raw data   │
└────────────────────────────────────────────────────────────────────────┘
```

### Move 1: STOP
- **Epistemic Pause**: When encountering an astonishing, sensational, or convenient claim, pause before ingesting it into working memory.
- **Identify Emotional / Novelty Hooks**: Check whether the source employs rage-bait, clickbait headlines, or unverified leaks designed to elicit viral spread.
- **Calibrate Assumption**: Treat uncorroborated single-source claims as unverified hypotheses rather than established ground truth.

### Move 2: INVESTIGATE THE SOURCE (Lateral Reading)
- **The Vertical Reading Trap**: Never judge a website's credibility by looking *at* the website itself. Polished typography, slick logos, and crafted "About Us" pages are trivially fabricated by PR agencies and state actors.
- **The Lateral Reading Practice**: Open a new tab and search *about* the publisher or author:
  - Query: `"<publisher_domain>" bias OR funding OR controversy OR review`
  - Query: `"<author_name>" credentials OR publications OR affiliations`
- **Verify Organizational Motives**:
  - Is the publisher an industry lobbying group (501(c)(6)), a think tank with undisclosed corporate donors, or a vendor promoting their own commercial solution?
  - Does the site host affiliate links or sponsored comparison tables?

### Move 3: FIND BETTER COVERAGE
- If an unknown technical blog makes an assertion about an architecture flaw, look for recognized industry authorities:
  - Search: `<claim_keywords> site:cve.mitre.org OR site:news.ycombinator.com OR site:github.com`
- Check for **Evidentiary Consensus**:
  - Do established engineering teams, academic researchers, or standards bodies independently corroborate this claim?
  - Is the topic actively contested with ongoing public debates?

### Move 4: TRACE CLAIMS, QUOTES, AND MEDIA TO ORIGINAL CONTEXT
- Downstream journalism and blog summaries frequently telephone-game original studies or statements.
- **Trace the Link Chain**:
  1. Secondary blog cites a tech magazine.
  2. Tech magazine cites an analyst tweet.
  3. Analyst tweet references a benchmark paper or GitHub commit.
  4. **Action**: Extract numbers, methodology, and caveats directly from the GitHub commit or benchmark paper—ignore downstream editorial embellishments.

---

## 2. The 4-Tier Source Hierarchy

Classify every cited source into one of four distinct authority tiers:

| Tier | Source Category | Description & Typical Examples | Reliability Rating |
| :---: | :--- | :--- | :---: |
| **Tier 1** | **Primary & Formal Specs** | Official API documentation, IETF RFCs, W3C standards, peer-reviewed journals (Nature, IEEE, ACM), audited SEC 10-K filings, raw code repositories, official vendor security advisories. | **Highest** |
| **Tier 2** | **Authoritative Secondary Analysis** | Established engineering team post-mortems (e.g. Cloudflare, AWS, Netflix tech blogs), major investigative news outlets with editorial boards (Reuters, Bloomberg), benchmark studies with public reproducible code. | **High** |
| **Tier 3** | **General Practitioner Commentary** | Medium/Substack technical essays, Hacker News / Reddit engineering discussions, vendor marketing whitepapers, conference talks, podcast transcripts. | **Moderate / Contextual** |
| **Tier 4** | **Unverified & Generated Content** | Anonymous forums, SEO affiliate review sites ("Top 10 Best Tools"), AI-generated summary farms, corporate press releases without independent review. | **Low / Discard unless verified** |

> [!IMPORTANT]
> **The Two-Source Triangulation Rule**: Any factual assertion presented in Tier 2 or Tier 3 research deliverables must be corroborated by at least **two independent sources** originating from disjoint provenance chains. A single Tier 4 source must never be cited as factual evidence.

---

## 3. Detecting Commercial Bias and Circular Echo Chambers

### Commercial Conflict of Interest (COI)
- **"Vendor Comparison" Bias**: When a vendor publishes a comparison matrix (e.g. "Us vs Competitor X"), the competitor will almost always be depicted with missing features or un-updated benchmarks. Look for independent third-party benchmarks or conduct manual reproduction.
- **Sponsored Content & Affiliate Links**: Look for tracking tags (`?utm_source=`, `aff_id=`, `ref=`) or disclosure statements (`"We may earn a commission from links on this page"`).

### The AI-Generated Circular Echo Chamber
As automated content farms proliferate, AI-generated sites scrape and rewrite each other's hallucinations:
- **Detection Clues**: Vague generalities, absence of author bylines, generic stock imagery, absence of concrete version numbers or git commit SHAs, and identical phrasing across 5+ newly registered domains.
- **Mitigation**: Discard any source that cannot be traced back to an identifiable human practitioner, verifiable repository, or registered organizational author.

---

## 4. Source Provenance Logging Standard

When recording evidence during research, capture the following provenance metadata for every key claim:

```markdown
- **Claim**: CockroachDB switched from Apache 2.0 to Business Source License (BSL) in 2019.
  - **Source Title**: "Why We’re Relicensing CockroachDB"
  - **Source URL**: https://www.cockroachlabs.com/blog/oss-relicensing-cockroachdb/
  - **Publisher**: Cockroach Labs (Primary Corporate Blog)
  - **Publication Date**: 2019-06-04
  - **Source Tier**: Tier 1 (Official corporate policy statement)
  - **Corroborating Source**: The Register (Tier 2 tech journalism), https://www.theregister.com/2019/06/04/cockroachdb_bsl_licence/
```
