# Censored demand, tools, Amazon's skill and "14 days"

## Demand that was not seen

- A sales average taken over days when a SKU could not be bought understates demand (O18).
- Sales observed while out of stock are a lower bound, treated in research as censored observations, and one study (Jain, Rudi & Wang 2015) finds the timing of the stock-out recovers most of the lost information (O18).
- An Amazon forecasting paper (Seeger, Salinas & Flunkert 2016) says an out-of-stock day's zero should be "explained away" and its likelihood term dropped, and that "ignoring the out of stock signal leads to systematic underbias" (O18).
- DeepAR's authors (Salinas et al. 2020) warn of a "downward spiral" (O18).
- These are Amazon's retail forecasting research, not the forecast behind a seller's Restock figures (O18).
- What moves Amazon's Restock figures: ../../restock/SKILL.md.

## How tools treat out-of-stock days

- Inventory Planner, sellerboard, ConnectBooks, 赛狐, 领星 and 积加 offer to divide by in-stock days only (O19).
- SoStocked imputes an average for out-of-stock days, and its stock-out rule is zero inventory with sales below a share of the daily average that its help text names (O19).
- RestockPro scales velocity by the in-stock share as an option and caps its upward adjustment at a bound its help text names (O19).
- The pages read for 易仓, 优麦云, 船长BI, 店小秘 and 马帮 show no correction (O19).
- The tools define an out-of-stock day in four ways, as their help text read on 2026-11-10 shows (O19).
- Each tool's wording and figures: research/areas/running-out.md.

## Amazon's open stock-out skill

- Amazon's open `stockout-prevention` skill (Amazon Selling Partner plugin 1.0.0; `amzn/selling-partner-agentic-toolkit` at head `8d90d3b`, 2026-10-12) computes cover as fulfillable units ÷ (30-day ordered units ÷ 30) (T2).
- It counts no inbound or reserved units, and it bands the result at 7 and 21 days (T2).
- It reads neither of Amazon's recommendation reports, because its connector exposes no reports tool (T2).
- Its README and `/sp-stockout-check` command describe a different method, metric discovery and a reorder quantity, from the skill body (T2).
- It bars its agent from raising price as an option (O27).
- It calls "days of supply < 14 → at risk" Amazon's rule without citing a page and applies it to an FBA metric (T1).
- It says its 14–21 early-warning band is its own addition, and it does not attribute its 7-day line (T1).

## "14 days" on Amazon's pages

- "14 days" appears on Amazon's pages in two roles, neither of them a stock-out rule for FBA (T1).
- One is an eligibility criterion of the FBM Restock recommendation feature, a ceiling of 14 days on current days of supply, announced for India on 2025-02-12 and the US on 2025-03-14 (T1).
- The other is a band of the low-inventory-level fee's historical days of supply, on help page GV43F6S76Y9DHYRH as the listing seat read it on 2026-10-14; the fee's bands and threshold for the seller's store are read there: ../../stock-cost/SKILL.md (T1).
- Amazon disagrees with itself here: its skill calls the rule Amazon's, and no Amazon help or developer page read states it for FBA (T1).

## Practitioners' choices around a stock-out

- Practitioners disagree on raising price before a stock-out: My Amazon Guy, BellaVix, 老魏, 日落大道 and others raise in small steps, while Sellics' case, Helium 10 and 董海温 leave the price and let the product run out (O27).
- Practitioners disagree on a seller-fulfilled backup offer during the gap: My Amazon Guy, 老魏 and SPS Commerce (for a short gap) use one, and Moss and Regan跨境 say its lower conversion harms the listing (O28).
- Those who use a backup offer (with SKU.io and Fast Brands) disagree on keeping it live while FBA has stock (O28).
- How one ASIN carries an FBA and an FBM offer: ../../fbm-and-channels/SKILL.md.
- Cover thresholds in circulation are each their author's: 60 days (Jungle Scout), 45 days (Ken Zhou), 30 and 21 days (BellaVix), 6 weeks (Regan跨境), 75 days (夕木运营笔记本), 30/60 days (优麦云) (O32).
- Named practitioners' targets run from 15 days of turnover to two months at FBA plus two in the pipeline (O32).
