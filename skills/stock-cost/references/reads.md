# Where each charge is read, and what no read gives

- How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.
- The reads-and-roles map for the whole pack: ../stock-position/SKILL.md and its references.

## Rates

- The rate Amazon applied is carried on the row that applied it: `storage_rate`, `base_rate`, `utilization_surcharge_rate`, `rate-surcharge`, `charge_rate` (C41).
- No operation returns a rate card, and Amazon changes these rates on a yearly cycle that differs by region (C41).

## Reports and roles

- The storage, long-term storage, fee preview and removal reports need Pricing or Amazon Fulfillment; the planning and overage reports need Amazon Fulfillment (C39).
- The settlement report and `listTransactions` need Finance and Accounting (C39).
- `listFinancialEvents` needs Finance and Accounting, or Amazon Fulfillment in the NA and FE regions only; in the EU region the five open it through Finance and Accounting alone (C39).
- No SP-API report type exists for the charged inbound placement fee, the low-inventory-level fee, capacity limits or reservation fees (C36).

## Finances

- Account-level holding charges (storage, aged, placement, overage, reservation) never appear in an order-scoped financial read (C37).
- Amazon's seller Finances models, v0 `FeeType` and 2024-06-19 `breakdownType`, are free strings that name none of these charges, so the strings are learned from live data (C37).
- AMALYTIX names `FBAStorageFee` and `FBALongTermStorageFee`, the latter carrying the aged surcharge, and in its reading finds no fee type of its own for the utilization surcharge or the low-inventory fee in European data (C37).
- Under which names these charges arrive in `listTransactions` and the settlement report on a US account was read in Amazon's documents and not yet seen on a live store (C37).

## Estimates

- The Product Fees API (Pricing or Product Listing) estimates per-sale fees only, takes no storage input, and Amazon says its estimates "are not guaranteed" (C38).
- The fee preview report, `GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA`, can be requested once a day per seller, is refreshed at least every 72 hours, and holds no storage, age, placement, removal or capacity charge (C38).
- Whether `getMyFeesEstimates` and the fee preview report include the low-inventory surcharge was read in Amazon's documents and not yet seen on a live store (C38).

## Data Kiosk Economics

- Amazon's pages disagree on the role for the Economics dataset: the Data Kiosk guide (2026-10-20) lists Brand Analytics on every operation and says each field requires a role checked at query creation (C40).
- Amazon's changelog correction, created 2024-07-02, says "The Economics dataset requires the Selling Partner Insights role", a role the five do not open; the door's reference states the correction (C40).
- Which role the dataset needs in practice was read in Amazon's documents and not yet seen on a live store (C40).
- Its `economicsPreview` projects fees up to 120 days ahead by MSKU (monthly storage, aged surcharge, utilization surcharge, low-inventory-level fee, placement) and is the only API read that states the low-inventory and placement fees as amounts per SKU (C40).
- It has no removal, disposal or liquidation type (C40).

## Beyond Amazon's charges

- Amazon's storage-side charges are one part of carrying cost; capital, obsolescence and shrinkage appear in no Amazon report, and the rate for them is the seller's number (C43).
- Practitioners quote days-of-cover figures, My Amazon Guy and SellerHow among them; those figures are their practice (C42).
- Amazon's fee and surcharge boundaries are dated definitions for one charge in some stores, and none is a rule for how much a seller holds (C42).
