# Seller-fulfilled orders, capacity, vacation and stock in other locations

## Orders and capacity

- A pending order is one whose payment is still being verified; it is the initial status of a standard order, and Amazon's page (2025-01-31) says not to ship it until it becomes Unshipped (F13).
- Amazon describes order handling capacity as lengthening the delivery promise, not stopping sales: past the daily limit, further orders get one more day of handling time (F14).
- Amazon's two posts state its scope differently: the US post *Automatic minimum thresholds for order handling capacity* (updated 2025-02-07) says it applies to Standard and Free Economy shipping and not to Premium Shipping or Seller Fulfilled Prime, and the European News post *Use Order handling capacity to manage your delivery time* (read 2026-11-10) says it does not apply to Prime or Premium shipping orders (F14).
- In the US, since 2025-02-24, Amazon sets a minimum capacity from the seller's average daily orders over the last 30 days, recalculated weekly, and the seller can set a higher limit (F14).
- The seller's limit and the minimum Amazon set are read in Seller Central only; no API read gives them (F14).
- Amazon's seller-fulfilled shipping metrics (late shipment, pre-fulfilment cancel, valid tracking and on-time delivery rates) apply only to seller-fulfilled orders (F30).
- The reports carrying the seller's own figures for them need Selling Partner Insights, which the five roles do not open (F30).

## Vacation

- Setting a store's listing status to Inactive (vacation) removes seller-fulfilled listings from detail pages and search within about an hour, per marketplace, as Amazon's forum posts describe it (TaylorR_Amazon, US; *Account vacation settings and support for the holidays*, UK) (F15).
- During it FBA listings stay active, and pending orders, returns and messages still have to be handled (F15).
- Whether the API shows a vacation status other than as a quantity above zero on a listing that is not `BUYABLE` is not stated in Amazon's documents as read and is not yet seen on a live store (F15).

## Multi-Location Inventory

- Multi-Location Inventory is for seller-fulfilled stock in the US store only, not for FBA inventory (F16).
- Each location's quantity is a `fulfillment_availability` record whose channel code is the supply source's id, with product type `PRODUCT` (F16).
- The `DEFAULT` channel must then be 0, since a `DEFAULT` quantity above zero produces a second, non-location offer that "might display inaccurate inventory and shipping timelines" (F16).
- The integration guide lists Selling Partner Insights as a prerequisite, and the Supply Sources API that lists and manages locations needs that role, which the five roles do not open (F16).
- Amazon's pages disagree on who may use it, all read 2026-11-10: the program page and the integration guide list Seller Central file upload and Manage All Inventory as ways to provide location inventory and exclude only FBA inventory (F17).
- The Supply Sources API page says the feature is not available to sellers who manage inventory in Seller Central or who use FBA inventory (F17).

## External fulfilment

- Location-level stock for Seller Flex, Multi Seller Flex, Easy Ship and Self Ship is published through the External Fulfillment Inventory API (F29).
- That API needs the restricted Direct-to-Consumer Shipping role and allow-listing, which the five roles do not open (F29).
- Easy Ship exists in Mexico, India, Turkey, Australia, Singapore, Japan, the Netherlands and Poland (F29).
