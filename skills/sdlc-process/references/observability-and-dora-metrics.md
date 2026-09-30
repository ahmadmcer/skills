# Observability, Operations & DORA Metrics

Read this guide when instrumenting application telemetry, configuring SLIs/SLOs,
measuring DORA delivery performance, or conducting blameless incident post-mortems.

---

## 1. The Three Pillars of Observability

True observability allows you to understand internal system states strictly through external outputs:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      THE OBSERVABILITY TRIAD                           │
├─────────────────┬──────────────────┬───────────────────────────────────┤
│ 1. Metrics      │ 2. Logs          │ 3. Traces                         │
├─────────────────┼──────────────────┼───────────────────────────────────┤
│ Aggregable time │ Structured JSON  │ Distributed spans with parent-    │
│ series data     │ with trace context│ child causality (OpenTelemetry)  │
│ (RED / USE)     │ and contextual tags│ across microservice boundaries    │
└─────────────────┴──────────────────┴───────────────────────────────────┘
```

### The RED Method for Request-Driven Services
- **Rate**: Requests served per second.
- **Errors**: Number of failing requests (4xx / 5xx) per second.
- **Duration**: Distribution of response times (p50, p95, p99 histograms).

---

## 2. SLIs, SLOs, and Error Budgets

- **Service Level Indicator (SLI)**: A quantifiable measure of service behavior:
  $$\text{SLI} = \frac{\text{Successful Requests}}{\text{Total Requests}} \times 100\%$$
- **Service Level Objective (SLO)**: The target reliability agreed upon with stakeholders (e.g. 99.9% of requests succeed in < 200ms over a rolling 30-day window).
- **Error Budget**: The allowable unreliability ($100\% - \text{SLO} = 0.1\%$). When the error budget is exhausted, freeze feature releases and prioritize reliability work.

---

## 3. DORA Metrics & The AI-Era Rework Rate

DORA (DevOps Research and Assessment) metrics provide an empirical scorecard of delivery throughput and operational stability:

| DORA Metric | Definition | Elite Performance Benchmark |
| :--- | :--- | :--- |
| **Deployment Frequency (DF)** | How often the team successfully deploys code to production. | Multiple deploys per day |
| **Lead Time for Changes (LTTC)** | Time elapsed between code commit and running in production. | Less than one hour |
| **Change Failure Rate (CFR)** | Percentage of production deployments causing degraded service requiring rollback or hotfix. | 0% – 15% |
| **Failed Deployment Recovery Time (FDRT)** | Time taken to restore service when a production incident occurs. | Less than one hour |

### Modern Metric: AI Rework Rate
In the era of AI coding agents, high deployment throughput can sometimes mask high code churn.
Track **Rework Rate**: The percentage of code modified or reverted within 14 days of original authoring. If rework rate spikes above 15%, strengthen spec-driven development and contract testing gates.

---

## 4. Blameless Post-Mortem Standard

Every Severity-1 or Severity-2 production incident requires a blameless post-mortem document
in `docs/incidents/YYYY-MM-DD-incident-title.md`:

```markdown
# Incident Post-Mortem: [Incident Title]

Date: YYYY-MM-DD
Severity: [Sev-1 | Sev-2]
Incident Commander: [Name]
Authors: [Names]

## Executive Summary
A concise 2-3 sentence overview: what broke, what was the customer impact,
how long did it last, and what restored service?

## Impact Assessment
- Duration: [Start Time UTC] to [Resolution Time UTC] (Total: X minutes)
- Customers Impacted: [Number or percentage of users affected]
- Revenue / SLA Impact: [Error budget consumed, financial loss]

## Detailed Timeline (UTC)
- 14:02 - Automated deployment v2.4.0 started.
- 14:07 - Telemetry alert: 5xx error rate spiked to 3.8%.
- 14:12 - On-call engineer paged and acknowledged incident.
- 14:18 - Automated canary rollback triggered to v2.3.9.
- 14:22 - 5xx error rate returned to normal baseline (0.01%).

## Root Cause (5 Whys Analysis)
1. Why did 5xx errors spike? A null reference exception occurred in user profile lookups.
2. Why was the reference null? The database migration had not yet populated the new field.
3. Why was the field not populated? The deploy ran before the asynchronous backfill completed.
4. Why did the deploy run early? The deployment pipeline lacked a synchronization gate check.
5. Why was there no gate check? The change was expedited without following the expand/contract pattern.

## Action Items & Preventative Measures
| Action Item | Type | Owner | Target Date |
| :--- | :--- | :--- | :--- |
| Add CI migration completion check | Prevent | @engineer | YYYY-MM-DD |
| Implement automated canary health gate | Detect | @devops | YYYY-MM-DD |
| Update deployment runbook with checklist | Mitigate | @lead | YYYY-MM-DD |
```
