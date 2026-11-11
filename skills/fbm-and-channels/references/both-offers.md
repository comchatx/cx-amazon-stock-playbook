# One ASIN with both offers, backups and channel buffers

## Amazon's text

- Amazon's developer documentation (updated 2026-10-28) states that one listing can carry both a seller-fulfilled and an FBA record through the SP-API (F18).
- Its words: "When FBA inventory is available, it is used first. MFN inventory is used after the FBA inventory is depleted", with a warning of limited or no Seller Central support (F18).
- Converting FBM to FBA by API is a patch that adds the `AMAZON_*` record and deletes `DEFAULT`, and it fails when required battery or dangerous-goods information is missing (F18).
- What a SKU carrying both records shows in Seller Central and to a shopper once FBA stock is gone, and what an FBA-to-FBM patch does to units in fulfilment centres, was read in Amazon's documents and not yet seen on a live store (F18).

## Practitioners and tools

- My Amazon Guy and SellerLogic describe an FBM backup as a second SKU on the same ASIN, while SellerActive flips one SKU by software (F19).
- My Amazon Guy's practice is a suffixed SKU with "a small live quantity, never zero", its real handling time, a price that covers shipping, and a share of the peak 30-day forecast held in it for Cyber Week (F19).
- Tools that run both offers warn that the two can reprice against each other (F19).
- SellerLogic's rule is a Buy Box strategy on both offers, at most two offers in one condition, and no combining of FBA with FBM Prime offers (F19).
- Inventory tools sell channel-level buffers on a shared stock figure: SkuVault Core (Linnworks) names Maximum Quantity, Push Constant Quantity and Low Quantity Cutoff buffers (F31).
- SellerActive names per-marketplace Min Threshold and Max Visible buffers and says a buffer on an FBA SKU acts on the outside channel, "but it will not impact the quantity on the Amazon site itself" (F31).

## Research

- In data from 2015-era Amazon read without a Prime account, FBA carried a relative importance of 0.02 in predicting the Buy Box winner, far below price at 0.36 and 0.33 (Chen, Mislove and Wilson, WWW 2016) (F32).
- In later data across several countries, an FBM offer from an otherwise perfect seller was penalised against Amazon Retail by the equivalent of a price increase several times the size of that for the same seller's FBA offer (Raval, "Steering in One Click", 2023-12-31) (F32).
- The studies' own figures: research/README.md (F32).
