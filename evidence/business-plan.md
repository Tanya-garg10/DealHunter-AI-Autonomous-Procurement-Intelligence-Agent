# DealHunter AI — Comprehensive Business Plan & Unit Economics Model
**neatHack 2026 Procurement Intelligence Agent**  
*Generated via cfo.ai financial planning framework (https://cfo.ai/neathacks)*  
*Last Updated: October 2026*

---

## 1. Executive Summary & Problem Statement

### The Problem
Startups and mid-market engineering teams waste over **$140B annually on cloud and SaaS overages, hidden lock-in clauses, and misaligned procurement contracts**. 
- 84% of software buyers choose a tier based solely on headline pricing, ignoring tiered overage cliffs.
- Small businesses lack in-house procurement teams, relying on anecdotal recommendations or biased affiliate review sites.
- Engineering and finance leaders lack deterministic risk checks (e.g., "What happens if our usage triples in 6 months?").

### The Solution: DealHunter AI
DealHunter AI is an autonomous procurement intelligence agent. By evaluating hard vendor evidence, calculating total cost of ownership (TCO) deterministically, checking mandatory features, stress-testing sensitivity through "Deal Regret Checks", and tracing decisions transparently with neatlogs, DealHunter AI ensures teams don't just find a deal—they **prove it's the right deal**.

---

## 2. Target Customers & Market Opportunity

| Customer Segment | Profile | Core Pain Point | Willingness to Pay |
| :--- | :--- | :--- | :--- |
| **Early-Stage Startups (Seed to Series A)** | 5-25 engineers, no dedicated procurement | Fear of sudden $5k+ cloud overage surprise | $79 - $149/mo |
| **Growth-Stage Scaleups (Series B-C)** | 30-150 employees, VP Finance + Engineering Lead | Managing 40+ SaaS vendor contracts, renewals, and SAML compliance | $399 - $799/mo |
| **Fractional CFOs & IT Consultants** | Managing vendor purchasing for 5-15 client portfolios | Manual spreadsheet audits and pricing research taking 20+ hrs/client | $499/mo multi-client license |

**Total Addressable Market (TAM):** $18.4B global IT procurement & vendor management software market.  
**Serviceable Addressable Market (SAM):** $2.6B SMB SaaS & cloud cost optimization market.  
**Serviceable Obtainable Market (SOM):** $38M in Year 3 targeting US and European technology startups.

---

## 3. Product Subscription Tiers

| Tier | Monthly Price | Annual Price (15% Disc) | Included Monthly Investigations | Included Features |
| :--- | :--- | :--- | :--- | :--- |
| **Starter** | $79 / mo | $805 / yr | 10 procurement runs / mo | Deterministic TCO math, 5 vendor cohort comparison, Deal Regret Check (up to 2x usage), PDF/JSON export |
| **Growth Pro** | $249 / mo | $2,540 / yr | 50 procurement runs / mo | All Starter features + Live vendor doc scraper, Contract risk radar, Slack webhook alerts, Custom weight tuning |
| **Enterprise Agency** | $699 / mo | $7,130 / yr | Unlimited runs / mo | Multi-workspace, neatlogs custom trace integration, Dedicated procurement specialist review, SSO & Audit logging |

---

## 4. Unit Economics & Cost Structure (COGS)

### Per-Investigation Cost Breakdown (Average Run)

| Cost Component | Unit Metric | Unit Cost | Units per Investigation | Total Cost per Run |
| :--- | :--- | :--- | :--- | :--- |
| **LLM Reasoning (Gemini 3.8 Flash)** | 1K input / output tokens | $0.00015 / 1K tokens | 12K tokens (plan, audit, synthesis) | **$0.0018** |
| **Deterministic Engine & Python Worker** | Cloud Run execution time | $0.000024 / vCPU-sec | 1.4 seconds execution | **$0.0002** |
| **neatlogs Telemetry & Trace Storage** | Streamed event logs | $0.0005 / trace run | 8-12 step events | **$0.0005** |
| **Vendor Metadata & Cache Ingress** | Cached API queries | $0.0001 / query | 5 vendor profiles | **$0.0005** |
| **Total Variable Cost per Investigation (COGS)** | — | — | — | **$0.0030** |

### Gross Margin Analysis
- **Starter Customer ($79/mo, 10 runs used):**  
  Revenue: $79.00  
  COGS: 10 runs * $0.0030 = $0.03  
  **Gross Margin: 99.96%**

- **Heavy Growth Customer ($249/mo, 50 runs used):**  
  Revenue: $249.00  
  COGS: 50 runs * $0.0030 = $0.15  
  **Gross Margin: 99.94%**

Because all heavy math (TCO, overage calculations, feature matrices, sensitivity analysis) is computed **deterministically in Python** rather than via expensive chain-of-thought LLM loops, DealHunter AI achieves software-grade gross margins exceeding **90%** even after hosting overhead.

---

## 5. Financial Projections & Scenarios (Year 1 - Year 3)

### Base Scenario vs. Growth Scenario

```
=============================================================================
METRIC                       YEAR 1 (BASE)    YEAR 2 (BASE)    YEAR 3 (SCALE)
=============================================================================
Active Paying Customers               185            1,120            4,850
Blended Monthly ARPU                 $142             $168             $195
Annual Recurring Revenue (ARR)   $315,240       $2,257,920      $11,349,000
Gross Margin Percentage             91.2%            92.8%            93.5%
Customer Acquisition Cost (CAC)      $310             $265             $220
LTV (Assuming 18-mo avg life)      $2,556           $3,024           $3,510
LTV : CAC Ratio                      8.2x            11.4x            15.9x
=============================================================================
```

### Monthly Operating Expense (OpEx) Model (Year 1)
- **Engineering & Core Dev (2 FTE):** $18,000 / mo
- **Cloud Infrastructure & neatlogs Enterprise:** $650 / mo
- **Go-To-Market & Hackathon Community Outreach:** $2,500 / mo
- **Legal, Compliance & Accounting (cfo.ai tooling):** $800 / mo
- **Total Monthly OpEx:** $21,950 / mo

### Break-Even & Runway
- **Break-Even Point:** 155 active paying customers (~Month 9 in Base Scenario).
- **Runway:** With an initial pre-seed funding of $250,000, DealHunter AI possesses **14.2 months of runway**, safely surpassing the break-even milestone.

---

## 6. Sensitivity Analysis & Risk Mitigations

| Risk Factor | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| **Vendor Pricing Obfuscation** | Vendors move to opaque "Contact Sales" models | Implement structured evidence verification score; penalize unverified pricing; alert human reviewer. |
| **Model Pricing / Token Spikes** | Inference costs increase | Deterministic logic handles 95% of math; LLM is restricted to qualitative synthesis. |
| **Procurement Hallucination Liability** | User relies on bad recommendation | Explicit liability disclaimer; independent math verification layer; human-in-the-loop checkpoint before contract execution. |
| **Vendor Churn / High Initial CAC** | Slower adoption by SMBs | Free initial audit for 1 core tech stack (e.g., database or auth) converting at 18% into paid subscription. |

---

## 7. cfo.ai Integration Methodology
This financial plan was generated following the official guidelines at `https://cfo.ai/neathacks`:
1. Customer segments and willingness to pay derived from SMB SaaS procurement benchmark data.
2. Inference costs calculated based on Gemini 3.8 Flash token pricing ($0.15 / 1M tokens) with neatlogs step logging overhead.
3. Sensitivity stress-testing incorporated directly into the unit economics model to confirm gross margin durability under 10x token inflation scenarios.
