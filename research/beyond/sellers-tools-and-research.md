# Sellers' tools, practitioners, Amazon's own agent, and published research

Read 2026-11-10 by the research seat.

Tags: **[official]** is Amazon's own page or Amazon's own published file, read at source. **[official, via <who>]** is Amazon's wording as a third party reproduced it; the Amazon page itself was not seen. **[opinion]** is a tool vendor, a practitioner or an outlet, recorded as theirs with a name and a date. **[research]** is a published paper or regulator's document. **[snippet]** is a search-result excerpt of a page that would not open. **[seat]** is this seat's own reading and enters no skill. **[survey]** marks a fact carried from the plugin survey of 2026-11-09 (`scratch/sp-api-plugins/03-tools-en.md`, `03-tools-cn.md`, `07-reuse.md`) that was **not re-read at source** for this file; it is always said where it applies.

How the pages were reached: plain GET with the default client, by this seat and by the seat's readers on 2026-11-09 and 2026-11-10; the files are under `scratch/stock-playbook/sellers-tools-and-research/`. A page that answered 403, a bot check, a login wall or a JavaScript shell is listed as unreachable and nothing was done to get around it. `web.archive.org` did not answer from this network (502). The readers stopped on a usage limit before writing notes for four of seven groups; for those groups the seat read the readers' downloaded pages itself, so a page counts as read only where a quotation below comes from it. Amazon's open skill set was read from the local zip (`scratch/sp-api-plugins/amazon-plugin-zip/`, Apache-2.0) and from the reader's copy of `amzn/selling-partner-agentic-toolkit` on github.com; the verifier recorded the head on 2026-11-10 as `8d90d3b` (2026-10-12). No Amazon API host was called. A verifier pass on 2026-11-10 corrected and filled this file; see *Verification* at the end.

## What this covers

What paid tools do with a seller's stock, what named practitioners teach in English and Chinese, what Amazon's own agent offer does with stock, what others publish in the open, and what published research has measured. It is the evidence for one stance: the method is the seller's, the facts are Amazon's.

Owned elsewhere and only cross-referenced: every `areas/` file for Amazon's rules (`areas/running-out.md` owns the stock-out literature in detail, `areas/restock-and-forecast.md` the reorder maths); `beyond/programs-and-regions.md`; `method/sp-api-stock-surface.md` for the API and its roles; `method/seller-central-only.md`.

## Amazon's own rules

This section holds only what Amazon itself publishes about its tools, its agent and its numbers. Fee and policy rules are the `areas/` files'.

### A. Amazon's two recommendation reports, and their roles

- [official] The **Restock Inventory Report** is `GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT`; roles **Pricing or Amazon Fulfillment** (*Role Mappings for SP-API Types*: "Required roles (need at least one)"; both are among the door's five); all stores except India; request-only; "Content updated in near real-time". Its columns include `Sales last 30 days`, `Units Sold Last 30 Days`, `Total Units`, `Inbound`, `Available`, `FC transfer`, `FC Processing`, `Customer Order`, `Unfulfillable`, `Working`, `Shipped`, `Receiving`, `Total Days of Supply (including units from open shipments)`, `Days of Supply at Amazon Fulfillment Network`, `Alert`, `Recommended replenishment qty`, `Recommended ship date`, and `Recommended action (available in the US store)`. (*Report type values: FBA*, developer-docs.amazon.com.)
- [official] The **inventory planning report** (the page's heading is "FBA Manage Inventory Health Report") is `GET_FBA_INVENTORY_PLANNING_DATA`; role **Amazon Fulfillment** (the only role the role-mapping page lists for it); not available in NL, PL, SE, BE. Its columns include `days-of-supply`, `estimated-excess-quantity`, `weeks-of-cover-t30`, `weeks-of-cover-t90`, `sell-through`, `historical-days-of-supply`, `Short term historical days of supply`, `Long term historical days of supply`, `Total Days of Supply`, `fba-minimum-inventory-level`, `fba-inventory-level-health-status`, `Recommended ship-in quantity`, `Recommended ship-in date`, `Exempted from Low-Inventory-Level fee?`, `Low-Inventory-Level fee applied in current week?`, and stock-age buckets from 181–210 to 365+ days. (Same page.)
- [official] Amazon therefore publishes **two** recommended quantities and dates, one per report. Neither page says how either is computed.
- [seat, from a local search] In the local clone of Amazon's API models, `daysOfSupply` and "days of supply" appear in no JSON model and no Data Kiosk schema; days of supply reaches a caller only as a report column.

### B. Where "14 days" appears on Amazon's pages

- [official] News_Amazon, "Get personalized restock recommendations for your inventory", Seller Central forums, 2025-03-14 (`datePublished` 2025-03-14T07:37Z; note on the post: "updated on March 19, 2025"), US: "The new Restock recommendation feature in Seller Central uses a demand forecasting model to help you maintain healthy inventory levels for your **Fulfilled by Merchant** listings. It calculates suggested restock quantities and restock-by dates for your products that meet specific criteria, including active sales in the last three months, projected demand, and current days of supply less than 14 days." It gives "Suggested restock quantities based on current inventory and projected two-week demand across all locations" and "Forecasted eight-week demand trends using artificial intelligence models"; about half of US FBM sellers had it at the post, all by 2025-04-18.
- So in that post Amazon's "14 days" is an **eligibility criterion of an FBM feature**.
- (corrected 2026-11-10 by the verifier) [official, listing playbook, 2026-10-14, not re-read] A second Amazon page uses 14, and 21 as well: the **Low-inventory-level fee** help page (GV43F6S76Y9DHYRH, version 29) charges the fee per unit by size tier, weight and a historical-days-of-supply band, "The bands are 0–14, 14–21 and 21–28 days" (the listing playbook's paraphrase; the rate table itself was not quoted). These are **fee-rate bands on historical (backward-looking, shipped-unit) days of supply**, not a stock-out risk rule. [opinion, ppc.land, 2026-11] reads the same band into its 2027 example: "a low-inventory-level fee of $2.90 on each unit shipped in a week when it has under 14 days of supply". A seller's reply in Bryce_Amazon's forum thread (2023-12-07) lists "0-14 Days of Supply: Highest fee charged. 14-21 … Moderate … 21-28 … Lowest" [opinion, a seller's reply, not Amazon's post body].
- No Amazon page read here states "days of supply under 14 means at risk of stock-out" for FBA. Amazon's open skills state it as "Amazon's own analysis rule" (section C) without citing a page.

### C. Amazon's open skill set: what is hard-coded about stock

Read from the local zip, and re-read by the verifier on 2026-11-10 at `amzn/selling-partner-agentic-toolkit` head **`8d90d3b7c1537254b53c82651ac31fdbf0089368`** (commit date 2026-10-12, "Merge pull request #7 from amzn/add-finance-month-end-closer"; repository `pushed_at` 2026-10-15). At that head the bodies of `stockout-prevention/SKILL.md`, `seller-analytics/SKILL.md`, `seller-analytics/references/metrics-catalog.md` and `commands/sp-stockout-check.md` match the zip; only the YAML front-matter formatting differs.

- [official] `skills/stockout-prevention/SKILL.md` computes over a fixed 30-day window: `avg_daily_units = unitCount / 30` and `days_of_cover = fulfillableQuantity / avg_daily_units`. It counts only `fulfillableQuantity`; inbound and reserved units are not in cover.
- [official] Its bands: "**CRITICAL** — days_of_cover < 7 / **WARNING** — 7 ≤ days_of_cover < 21 / **HEALTHY** — days_of_cover ≥ 21". Its own note: "Amazon's own analysis rule is *days of supply < 14 → at risk*. These bands are intentionally more conservative: 7–14 is the canonical at-risk range, and 14–21 is an *early-warning* buffer this skill adds so a fast-moving SKU is caught before it crosses 14." (corrected 2026-11-10 by the verifier) So by the skill's own words the **21-day line is the skill's addition**; the **7-day line is not attributed** by the skill to anything (it calls 7–14 part of "the canonical at-risk range"), and no Amazon page read here prints a 7-day days-of-supply line. The 21 does appear on an Amazon page, but as a low-inventory-level fee band on historical days of supply (section B), which the skill does not cite. The "< 14 → at risk" rule the skill calls Amazon's cites no page.
- [official] The skill's description in the repository's `README.md` and the `/sp-stockout-check` command describe a different method from the skill body: the command says "Discover the right analytics metrics first … then read days of supply and sales velocity per SKU … and tell me how much to reorder and by when", and the README says the skill quantifies "stockout risk from days-of-supply and velocity, recommend[s] how much to reorder and by when"; the skill body computes its own cover from order metrics and states no reorder quantity.
- [official] Fixed steps and gates: a chart artifact is mandatory at two steps (3b "days-of-cover bar chart", 4b "timeline"); the gap is `estimatedDeliveryWindow.start − (today + days_of_cover)`; "Do not raise pricing as an option at all"; a listing change goes through `listings_patchListingsItem` in `VALIDATION_PREVIEW` and waits for the seller to type "approve". Its price reference adds "One change at a time" and "No unsolicited follow-up". Its option B names the cost of accepting a stock-out as "lost sales, BSR/rank recovery, and that running very lean can trigger the **low-inventory-level fee**".
- [official] Its tools are `fbaInventory_getInventorySummaries`, `sales_getOrderMetrics`, `fbaInbound_listInboundPlans`, `listings_patchListingsItem`. Its reference says "there is **no `reports` tool** exposed" in the connector, and that `sku` and `asin` are mutually exclusive in order metrics. So the connector's skill cannot read either report in section A.
- [official] `skills/seller-analytics/SKILL.md` repeats "days of supply < 14 → at risk of stockout", says its data is delayed about two days, and says the metric tool is "private beta … `Threep_`-prefixed domain names … may change before GA".
- [official] `references/metrics-catalog.md` lists private-beta inventory metrics that no public model carries: `FBA_AVAILABLE_QTY`, on-hand and total days of supply at mean and P90 (`FBA_INV_VIS_ONHAND_PMEAN_DOS`, `_P90_DOS`, `FBA_INV_VIS_TOTAL_PMEAN_DOS`, `_P90_DOS`), forecasts `FBA_FORECAST_N7_P80`, `N30`, `N60`, `FBA_INV_VIS_RESTOCK_ORDER_DATE`, `FBA_INV_RESTOCK_QTY`, recommended minimum level in days (`FBA_INV_VIS_RECOMMENDED_MIL_PMEAN_DOS`, `_P90_DOS`), `FBA_UNITS_SHIPPED_T30`, reserved breakdowns, inbound totals, and `FBA_INV_HIL_ZONE`. "Not every metric in this catalog is exposed to every seller."
- [official] At head `8d90d3b` the repository holds twelve skills (fba-inbound-management, finance-month-end-closer, invite-secondary-users, listing-buyability, listing-compliance, listing-issues, listing-searchability, listing-troubleshooter, seller-analytics, sp-api-knowledge, stockout-prevention, support-case-helper) and three commands; the local zip holds eleven. The added one is `skills/finance-month-end-closer` (commit `11d828a`, 2026-10-08). No stock skill was added. The last change to a stock-adjacent skill was `ba42633` (2026-09-25), "seller-analytics: port … getMetricData contract".
- [official] `fba-inbound-management/SKILL.md` at that head: "The seller types **`CONFIRM`** — a plain "ok"/"yes" is **not** enough" before a placement or transport confirm, and "**Cap at 3 polls.**" (re-read 2026-11-10). [survey] The connector's eight-tool list and "Currently in beta" were not re-read (they come from the connector, whose host is off limits).

### D. Seller Assistant, as Amazon describes it

- [official] About Amazon, 2025-09-17: "Seller Assistant will now actively monitor inventory levels"; it will "proactively flag slow-moving products before they incur long-term storage fees and recommend specific items to leave as-is vs. others where it would be best for the seller to mark down pricing or remove the item"; it gives "recommendations for the best allocation between FBA fulfillment centers and Amazon Warehousing and Distribution". "Seller Assistant is free", "currently available to all sellers in the U.S. store and will be rolled out to other countries in the coming months, at no additional cost".
- [official] About Amazon, 2026-09-23: "persistent memory of each seller's pricing patterns, inventory cycles, and growth goals"; "New Seller Assistant workflows … continuously monitor and execute routine tasks like restocking and pricing adjustments with full audit trails and seller-defined guardrails"; the plugin is "launching first with Amazon Quick and in beta with Anthropic's Claude", "now available in beta for sellers in Amazon's U.S. stores, with international expansion to follow".
- [official] Amazon's developer-docs index (`llms.txt`, announcements through the 2026-11-04 release) contains no page about MCP, the connector or agents. The two doc URLs guessed for one are empty shells.
- [official] Veeqo's pricing page: "acquired by Amazon in 2021. It is now part of Amazon"; it lists "Seller Assistant — AI agent for warehouse and fulfillment tasks" and "Veeqo MCP — Connect Veeqo with ChatGPT and Claude"; "Any FBA orders fulfilled by Amazon are excluded from your chargeable order volume".

### E. Amazon's dated figures that practitioners plan around

Stated as Amazon's dated definitions; the `areas/` files own them.

- [official] 2027 fee letter (sellingpartners.aboutamazon.com, the page's own publish date 2026-11-05, re-read 2026-11-10): from 2027-02-01 Amazon will "eliminate the storage utilization surcharge" and "remove the aged inventory surcharge and combine it with monthly storage fees into a single, age-based rate"; the low-inventory-level fee, today "assessed using trailing 30- and 90-day sales", "will apply only when your inventory falls below 28 days of supply, based on actual shipments in both the four weeks before and after the assessment date". Fulfilment fees rise "$0.19 per unit sold" on average ("approximately 0.8% of the average item's selling price"), most changes effective 2027-01-15.
- [official] 2026 fee letter (published 2025-10-15): an average rise of "about $0.08 per unit sold", effective 2026-01-15.
- (gap fill 2026-11-10) [official] News_Amazon, "Plan FBA inventory levels using a new metric", 2023-12-19, https://sellercentral.amazon.com/seller-forums/discussions/t/1aa7614a-5542-4529-abe1-ddf452681630: "Sellers who maintain units above the Minimum Inventory Level see a 15% increase in sales over a four-week period on average, though actual results may vary." Amazon gives no method, sample or period for the figure. This is the source of the "15%" that Amazon Global Selling's Chinese channel relays (P5).
- [official] News_Amazon, "Holiday 2026: Same fees, same eligibility, earlier deadlines" (forum, 2026-07-07): peak fulfilment fees run "from October 15, 2026, to January 14, 2027"; the Prime-badge arrival dates differ by placement option (for example "October 21: FBA shipments with "minimal shipment splits" option selected").
- [official] News_Amazon, 2024-04-01: the low-inventory-level fee began 2024-04-01 with April 2024 as a credited transition month.

## What practitioners add

Every figure here is the named tool's or person's, not Amazon's and not cx's.

### P1. The tools share one formula family and no default

The shape is the same almost everywhere: a daily-sales figure × (lead time + cover days + safety days) − stock position. What differs is every setting.

| Tool | Daily-sales basis (default) | Stock-out correction | Lead time and cover | Safety / buffer default | Alert default | Source and date |
|---|---|---|---|---|---|---|
| Amazon skill `stockout-prevention` | 30 days ÷ 30 | none | none | none | <7 critical, <21 warning | [official] local zip |
| Amazon FBM Restock recommendation | forecast, two-week demand | not stated | not stated | not stated | days of supply <14 (eligibility) | [official] forum post 2025-03-14 |
| SoStocked | plain average of seven averages (2/7/15/30/60/90/180 days); weights off by default | on: day is out when "ZERO inventory AND if your sales drop below 30% of your daily average sales" | stages, seller-entered; FBA transfer default 10 days; AWD→FBA fixed 20 days | no default; "The standard rule of thumb is to keep 30 days' of supply at Amazon FBA." | seller-set min-max | [opinion] help.sostocked.com articles 106, 108, 102, 225, 173; 2025-08 to 2026-08 |
| Inventory Planner | "Recent sales and trends"; "Seasonal" needs 12+ months | on by default; stock-out days leave the denominator; ≤3 sale days → divide by 30 | lead time + days of stock, seller-entered (example 14 + 30) | minimum stock, no default number stated | stock ≤ minimum | [opinion] help.inventory-planner.com articles 589017, 2242706, 638170, 1959514 |
| Helium 10 | "Helium 10 Exponential"; "Additive" for seasonal; up to two years | not stated | one lead-time number + reorder frequency | page prints both "around 60 days' worth of inventory" and "four weeks of inventory cover" | not stated (help 403) | [opinion] podcast #176, 2020-09-12; tool page modified 2026-01-20 |
| Jungle Scout | simple average over a chosen window | not stated | seller-entered, no default | none | [snippet] "Reorder Soon … within a 7-day window"; Overstock at 150% of reorder days | [opinion] blog 2019-11-12; help 403 |
| RestockPro (gap fill 2026-11-10) | "7, 30, 60, 90, or 180 days", or "Average" with seller-set weights; default window and weights not published ("For most products, choosing 30 or 60 days works well" is advice) | optional: "it will adjust the velocity up to 15% to account for out of stock time periods"; "only looks at out of stock periods in the last 30 days"; default on/off not published | "(45 + 14) x 1.2 = 70.8 units … Coverage Required"; one lead time per supplier or for local→FBA; default not published | "Most sellers start with a minimum of 30 days here and a maximum of 45" (a starting point, not a stated default) | below min "flagged red", between min and max "flagged yellow" | [opinion] ecomengine.com/help/restocking-preferences, /suggested-quantity-calculation (no page date), re-read 2026-11-10 |
| InventoryLab (Restock Report add-on, Threecolts) (gap fill 2026-11-10) | "Avg. Daily Sales of the past 30 days" (all-time if none); forecast picks per MSKU the lowest-error of Linear, Moving Average (5-day window), Seasonality Moving Average | stock-outs: not published; outliers replaced "with the average of the last 7 days prior" | lead time per MSKU, default not published; "Est Replen Period … default setting is 30 days" | "Safety Stock = Avg Daily Sales x Lead Time"; reorder point = lead-time usage + safety stock | "The default number of days for Restock Soon is 14 days"; "Restock Now is 0 days" | [opinion] thjrecvolts.useresponse.com knowledge-base articles restock-report-calculations, -settings, -stock-status-definitions (modified 2023-10-30), re-read 2026-11-10 |
| sellerboard (gap fill 2026-11-10) | "weighted averages across multiple periods: 3 days 7 days 30 days 60 days 180 days"; default weights not published | "Days when the product was out of stock are excluded" | stages: "manufacturing time, shipping to prep center, shipping to FBA, and an FBA buffer for check-in"; defaults not published | "FBA buffer adds a safety margin (in days)"; default not published | "Red: You are past the optimal reorder date"; "Yellow: You are approaching the reorder point"; email alerts opt-in | [opinion] help.sellerboard.com "Inventory planner" (modified 2026-02-24); blog 2026-08-05; re-read 2026-11-10 |
| Extensiv | "Sales Velocity x (Days In Stock + Lead Time + Reorder Buffer) x (1 + Forecasted Growth) – Incoming Units" | not stated | as formula | "prepopulates every account with default values" (not printed) | minimum level formula | [opinion] help.extensiv.com |
| Inventory Hero | "Reorder point = (daily sales velocity x total lead time in days) + safety stock" | not stated | 30/90/365-day projection | per SKU | not stated | [opinion] inventoryhero.ai |
| 领星 Lingxing | "7天日均：50%，14天日均：30%，30天日均：20%"; last two days excluded | optional | six stages; slowest channel by default | 安全天数 seller-set; 补货频率 "默认是0天" | reminder "默认是3天" ahead | [opinion] lingxing.com/help/article/replenishmentAadvice |
| 赛狐 Sellfox | same 50/30/20; last two days excluded | "x天日均 = x天日销量/(x-n)" | (备货天数 + 安全天数) | seller-set | seller-set rules | [opinion] Sellfox help, 补货建议 |
| 积加 Gerpgo | "系统默认为历史7天日均", counted from the day before yesterday | "过去N天的总销量 /（N-断货天数）" | approval 3, QC 2, receiving 3, cycle 0 days | "安全库存天数…（默认为14天）" | 红绿线 chart | [opinion] help.jijiaerp.com/docs/eeE2AHAR |
| 优麦云 SellerSpace | weighted 3/7/14/30 | not stated | "安全天数 ≥ 采购计划 + 采购天数 + 头程" | seller-set | not stated | [opinion] sellerspace.com |
| 马帮 Mabang | seller-built formula over 3/7/14/30-day sales | not stated | seller-set | none | not stated | [opinion] mabangerp.com news, 2022-09-05 |
| 船长BI CaptainBI | seller edits the formula for 日均销售, 可售天数, 建议补货 per store | not stated | "设置自己的备货天数和到货天数" | per SKU quantity | not stated | [opinion] CaptainBI help |
| 店小秘 Dianxiaomi | 按备货天数 or 按销量权重, with order-size and promotion coefficients | coefficients, up to five bands | seller-set | seller-set | not stated | [opinion] help.dianxiaomi.com article 2260 |
| 通途 Tongtool (gap fill 2026-11-10) | 采购建议: trend-dependent weights over 3/7/15/30-day averages, e.g. rising: "日均销量=avg3*0.4 + avg7*0.3 + avg15*0.2 + avg30*0.1"; the page says the numbers are illustrations only ("请不要以此作为您的数据设置参考"); defaults not published | not published (a 客单量系数 caps one-off bulk orders; a 销售系数 scales holiday/promotion ranges) | "[日均销量*(安全交期 + 采购频率)] - 当前库存 - 在途库存 … - AWD可用库存 - AWD补货至FBA在途库存 …" [read off the formula image]; 安全交期 = 在途天数 + 预警天数 | 安全库存 seller-set units; 采购频率 30 in the built-in template [image] | a "仅显示低于安全库存的货品" filter; no push alert described | [opinion] help.tongtool.com articles 150 (2026-04-15), 149 (2026-03-18), 88 (2026-08-05), read via the help site's own GET JSON calls |

Not in the table: 酷鸟 Koniao (koniao.com) is a review, repricing and PPC assistant with no replenishment feature on any page read (2026-11-10); its help desk domain did not resolve. Also not in the table, because their pages give no setting: Prediko, Flieber, Linnworks and Veeqo (product pages give no number), Cogsy ("Cogsy has been discontinued and is no longer available"), Forecastly ("officially closed on September 15, 2021").

### P2. What counts as stock differs by tool

- [opinion, Sellfox] Its formula subtracts "FBA库存 + FBA在途 + AWD库存 + AWD在途" and overseas-warehouse stock; inbound counts by shipment status, default SHIPPED, IN_TRANSIT, DELIVERED, CHECKED_IN, RECEIVING.
- [opinion, Lingxing; survey for the definition] FBA库存 = 可售 + 待调仓 + 调仓中.
- [opinion, SoStocked] "FC Transfer and FC Processing appear to be included in utilization"; In-Stock Head Start makes inbound look available.
- [opinion, Inventory Hero] "Reserved and in-transit units are not sellable cover yet".
- [official] Amazon's skill counts fulfillable only (section C); Amazon's Restock report prints two days-of-supply columns, one with open shipments and one without (section A).
- [opinion, forum reply in "Low Inventory Fees - Removal", 2025-07-01] The low-inventory-level fee counts sellable units only; inbound is not counted until received. The asker had 448 on hand and 588 inbound and was charged.

### P3. What the tools take from outside SP-API, and what they say the API cannot do

- [opinion, Gerpgo] FBA capacity is scraped: "抓取相应亚马逊后台FBA库容统计，每天8点，12点，16点、21点更新一次" (fetched from Seller Central four times a day), through a sub-account that must hold the capacity permission.
- [opinion, Sellfox] A browser plug-in fetches Seller Central reports: "插件只是模拟人工手动去亚马逊后台下载报告" (the plug-in only imitates a person downloading the report), and Seller Central must stay signed in.
- [opinion, SoStocked] Capacity limits are typed in by hand from Capacity Monitor (article 226, 2025-08-14). [snippet] "Amazon does not provide us with an API data on Utilization Qty or Restock Limits" (the page is now 404).
- [opinion, Gerpgo] Send to Amazon by API: "目前仅支持“非亚马逊合作承运人”…（亚马逊未提供API）" (only non-partnered carriers; Amazon gives no API), and several destination stores are unsupported "(亚马逊API不支持)".
- [opinion, Inventory Planner] The new inbound API became mandatory on 2024-12-20; a plan's splits show only after it is progressed in Seller Central.
- [opinion, sellerboard, help "Inventory planner", modified 2026-02-24, re-read 2026-11-10] It shows Amazon's "Recommended ship-in quantity / date by Amazon": "They are shown for reference and are not calculated by sellerboard." (corrected: the survey's wording "sellerboard does not calculate these two values" is a paraphrase not found on the page.) It also states "AWD inventory does not count toward your FBA historical days of supply" (blog, 2026-08-05).
- (gap fill 2026-11-10) [opinion, InventoryLab] its On Hand column "includes fulfillable, unfulfillable, and reserved inventory quantities", while its replenishment quantity uses "Fulfillable on-hand". [opinion, RestockPro] "QoH at Amazon + Local + On Order = Coverage Available", with "Quantity on Hand (QOH) is the fulfillable quantity that you have on hand at Amazon FBA"; AWD columns appear in its grid, their use in the calculation is not stated. [opinion, 通途] its FBA sync maps "可用库存数" to Amazon's sellable count and "在途数" to "正在接收中的数量", and recommends ("建议勾选") treating a warehouse's in-transit stock as available.

### P4. Pricing and agent surfaces, one line each (all as read on the dates in Pages read)

- SoStocked "Starting at $175 per month"; no MCP. Inventory Planner quote-only; a "Retail Intelligence agent" in Sage Copilot; public API in beta. Helium 10 Platinum $129, Diamond $359 a month (billed monthly); MCP since 2026-07-16 for Diamond users, with "40+ MCP tools", of which the landing page names eight; at launch the scope was "Research, Ads, and Profits data", and none of the eight named tools is a restock or forecast tool, though `get_account_profit` is described as returning "inventory health, sales velocity, and listing details on demand" (re-read 2026-11-10; whether any unnamed tool reaches Inventory Management is not published). Jungle Scout from $29 a month billed yearly; its MCP (2026-06-29) is market data only. Prediko priced by GMV. Flieber "Priced to your operation"; "MCP-native", with an MCP server, a CLI and a connector. Veeqo: MCP listed. (gap fill 2026-11-10) RestockPro "$49 /mo", tiered by FBA orders, no MCP found. InventoryLab's Restocking Insights "Optional $25/mo add-on" on a $69/mo plan; the Seller 365 bundle advertises an "AI Operator", no MCP. sellerboard $19–$79 a month, inventory management on every tier, no MCP found. 通途 ERP2.0 "¥299/月 包含6000个订单", and an official MCP (`mcp.tongtool.com`) for order, product and stock queries; whether it exposes 采购建议 is not stated.
- Lingxing (re-read 2026-11-10, https://www.lingxing.com/help/article/mcp): "领星 MCP Server 提供了300种工具…每用户将可以在1分钟调用100次MCP TOOL" (300 tools; 100 calls a minute per user), enabled "（仅限付费用户）" (paid users only); under "FBA › 补货" the tool `query_fba_valid_list` "查询 FBA 补货建议" (reads the FBA replenishment-suggestion list), and under "货件" the writes `fba_plan_storage_allocate` "锁定 FBA 发货计划库存" (locks the ERP's own stock against a shipment plan) and `fba_plan_storage_release` (releases it). The stock lock is a write to Lingxing's warehouse records, not to Amazon. Sellfox MCP reads and writes at one call a second per tool; its listed write tools are advertising. CaptainBI MCP is in public test, "免费版每日仅可调用 100 次". ECCANG markets "万多MCP" (2026-08-14). SellerSpace sells an MCP with a free quota in October 2026.

### P5. Vendors and practitioners on Amazon's own recommendations

- [opinion, SoStocked] "Amazon's restock suggestions are very basic and faulty."
- [opinion, ECCANG, 2025-03-18 and 2025-03-26, eccang.com/news/3811 and /3833] On Amazon's AI restock: it has a "数据孤岛" (data island) problem. Its "14天" and "8周" match the FBM post in section B. (corrected 2026-11-10 by the verifier) The page also attributes a stock-out-rate figure and other percentages to "亚马逊官方测试" (Amazon's official tests); no Amazon page, and no other source, was found carrying them (searches in Chinese and English, 2026-11-10), and Amazon's FBM post of 2025-03-14 gives none; the figures are not carried here.
- [opinion, sellers on sellersasksellers.com] "We follow it somewhat, but find it rather inaccurate"; another reports recommendations for items with no sales in 30 days.
- [opinion, Seller Central Europe forum, 2024-06-20] "Recommendations from IP report and Restock report don't match up."
- [official, via 跨境追风者, 2024-01-19] Amazon Global Selling: "保持最佳库存水平的卖家在4周内单位销售额增长了15％" (sellers at the optimal level grew unit sales 15% in four weeks). (corrected 2026-11-10 by the verifier) The figure is Amazon's own: News_Amazon, 2023-12-19, "Sellers who maintain units above the Minimum Inventory Level see a 15% increase in sales over a four-week period on average, though actual results may vary" (section E). Amazon gives no method; the English says "sales", the Chinese relay "单位销售额".
- [opinion, Mabang; survey, 2020] "亚马逊后台推荐的补货数量并非是卖家实际能够创建的真实的商品补货数量" (the recommended quantity is not what a seller can actually ship in).

### P6. Days-of-cover targets: the spread

| Who, when | Target as stated |
|---|---|
| Amazon's skill | 21 days of fulfillable stock is "HEALTHY" |
| My Amazon Guy, "Avoid Stockouts and Overstocks", published 2024-07-30, modified 2026-10-31 (re-read 2026-11-10) | "Hold 35 to 55 days of cover rather than aiming at 28, because the threshold is a cliff and not a slope"; FAQ: "Hold 35 to 55 days of cover on anything moving more than 100 units a month"; for Q4 "Build to 60 to 75 days by early October, before peak fulfillment fees start on October 15" |
| SPS Commerce / Carbon6 | "Maintain enough FBA inventory to cover 30 to 60 days"; elsewhere "30 days of buffer stock and then 60 or 90 days of your max stock"; "at least 35 days of buffer stock at FBA" for the fee |
| eComCrew, episode 542 | "between 29-181 days of inventory in stock" |
| A seller on sellersasksellers.com | "around 50-70 days of stock at a time" |
| 什么都不懂, 2023-05-06 | 1.5–2 months at FBA, 1–1.5 at sea, 1 in the local warehouse |
| 章鱼工作室, 2026-07-02 | "30—60天：健康库存；20—30天：补货预警；10—20天：高风险库存；低于10天：断货危险。" |
| Thread 92245, 2024-05-26 | 35 days transit + 35 days safety + 7 days frequency |
| Hello哥, 2022-09-26 | turnover about 60 days; safety 10 days by air, 15–20 by sea |
| 跨境Andy, 2019-12-04 | FBA stock at least double monthly sales |
| 积加跨境ERP | 1.2–1.5 times monthly sales |
| Mabang; survey | turnover within 15 days |

### P7. Where practitioners disagree

- **Raise the price when cover runs short.** For: jerryhuang01 (2023-12-06), 什么都不懂, 跨境阿杜 (gap over 15 days, raise 10–20%; under 7 days, keep the price). Bounded: My Amazon Guy, "Jumping more than 10% in a single change can trigger Amazon to remove your Buy Box". Against: Amazon's skill, "Do not raise pricing as an option at all".
- **Close the listing or leave it.** Hello哥 (2022-08-15) records both schools. My Amazon Guy: closing a child "does not preserve BSR", and "Keep one listing variation live".
- **After restock: price cut or coupon.** 深深深情 says cut the price or build a new listing; Hello哥 says use a coupon, not a cut.
- **Peak: send early or send small.** Amazon asked for arrival by fixed dates (section E; 2024: by 2024-10-19, via 跨境追风者). 亚马逊森林中的麋鹿 (2024-12-04) shipped at the end of August, paid a month of peak storage, and now says "少量多批次". Hello哥 stocked 6–9 months for peak 2021 and spent half a year clearing.
- **A honeymoon period.** My Amazon Guy: "a brief launch window lasting 15–30 days". Kevin King's episode of 2024-10-21 is titled "No such thing as a "honeymoon" period on Amazon".
- **Removal and IPI.** Empire Flippers lists removal as a way to raise sell-through; alexya (2022-09-07) says "移除冗余库存是不能有效提升店铺的平均售出率的" (removing excess does not raise sell-through).
- **How big a stock-out's cost is.** My Amazon Guy budgets "two to three times normal ad spend" to recover; Hello哥 measured one product at nearly 50% lower sales after a one-month gap; 跨境Andy relays "三四天的缓冲时间" (three or four days of grace); Hello哥 says a niche product is hardly affected. None is Amazon's.
- **Placement splits.** 暴富Lucky (2024-05-31) needed four identical cartons by trial; Amazon's later text asks for five (via 跨境追风者, 2025-02-07). eComCrew (episode 564) lists three ways to cut the fee, AWD among them; a 知无不言 thread calls the two 2024 fees a push onto AGL and AWD (qilingwang111, 2023-12-06).
- **One rule or per SKU.** Inventory Hero: "A single weeks-of-cover rule across the catalog overstocks slow movers and starves fast ones".

### P8. Other teaching worth knowing

- [opinion, Chelsea Cohen, OMG podcast 187] Produce slightly more than a container and leave the extra at the supplier, to air-freight only if needed. [opinion, same, MerchantSpring webinar] under the 2021–2022 restock limits, "Smaller orders more frequently", and FBM sales counted toward the 90-day sales.
- [opinion, 积加跨境ERP] Safety stock = (expected peak daily sales − 30-day average) × purchase lead time. [opinion, Jamie咩, 2023-09-12] change the window weights by hand when a window is distorted by a stock-out.
- [opinion, Hello哥, 2022-09-26] weights 60/30/10 over 3/7/15 days for a pushed product; air covers the gap and sea carries the rest.
- [opinion, Susanna5 and Ronghe, 2024] capacity requests: credits at $0.15 per $1 of sales; a bid of 1.6 was charged 1.45.
- [opinion, freight] 货代超人不会飞 (2026-01-24) files ZIM as a fast ship at 13 days; 爆米花l (2025-03-17) files it as a slow ship at about 30 days door to door.
- [opinion, Marketplace Pulse] "Amazon Takes a 50% Cut of Sellers' Revenue"; "in practice, most sellers cannot manage their supply chains as perfectly as Amazon theorizes".
- [opinion, Canopy Management] IPI: "Technically, 400 is the floor"; it says the minimum inventory level "will contribute directly to your overall IPI score", which this seat did not find on an Amazon page.
- [opinion, Thrasio's filing as summarised by Best at Amazon] about $425 million of excess inventory at the end of 2022.

### P9. Practitioners not covered by the seat (gap fill 2026-11-10)

Read 2026-11-10 by the verifier's reader by plain GET; quotes verbatim, downloads under `scratch/stock-playbook/sellers-tools-and-research/verifier-dl/practitioners/`. Every number is the named source's practice or claim.

English:
- [opinion, Riverbend Consulting, Brianna Kipnis, "Amazon Restock Limits: How to Survive and Thrive", 2025-10-07, https://riverbendconsulting.com/blog/amazon-restock-limits/] "Don't send in 90 days of inventory. Amazon now rewards 30-45 day supply strategies."; "Create smaller, more frequent shipments: Ship weekly or bi-weekly"; on peak, "Seasonal buffer zones have shrunk … Amazon requires strong historical data to justify any bump in restock allowances"; "Testing FBM on at least 10% of SKUs". Same author, "Avoid Fees: Improve your Amazon IPI Score Now", 2025-10-21: below "typically 400, though it can vary by quarter, you risk losing access to unlimited storage"; "Sellers report drops of 30, 50, even 100 points in a matter of days with no apparent cause." Riverbend, "Navigating the New Amazon FBA Capacity Limits Guidelines" (updated 2026-09-23) says limits "are calculated during the third week of each month"; the listing playbook's read of Amazon's help page has them announced "during the fourth week of the month" (`areas/restock-and-forecast.md` G1); the two do not match.
- [opinion, James McConnell Jr., Marketplace Prep (a prep centre), "Low Inventory Fee Explained", published 2024-02-12, "Updated September 2026", https://marketplaceprep.com/low-inventory-fee] "never dipping below 35 days of stock. Yes, 35, not 28", because Amazon is "calculating these metrics on a 7-day cycle"; checking in at 5 days left and topping up to about 40 days "is no longer enough"; for one example product "29-54 days at Amazon at all times" on 2024 rates ("directional"); for seasonal goods "sending in the product, 120 days before the holiday may be a better move"; and "The IPI Score rewards fast sell-through and dings you for excess inventory. Yet this fee penalizes you for dipping below 4 weeks?"
- [opinion, Seller Sessions, host Danny McMillan with James McConnell Jr., "The Challenge of Amazon's New Fee", 2024-02-20, show notes only, https://sellersessions.libsyn.com/the-challenge-of-amazons-new-fee] the fee "does not account for inbound shipments until they're officially checked in"; sellers should keep "a buffer". No McMillan-bylined stock article was found on sellersessions.com.
- [opinion, My Amazon Guy, Ken Zhou, page modified 2026-10-31] "Stay above roughly 35 days of supply and below 150 days of inventory age and you sit outside both fee walls"; "Set the alert threshold at 45 days rather than at your reorder point"; "Under 35 days is your stockout watchlist, and over 120 days is your overstock watchlist."
- [opinion, Steve Chou, MyWifeQuitHerJob, "Amazon's 2026 Fee Hikes", undated, refers to January 2026] on placement: "Now you pay Amazon to ship to one warehouse, or you ship to 10 warehouses yourself at great cost. Either way you lose."; episode 578: "Hitting Amazon's ideal inventory window is nearly impossible in practice"; his answer is selling off Amazon, not a days target.
- [opinion, Reddit r/FulfillmentByAmazon, pseudonymous posters, read via the reddit.sentinel-team.org snapshot service because reddit.com answered 403] thread "How are you dealing with new FBA restock limits?" (about April 2025; snapshot 2026-02-04): "I started holding all of my excess inventory locally and just shipping in what I need to … I'm careful to be stocked up in Sep/Oct. on my best sellers" (u/foxinHI); "I keep about 3 weeks worth at a local 3PL now specifically for when limits get weird" (u/springcaterpillar); "AWD, IMO, doesn't make sense if your master cartons only have a few units" (u/fmckinnon). Thread "Inventory management automation to prevent FBA limits" (about November 2025): "forecast demand + lead time + inbound + safety stock + Amazon limits = reorder point", with "2–3 years of historical sales to build the seasonal curve" adjusted by "the last 3–6 months" (u/Chrolm). Threads on the 2024 placement fee were seen as search titles only.

Chinese:
- [opinion, AMZ123 Q&A, undated, https://www.amz123.com/ask/JkJd7b6t] "分批次走海运推新品：第一批货不超过三千" (launch new products by sea in batches, the first no more than 3,000 units); on a launch spike "即使利润低也要发空派，防止在新品周期内断货" (send air-express even at thin margin rather than stock out in the launch period); steady phase "一般以两个月为周期" (a two-month cycle).
- [opinion, 一汤说 on AMZ123, 2026-09-10, https://www.amz123.com/t/6nfV5YtQ] peak planning is "倒排日期" (back-scheduling from the date stock must be sellable, through receiving, final-mile appointment, customs, transit and factory lead time), with a written fallback including "要不要分一批空运做保险" (whether to split a batch onto air as insurance). The piece ends by promoting Amazon's SEND service.
- [opinion, 法思特海外仓 (an overseas-warehouse firm) on AMZ123, 2026-09-08, https://www.amz123.com/t/9NCw12dy] "过去大批量囤货进 FBA，慢慢售卖的老打法，今年风险极大" (bulk-loading FBA is very risky this year); "富余库存存放海外仓，按销量小批量补货 FBA" (hold excess in an overseas warehouse and refill FBA in small batches by sales). The author sells that storage.
- [opinion, 跨境潮汕妹 on AMZ123, 2026-09-10, https://www.amz123.com/t/7RQzZsRe] "按批次安排补货。不要一次性把所有资金压在同一批货上" (replenish in batches; do not sink all cash into one lot).
- [opinion, 德速电商物流 (a logistics firm) on AMZ123, 2024-03-08, https://www.amz123.com/t/DqajEhrV] on the placement fee: "建议选择多点入仓，特别是对于标准件的货物" (choose multi-point inbound, especially for standard size); AWD auto-replenishment "能够免去入库配置服务费+低量库存费" (avoids the placement fee and the low-inventory fee). [opinion, 巨宝物流, 2024-03-22, https://www.amz123.com/t/7sfS0K3T] the highest minimal-split fee is "大致为FBA配送费的6%-8%"; fee-dodging "黑科技" tricks drew "绩效警告" (performance warnings).
- [opinion, 大湿聊跨境, reprinted by 雨果网 cifnews, 2024-03-04, https://www.cifnews.com/article/155729] sea cost must be judged as "海运费和入库配置费的总和" (freight plus placement fee), billed 45 days after receipt; recommends AGL.
- [opinion, 强哥 (account 跨境电商张), 卖家之家 mjzj, 2018-12-03, https://mjzj.com/article/41226; before both 2024 fees] "我一般会准备一个月的货…宁愿多频率少数量的备货" (I stock one month and would rather ship small and often); "发海运能让你挣更多的钱，我一直觉得这是个伪命题" (that sea freight earns more is, to me, a false proposition); his reorder point is 45 a day × 20 days of lead time (7 production + 3 domestic + 4 express + 3–7 check-in), about 900 units.
- [opinion, 亿极科技 on mjzj, 2018-07-18] a two-echelon trigger: order when total days of sale fall below the purchase lead time; ship to FBA when FBA days of sale fall below the local-to-FBA replenishment time.
- [opinion, 九方通逊 (an Amazon SEND carrier), sponsored piece on 凤凰网科技, 2026-10-28, https://tech.ifeng.com/c/8xaf0dAiGtw] safety stock "覆盖 14 天左右销量", raised to "21–28 天" at peak or congestion; "海运为主、快船为辅、空运兜底" (ocean as base, fast ship as support, air as backstop), with ocean base stock covering "30–45 天"; book main ocean freight three months before an event, switch to fast ships one month before; "海运旺季，建议额外预留 7–10 天缓冲，空运预留 3–5 天".
- [opinion, AMZ123 "Summer", 2026-11-06, https://www.amz123.com/t/bu8s3Gz7] restates the 2027 letter and reads the surcharge's removal as letting sellers stage stock "更灵活" (more freely) before peak. No Chinese or English operator's method response to the 2027 letter was found.

Where these disagree (added to P7):
- **Days at Amazon.** Riverbend "30-45 day supply"; McConnell a 35-day floor, a 40-day top-up "no longer enough"; Ken Zhou 35 days to 150 days of age; Cohen at least 30 days; 强哥 one month; 九方通逊 14 days of safety on top of 30–45 days of ocean base stock (a buffer, not total cover).
- **Small and often, or front-loaded before peak.** Small: Riverbend, Cohen, 强哥, 法思特, 跨境潮汕妹. Front-loaded: McConnell (120 days ahead for seasonal goods), u/foxinHI (stocked by September–October), with Cohen's surplus held at the supplier rather than at Amazon.
- **Air or sea.** 强哥 calls sea's advantage "伪命题"; 九方通逊 puts ocean first and air last; the AMZ123 Q&A sends air on a launch spike "即使利润低"; Cohen airs "only, if you need to".
- **Placement fee.** 德速: multi-point inbound or AWD; 大湿聊跨境: AGL; Riverbend: 3PLs or forwarders "may offer better rates"; Steve Chou: "Either way you lose"; u/fmckinnon: AWD does not pay for few-unit cartons.
- **Low-inventory fee.** McConnell: 35 days plus exemptions; Ken Zhou: a corridor; 德速: AWD auto-replenishment; Steve Chou: leave Amazon. Riverbend's 30–45 days does not mention the fee.

Not reached: 跨境眼 (kjyan.com gave no response), 老魏/赢商荟 and Moss (no bylined article found by search), Vanessa Hung (her Substack lists no posts), reddit.com itself (403).

## Published research

A map only. Records marked "record" were read as the publisher's metadata and abstract (OpenAlex or RePEc), not the full paper.

- **Inventory theory.** Arrow, Harris and Marschak 1951 and Harris 1913 (order quantity); Clark and Scarf 1960 and Graves and Willems 2000 (multi-echelon, the frame for a 3PL or AWD feeding FBA); Eppen and Martin 1988 and Chopra, Reinhardt and Dada 2004 (safety stock when lead time varies); Lee, Padmanabhan and Whang 1997 (bullwhip); Schweitzer and Cachon 2000 (people order toward the mean even with known demand). [research, records] King's practitioner article gives the combined formula and separates cycle service level from fill rate (full text read). These tell a seller what a safety-stock figure assumes; none gives a number.
- **Forecasting.** Croston 1972, Syntetos and Boylan 2004/2005, Teunter, Syntetos and Babai 2011, Kostenko and Hyndman 2006 (intermittent demand and how to classify it; the last read in full); Hyndman and Koehler 2006 (accuracy measures); Fildes, Ma and Kolassa 2019 (retail forecasting review). The M5 accuracy competition forecast "42,840 time series" of Walmart unit sales [research, record]; it is store retail, not Amazon. Amazon's own papers: DeepAR (arXiv 1704.04110, Amazon Research), MQ-RNN (arXiv 1711.11053, tested on Amazon.com demand) and "Deep Inventory Management" (arXiv 2210.03137), which reports a learned policy that "outperforms model-free RL and newsvendor baselines, in both simulations and real-world deployments" [research, full text]. These say what Amazon's researchers published; no paper says which model produces a Seller Central recommendation.
- **Censored demand.** Wecker 1978, Conrad 1976, Nahmias 1994, Agrawal and Smith 1996, Lau and Lau 1996, Anupindi, Dada and Gupta 1998, Huh, Levi and Rusmevichientong 2011, Vulcano, van Ryzin and Ratliff 2012, Besbes and Muharremoglu 2013, Jain, Rudi and Wang 2014 [research, records]. Sales during a stock-out understate demand; dropping the days (what the tools in P1 do) is the simplest correction, and the literature shows estimates differ by method.
- **Stock-out and availability effects** (detail in `areas/running-out.md`). Anderson, Fitzsimons and Simester 2006: a field test finding the cost "extends to both other items in the current order as well as future orders" (a catalogue retailer). Jing and Lewis 2011: an online grocer, "dramatic but nonlinear". Gruen, Corsten and Bharadwaj's worldwide study: average out-of-stock rate 8.3% in stores [research, full text]. On Amazon itself: Cui, Zhang and Bassamboo 2018, two field experiments on Lightning Deals, "a 10% increase in past claims leads to a 2.08% increase in cart add-ins in the next hour"; Chen and Tsai 2024 use Amazon's own stock-outs to study recommendations. Park, Rabinovich and Tang 2020: scarcity messages "can decrease daily sales by an average of 17.60%" at one online retailer, not Amazon. No paper found measures search-rank loss after an FBA stock-out; that claim rests on practitioners.
- **FBA, the Buy Box and fees.** Raval 2023: Amazon "substantially prioritizes its retail arm and fulfillment arm" in the Buy Box. Lee and Musolff 2021; Dendorfer and Seibel 2026; Lai, Liu and Xiao 2022 (theory); Gutiérrez 2022 (welfare model of fees); Zhu and Liu 2018; Crawford et al. (first-party entry). Italy's AGCM fined Amazon over €1.128 billion for tying Prime benefits to FBA [research, press release read]. **This seat found no published study of Amazon's storage limits, capacity limits, low-inventory-level fee or placement fee and sellers' stocking behaviour.**

### The research map, read in the open (gap fill 2026-11-10)

`areas/restock-and-forecast.md` carries its own research section; this is only the map, with what each strand can and cannot tell a seller. Quotes come from versions opened on 2026-11-10 by the verifier's reader (downloads under `scratch/stock-playbook/sellers-tools-and-research/verifier-dl/research/`). The "can / cannot" lines are [seat].

- **M5 accuracy competition** [research] Makridakis, Spiliotis, Assimakopoulos, IJF 2022 (doi 10.1016/j.ijforecast.2021.11.013); read as the authors' preprint of 2020-10-06, https://statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf (may differ from the journal text; ScienceDirect answered 403). Data: "42,840 time series that represent the hierarchical unit sales of … Walmart", 3,049 products, a 28-day horizon, and "for the first time ever … series that display intermittency". Findings: "most of the methods examined utilized LightGBM"; "an impressive 22.4% for the winning team" over the best benchmark (bottom-up exponential smoothing); but "the average improvement … is 40% at level 1, which drops to about 23% at levels 5, 6, and 7, and reaches 3% at levels 10, 11, and 12 … rather limited … at product, product-State, and product-store levels"; "all winning submissions utilized external information", price features among the most important; cross-learning over related series beat series-by-series fitting. Can: pooling related SKUs and feeding price and event data helps aggregate forecasts. Cannot: at single-SKU level, where a seller restocks, the best methods gained about 3% over exponential smoothing; Walmart store sales are not FBA demand, and the paper models no stock-out, lead time or cost.
- **M5 uncertainty competition** [research, abstract via the OpenAlex record] doi 10.1016/j.ijforecast.2021.10.009: the same 42,840 series, nine quantiles "(0.005, 0.025, 0.165, 0.250, 0.500, 0.750, 0.835, 0.975, and 0.995)". Full text unreachable (403); its findings are not recorded here.
- **Amazon's forecasting papers** [research] DeepAR (Salinas, Flunkert, Gasthaus, arXiv 1704.04110v3): trained on "weekly item sales from Amazon" among other sets, "accuracy improvements of around 15% compared to state-of-the-art methods"; the paper makes no production claim. MQ-RNN/MQ-CNN (Wen et al., arXiv 1711.11053v2): "Weekly demand series of around 60,000 sampled products … within the US marketplace … 2012 to 2017", horizons 1–52 weeks. [official] Amazon Science, "The history of Amazon's forecasting algorithm", 2021-08-09: MQ-RNN/CNN "outperformed a dozen legacy systems designed for difference product lines", and "With MQ Transformer, Amazon now has a unified forecasting model"; the page does not mention DeepAR. Deep Inventory Management (Madeka et al., arXiv 2210.03137v3): a 26-week trial on 10K products against a "Control (receiving Newsvendor policy buy quantities) group … the current production system"; treatment cut inventory "by ∼12%" with no significant revenue loss; it assumes lost sales because "only 15% - 23% of customers are willing to delay a purchase when confronted by an out-of-stock item". Can: Amazon's own retail buying forecasts quantiles across the catalogue and treats a stock-out as a lost sale. Cannot: none of these papers says which model produces a seller's Restock report, MIL, FBM recommendation or fee metric.
- **Newsvendor, reorder point, safety stock, service measures** [research, course notes] MIT OCW 15.772J "Newsvendor Inventory Problem": choose Q with F(Q) ≥ underage / (underage + overage); for normal demand "Q = µ + (z*)(σ)". Bricker (Univ. of Iowa), "Reorder Point" slides: "Safety stock: (reorder point) − (expected lead-time demand)"; "Cycle service level: percentage of cycles without a stockout"; "Product fill rate: percentage of product demand filled without backordering"; "These two measures can be quite different!"; with random lead time, lead-time demand variance "σLT² = µt σd² + µd² σt²"; a 99% fill-rate example gives a cycle service level of "only 81.6%". Chopra, Reinhardt and Dada (working paper 2003-07-31, published Decision Sciences 2004): "fill rates of between 97-99 percent are achieved for cycle service levels between 50-70 percent", and at those service levels the normal approximation "erroneously encourages managers to focus on reducing the variability of lead times when they would be better of reducing the lead time itself". Can: a stated "in-stock %" means different things as fill rate or cycle service level; lead-time variance enters safety stock. Cannot: these single-location models carry no capacity limit, low-inventory fee or placement fee. No open note stating (s,S) or (R,S) formulas was reached (two MIT DSpace notes answered 404).
- **Intermittent demand** [research] Teunter, Syntetos and Babai 2011 (EJOR; abstract via Semantic Scholar's record): Croston "is positively biased" and does not update through long zero runs; TSB "updates the demand probability instead of the demand interval, doing so in every period"; tested by simulation. The classification cut-offs, as quoted by Wang, Kang and Petropoulos (arXiv 2304.03092v4): "The critical values of segmentation are 1.32 for ADI and 0.49 for CV2" (from Syntetos, Boylan and Croston 2005, tested on "3000 real-intermittent demand data series coming from the automotive industry", Lancaster EPrints abstract). Can: a slow SKU with many zero days has a published classification and forecasting family. Cannot: the rules do not tell zeros from no demand apart from zeros from a stock-out.
- **FBA and seller inventory behaviour** [research] Searches on 2026-11-10 (Crossref, arXiv and web; OpenAlex and Semantic Scholar searches were refused, SSRN 403) found **no study of capacity limits, storage limits, the low-inventory-level fee, the inbound placement fee or storage fees and sellers' stocking behaviour**. The nearest: Sun, Lyu, Yu and Teo 2020 (Naval Research Logistics, doi 10.1002/nav.21897), FBA versus seller fulfilment for one Chinese wedding-gown seller, a decision rule improving "total rewards by more than 35%"; Etumnu and Foster 2026 (SSRN 6749860), FBA "significantly boosts a seller's reputation"; Caldentey and Xie 2026 (arXiv 2604.07312), a theory model in which "by changing the predictability of each seller's sales stream, the platform changes sellers' safety-stock needs"; Hu, Zhou and Jasin, "Inventory Recommendations in Platform-Operated Fulfillment Service: Trust and Information Asymmetry" (SSRN 6025254), title only, abstract unreachable; Lai, Liu, Xiao and Zhao 2022 and Iyengar et al. 2023, theory of FBA's competitive and welfare effects.
- **Stock-outs and rank on Amazon** [research] Etumnu, Chenarides and Jaenicke, "Grocery Stockouts and Seller Performance in Amazon's Marketplaces", Agribusiness 42(4), 2026 (abstract via pure.psu.edu): over 290,000 grocery products, "when products are unavailable for a 90-day period, average sales rankings across all seller types are 14%–67% higher, indicating lower sales performance", which the authors call correlations, stronger for Amazon's own products. It is not an event study of recovery and does not separate FBA. No published study of rank or sales recovery after a seller's FBA stock-out was found; that claim still rests on practitioners.

## Stable enough for a skill

- The formula family and its named settings (P1), as a vocabulary of choices.
- That stock position has no single definition and each reading names what it counts (P2).
- That Amazon publishes two recommendation reports whose figures can differ, and does not publish their method (A, P5).
- That 14 on Amazon's pages is an FBM feature's eligibility criterion and a low-inventory-level fee band, 21 a fee band and the stock-out skill's own early-warning line, and 7 the skill's unattributed critical line (B, C).

Not stable: any price, any vendor's MCP tool list, the private-beta metric names, every fee figure.

## What cx must read at run time

- **R1.** Amazon's own recommendation and days of supply: the Restock report (roles Pricing, Amazon Fulfillment) and the planning report (role Amazon Fulfillment), per `method/sp-api-stock-surface.md`. Both roles are among the five.
- **R2.** If the seller keeps a planning tool, its export or MCP can add what Amazon does not hold: supplier lead times by stage, purchase orders, 3PL and local-warehouse stock, the seller's own cover and safety settings, and its record of stocked-out days. The reading is the tool's, under the tool's settings.
- **R3.** Capacity limits and IPI, where the seller's tool scraped or the seller typed them (P3); see `method/seller-central-only.md`.

## Reads that need a role outside the five

None found in this area. The private-beta metrics in section C come through Amazon's connector, not through a role the door could hold.

## Only in Seller Central

Seller Assistant and its workflows; the FBM Restock recommendation page; Capacity Monitor figures the tools copy by hand; the two help pages this seat could not open. Detail is `method/seller-central-only.md`'s.

## The seller's choices

Which sales windows and weights; whether stocked-out days leave the average; which stages make up lead time; cover and safety days; what counts as stock; whether to follow Amazon's recommended quantity, a tool's, or their own; what to do with price when cover runs short; early bulk or small frequent shipments. Sections P1, P6 and P7 show that named, competent sources choose differently on each.

## Open questions

1. (closed 2026-11-10) RestockPro, InventoryLab and sellerboard were re-read (P1). Their default velocity weights and default lead or buffer days are not published.
2. Helium 10 and Jungle Scout help articles answer 403; their alert defaults rest on snippets.
3. (closed 2026-11-10) The toolkit head is `8d90d3b` (2026-10-12); the stock skills' bodies match the zip (section C).
4. (partly closed) The low-inventory-level fee help page (GV43F6S76Y9DHYRH) carries 0–14 / 14–21 / 21–28 day fee bands, read by the listing playbook on 2026-10-14 and not first-hand here. The page's rate table and its current version are unread, as are the help pages GAFFEKSK9UR4MGTF and GKH7ASMAL93YECBF. No Amazon page read states "< 14 days → at risk" as an FBA rule.
5. (partly closed) Riverbend, Seller Sessions (show notes only), Reddit (via a snapshot service), AMZ123, 雨果网 and 卖家之家 are now covered (P9). Still open: 跨境眼 (no response), 老魏/赢商荟 and Moss (no bylined article found), Vanessa Hung (no posts), the Seller Sessions audio, Reddit itself (403), and replies on 知无不言 (login).
6. (closed 2026-11-10) 通途 is in P1; 酷鸟 has no replenishment feature. Sellfox page URLs are still known only as help-site paths.
7. Others' open MCP servers and the npm `pi-package` search are the survey's (2026-11-09), not repeated; Amazon's sample MCP READMEs were downloaded and not read in detail.
8. (partly closed) The M5 accuracy findings are read from the authors' preprint. The M5 uncertainty paper's findings, the FTC and ILSR pages, and the abstract of Hu, Zhou and Jasin (SSRN 6025254, on platform inventory recommendations) stay unread.
9. (closed 2026-11-10) The 15% is Amazon's own (News_Amazon 2023-12-19). No source was found for ECCANG's figures, which are removed.
10. (new) Riverbend says capacity limits are calculated in the third week of the month; Amazon's help page, as the listing playbook read it, announces them in the fourth week.

## Positions

**P-sellers-tools-and-research-1.** Amazon publishes two recommended restock quantities and dates, in the Restock report (role Pricing or Amazon Fulfillment) and the inventory planning report (role Amazon Fulfillment), and does not publish how either is computed; sellers report the two disagree. [official] *Report type values: FBA*; [opinion] Seller Central Europe forum thread, 2024-06-20. Section A, P5.

**P-sellers-tools-and-research-2.** (corrected 2026-11-10) "14 days" appears on Amazon's pages in two roles, neither of them a stock-out risk rule: as an eligibility criterion of the US FBM Restock recommendation feature ("current days of supply less than 14 days", 2025-03-14), and as a low-inventory-level fee band (0–14, 14–21, 21–28 days of historical supply). Amazon's open stock-out skill calls "days of supply < 14 → at risk" Amazon's rule without citing a page, says its 14–21 early-warning band is its own addition, and does not attribute its 7-day line. [official] News_Amazon, "Get personalized restock recommendations for your inventory"; [official, listing playbook 2026-10-14, not re-read] Low-inventory-level fee help page GV43F6S76Y9DHYRH; `stockout-prevention/SKILL.md` at `8d90d3b`. Sections B, C.

**P-sellers-tools-and-research-3.** Amazon's open stock-out skill measures cover as fulfillable units over 30-day sales divided by 30, counts no inbound or reserved units, and its connector exposes no reports tool, so it reads neither of Amazon's recommendation reports. [official] `stockout-prevention/SKILL.md`; `references/reports-vs-ordermetrics.md`. Section C.

**P-sellers-tools-and-research-4.** Days of supply, forecasts and restock date and quantity exist as private-beta metrics behind Amazon's connector and as report columns; no public JSON model carries days of supply. [official] `references/metrics-catalog.md`; *Report type values: FBA*. Sections A, C.

**P-sellers-tools-and-research-5.** Paid tools compute a restock figure from the same family (daily sales × lead time plus cover and safety days, minus stock position) and the seventeen tabulated here do not share one set of defaults for window, weights, stock-out handling, safety days or alert. [opinion] each vendor's help page as cited in the table. Section P1.

**P-sellers-tools-and-research-6.** A stated stock figure names what it counts: tools and Amazon's own pages differ on whether inbound, reserved, AWD, overseas-warehouse and 3PL units are in it. [official] *Report type values: FBA* (two days-of-supply columns); [opinion] Sellfox, SoStocked, Inventory Hero. Section P2.

**P-sellers-tools-and-research-7.** Capacity limits reach third-party tools by scraping Seller Central or by hand entry, as the vendors themselves say. [opinion] Gerpgo help (FBA库容); SoStocked article 226; Sellfox plug-in help. Section P3.

**P-sellers-tools-and-research-8.** Named practitioners' days-of-cover targets run from 15 days of turnover to two months at FBA plus two more in the pipeline, and they disagree on raising price before a stock-out, on closing a listing, and on sending peak stock early. [opinion] sources in the P6 table and P7. Sections P6, P7.

**P-sellers-tools-and-research-9.** A sales average taken over days with no stock understates demand; several tools remove those days and several do not, and the published literature treats this as a known bias with more than one correction. [research] Wecker 1978; Jain, Rudi and Wang 2014 (records); [opinion] Inventory Planner, Gerpgo, Sellfox help. Sections P1, Published research.

**P-sellers-tools-and-research-10.** Published measurements of stock-out cost come from a catalogue retailer, an online grocer and stores; the studies on Amazon measure Lightning Deal availability signals, Buy Box preference for FBA, and (in grocery) a correlation of 90-day unavailability with 14%–67% higher sales rankings; none measures rank recovery after an FBA stock-out. [research] Anderson, Fitzsimons and Simester 2006; Jing and Lewis 2011; Cui, Zhang and Bassamboo 2018; Raval 2023; Etumnu, Chenarides and Jaenicke 2026. Section Published research.

**P-sellers-tools-and-research-11.** A seller's planning tool holds facts Amazon does not: staged supplier lead times, purchase orders, non-Amazon stock and the seller's own settings; several vendors now expose these through an MCP server. [opinion] Lingxing MCP help; Flieber; Sellfox MCP help. Sections P4, R2.

**P-sellers-tools-and-research-12.** (added 2026-11-10) Amazon's one published sales effect of stock level is its own: "Sellers who maintain units above the Minimum Inventory Level see a 15% increase in sales over a four-week period on average, though actual results may vary" (US, 2023-12-19), with no method, sample or period stated. [official] News_Amazon, "Plan FBA inventory levels using a new metric". Sections E, P5.

**P-sellers-tools-and-research-13.** (added 2026-11-10) No published study was found, by searches of 2026-11-10, of Amazon's capacity or storage limits, low-inventory-level fee, inbound placement fee or storage fees and sellers' stocking behaviour; the academic work on FBA studies adoption, reputation and competition, and the one study linking Amazon unavailability with sales rank (grocery, 2026) reports correlations. [research] Sun et al. 2020; Etumnu and Foster 2026; Caldentey and Xie 2026; Etumnu, Chenarides and Jaenicke 2026. Section Published research.

**P-sellers-tools-and-research-14.** (added 2026-11-10) Named practitioners split on whether to send small and often or to front-load before peak, and on air versus sea: Riverbend, Chelsea Cohen, 强哥 and 法思特 teach small frequent batches; James McConnell Jr. suggests sending seasonal goods 120 days ahead; 强哥 calls sea freight's advantage "伪命题" while 九方通逊 teaches "海运为主…空运兜底". [opinion] sources in P9. Section P9.

The seat's own (no source; enters no skill):

- [seat] A cx pack adds past Amazon's skill: both reports, inbound and reserved in the position, the seller's own windows and cover, and price left as the seller's choice.
- [seat] The spread in P1 and P6 is the argument for stating settings as choices and carrying no band.
- [seat] No study of Amazon's storage or low-inventory fees and seller behaviour was found; absence here is a search result, not proof.

## Pages read

| Page | URL | Date read | Tag | Reached how / unreachable |
|---|---|---|---|---|
| Report type values: FBA | developer-docs.amazon.com/sp-api/docs/report-type-values-fba | 2026-11-09 | official | GET |
| SP-API docs index | developer-docs.amazon.com `llms.txt` | 2026-11-09 | official | GET |
| Guessed MCP / AI-tools doc pages | developer-docs.amazon.com/sp-api/docs/sp-api-mcp, /sp-api-ai-tools | 2026-11-09 | official | empty shells; no such pages |
| Amazon plugin zip (skills, references, commands, evals) | local `scratch/sp-api-plugins/amazon-plugin-zip/` | 2026-11-09/10 | official | local file |
| amzn/selling-partner-agentic-toolkit | github.com/amzn/selling-partner-agentic-toolkit | 2026-11-09; re-read 2026-11-10 at head `8d90d3b7c1537254b53c82651ac31fdbf0089368` (2026-10-12) | official | GitHub API commit list and tree; raw files at that sha |
| amzn/selling-partner-api-samples MCP READMEs | github.com/amzn/selling-partner-api-samples | 2026-11-09 | official | downloaded; not read in detail |
| Get personalized restock recommendations for your inventory | sellercentral.amazon.com/seller-forums/discussions/t/33b8ff50-5efb-456d-a2d3-12bcf9b86231 | 2026-11-09 | official | GET |
| Holiday 2026: Same fees, same eligibility, earlier deadlines | …/t/3e31fbb7-04e0-4ed4-873e-f74b1052e2ff | 2026-11-09 | official | GET |
| Update: Credit for FBA low-inventory-level fees incurred during April 2024 | …/t/e4922716-241e-48db-ac74-411e71825614 | 2026-11-09 | official | GET |
| Low Inventory Fees - Removal | …/t/74084420-14ee-4554-89bd-b57b6aebab7a | 2026-11-09 | opinion | GET |
| Which data to use for RESTOCK DATE & RECOMMENDED QTY? | Seller Central Europe forum, …/t/c43f712e-ce45-4b01-9c5b-07301e2b6664 | 2026-11-09 | opinion | GET |
| Amazons Double Wammy Inbound Placement Fees | …/t/e8c94895-dbca-485e-b26b-442fa12187f9 | 2026-11-09 | opinion | GET |
| Seller Central help GAFFEKSK9UR4MGTF, GKH7ASMAL93YECBF | sellercentral.amazon.com/help/hub/reference/… | 2026-11-09 | official | unreachable: JavaScript shell |
| Seller Assistant, agentic AI | aboutamazon.com/news/innovation-at-amazon/seller-assistant-agentic-ai | 2026-11-09 | official | GET |
| Seller Assistant plugin | aboutamazon.com/news/innovation-at-amazon/seller-assistant-plugin-amazon-quick-claude | 2026-11-09 | official | GET |
| 2026 and 2027 US fee letters | sellingpartners.aboutamazon.com/update-to-u-s-referral-and-fulfillment-by-amazon-fees-for-2026, …-for-2027 | 2026-11-09 | official | GET |
| Veeqo pricing, forecasting | veeqo.com/pricing | 2026-11-09 | official | GET |
| SoStocked help articles 102, 106, 108, 165, 173, 174, 179, 225, 226, 227, 237, 240, 264, 306, 322, 324 | help.sostocked.com/article/<n> | 2026-11-09 | opinion | GET (reader notes `en-tools-a.md`) |
| SPS Commerce articles (restocking, reserved, 5 mistakes, capacity 2025, 2026 fees) | spscommerce.com/community/articles/… | 2026-11-09 | opinion | GET |
| SoStocked restock-limits post | sostocked.com/now-factor-restock-limits-into-forecasts | 2026-11-09 | snippet | 404 |
| Inventory Planner help 589017, 2242706, 638170, 1959514, 3496048, 2303075, 1959506, 11331033, 10185459, 13843704, 674662 | help.inventory-planner.com | 2026-11-09 | opinion | GET |
| Helium 10 podcast #176; tool page; blog 2021-04-23 | helium10.com/podcast/amazon-inventory-management-tool/, /tools/inventory-management/ | 2026-11-09 | opinion | GET |
| Helium 10 knowledge base | kb.helium10.com | 2026-11-09 | snippet | unreachable: 403 |
| Jungle Scout blog 2019-11-12; plans; inventory and IPI articles | junglescout.com | 2026-11-09 | opinion | GET |
| Jungle Scout support articles | support.junglescout.com | 2026-11-09 | snippet | unreachable: 403 |
| Cogsy; Prediko; Flieber; Extensiv; Linnworks; Inventory Hero | cogsy.com; prediko.io/amazon-inventory-forecasting; flieber.com; help.extensiv.com/om-purchase-orders/auto-pos-reorder-rules; linnworks.com/features/stock-forecasting/; inventoryhero.ai/blog/amazon-fba-restock-planning | 2026-11-09 | opinion | GET |
| RestockPro help: restocking-preferences, suggested-quantity-calculation, the-restock-suggestions-grid; inventory-forecasting | ecomengine.com/help/…, /restockpro/inventory-forecasting | 2026-11-10 | opinion | GET (verifier); /restockpro/pricing 404 |
| InventoryLab Restock Report articles; Seller 365 | thjrecvolts.useresponse.com/knowledge-base/article/restock-report-{calculations,overview,settings,stock-status-definitions}; threecolts.com/seller-365/inventorylab | 2026-11-10 | opinion | GET (verifier) |
| sellerboard Inventory planner; blog 2026-04-28, 2026-08-05; home pricing | help.sellerboard.com/?p=3397; blog.sellerboard.com; sellerboard.com | 2026-11-10 | opinion | GET (verifier) |
| 通途 help 150, 149, 1075, 88, 386743, 386605; price | help.tongtool.com (its own GET JSON calls); tongtool.com/price.html | 2026-11-10 | opinion | GET (verifier) |
| 酷鸟 Koniao | koniao.com, /function_introduction.html, /package_detail.html | 2026-11-10 | opinion | GET; faq.kuniao.com did not resolve |
| Low-inventory-level fee further explained (Bryce_Amazon, 2023-12-07) | sellercentral.amazon.com/seller-forums/discussions/t/aa9f98e5-fa91-4949-af8f-6cf918c86a77 | 2026-11-10 | official (post); opinion (replies) | GET |
| Plan FBA inventory levels using a new metric (News_Amazon, 2023-12-19) | sellercentral.amazon.com/seller-forums/discussions/t/1aa7614a-5542-4529-abe1-ddf452681630 | 2026-11-10 | official | GET |
| Role Mappings for SP-API Types | developer-docs.amazon.com/sp-api/docs/role-mappings-for-types.md | 2026-11-10 | official | GET |
| Riverbend: restock limits, IPI, capacity, logistics | riverbendconsulting.com/blog/amazon-restock-limits/, /amazon-ipi-score/, /amazon-fba-capacity/, /amazon-fba-logistics-strategy/ | 2026-11-10 | opinion | GET (the earlier downloads were bot-check pages) |
| Marketplace Prep, low inventory fee | marketplaceprep.com/low-inventory-fee | 2026-11-10 | opinion | GET |
| Seller Sessions episodes | sellersessions.libsyn.com/the-challenge-of-amazons-new-fee; /demystifying-restock-limits-on-amazon-how-they-work | 2026-11-10 | opinion | GET (show notes only) |
| Reddit r/FulfillmentByAmazon threads | reddit.sentinel-team.org snapshots of posts 1qt7g9l, 1thu9ni | 2026-11-10 | opinion | snapshot service; reddit.com 403 |
| AMZ123 articles and Q&A | amz123.com/t/bu8s3Gz7, /6nfV5YtQ, /9NCw12dy, /7RQzZsRe, /DqajEhrV, /7sfS0K3T; /ask/JkJd7b6t | 2026-11-10 | opinion | GET |
| 雨果网 cifnews 155729, 156041, 174986; 卖家之家 mjzj 41226, 34489; 凤凰网科技 8xaf0dAiGtw; 白鲸出海 47040 | cifnews.com; mjzj.com; tech.ifeng.com; baijing.cn | 2026-11-10 | opinion | GET |
| 跨境眼 | kjyan.com | 2026-11-10 | — | unreachable: no response |
| M5 accuracy preprint | statmodeling.stat.columbia.edu/wp-content/uploads/2021/10/M5_accuracy_competition.pdf | 2026-11-10 | research | GET (preprint; ScienceDirect 403) |
| MQTransformer; Wang, Kang and Petropoulos | arxiv.org 2009.14799; 2304.03092 | 2026-11-10 | research | GET (full text) |
| Amazon Science, history of Amazon's forecasting algorithm | amazon.science/latest-news/the-history-of-amazons-forecasting-algorithm | 2026-11-10 | official | GET |
| Course notes: MIT OCW 15.772J newsvendor; Bricker reorder point; Chopra et al. 2003 | ocw.mit.edu; user.engineering.uiowa.edu/~dbricker; kellogg.northwestern.edu | 2026-11-10 | research | GET |
| Records: TSB (Semantic Scholar), Syntetos et al. 2005 (Lancaster), FBA papers (Crossref), Etumnu et al. 2026 (pure.psu.edu) | api.semanticscholar.org; eprints.lancs.ac.uk/73095; api.crossref.org; pure.psu.edu | 2026-11-10 | research | GET (abstracts) |
| 领星 replenishment, MCP, FBA inventory help | lingxing.com/help/article/replenishmentAadvice, /mcp | 2026-11-09 | opinion | GET |
| 积加 智能补货, FBA库容, STA help | help.jijiaerp.com/docs/eeE2AHAR, /cOmfrT3w, /StSWq6rA | 2026-11-09 | opinion | GET |
| 赛狐 补货建议, MCP, 插件管理, 预警规则 | Sellfox help site, `/help/features/…` | 2026-11-09 | opinion | GET; full URLs in the reader's nav map only |
| 易仓 news 3811, 3833, 4950, 5016 | eccang.com/news/<n> | 2026-11-09 | opinion | GET |
| 船长BI help and MCP page; 优麦云 pages; 店小秘 article 2260; 马帮 news 2022-09-05 | captainbi.com; sellerspace.com; help.dianxiaomi.com/article/procurementManagement/2260; mabangerp.com | 2026-11-09 | opinion | GET |
| 通途; 酷鸟 | tongtool.com; kuniao | 2026-11-09 | opinion | no replenishment text; empty downloads |
| 知无不言 threads 14838, 31484, 52000, 53239, 53593, 62937, 64064, 64646, 64909, 73921, 81301, 85315, 85317, 85327, 85351, 85612, 87160, 87479, 88039, 88355, 92245, 92495, 93511, 94383, 95146, 95195, 99985, 101914, 103253, 107496, 115081, 115504, 116095, 116534, 116955, 117803, 117891, 121755 | wearesellers.com/question/<id> | 2026-11-10 | opinion; official, via poster | GET; opening posts only, replies behind login |
| My Amazon Guy: stockouts (two pages), honeymoon, avoiding fees, storage limit | myamazonguy.com | 2026-11-09 | opinion | GET |
| Billion Dollar Sellers episode 2024-10-21 | billiondollarsellers.podbean.com | 2026-11-09 | opinion | GET (title and summary) |
| Chelsea Cohen: OMG podcast 187; MerchantSpring webinar; Million Dollar Sellers; Firing the Man | omg; merchantspring.io/resources/webinars/on-demand/how-to-avoid-stockouts-in-q4-with-restock-limits; buzzsprout.com/773804 | 2026-11-09 | opinion | GET |
| eComCrew episodes 542, 564; capacity and storage guides | ecomcrew.com | 2026-11-09 | opinion | GET |
| Canopy Management: minimum level; IPI | canopymanagement.com | 2026-11-09 | opinion | GET |
| Marketplace Pulse: 50% cut; fees only go up; fulfillment elasticity | marketplacepulse.com/articles/… | 2026-11-09 | opinion | GET |
| ppc.land: 2027 fees; Holiday 2026 | ppc.land | 2026-11-09 | opinion | GET |
| Empire Flippers forecasting; Best at Amazon (Thrasio, Q4 storage); sellersasksellers thread 1314 | empireflippers.com; bestatamazon.kit.com; sellersasksellers.com/t/restock-fba-inventory-calculation/1314 | 2026-11-09 | opinion | GET |
| Riverbend, Seller Sessions, Vanessa Hung, Reddit pages | various | 2026-11-09 | opinion | downloaded, not read |
| OpenAlex records for 48 papers | api.openalex.org | 2026-11-09 | research | GET (metadata and abstracts) |
| RePEc pages: Courty and Ozel 2019; Crawford et al.; Chen and Tsai 2024 | ideas.repec.org | 2026-11-10 | research | GET (abstracts) |
| DeepAR; MQ-RNN; Deep Inventory Management | arxiv.org 1704.04110; 1711.11053; 2210.03137 | 2026-11-09 | research | GET (full text) |
| Raval; Lee and Musolff; Gutiérrez; Dendorfer and Seibel; King; Kostenko and Hyndman; Gruen et al. | authors' PDFs; source URLs not recorded by the reader | 2026-11-09 | research | local copy read |
| AGCM press release; CMA case page | agcm.it; gov.uk | 2026-11-09 | research | GET |
| FTC press release and complaint; ILSR report; M5 pages | ftc.gov; ilsr.org | 2026-11-09 | research | unreachable: refused automated request / Cloudflare block |
| Internet Archive | web.archive.org | 2026-11-09 | — | unreachable: 502 |

## Verification

Verifier pass, 2026-11-10. Sources were re-opened by plain GET or read from local files on that date. The help hub's content call was not used, and no Amazon API host was called. Three readers worked under the verifier (tool rows, practitioners, research); their notes are `scratch/stock-playbook/sellers-tools-and-research/verifier-{tools,practitioners,research}.md`. The verifier spot-checked their key quotes against their downloads.

**Checked.** All 11 original positions, plus about 60 other claims: section A's report names, columns and roles; B's forum post; every quoted line of C against the toolkit at head; D's two About Amazon pages and the Veeqo page; E's fee letters and forum posts; the SoStocked, Lingxing, Gerpgo, Helium 10, Cogsy, Forecastly and ECCANG cells; the My Amazon Guy quotes; and the research quotes (Anderson et al., Jing and Lewis, Cui et al., Park et al., Gruen et al.) against their records.

**Changes.**
- **P-2.** It said the only "14 days" on an Amazon page is the FBM eligibility criterion, and that the 7/21 bands are the skill's own by its own words. The Low-inventory-level fee help page has bands at 0–14, 14–21 and 21–28 days (listing playbook read, 2026-10-14). The skill says only that the 14–21 band is its addition; it calls 7–14 "the canonical at-risk range" and does not attribute the 7. The position is rewritten, and B, C and *Stable enough* are corrected to match.
- **P-1, section A.** It said the Restock report needs "roles Pricing, Amazon Fulfillment". The role page says "need at least one". It now reads Pricing **or** Amazon Fulfillment. The planning report's page heading ("FBA Manage Inventory Health Report") is added.
- **C.** The head commit was not recorded. It is now recorded (`8d90d3b`, 2026-10-12), and the skill bodies match the zip. The inbound skill's `CONFIRM` gate and 3-poll cap are re-read and moved from [survey] to [official]. Added: the README and the `/sp-stockout-check` command describe a different method (metric discovery, a reorder quantity) from the skill body.
- **P4, Helium 10.** It said none of the "40+" MCP tools is a restock tool. Only eight tools are named. None is a restock tool, but `get_account_profit` returns "inventory health, sales velocity". The line is reworded.
- **P4, Lingxing.** It said the MCP has "stock-lock writes". These are confirmed (`fba_plan_storage_allocate` / `_release`) and clarified as writes to the ERP's own stock, not to Amazon. `query_fba_valid_list` is named.
- **P5, ECCANG.** The 37% had no source. No Amazon or other source was found in Chinese or English. The figure is removed.
- **P5, Amazon Global Selling.** The 15% had no source. It is Amazon's own (News_Amazon 2023-12-19, Minimum Inventory Level, no method stated). It is re-sourced, and P-12 is added.
- **P3, sellerboard.** The quote "does not calculate these two values" is a paraphrase. It is replaced with the page's words.
- **P6, My Amazon Guy.** The row said "text since revised". The page (modified 2026-10-31) carries the quote. The date is corrected, and the Q4 "60 to 75 days" is added.
- **E.** The 2027 letter's date was taken from ppc.land. It now comes from the page itself (2026-11-05). The 2026 letter's date (2025-10-15) and the "0.8%" are added.
- **P-5.** "sixteen" is now "seventeen" after the gap fills.
- **P-10.** Etumnu, Chenarides and Jaenicke 2026 (a grocery correlation) is added.

**Confirmed unchanged.** SoStocked's stock-out rule ("ZERO inventory AND if your sales drop below 30% of your daily average sales", article 108, updated 2025-08-05), seven-period average, 10-day transfer default, 20-day AWD lead time and hand-copied capacity. Cogsy ("Cogsy has been discontinued and is no longer available"). Forecastly (closed 2021-09-15). Lingxing's 50/30/20 weights, two-day lag, "默认是0天" and "默认是3天". Gerpgo's 14-day safety default, scraped capacity and STA limits. Seller Assistant's 2025 and 2026 quotes. The FBM post (2025-03-14). Holiday 2026 dates. The LIL credit post (2024-04-01). That no developer-docs page covers MCP (`llms.txt` re-read). That no local model or schema carries days of supply.

**Not re-opened.** The Low-inventory-level fee help page itself, which is off limits (its bands rest on the listing playbook's read). The connector's tool list ([survey]; its host is off limits). Helium 10 and Jungle Scout knowledge-base articles (403). Prediko, Flieber, Extensiv, Linnworks and Inventory Hero pages. The Sellfox, 优麦云, 马帮, 船长BI and 店小秘 rows. The 知无不言 quotes (spot-checked in local copies only: 章鱼工作室, 跨境阿杜, 92245). Prices other than Helium 10, Veeqo and the gap-filled tools.

**Gaps filled.**
- P1 rows for RestockPro, InventoryLab, sellerboard and 通途, with 酷鸟 found to have no replenishment feature.
- P2 and P4 additions.
- P9, practitioners in English and Chinese with their disagreements.
- The research map (M5, Amazon's forecasting papers and Amazon Science's account, course notes, intermittent demand, the FBA literature search, the Amazon stock-out and rank study).
- Section E's MIL 15%.
- Positions 12–14.

**Gaps left.**
- 跨境眼, 老魏/赢商荟, Moss and Vanessa Hung: nothing reachable.
- No practitioner method response to the 2027 letter, in either language.
- The Seller Sessions audio.
- The M5 uncertainty findings.
- An open (s,S) note.
- The abstract of Hu, Zhou and Jasin.
- Default cells in the side-by-side table that the vendors do not publish. These are marked "not published", "not stated", "seller-set" or "none".
- Others' MCP servers and the pi-package search (still [survey]).
