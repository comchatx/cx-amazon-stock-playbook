# Storage: the monthly fee, the utilization surcharge and the aged surcharge

- How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## Monthly storage

- Monthly storage is charged on the daily average volume a seller's units occupy in a calendar month, by size class and by season, on Amazon's own measurement of the packaged unit (C1).
- The month's fee is charged in the following month (C1).
- `GET_FBA_STORAGE_FEE_CHARGES_DATA` gives the fee as an estimate per FNSKU per fulfilment centre, with the base rate and the utilization surcharge in separate columns; Pricing or Amazon Fulfillment opens it (C1, C39).
- The rate applied to the seller's units is in its `storage_rate`, `base_rate`, `country_code` and `month_of_charge` columns (C1, C41).
- The seasons and the published rates are on the US help page G3EDYEF6KUCFQTNM, which this research could not read (C1).
- In Europe they are on the rate card PDF linked from each `sell.amazon.<tld>/pricing` page, edition of 2026-11-02: https://m.media-amazon.com/images/G/02/sell/images/261014-FBA-Rate-Card-EN.pdf (C1).
- Elsewhere they are on the store's pricing page: `sell.amazon.ca/pricing`, `sell.amazon.co.jp/pricing`, `sell.amazon.com.au/pricing`, `sell.amazon.co.uk/pricing`, https://vender.amazon.com.mx/precios, `sell.amazon.ae`, `sell.amazon.sa`, `sell.amazon.in` (C1).
- Stranded stock keeps paying storage (C2).
- US staff posts, not a policy page, say units under a submitted removal or liquidation order stop accruing storage and the aged surcharge; this was read in Amazon's documents and not yet seen on a live store (C2).
- Sellers dispute that storage stops at order creation in every case (C2).

## Volume units

- Storage volume is in cubic feet in the US, UK, UAE and Saudi Arabia, cubic metres in the euro stores, Sweden, Canada and Australia, cubic decimetres in Mexico, and units of 1,000 cm³ in Japan (C33).
- The storage, long-term storage and overage reports carry a unit column beside every volume: `volume_units`, `volume-unit` or `volume_unit` (C33).

## Europe

- In Europe storage is billed at the rate and in the currency of the country where the unit physically sits; the rate per country applied is in the storage report's `country_code` and `storage_rate` (C34).
- The utilization surcharge is computed once for Germany, France, Italy and Spain together and once for the UK (C34).
- A European FBA unit pays the local fulfilment fee where the order's country is enabled for storage and the EFN fee elsewhere; local fees in Sweden and the Netherlands need placement in Germany, and in Belgium placement in Germany or France (C34).
- A seller with stock in Germany who does not allow storage in Poland and the Czech Republic pays a Central Europe Programme surcharge per unit shipped from German centres, its rate on the Europe rate card and its charge in Finances (C34).
- Programs and regions in full: ../stock-position/SKILL.md and its references.

## Storage utilization surcharge

- Amazon defines the storage utilization ratio as average daily volume stored over average daily volume shipped over a trailing window, in weeks, per seller per size class on the last day of the month; the window is on the Europe rate card (C3).
- The ratio is not a per-SKU number; Europe defines it in Amazon's words, and the US report carries the same ratio (C3).
- The storage fee report carries `storage_utilization_ratio`, `storage_utilization_ratio_units`, `utilization_surcharge_rate` and `est_sus` (C3).
- Whether `storage_utilization_ratio` is the account's ratio repeated on each row was read in Amazon's documents and not yet seen on a live store (C3).
- The surcharge began on 2023-04-01 in the US, 2023-05-01 in Europe, 2023-09-01 in Canada and 2024-06-01 in Japan (C4).
- The US and Canadian surcharge ends with the 2027 change, on the date in Amazon's 2027 letter and Global Selling notice; Europe and Japan had announced no end by 2026-11-10 (C4).
- Whether the surcharge still applies in a month is read in the storage report's `utilization_surcharge_rate` and `est_sus` (C4).
- The threshold ratio is not one number across stores or years: Europe's changed between its 2023 text and its 2026 card, and Japan's 2025 text states its own (C5).
- In Europe the surcharge does not apply to sellers whose first shipment is recent, to Individual accounts, or below a floor of daily volume, and clothing, eyewear, shoes and bags are outside the ratio (C5).
- In Japan its scope includes apparel, shoes and bags at every size (C5).
- The threshold and exemptions are on the Europe rate card, Japan's Seller Central News posts, and the US tier table GJ9NNG7RK4TU6E3Z, which this research could not read (C5).

## Aged inventory surcharge

- The US aged inventory surcharge is assessed once a month on a snapshot date and charged some days later, on top of monthly storage (C6).
- A removal or disposal order submitted before the monthly cut-off takes those units out of that month's surcharge even if they have not left; the cut-off is in Amazon's staff post *AVOID Costly Fees: Aging Inventory Action Plan* on the US seller forum (C6).
- The charged amounts are in `GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA` (`snapshot-date`, `qty-charged`, `amount-charged`), and the next month's exposure in `GET_FBA_INVENTORY_PLANNING_DATA` (`quantity-to-be-charged-ais-*`, `estimated-ais-*`, `Inventory age snapshot date`) (C6).
- In the oldest US bands the surcharge is the greater of a per-cubic-foot and a per-unit charge, in younger bands it is per cubic foot only, and the youngest bands exclude clothing, shoes, bags, jewelry and watches (US, 2026) (C7).
- The band and rate applied are the long-term storage report's `surcharge-age-tier`, `rate-surcharge` and `amount-charged`, and the planning report's `estimated-ais-*` columns (C7).
- Amazon's US texts disagree on sellable stock in the oldest bands: the aged-surcharge schedule effective 2026-01-16 prices it, while a moderator replied in a thread of 2026-06-26 that such stock is removed; both stand with their dates (S12, C7).
- How the two coexist on a US account was read in Amazon's documents and not yet seen on a live store (C7, S12).
- Inventory age is counted first-in-first-out across the whole fulfilment network: a sale or removal is deducted from the oldest units, whatever unit is physically picked (US) (C8).
- The age at which the surcharge starts differs by store: the US, Canada and Mexico share one start, the UK and the euro stores a later one, Japan a later one still, and the UAE and Saudi Arabia state their own (C9).
- India states its own age, and in Japan and Australia Amazon's own pages disagree, one stepped and one single (G13).
- The start for the seller's store is in the long-term storage report's `surcharge-age-tier` and `country`, the planning report's age columns, the Europe rate card and the store's pricing page (C9, G13).
- The planning report's age columns are fixed bands: two overlapping coarse cuts for older stock, a finer cut for the youngest, and over a year either `inv-age-365-plus-days` or, in the US, DE, UK, FR, IT and ES stores only, two columns that split it (C10).
- Surcharge exposure sits in the matching `quantity-to-be-charged-ais-*` and `estimated-ais-*` columns, and Brazil gets the old long-term-storage columns; the columns present are those in the header of the store's file (C10).
- Amazon's Mexican pricing page, https://vender.amazon.com.mx/precios, states the prolonged-storage surcharge twice and differently: a table from one age, its rates marked updated on 2025-05-15, and a line from a later age with its own amount per dm³ (C44).
- As applied in Mexico, the long-term storage report's `surcharge-age-tier` and `rate-surcharge` give the band and rate (C44).
- Stock past an age Amazon removes on its own: ../stuck-stock/SKILL.md.
