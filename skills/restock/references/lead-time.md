# Lead time and its stages

Ids in brackets are positions in ../../../research/README.md.

## Receiving at Amazon

- Amazon's stated receiving windows, posted 2024-08-08, are stages and not a total: scheduled delivery to Checked in, Checked in to Receiving, and received to available for immediate shipping (R15).
- The first two stages are stated separately for small parcel and for LTL/FTL shipments, and every stage is longer at peak (R15).
- Units count as available as soon as received, while they may still be in transfer to other centres (R15).
- The stated windows are read in Dominic_Amazon's *FBA Receiving Times* (2024-08-08) on the US seller forum, and no later post read restates them; the holiday posts give event arrival dates, not these windows (R15).
- The seller's own receiving times are read in the shipment status history and the Inventory Ledger's `Receipts` dates (R15).
- Shipments, their statuses, delivery windows and peak cut-offs: ../../stock-inbound/SKILL.md.

## AWD to FBA (US)

- Amazon gave AWD receiving and AWD-to-FBA transfer times in 2024 posts, and neither is a 2026 measurement (R13).
- They are read in Topher_Amazon's post of 2024-08-27 on the US seller forum, https://sellercentral.amazon.com/seller-forums/discussions/t/41814845-f32a-4453-9c26-65dfe9409a2c (R13).
- They are also read in Amazon China's 2024 AWD article, https://gs.amazon.cn/news/news-brand-240602, and its undated MCD page, https://gs.amazon.cn/logistics/mcd, whose transfer time differs from the moderator's (R13).
- An AWD-held unit's promised delivery date differs from that of a unit already in a fulfilment centre (R13).
- Sellers and 3PLs reported AWD transfers taking weeks at peak in 2024 (Supply Chain Dive, SellerLogic, 3PL Guys) (R13).
- No operation states AWD transit time (R13).
- A seller's own AWD history is in the AWD reads, which need the Amazon Warehousing and Distribution role that the five roles do not open (R13).
- On the five roles, it is in the dates FBA inbound shipments from AWD were created and received: `getShipments` (v0) and the ledger's `Receipts` (R13).

## Tools' receiving allowance

- Gerpgo (积加) defaults its receiving days (入库处理天数) to 3, as its practice (R22).
- SoStocked defaults warehouse-to-Amazon transfer to 10 days and AWD lead time to 20 days, as its practice (R22).

## Transit

- Practitioners' dated transit figures for China to the US West Coast run from Matson CLX's days on the water (AMZ123) to Flexport's 37.6 days from cargo-ready to port departure in the week to 2026-08-10 (R25).
- To the US East Coast, Flexport measured 66.1 days in the same series (R25).

## Factory closures

- Of the tool pages read, only Sellfox (赛狐, holiday no-ship and no-production periods) and SoStocked (supplier blackout dates) model factory closures (R23).
- Chinese New Year moves each year, and forwarders (STG, SEKO, DocShipper) put closures around it at two to six weeks (R23).

## Two quantities

- Chinese ERPs compute a purchase quantity, with factory lead time included and local stock netted (R20).
- They compute a separate ship-to-FBA quantity, with transit and safety days only and FBA-side stock netted (R20).

## When to send

- Riverbend, Chelsea Cohen, 强哥 and 法思特 teach small, frequent batches (R27).
- James McConnell Jr. suggests sending seasonal goods 120 days ahead (R27).
- 强哥 calls sea freight's advantage a false premise, while 九方通逊 teaches sea freight as the main mode with air as the backstop (R27).
- SupplyKick's practice is to ship three weeks ahead for LTL and two for parcel, plus a week before Q4 or Prime Day (R27).
