---
name: google-pnl-data-sources
description: Where every number in the example's quarterly P&L dataset came from (Alphabet's SEC earnings releases, with links) and the arithmetic and SEC cross-checks that verified it. Use when citing, checking or extending a figure in quarterly_pnl.csv or one_offs.csv.
metadata:
  last_modified: "2026-11-14"
---

# Data sources and checks

`quarterly_pnl.csv` holds Alphabet's reported results for 12 quarters, 2023-Q4 through 2026-Q3 (the latest reported quarter, filed 2026-10-29). Values are USD millions as reported, except `diluted_eps` (USD) and `diluted_shares_m` (millions of shares). Columns: revenue by type and segment, segment operating income, and the consolidated income statement. For 2026-Q2 and 2026-Q3, `net_income_to_common` is net income after preferred stock dividends; diluted EPS is computed on that figure.

## Where the numbers come from

Alphabet's earnings releases, filed with the SEC as Form 8-K Exhibit 99.1. Each release shows its quarter and the same quarter a year earlier, so eight releases cover all 12 quarters. Each URL is `https://www.sec.gov/Archives/edgar/data/1652044/<accession>/<file>`.

| Release | Accession | File | Quarters taken from it |
|---|---|---|---|
| 2024-Q4 | 000165204425000010 | googexhibit991q42024.htm | 2023-Q4, 2024-Q4 |
| 2025-Q1 | 000165204425000040 | googexhibit991q12025.htm | 2024-Q1, 2025-Q1 |
| 2025-Q2 | 000165204425000056 | googexhibit991q22025.htm | 2024-Q2, 2025-Q2 |
| 2025-Q3 | 000165204425000087 | googexhibit991q32025.htm | 2024-Q3, 2025-Q3 |
| 2025-Q4 | 000165204426000012 | googexhibit991q42025.htm | 2025-Q4 |
| 2026-Q1 | 000165204426000043 | googexhibit991q12026.htm | 2026-Q1 |
| 2026-Q2 | 000165204426000066 | googexhibit991q22026.htm | 2026-Q2 |
| 2026-Q3 | 000165204426000080 | googexhibit991q32026.htm | 2026-Q3 |

Where a quarter appears in two releases (as the current quarter and as a prior-year comparison), the values matched.

## Checks run

1. **Arithmetic, all 12 quarters:** revenue types sum to Services; Services + Cloud + Other Bets + hedging equals total revenues; segment operating income sums to consolidated; costs sum; revenue less costs equals operating income; operating income plus other income equals pre-tax income; pre-tax less tax equals net income; EPS agrees with net income over diluted shares.
2. **Against the SEC's structured financial data (XBRL):** 118 consolidated values compared. All matched except 2025-Q4 revenue, cost of revenues and total costs, each $1M different. The SEC figure is derived (full year less nine months), so this is consistent with rounding; the CSV carries the value the release prints. Revenue for 2023-Q4 and 2024-Q1 is tagged differently in XBRL and was checked under that tag: both match.

The segment and revenue-type lines are not in the SEC's structured data; they come from the releases and are checked only by the arithmetic above.

## Use in the example brain

This folder is an approved location registered in the brain's `sources/`: source data the brain points to and queries. No figure from it is copied into a brain entry (SPEC principle 3).

`one_offs.csv` lists the charges and below-the-line items that the releases call out, with amounts as printed.
