# Forecast and cover methods

Ids in brackets are positions in ../../../research/README.md.
Each method below is one a seller, a tool or a study uses; the seller's choice of window, cover and service target changes the quantity and date it gives (R18, R29, R30).

## Ordered against shipped units

- `getOrderMetrics.unitCount` and Sales and Traffic `unitsOrdered` count ordered units (R16).
- Sales and Traffic `unitsShipped` and the planning report's `units-shipped-t7/t30/t60/t90` count shipped units, by date and by ASIN (R16).
- Amazon's own cover measures (historical days of supply, the fee tests) are built on shipped units, so a rate built on ordered units need not agree with them (R16).
- How far apart ordered and shipped units run in a 30-day window, and the Restock report's "Units Sold Last 30 Days" against both, was read in Amazon's documents and not yet seen on a live store (R16).
- `getOrderMetrics` counts units in orders, filters by `AFN` or `MFN`, and takes its day boundary from the caller's `granularityTimeZone` (R17).
- It reaches back 30 days at hourly granularity and two years at the others (R17).
- Outside the Far East region Amazon names Product Listing and Inventory and Order Tracking for `getOrderMetrics`, so of the five roles Product Listing opens it (R17).
- Sales and Traffic needs the Brand Analytics role (R17).
- `searchOrders` returns each order's items with `quantityOrdered` and seller SKU (R17).
- Rates and how a call is made: the amazon-sp-api skill's references/door.md.

## Tools' formulas and defaults

- The paid tools read share one shape, (lead time + target or safety days) × daily sales − stock on hand and on the way, and differ in each term (R18).
- The seventeen tools tabulated (RestockPro, Inventory Planner, Lingxing 领星, Sellfox 赛狐, Gerpgo 积加, 优麦云 and the rest) do not share one set of defaults for window, weights, stock-out handling, safety days or alert (R18).
- Lingxing and Sellfox default daily sales to weights of 0.5, 0.3 and 0.2 on the 7-, 14- and 30-day averages, and leave out the two most recent days, as their defaults (R19).
- Gerpgo defaults to the trailing 7-day average, and 优麦云 to weights of 0.4, 0.3, 0.2 and 0.1 on the 3-, 7-, 14- and 30-day averages, as their defaults (R19).
- When no freight mode can land stock before it runs out, Lingxing, 店小秘 (Dianxiaomi) and Gerpgo offer to remove the unrecoverable demand from the suggested quantity (R24).
- The full table of tools and defaults: ../../../research/areas/restock-and-forecast.md and ../../../research/beyond/sellers-tools-and-research.md.

## Safety stock

- "Safety stock" names different things in practice (R21).
- At Lingxing and Sellfox it is extra days of cover at FBA, and at Gerpgo the same with a 14-day default (R21).
- At 易仓 (Eccang) it is a reserve in the seller's own warehouse (R21).
- At SoStocked it is a formula on maximum and average sales and lead time (R21).

## What a seller's tool holds

- A seller's planning tool holds facts Amazon does not: staged supplier lead times, purchase orders, non-Amazon stock and the seller's own settings (R28).
- Several vendors (Lingxing, Flieber, Sellfox) now expose these through an MCP server (R28).

## Research models

- Reorder point = expected lead-time demand + safety factor × standard deviation of lead-time demand (R29).
- With random lead time that deviation is √(μ_t·σ_d² + μ_d²·σ_t²), so lead-time and demand variability enter separately (R29).
- This is a textbook model assuming normal, independent demand, one choice among several (Bricker, University of Iowa slides) (R29).
- Cycle service level (no stock-out in a cycle) and fill rate (the share of demand served from stock) are different targets (R30).
- In a textbook example a high fill rate corresponds to a markedly lower cycle service level (Bricker; MIT CTL.SC1x; MIT ESD.260) (R30).
- Under periodic review the period safety stock must cover is the review interval plus the lead time (R+L), against L under continuous review (R31).
- Amazon's "Replenishment frequency" setting and the ERPs' replenishment cycle (补货周期) are such an interval (R31).
- Croston's method forecasts intermittent demand from separately smoothed demand size and interval, updates only after a positive demand, and is positively biased (R32).
- TSB updates a demand probability every period and lowers the forecast through zero periods (Teunter, Syntetos and Babai 2011) (R32).
- In the M5 competition on Walmart unit sales, all top methods were machine-learning models pooled across series with price and calendar inputs (R33).
- They beat the benchmarks on average and by less at product-store level, where Croston beat seasonal naive (Makridakis, Spiliotis and Assimakopoulos 2022) (R33).
- Amazon's published retail forecasters and what is not known of the model behind its recommendation: references/reports.md.
