# The seller-fulfilled quantity: record, writes, reports, notifications

How a call is made and a report is asked for and landed: the amazon-sp-api skill's references/door.md.

## The record

- The `fulfillment_availability` attribute is the seller's last submission, and the `fulfillmentAvailability` data set is, in Amazon's words, "the live quantity available for purchase and source of truth for actual inventory levels" (F1).
- Product Listing reaches both copies (F1).
- Amazon decrements a seller-fulfilled SKU's available quantity when an order is placed, changes it again when an order is cancelled, and stops taking orders at zero (F2).
- Whether the live quantity falls while an order is `PENDING`, and how soon it rises on a cancellation, was read in Amazon's documents and not yet seen on a live store (F2).
- `fulfillment_availability` is an array of records keyed by `fulfillment_channel_code` (F3).
- `DEFAULT` is the seller-fulfilled channel, and `AMAZON_NA`, `AMAZON_EU`, `AMAZON_JP` and `AMAZON_IN` are FBA (F3).
- The channel codes valid for a seller and store are read from the product type schema (F3).
- Amazon's text: `quantity` "is supported for MFN fulfillment, but not for Fulfillment by Amazon (FBA) fulfillment" (F3).

## Writes

- A patch with `op: merge` on `/attributes/fulfillment_availability` changes `quantity` for the channel named as the selector and leaves `restock_date` and `lead_time_to_ship_max_days` as they were (F4).
- Only top-level attributes can be patched, so a `replace` submits the whole array (F4).
- `merge` has been available for this attribute since 2025-05-28, and only for it and `purchasable_offer` (F4).
- A quantity write can use the product type `PRODUCT` (F5).
- `patchListingsItem` and `JSON_LISTINGS_FEED` are both open to Product Listing (F5).
- `JSON_LISTINGS_FEED` takes up to 25,000 SKUs a feed and five feeds every five minutes, as Amazon's Listings pages state (F5).
- A submission status of `ACCEPTED` means the write was taken for processing; issues that arise afterwards are read from `getListingsItem` (F6).
- Amazon says `getListingsItem` reflects a change "within 1-5 minutes", while listing status and issues notifications normally lag 15–20 minutes (F6).
- Amazon orders a patch and a feed by submission time, applying the feed's submission time to every message in it, so an earlier-submitted feed does not overwrite a later patch (F7).
- The Feeds API no longer accepts the legacy flat-file and XML inventory feeds (`POST_FLAT_FILE_INVLOADER_DATA`, `POST_FLAT_FILE_PRICEANDQUANTITYONLY_UPDATE_DATA`, `POST_INVENTORY_AVAILABILITY_DATA` and the rest) (F8).
- Amazon's pages give two ends for them: the feed page and the release note of 2025-06-25 date the end to 2025-07-31, and the deprecation schedule dates the removal to 2025-12-03 (F8).
- The announcement says the change "does not impact any listings feeds submitted by sellers directly through Seller Central" (F8).
- In Seller Central, deleting a SKU and zeroing its quantity are separate operations: an offer whose quantity is not set to zero "will remain live on the All-Offers Display" (help page G200216110 v9, as the listing playbook's seat quoted it on 2026-10-14) (F11).
- Whether `deleteListingsItem` behaves the same is not stated in the pages read (F11).

## Reads and reports

- `searchListingsItems` returns at most 1,000 listings across all pages, 20 a page (F9).
- Amazon's listing reports are not near real time: the stated freshness is 3 hours, and a repeat request from the same account returns data 1 to 6 hours old depending on catalogue size (F10).
- `GET_MERCHANT_LISTINGS_ALL_DATA` holds active, inactive and suppressed listings with a `status` column (F10).
- `GET_MERCHANT_LISTINGS_DATA` holds purchasable and zero-quantity listings without a `status` column (F10).
- `GET_MERCHANT_LISTINGS_DATA_LITE` and `GET_MERCHANT_LISTINGS_DATA_LITER` hold only SKUs with quantity above zero (F10).
- These listing reports are open to Product Listing or Pricing (F10).
- What `quantity` holds on an Amazon-fulfilled row of `GET_MERCHANT_LISTINGS_ALL_DATA`, and what `pending-quantity` holds, is not stated in Amazon's documents as read and is not yet seen on a live store (F10).

## Notifications

- `LISTINGS_ITEM_MFN_QUANTITY_CHANGE` carries the SKU, the channel code and the new available quantity (F12).
- It is delivered through Amazon EventBridge and is open to Product Listing (F12).
