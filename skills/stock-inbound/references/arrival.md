# Arrival: statuses, closure, delivery windows and receiving

## Statuses

- A v2024-03-20 shipment's status is one of `UNCONFIRMED`, `WORKING`, `READY_TO_SHIP`, `SHIPPED`, `IN_TRANSIT`, `DELIVERED`, `CHECKED_IN`, `RECEIVING`, `CLOSED`, `CANCELLED`, `DELETED`, `ABANDONED` and `MIXED` (I7).
- Amazon's inbound FAQ spells the cancelled value `CANCELED`, and the model `CANCELLED` (I7).
- `DELIVERED` means delivered and not yet checked in, `CHECKED_IN` means moved from the yard to the dock door, and `RECEIVING` begins when the first shipment label is scanned (I7).
- A shipment's status and dates are read with `getShipments` (v0) or `listInboundPlans` and `getShipment` (2024-03-20) (I8).

## Closed

- Amazon defines `CLOSED` as either all units confirmed received, or the shipment having been open longer than a domestic or an international number of days (I8).
- Those numbers are stated for the US on sell.amazon.com *How to track FBA shipments* (modified 2025-10-03); no page read and no operation states another store's (I8).
- A discrepancy can be researched only after `CLOSED`, and not while final counts are pending or when the contents are fully received or already reconciled (I8).

## Automatic closure in the US

- Since 2024-02-01 a US shipment that has not arrived within a set number of days of creation, one for domestic and one for international, is closed automatically, and the shipments of a multi-destination plan must arrive within a set span of the first (I9).
- "Arrived" means in-transit, delivered, checked-in or receiving (I9).
- Amazon's post of 2026-10-30 lengthened these spans for US international plans created in a window it names, counting from first receipt, kept the defect on the Inbound Performance Dashboard, waived its fee and reimbursed fees already charged, as its post of 2024-10-24 did for an earlier window (I9).
- The rule and its changes are read in the store's News posts on `sellercentral.amazon.com/seller-forums` (US: 2024-01-11; the relaxation: 2026-10-30) (I9).
- An Amazon moderator's guidance of 2024-11-18 is that a shipment still in transit at automatic closure can be received if the carrier holds a valid, active delivery appointment in Carrier Central, and otherwise the goods go back and the shipment is recreated with new box labels (I10).
- A seller reported on 2026-01-27 pallets delivered after the international closure left unscanned (I10).
- Whether a shipment closed by timeout is still received when it arrives was read in Amazon's documents and not yet seen on a live store (I9, I10).

## Delivery windows

- A shipment sent with a non-partnered carrier needs a confirmed delivery window, editable until the window starts and ending no later than a domestic or international limit from creation; partnered carriers and AGL supply arrival information themselves (I11).
- The requirement began in the US on 2023-04-24 and in Canada on 2024-02-09, and was announced for the UK on 2024-02-15 (I11).
- Amazon's API guide gives one window length for domestic shipments and a longer one for international (I11).
- Amazon's post of 2025-08-14 says US non-partnered shipments, domestic and international alike, are scheduled with one window length from 2025-08-18 (I11).
- The window options offered for the seller's own shipment are read with `generateDeliveryWindowOptions` and `listDeliveryWindowOptions` (Fulfillment Inbound 2024-03-20) (I11).
- Whether the international window equals the domestic one, and what a missed window costs, was read in Amazon's documents and not yet seen on a live store (I11).
- Amazon says shipments arriving inside their delivery window get priority processing and those outside it may face appointment and receiving delays, by a Seller Central event readiness playbook as the office captured it on 2026-10-14 (I12).
- An Amazon moderator replied in 2026-02 that the seller stays responsible for the window even when a carrier updates it (I12).

## Receiving

- Amazon's stated receiving windows are stages, not a total: scheduled delivery to Checked in, Checked in to Receiving, and received to available for immediate shipping, each with a small-parcel and an LTL/FTL figure and each longer at peak (R15).
- Dominic_Amazon posted the stated windows as *FBA Receiving Times* on 2024-08-08 (R15).
- Units count as available as soon as received, while still possibly in transfer to other centres (R15).
- The stated figures are in that post on the US seller forum, and no later post read restates them; the seller's own are the shipment's status history and the ledger's `Receipts` dates (R15).
- Lead time and its stages as the seller's restock choices: ../../restock/SKILL.md.
