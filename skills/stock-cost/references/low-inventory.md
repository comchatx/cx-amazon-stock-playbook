# The low-inventory-level fee

- The 2027 US and Canadian rule: references/2027.md.

## What it is

- The low-inventory-level fee is a per-unit surcharge on the fulfilment fee of units shipped; it is not charged on stock held, and a product that ships nothing pays none (C11).
- It exists in the US, Canada, Pan-EU and Japan (C11).
- It began in the US on 2024-04-01, with the first month credited as a transition (C11).
- Whether the fee applied to a SKU this week is in `GET_FBA_INVENTORY_PLANNING_DATA` (`Low-Inventory-Level fee applied in current week?`, `Exempted from Low-Inventory-Level fee?`), which Amazon Fulfillment opens (C11, C39).
- No report type carries the per-unit amount; the charge arrives in Finances (C11, C36).
- Data Kiosk's `economicsPreview` states the fee as an amount per SKU, and that dataset needs a role outside the five (C11, C40).

## The rule until the 2027 change (US)

- Until the 2027 change the US fee applies only when both the short-term and the long-term historical days of supply are below the store's threshold (C12).
- Historical days of supply is average daily units on hand over average daily shipped units, excludes inbound, and its single displayed figure is the greater of the two windows (C12).
- Amazon's 2023 definition computed it "at the parent-product level"; help page GV43F6S76Y9DHYRH, as the listing playbook's research quoted it on 2026-10-14, puts it at FNSKU from 2026-01-15 (C12).
- The columns are `Short term historical days of supply`, `Long term historical days of supply`, `historical-days-of-supply`, `Last updated date for Historical Days of Supply` and the two fee flags in the planning report (C12).
- The fee's inventory count includes sellable units, transfers and units in processing and excludes inbound units and units pending removal, disposal or liquidation (US, 2026, help page GV43F6S76Y9DHYRH as the listing playbook's research quoted it on 2026-10-14) (C13).
- Multi-Channel and Remote Fulfillment shipments count as demand, so a shipment on its way does not lift the measure (C13).

## Grain, scope and floor by date (US)

- From 2024-04-01 the fee was charged per parent product on standard-size units (C16).
- From 2026-01-15 it is per FNSKU, with Small and Large Bulky added and Grocery exempt; this is on Amazon's help and summary pages as the listing playbook's research read them on 2026-10-14, not in Amazon's 2026 News post or letter (C16).
- From the 2027 change all oversize tiers enter, by a third party's relay of Amazon's 2027 page (C16, C15).
- Since 2024-05-15 a US product selling below a weekly unit floor is outside the fee, and Canada's copy of the rule states a different floor (C16).
- The floor in force is on help page GV43F6S76Y9DHYRH, which this research could not read, and the store's News posts; whether a SKU is exempt is the planning report's `Exempted from Low-Inventory-Level fee?` (C16).

## By store

- The days-of-supply threshold differs by store: the US and Pan-EU share one, and Japan's is lower and met on either window (C17).
- The UK has no such fee in the 2026 Europe rate card, and the Pan-EU fee does not apply in the Netherlands, Poland, Sweden, Belgium or Ireland and exists only for Pan-EU inventory (C17).
- The help page sets the rate per unit by size tier, weight and a band of historical days of supply; the listing playbook's research paraphrased it on 2026-10-14 and did not quote the rate table (C17).
- The threshold for the seller's store is on the Europe rate card (Pan-EU), the Japanese News post of 2024-04-18 on `sellercentral.amazon.co.jp/seller-forums`, and the US help page GV43F6S76Y9DHYRH, which this research could not read (C17).
- No report column names the band charged; Finances carries the charge (C17).

## Exemptions

- The New Selection program (2026) exempts a first number of units of a new branded FBA ASIN, for a window, from storage, the low-inventory-level fee and the storage utilization surcharge (US, with a UK twin) (C18).
- Amazon's texts give two windows: the 2026 program post and a News post of 2026-10-28 give one, and help page GV43F6S76Y9DHYRH, as the listing playbook's research read it on 2026-10-14, gives a longer one; both are Amazon's (C18).
- The window and unit count are in that year's New Selection post on the store's seller forum, and which SKUs are exempt is the planning report's `Exempted from Low-Inventory-Level fee?` (C18).
- An AWD SKU is waived from the low-inventory-level fee and the storage utilization surcharge when the share of its FBA inbound over a trailing window that was auto-replenished from AWD meets Amazon's threshold, a ratio Amazon computes daily (US, 2026) (C19).
- A seller-set maximum brings the fee back when FBA stock falls under the required days of supply (C19).
- Auto-replenished AWD stock is outside FBA capacity limits; manual replenishment is inside them and rejected when over the limit (C19).
- The ratio and the waiver are on the AWD dashboard and help page GAYG62Q3MPE6STFS, which this research could not read, its waiver wording seen only in a search result; whether the fee was waived is the planning report's `Exempted from Low-Inventory-Level fee?` (C19).
