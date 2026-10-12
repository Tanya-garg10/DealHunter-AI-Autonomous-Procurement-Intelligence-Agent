# cfo.ai Financial Model & Business Plan (`evidence/cfo.md`)
**DealHunter AI — neatHack 2026**  
*Role: Business Planning, Financial Modeling, Unit Economics & Runway*  
*Generated via cfo.ai Financial Planning Framework (https://cfo.ai/neathacks)*

---

> **Honesty & Methodology Disclaimer:**  
> This financial plan represents modeled projections and business assumptions generated for neatHack 2026 via the `cfo.ai` financial framework. These figures are **deliberate planning assumptions**, not established historical market facts or verified commercial audits. DealHunter AI does not make real payment transactions or claim fictitious external funding.

---

## 1. Executive Summary & Value Proposition

- **Product:** DealHunter AI
- **Tagline:** *"Don't just find a deal. Prove it's the right deal."*
- **Problem Solved:** Startups and SMBs waste over $140B annually on software overages and hidden lock-in contracts because they rely on biased review sites or headline pricing. DealHunter AI evaluates vendor evidence, deterministically audits TCO, and alerts buyers to overage traps before contracts are signed.
- **Target Customer Segments:**
  1. *Early-Stage Tech Startups (Seed / Series A):* 5–25 team members with no dedicated procurement lead.
  2. *Internal Ops & Engineering Leads:* Managing 10–30 SaaS vendor renewals and compliance needs.
  3. *Digital Agencies & Fractional CTOs:* Procuring stacks across multiple client portfolios.

---

## 2. Proposed Monetization Model & Pricing Tiers

The financial model was constructed using the following proposed pricing tiers:

| Plan Tier | Monthly Price | Annual Price (15% Disc) | Included Usage Allowance | Target Buyer |
| :--- | :--- | :--- | :--- | :--- |
| **Starter** | **$19 / mo** | $194 / yr | 5 procurement runs / mo | Solo founders & seed teams checking a single tool |
| **Pro** | **$49 / mo** | $500 / yr | 25 procurement runs / mo | High-growth startups with active monthly renewals |
| **Business** | **$149 / mo** | $1,520 / yr | 100 procurement runs / mo | Multi-seat teams, agencies, and fractional CFOs |

---

## 3. Cost of Goods Sold (COGS) & Variable Unit Economics

Because DealHunter AI computes TCO math, overages, and sensitivity calculations **deterministically in Python/TypeScript** rather than through multi-turn recursive LLM loops, variable inference cost is minimal:

| Component | Metric | Rate | Cost per Investigation |
| :--- | :--- | :--- | :--- |
| **Gemini 3.8 Flash Synthesis** | 3.5k tokens | $0.15 / 1M tokens | $0.0005 |
| **Cloud Run Execution Time** | 1.2s vCPU | $0.000024 / vCPU-sec | $0.0001 |
| **Neatlogs Telemetry Streaming** | 7 trace spans | $0.00005 / span | $0.00035 |
| **Vendor Registry Caching & Ingress** | Cached lookup | $0.00005 / lookup | $0.00005 |
| **Total Cost per Investigation (COGS)** | — | — | **$0.0010** |

### Gross Margin Calculation
- **Starter Customer ($19/mo, 5 runs used):**  
  Revenue: $19.00 | COGS: $0.0050 | **Gross Margin: 99.9%**
- **Pro Customer ($49/mo, 25 runs used):**  
  Revenue: $49.00 | COGS: $0.0250 | **Gross Margin: 99.9%**
- **Business Customer ($149/mo, 100 runs used):**  
  Revenue: $149.00 | COGS: $0.1000 | **Gross Margin: 99.9%**

Even factoring in fixed cloud hosting overhead ($120/mo) and database replication ($50/mo), gross margin comfortably exceeds **92%** at scale.

---

## 4. 12-Month Financial Forecast (Base Scenario)

```
========================================================================================
MONTH       ACTIVE CUSTOMERS    MRR ($)      COGS ($)    OPEX ($)     NET CASH FLOW ($)
========================================================================================
Month 1                  15       $510         $12         $650               -$152
Month 2                  32     $1,085         $25         $680               +$380
Month 3                  58     $1,960         $45         $750             +$1,165
Month 4                  95     $3,210         $72         $850             +$2,288
Month 5                 145     $4,900        $110       $1,000             +$3,790
Month 6                 210     $7,100        $160       $1,200             +$5,740
Month 7                 285     $9,630        $215       $1,400             +$8,015
Month 8                 370    $12,500        $280       $1,650            +$10,570
Month 9                 465    $15,710        $350       $1,950            +$13,410
Month 10                575    $19,430        $435       $2,300            +$16,695
Month 11                700    $23,660        $530       $2,700            +$20,430
Month 12                850    $28,730        $640       $3,150            +$24,940
========================================================================================
TOTAL Y1 ARR: $344,760 | ENDING MRR: $28,730 | YEAR 1 NET PROFIT: $106,641
========================================================================================
```

*Customer Tier Distribution: 45% Starter ($19), 40% Pro ($49), 15% Business ($149). Blended ARPU: $33.80/mo.*

---

## 5. Scenario Comparison & Sensitivity Analysis

| Metric | Downside Scenario (Slow Growth) | Base Scenario (Target) | Optimistic Scenario (Viral Hackathon Adoption) |
| :--- | :--- | :--- | :--- |
| **Month 12 Customers** | 240 active | 850 active | 2,100 active |
| **Ending MRR** | $8,110 / mo | $28,730 / mo | $70,980 / mo |
| **Annualized ARR** | $97,320 | $344,760 | $851,760 |
| **Break-Even Month** | Month 4 | Month 2 | Month 1 |
| **Gross Margin** | 88.5% | 92.4% | 94.1% |

### Sensitivity Triggers
- **Pricing Elasticity:** If Pro tier is reduced from $49 to $39, customer volume must increase by 26% to maintain revenue parity.
- **AI Token Inflation:** Even if LLM token costs rise 10x, variable COGS increases only from $0.0010 to $0.0060 per run, preserving a >95% gross margin.

---

## 6. Three Biggest Financial Risks & Mitigation

1. **Risk 1: High Customer Churn After a Single Purchasing Decision**
   - *Impact:* Buyers use DealHunter once to evaluate a database, then cancel their subscription.
   - *Mitigation:* Transition from one-off audits to **Continuous Contract Renewal Monitoring** (quarterly overage alerts, auto-renew notice radars, and contract renegotiation scripts).
2. **Risk 2: Vendor Pricing Transparency Obfuscation**
   - *Impact:* B2B vendors remove self-serve pricing in favor of opaque "Contact Sales" quotes.
   - *Mitigation:* Incorporate buyer quote-upload parsing and community crowdsourced enterprise pricing benchmarks with evidence scoring.
3. **Risk 3: Model Hallucination Liability**
   - *Impact:* An incorrect calculation leads a customer to purchase an expensive tool.
   - *Mitigation:* Strict architecture separation: 100% deterministic calculations in Python, explicit human review checkpoints, and terms stating DealHunter is a decision-support tool.

---

## 7. Recommended Launch Strategy for a Solo Student Founder

1. **Phase 1: Free Public Hackathon Benchmarking (Weeks 1–4)**
   - Offer free unlimited investigations for neatHack community projects and student founders.
   - Post side-by-side breakdowns on X/LinkedIn (e.g. *"Why Startup X overpaid $2,400 on AWS vs Supabase"*).
2. **Phase 2: Freemium Launch with $19 Starter Tier (Month 2)**
   - Launch on Product Hunt and Hacker News. Provide 2 free runs/month; charge $19/mo for up to 5 runs with PDF export.
3. **Phase 3: Agency & Fractional CFO Partnerships (Months 3–6)**
   - Partner with early-stage startup accelerators and fractional finance consultants to white-label DealHunter reports for their portfolio companies.
