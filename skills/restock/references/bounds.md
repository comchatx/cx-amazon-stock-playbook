# Restock settings and the bounds Amazon sets

Ids in brackets are positions in ../../../research/README.md.

## The seller's Restock settings

- A seller can key lead time, minimum order quantity, replenishment frequency and case pack quantity per SKU in Seller Central to personalise the recommendation, as News_Amazon UK (2024-05-13) and AU (2024-09-24) state (R5).
- The Restock report's documented columns carry the recommendation and the supplier fields, and none of the four settings (R5).
- No SP-API read returns the four settings; they are read in Seller Central only (R5).
- That a lead-time change in Seller Central moves the next report was read in Amazon's documents and not yet seen on a live store (R5).
- Amazon's "Replenishment frequency" setting is a review interval in the sense of periodic review, which the research in references/methods.md treats (R31).

## Bounds on different bases

- "Restock today" counts SKUs whose days of supply is less than the restock lead time (R9).
- Amazon gives a cover guideline in days of expected sales, and defines excess as days of supply above a figure on forecasted demand (R9).
- Both figures are on the help page *Inventory performance* G202174810, which this research could not read; its v9 was quoted by the listing playbook's seat on 2026-10-14 (R9).
- The low-inventory-level fee tests historical days of supply on shipped units against a threshold that differs by store (R9).
- The fee's rule, its 2027 US change and where its threshold is read: ../../stock-cost/SKILL.md.
- Historical days of supply looks back at shipped units and forward days of supply rests on a forecast, so one SKU can read short on one and long on the other (R9).
- Amazon's figures per SKU are read in `GET_FBA_INVENTORY_PLANNING_DATA` (`days-of-supply`, `estimated-excess-quantity`, `historical-days-of-supply`) and in the Restock report (`Total Days of Supply`, `Alert`) (R9).

## Event guidance

- Amazon's Prime Day readiness playbook gives a days-of-inventory figure for products without recommendations and a weeks-of-inventory span before a deal event (R11).
- The office captured that playbook's v4 (GM2ADTH3XH3A5N57) on 2026-10-14 (R11).
- These are Amazon's event guidance, and the figures are read in that year's event readiness playbook in Seller Central (Prime Day GM2ADTH3XH3A5N57, Q4 G4QH4XCRWUXRJBLY), help pages this research could not read (R11).
- They are also read in that year's News_Amazon holiday post on the store's seller forum (R11).
- The 2026 US holiday post is *Holiday 2026: Same fees, same eligibility, earlier deadlines*, https://sellercentral.amazon.com/seller-forums/discussions/t/3e31fbb7-04e0-4ed4-873e-f74b1052e2ff (R11).
- The 2026 UK post is *Peak season 2026*, https://sellercentral.amazon.co.uk/seller-forums/discussions/t/d8c34b0b-86ed-4aec-9b0a-8be6eabb8fb0 (R11).

## Capacity and shipment restrictions

- Amazon states that a seller's capacity "will allow you to carry enough inventory to avoid the low-inventory-level fee, provided you don't utilize your capacity to hold excess inventory" (R14).
- Separately Amazon "may temporarily restrict shipment creation for certain products", including "items with excess inventory levels" and for dangerous-goods reasons (R14).
- Amazon monitors "on a daily basis", lifts a restriction "once your products return to healthy inventory levels", and publishes no threshold (R14).
- The maximum inventory level is shown on the Restock Inventory page and in no API; the API shows only an eligibility reason or a plan error (R14).
- Sellers report the block on SKUs the dashboard marks low stock, in a thread of 2025-06-01 (R14).
- Capacity limits reach third-party tools by scraping Seller Central or by hand entry, as the vendors say (T4).
- Gerpgo (积加) states its capacity report is scraped from Seller Central four times a day through a seller sub-account holding the manage-capacity permission (help "FBA库容", modified 2025-03-20) (T4).
- SoStocked and Sellfox (赛狐) describe the same routes for capacity in their help (T4).
- Capacity limits, Capacity Manager and when a limit is announced: ../../stock-cost/SKILL.md.

## AWD auto-replenishment (US)

- AWD auto-replenishment is triggered when available inventory in fulfilment centres plus inventory in transit to them falls below an "Optimum level of supply" Amazon sets per seller-ASIN (R12).
- The model "runs 7 days a week", and the level is on the AWD dashboard and in no API model (R12).
- Replenishment has three settings per SKU: Amazon's recommended quantity, a seller minimum and maximum, or off (R12).
- Where several SKUs share an ASIN, Amazon uses the highest value set, and a change can take up to 24 hours (R12).
- Amazon's documents do not say whether AWD units count in the Restock report's days of supply or which FBA field shows AWD units Amazon calls in stock; this was read in Amazon's documents and not yet seen on a live store (R1, R12).
- Reading AWD inventory and replenishment needs the Amazon Warehousing and Distribution role, and the five roles do not open it (R13).
