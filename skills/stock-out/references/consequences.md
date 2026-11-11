# What Amazon says a stock-out stops

## Featured Offer and ads

- Amazon states "Your offer can't become featured if you're out of stock", in *Becoming the Featured Offer* G201687550 as the office captured it on 2026-10-14 (O8).
- Amazon Ads states "If your product isn't the Featured Offer or is out of stock, your ad will not display", in its *Amazon Ads FAQ* and *New advertiser success guide* (O8).
- The two Amazon Ads pages read do not say whether Sponsored Brands and Sponsored Display stop in the same way (O10).
- Tools and practitioners (Optmyzr, Ad Badger, Profit Whales, 夕木运营笔记本) say Sponsored Products stop on their own and Sponsored Brands keep serving, and disagree on Sponsored Display (O10).
- Practitioners on 知无不言 report that a returned unit re-shelved during a stock-out reopens the offer and its Sponsored Products ads on one or two units (O30).
- How ads serve and report around a stock-out: the ads playbook's ads-review skill, references/serving.md.

## Search

- Amazon states that "ASINs without a buyable offer are unsearchable" and that a change "can take up to 72 hours to reflect in shopping results", on *My ASIN is unsearchable* GHGHDMU4X5K9QGCV as the listing seat read it on 2026-10-14 (O6).
- The condition is on the ASIN, so another seller's buyable offer keeps it searchable (O6).
- No Amazon page read states a ranking consequence of a stock-out beyond losing the Featured Offer, ad display and searchability while no offer is buyable, and none states a grace period (O20).

## In-Stock Head Start

- Amazon announced In-Stock Head Start on 2019-07-25 as a US pilot that makes "temporarily out-of-stock products available for customers to find and buy when your shipment is on its way and we are confident about its arrival date" (O7).
- Its terms are known through third parties (ChannelX, Feedvisor, 观海论商), a UK seller reported it working for some products on 2024-11-20, and no Amazon text of 2025–2026 on it was found (O7).
- Whether the program is still offered and in which stock field its units appear was read in Amazon's documents and not yet seen on a live store (O7).

## Subscribe & Save

- Amazon lists an in-stock rate above a threshold among Subscribe & Save eligibility criteria; the threshold is read on *What is Amazon Subscribe & Save?* on sell.amazon.com (US, 2025-08-25) (O13).
- A staff reply (Manny_Amazon, 2024-07-23) gives the window as the trailing 28 days (O13).
- A Subscribe & Save offer's state in the Replenishment API decides what a stock failure costs: `INELIGIBLE` cancels existing subscriptions, and `SUSPENDED` keeps them (O13).
- `REPLENISHMENT_ONLY_ORDERING` "blocks one-time purchases to preserve inventory for existing subscriptions" (O13).
- Delivery conditions can say deliveries are paused because the offer is not buyable or at low-inventory risk (O13).
- The seller's own offers' states are read through the Replenishment API's offer eligibility (O13).

## Deals and coupons

- Amazon states that setting an ASIN in a deal to Closed "will cancel any deal currently scheduled for that ASIN" and that "Canceled deals cannot be reactivated", in *Amazon deals* G202111490 as the office captured it on 2026-10-14 (O15).
- Amazon validates a coupon about six hours before it starts and while it is active, and disables it on a product without "enough inventory to accommodate the customer demand that your coupon might generate" (Danny_Amazon, 2024-08-09) (O15).
- Amazon publishes no quantity for that requirement, and a disabled coupon is recreated, not resumed (O15).
- The coupon's and deal's state is in Seller Central, and no API states the stock requirement (O15).

## Variations

- Amazon states that a child listing that "is inactive or has no inventory" typically does not show on the detail page, in *Variation relationship FAQ* G201951410 as the office captured it on 2026-10-14 (O16).
- No Amazon page read says what a child's stock-out does to its siblings' search placement (O16).
- Sellers' reports conflict: one (newbeeseller on 知无不言, 2022-11-15) lost organic placement for all four children the day after the best-selling child sold out, and others (日落大道; an unsigned AMZ123 page) say a minor child's stock-out leaves siblings unaffected (O16).
