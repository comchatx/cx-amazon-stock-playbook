# One fact, one home: what this pack owns, and what it points to

Written 2026-11-10 by the lead, from files read that day: `cx-listing-playbook` at `origin/main` `68df042d` (its `research/angles/inventory-and-fulfillment.md`, 26 positions, and the skill lines that cite them); `cx-amazon-sp-api` PR #5 head `dd0343dc` (`SKILL.md`, `references/door.md`, `prompts/low-stock.md`); the Amazon Seller bundle's Overview (`comchatx` `src/shared/bundles.ts`, line 43, signed 2026-11-09); the money playbook's research tree (`packages/money-playbook/research/`, unpublished, read 2026-11-10). Nothing in those packages is changed by this file (brief 307, item 5). Every row below is a proposal for the office; the move itself is a follow-up in each owning package.

## The rule this file applies

A fact has one home: the package whose job it is. A package that needs the fact for its own job states the one consequence it uses and points to the owner by package and position id. The test for "whose job": the question the fact answers. "Where is my stock, what does holding it cost, when must more land" is this pack's. "Why did this listing's sales move, and is it the content" is the listing playbook's. "What did I make, and where is my money" is the money playbook's. "How do I reach Amazon" is the door's.

## 1. The listing playbook's 26 stock positions

Read: `research/angles/inventory-and-fulfillment.md` §Positions; the skill lines that cite each (grep of `skills/` for `P-inventory-and-fulfillment`). "Cited by" names the skill reference that uses it today.

| Listing position | What it states (short) | Cited by | Home proposed | Why |
|---|---|---|---|---|
| 1 | Read the offer state (BUYABLE, DISCOVERABLE, issues, live quantity; FBA fulfillable) for the whole window before crediting content | listing-review (L2), featured-offer `reads.md` | **Split.** Listing keeps the discipline for its own verdict; the stock pack owns what each FBA quantity field means | The discipline is a listing judgement; the state definitions are stock facts (`areas/stock-states.md`) |
| 2 | Live quantity comes from `fulfillmentAvailability`, not the `fulfillment_availability` attribute | featured-offer `reads.md` | **Stock pack** (`areas/fbm-and-outside-fba.md`, which confirms it); listing points | A quantity-read fact, used by both |
| 3 | A drop coinciding with no buyable offer is an offer problem, not a content problem | funnel, L40 | **Listing** | Its own verdict rule; the stock pack has nothing to say about content |
| 4 | Only fulfillable FBA units are sellable; stranded, reserved, researching, unfulfillable, inbound named apart | featured-offer `reads.md` | **Stock pack** (`areas/stock-states.md`); listing points | Core state definitions. Note: the stock research qualifies it: Amazon's moderator says FC-transfer reserved units are buyable (one post), so the listing line needs the qualification when it points |
| 5 | Read why a SKU is inactive, its FBA units and stranded reason before proposing to delete or close it | record.md (L87) | **Stock pack** (`areas/stuck-stock.md`); listing keeps one line and points | Stranding is a stock outcome of a listing action |
| 6 | Stranded units carry a `stranded-reason` and an auto-removal date | causes.md, watch.md | **Stock pack** (`areas/stuck-stock.md`) | Stranded and its ways out are this pack's area |
| 7 | Stock-out precursors (restock alert, ship-by date, low historical days of supply, fee flag, minimum level, capacity block) are stock risk, not a listing problem | watch.md | **Split.** Stock pack owns every precursor's definition (`areas/restock-and-forecast.md`, `areas/running-out.md`, `areas/holding-costs.md`); listing keeps "stock risk is not a listing fault" | The precursors are stock facts; the classification is the listing's |
| 8 | Past daily stock comes from the Inventory Ledger summary, not today's snapshot | confounders.md | **Stock pack** (`areas/stock-states.md`); listing points | A fact about where stock history lives |
| 9 | effect-review returns "cannot tell" when the window holds a day without buyable stock or a promise change | confounders.md | **Listing** | Its verdict rule; it points to the stock pack for how a stock-out day is read |
| 10 | Delivery-message share in Search Catalog/Query Performance as a confounder | confounders.md | **Listing** | A search-report fact, not a stock fact |
| 11 | Keepa out-of-stock percentages are the competitor-side signal only | figures.md | **Listing** (competitor reading); the stock pack names it only as a pointer | Competitors' stock is market reading, not the seller's position |
| 12 | Date a stock event from a settled read (hourly notification delay; report freshness; `startDateTime` misses inbound) | confounders.md | **Stock pack** (`areas/stock-states.md`, `method/sp-api-stock-surface.md`) | Freshness of stock reads |
| 13 | No lasting search-rank penalty from a past stock-out is stated as fact | — (research only; L43) | **Stock pack** (`areas/running-out.md`, which re-researched it: no Amazon page and no study measures one; the few practitioners with data saw recovery in one to four weeks) | The stock-out's cost is this pack's question |
| 14 | The delivery promise is offer configuration; the change file records the offer state at write time | record.md | **Listing** (its change record); the fields' meanings point to the stock pack (`areas/fbm-and-outside-fba.md` for handling time and channel) | |
| 15 | Channel codes and shipping templates come from the seller-specific product-type schema | request.md | **Listing** | A listing-write fact |
| 16 | An FBA stock-out with an MFN record is a switch to the MFN promise, not an outage | featured-offer SKILL.md | **Stock pack** (`areas/fbm-and-outside-fba.md`, verified: Amazon describes the behaviour in one developer-docs sentence, with no product name); listing points | Dual-channel stock is this pack's |
| 17 | Seller Fulfilled Prime badge withheld on slow promises | confounders.md | **Listing** (as a confounder); not a stock fact | |
| 18 | One view of the detail page is not evidence of the promise or the Featured Offer | featured-offer SKILL.md | **Listing** | |
| 19 | When thin on stock, Amazon's stated consequences and the opposing pressures are the seller's trade-off | causes.md | **Stock pack** (`areas/holding-costs.md`, `areas/running-out.md`); listing keeps "not a listing fix" and points | The trade-off is this pack's centre |
| 20 | A fee change after remeasurement or a tier change is a fee event | reports.md | **Money playbook** for the fee as a charge (`areas/fulfilment-charges.md`); listing keeps "not a listing effect" | Fulfilment fees are a per-unit selling cost, not a holding cost |
| 21 | Do not edit package dimensions to lower a fee; remeasurement is Amazon's route | (L45) | **Money playbook** (fee); the stock pack names remeasurement as Seller Central only (`method/seller-central-only.md`) | |
| 22 | A price recommendation carries a Product Fees estimate | record.md | **Listing / money** (price is the listing's `featured-offer`, fees the money playbook's) | Not a stock fact; Product Fees takes no storage input (`method/seller-central-only.md`) |
| 23 | A price crossing a fulfilment-fee band is a fee change | record.md | **Money playbook** | |
| 24 | Fee rates, peak periods and surcharges read at run time; fees charged at ship date | — | **Split.** Storage, aged, low-inventory, overage, placement, removal and disposal rules: **stock pack** (`areas/holding-costs.md`). Fulfilment and referral fees, and how every charge posts: **money playbook** | See §3 |
| 25 | Only current FBA report types, never a removed one | reports.md | **Stock pack** (`method/sp-api-stock-surface.md`, which dates every removal) | |
| 26 | Peak inbound cut-off dates are the last dates for Prime-ready stock | watch.md | **Stock pack** (`areas/inbound.md`, `beyond/programs-and-regions.md`) | |

Count: the stock pack would own 13 outright (2, 4, 5, 6, 8, 12, 13, 16, 19, 25, 26, and the stock halves of 1 and 7); the listing keeps 8 (3, 9, 10, 11, 14, 15, 17, 18) plus its halves of 1 and 7; the money playbook takes 4 (20, 21, 23, and the fee half of 24); 22 stays between listing and money. The listing playbook's `research/README.md` lines L39–L45 and the skill reference lines named above would then cite the stock pack's position ids in place of their own for the moved facts.

**Corrections the stock research makes to the listing's lines** (to carry over when the listing points):
- P-4's "shoppers cannot buy reserved units" needs the FC-transfer qualification (`areas/stock-states.md`, one Amazon moderator post).
- The listing's Seat note on the 15% figure: the Minimum Inventory Level "15% sales lift" is on an Amazon page (News_Amazon announcement, December 2023), per `areas/running-out.md` (under verification on 2026-11-10).
- P-26's cut-off source: the 2026 peak relaxation for international plans is Amazon's own post of 2026-10-30 (`areas/inbound.md`, verified).

## 2. The door's `/low-stock` template, and the bundle's Overview

- **The door** (`prompts/low-stock.md`): "Which of my FBA listings will run out of stock within ${1:-14} days at the rate they sold over the last 30 days? … the units available and inbound, the units sold a day, and the day it runs out." It is a Try it example on the door: one question, with the window and the rate as the seller's arguments. It carries no fact; the model answers it from whatever it knows.
- **The bundle's Overview** (store section): "Finds the FBA listings that will run out of stock within two weeks at the last 30 days' rate, with the units available and inbound."
- **What this pack adds past both**, as facts the model reads when it answers that question or any other about stock:
  - which quantity fields can be bought now, which arrive and when, and which never return (`areas/stock-states.md`, `areas/inbound.md`); that `totalQuantity` includes inbound, that reserved is not one thing, that AWD units are invisible on the five roles;
  - that a 30-day rate taken over days without stock understates demand (censored demand), and the choices sellers and tools make about it (`areas/running-out.md`, `areas/restock-and-forecast.md`);
  - Amazon's own recommendation reports, their columns, what moves them, and the seller settings the API cannot see (`areas/restock-and-forecast.md`, `method/seller-central-only.md`);
  - what holding costs, by rule and date, so "how much to send" meets "what holding it costs" (`areas/holding-costs.md`);
  - everything the template does not ask: stranded, excess, aged and unsellable stock and the ways out; FBM quantity; programs and regions.
- **No change proposed** to either. The template stays the door's example (its 14 is the seller's argument, not a rule); the Overview's line is true on the door alone. The pack's own Try it templates are proposed in the report.

## 3. The money playbook beside this one

The money playbook's research (`areas/fulfilment-charges.md`, `areas/product-profit.md`) treats storage, aged, low-inventory, placement, overage, removal and disposal charges as **money lines**: how each posts, under what name, on which date, and how it is split across products. This pack treats the same charges as **the price of a stock decision**: what triggers each, which units count, when age resets, what a removal or a shipment changes.

| Fact | Home proposed | The other points for |
|---|---|---|
| The rule that triggers a holding charge (thresholds, ages, units counted, exemptions, assessment dates), its dated history, and its differences by store | **Stock pack** (`areas/holding-costs.md`) | money: the rule behind a line it posts |
| Rates and amounts | Neither: read at run time (both packs say where) | — |
| How a charge posts: Finances transaction and fee-type names, posting date against period, settlement grouping, account-level against SKU-level rows | **Money playbook** | stock: where a charge it predicts shows up afterwards |
| Data Kiosk `economics` fee types and `economicsPreview` as a forecast of holding charges | **Split.** Money owns the dataset; stock owns which holding fees a preview names and what each depends on | |
| The fulfilment, referral and other per-sale fees, size tiers and remeasurement | **Money playbook** | stock: none needed beyond a pointer |
| Reimbursements for lost, damaged and short-received units | **Neither pack's core.** The survey's `cx-reimbursement-claims`; until it exists, money owns the money line and stock owns the unit movements in the ledger | |

**Checked across the two packs (2026-11-10):** the money research states the US low-inventory-level fee moves to FNSKU level from 2026-01-15, applies to Small and Large Bulky and exempts Grocery; `areas/holding-costs.md` (verified that day) states the same in its calendar row for 2026-01-15, through the same third-party relay of Amazon's 2026 fee letter (`[official, via sellersasksellers]`). The two agree; neither has Amazon's own text first-hand.

## 4. What none of the packs owns today

- AWD as stock (role Amazon Warehousing and Distribution, US API only): this pack states it as a gap; nothing is built on it.
- Inbound shipment creation and steering: the survey's `cx-inbound-shipments`. This pack reads inbound and states the writes' consequences (`areas/inbound.md`); it builds no workflow.
- Account health effects of overselling FBM stock: the survey's `cx-account-health`; this pack points.
