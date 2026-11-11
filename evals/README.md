# evals

The test cases and trigger queries the seven skills are measured with, in the shapes Anthropic's `skill-creator` reads. Nothing here ships: `package.json`'s `files` names `skills`, `prompts` and `README.zh-CN.md` only.

| File | What it holds |
|---|---|
| `stock-position.json`, `stock-cost.json`, `stock-out.json`, `restock.json`, `stock-inbound.json`, `stuck-stock.json`, `fbm-and-channels.json` | `skill-creator`'s `evals.json` for each skill: two cases each, the seller's message, the expected result and the assertions a grader checks. Two cases are on the German store: `stock-position`'s `pan-eu-sum` and `stock-cost`'s `eu-storage-by-country`. |
| `triggers/<skill>.json` | 20 queries per skill, 10 that should load it and 10 near misses that should not, for `skill-creator`'s description loop. |
| `fixture.py` | Writes a synthetic seller's tree: `python3 -I evals/fixture.py <dir>` replaces `<dir>/tenant` and `<dir>/stub-replies` and leaves the rest of `<dir>` as it was; `--summary` after `<dir>` also prints, as JSON, the figures the cases are graded on. Its docstring holds the scenarios, each with its right answer and the research positions (`research/README.md`) it rests on. Today in it is 2026-11-10, a Tuesday; seller `A1FIXTURESELLER`, brand Kettlewick; the US store `ATVPDKIKX0DER` on origin `https://sellingpartnerapi-na.amazon.com` and the German store `A1PA6795UKMFR9` on `https://sellingpartnerapi-eu.amazon.com`, under Pan-European FBA with FR, IT, ES and NL; the seller's ASINs are `B0STOCK001`–`9`, the fulfilment centres `QQA1`, `QQB2` (US), `QQD1`, `QQP1`, `QQC1` (DE, PL, CZ). No real seller's data and no Amazon reply is in it: every figure is invented, in the shapes Amazon's models and report pages document. |
| `cx` | A stand-in for the box's `cx` for these runs, on bash 3.2 and 5 with `python3`. It never touches the network. `cx raw amazon-sp-api --origin O --method M --path P [--header K=V]... [--query k=v]... [--body FILE\|@FILE\|B] [--output F] [--json]` answers reads from `<dir>/stub-replies/` first, then from the tree's landed replies under `tenant/raw/amazon-sp-api/`. It answers the FBA Inventory summaries, the Reports API, Listings Items, Fulfillment Inbound v0 and 2024-03-20 reads, Product Fees, `getOrderMetrics` and the two Multi-Channel Fulfillment previews; a marketplace outside the origin's region is answered 400. It refuses every change, `out_of_scope` with exit 2: any `PUT`, `PATCH` or `DELETE`, and any `POST` that is not a report request, a fee estimate or a fulfilment preview (so no feed, no inbound confirmation, no MCF order). A call that needs a role outside the application's five (AWD's `/awd/2024-05-09/...`, Supply Sources, the Data Kiosk Economics dataset, the seller performance report, among others) is answered 403 `Unauthorized`, as Amazon answers it. `POST /reports/2021-06-30/reports` answers 202 with a `reportId`; `GET /reports/2021-06-30/reports/{reportId}` answers `DONE` with a `reportDocumentId` (or `CANCELLED` for a type the fixture holds no rows for, as Amazon cancels a report with no data); `GET /reports/2021-06-30/documents/{id}` answers a `url` that is a `file://` path under `stub-replies/report-files/`, tab-separated, with `compressionAlgorithm: GZIP` for the ledger pair and the planning report, cut from `stub-replies/report-sources/` to the ask's dates and options (the ledger summary aggregates by `aggregatedByTimePeriod` and returns no rows for a monthly or weekly range that is not a whole month or week). Each call is appended to `<dir>/cx-calls.log`. |

## The tree

`tenant/` is what the box holds after earlier sessions:

- `raw/amazon-sp-api/getInventorySummaries-ATVPDKIKX0DER-2026-10-15.json`: an earlier read, before the white kettle ran out and before the scale and frother shipments arrived.
- `raw/amazon-sp-api/reports/GET_FBA_STORAGE_FEE_CHARGES_DATA/ATVPDKIKX0DER_2026-09-01_2026-09-30/`: September's storage fee report, downloaded as `report.tsv`, with a `receipt.json` holding the ask, the report id and when it was read.
- `notes/`: the seller's `catalog.md` (SKUs, prices, landed costs, supplier lead times, the Pan-EU setup), `awd.md` (black kettles in AWD, a count the seller wrote down on 2026-10-01) and `channels.md` (the FBA and FBM teapot SKUs, the Shopify store on MCF, the automated settings never opened).

`stub-replies/` is what Amazon answers today: inventory summaries for the US and each Pan-EU marketplace, marketplace participations, four listings items, the inbound shipments (v0) and plans (2024-03-20) with their items and placement options, the fee-estimate table, daily ordered units, MCF fees, and the report sources.

## The scenarios

| Skill | Cases | Where the answer is |
|---|---|---|
| stock-position | total-with-awd; pan-eu-sum (DE) | `getInventorySummaries` with `details=true`; the AWD read answered 403; `notes/awd.md`; the Pan-EU summaries and `GET_AFN_INVENTORY_DATA_BY_COUNTRY` through the EU origin |
| stock-cost | storage-rate-2027; eu-storage-by-country (DE) | `GET_FBA_STORAGE_FEE_CHARGES_DATA` for October (US and DE) against September's in the tree |
| stock-out | censored-demand; zero-but-not-gone | the daily ledger summary and `getOrderMetrics` for the white kettle; the frother's inventory and the Restock report |
| restock | two-recommendations; low-inventory-fee | the Restock and planning reports; `notes/catalog.md`'s lead times; the pour-over's planning row and inbound shipment |
| stock-inbound | shortfall-not-closed; peak-placement | v0 `getShipments` and `getShipmentItemsByShipmentId`; the ledger detail's `Receipts`; the 2024-03-20 plan, shipments and placement options |
| stuck-stock | stranded-vs-unfulfillable; aged-ways-out | the stranded report and the caddy's listing issues; the mugs' inventory; the planning, long-term storage fee and removal order detail reports |
| fbm-and-channels | both-offers-quantity; mcf-pool | `getListingsItem` for both teapot SKUs; the pour-over's inventory and an MCF preview |

Every case carries one expectation that no fee rate or band is quoted from memory where the store's own value is readable, and that the answer does not choose a forecast or cover method for the seller.

Values the research gives no value set for, and so are this fixture's guesses: the Restock report's `Alert` and `Recommended action` values (`low_stock`, `out_of_stock`, `Restock`), the planning report's `alert`, `recommended-action` and `fba-inventory-level-health-status` values, the stranded report's `primary-action`, `status-*` and `stranded-reason` values, the removal report's `order-source` value, the long-term storage report's `surcharge-age-tier` wording, the ledger summary's `Date` format (`MM/DD/YYYY` by day and week, `MM/YYYY` by month), which report documents are gzipped, the `researchingQuantityBreakdown` entry names, the storage report's unit strings (`cubic feet`, `cubic meters`), the MCF fee names, the place of the planning report's US-only age columns (at the end), and the Polish and Czech rows billed in PLN and CZK as the research's C34 reads Amazon's rate card.

## A run

Each run gets its own copy of the tree, written fresh by `fixture.py` into its own `<run>/`, and is told the same way in every configuration: the seller's message; that `<run>/tenant` is the box's `/tenant`; to `export PATH=<dir of this cx>:$PATH TENANT_TREE=<run>/tenant` before any `cx` call, with `cx`'s flags; seller `A1FIXTURESELLER`, stores `ATVPDKIKX0DER` on `https://sellingpartnerapi-na.amazon.com` and `A1PA6795UKMFR9` on `https://sellingpartnerapi-eu.amazon.com`; today 2026-11-10, no internet; not to read `<run>/stub-replies/` or this directory; to save the reply as `outputs/answer.md` and the shell commands it ran as `outputs/commands.txt`. A with-skill run is also given the skill's directory and the amazon-sp-api skill with its `references/door.md`; a baseline run is given only the amazon-sp-api skill.

A grader reads `skill-creator`'s `agents/grader.md` and checks each assertion against `answer.md`, `commands.txt`, `<run>/cx-calls.log` and `diff -r` of the run's tree against a fresh one. The only differences a run can leave are replies `cx` landed under `tenant/raw/` and files the run wrote itself; nothing reaches Amazon, and an attempted change shows in `cx-calls.log` and as a refusal in `commands.txt`.

## Rerunning

With `skill-creator` installed in Claude Code, its `scripts/aggregate_benchmark.py` builds the benchmark, `eval-viewer/generate_review.py --static <file>` writes the viewer, and `scripts/run_loop.py --report none` runs the description loop. `run_eval.py` writes a temporary command file under the nearest `.claude/` above its working directory, so it is run from a scratch directory that has its own `.claude/`. `python3 -I evals/fixture.py <dir> --summary` reprints the graded figures after any change to the fixture; the tree it writes is the same on every run.

## What was measured

One run per case and configuration, in Claude Code (Opus 5.5), on 2026-11-10, each graded by a `skill-creator` grader against the case's expectations; a baseline run had only the `cx-sources` and `amazon-sp-api` skills, since nothing in this package's ground is reachable without the door.

| Skill | With the skills | Baseline |
|---|---|---|
| stock-position | 16 of 16 | 13 of 16 |
| stock-cost | 16 of 17 | 11 of 17 |
| stock-out | 14 of 16 | 11 of 16 |
| restock | 12 of 17 | 10 of 17 |
| stock-inbound | 15 of 16 | 12 of 16 |
| stuck-stock | 12 of 17 | 8 of 17 |
| fbm-and-channels | 12 of 15 | 11 of 15 |
| All fourteen cases | 97 of 114, 85.1% | 76 of 114, 66.7% |

Both configurations read Amazon's reports equally well; the gap is in what the store's data does not hold. Without the skills, runs quoted a removal fee, an auto-disposal period and fee thresholds from memory, wrote an FBM quantity with `replace` where `merge` keeps the other records, could not state the 2027 US change, and treated FC-transfer units as buyable. With the skills, `mcf-pool` asked for the customer's address and gave no fee preview, where the baseline previewed with a stand-in address (and misread it). In both configurations the low-inventory-fee and censored-demand answers chose a cover target or a forecast for the seller, which the expectations as first worded marked as a fail (they now pass an answer that recommends one when asked and names its basis; the cases were not rerun or regraded under the new wording); neither restock run said the Restock settings are not readable through the API; and `aged-ways-out` missed the surcharge's assessment timing, Amazon's liquidation terms and Amazon's two texts on stock past 270 days, the first of which is a value no skill line carries. The runs started before the stand-in took `--body FILE` met a 400 on that form and retried with `@FILE`. A single run per configuration leaves per-case figures noisy.

The trigger queries in `triggers/` were not run through `skill-creator`'s description loop; the descriptions stay as written, in the listing playbook's form.
