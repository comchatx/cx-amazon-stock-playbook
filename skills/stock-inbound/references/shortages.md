# Shortages: discrepancies, claims and reimbursement

## Where a shortage shows

- `CLOSED` is not proof of full receipt, and a discrepancy can be researched only after `CLOSED`, not while final counts are pending or when the contents are fully received or already reconciled (I8).
- Received units per SKU per shipment are `QuantityReceived` beside `QuantityShipped` in the v0 item reads; otherwise receipts are in the Inventory Ledger (I3).
- The Inbound Performance report carries `expected-quantity` and `received-quantity` on its problem rows (I14).

## The claim line

- For US FBA, Amazon moderator Indy_Amazon's forum post *FBA Lost Your Inventory? Steps to File a Reimbursement Claim* (2026-08-13) gives the claim window's length for units missing from an inbound shipment, to be filed after the shipment is closed or finalized; it does not say what the window runs from (I21).
- That it runs from the verified delivery date is the sentence of the help page *FBA inventory reimbursement policy* (`GEYPWTSQRTXXXMVB`) as a seller quoted it on 2024-09-26; the page itself is one this research could not read, and Amazon's reply in that thread did not affirm the quote (I21).
- supplychain.amazon.com/support/reimbursements states a window for Multi-Channel Fulfillment, its own program, not for FBA (I21).
- A post of 2024-08-06 giving a different window was issued on the UAE forum (I21).
- Proactive reimbursement (US from 2024-11-01; UK from 2025-01-15) covers items lost in fulfilment centres; units missing from an inbound shipment go through reconciliation (I21).
- My Amazon Guy reports that a case opened during a receiving backlog returns a wait instruction (I26).

## Reimbursement

- Amazon reimburses stock lost or damaged before a customer order, shipment-to-Amazon claims included, at the item's sourcing (manufacturing) cost, excluding shipping, handling and duties (I22).
- It uses its own estimate unless the seller enters a cost on the Manage Your Manufacturing Cost page (I22).
- The US start was announced on 2024-12-18 for 2025-03-10 and moved to 2025-03-31 by a post of 2025-02-28; the UK forum announced 2025-03-10 (I22).
- Removal claims are filed manually within their own windows (I22).
- The outcome of a reimbursement is in `GET_FBA_REIMBURSEMENTS_DATA` (Amazon Fulfillment or Pricing), whose `case-id` names the case (I22).
- Amazon may refuse reimbursement where it determines units were not in the shipment, including when box or unit labels did not tie them to it, by a moderator's reply of 2025-12 (I23).
- The claim itself is outside this pack, which states the unit movements and the dated rule (I22).
