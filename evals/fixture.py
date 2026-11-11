"""A synthetic seller's tree for the skill-creator runs of the stock playbook: no real seller, no Amazon call, no network.

    python3 -I evals/fixture.py <dir>            replaces <dir>/tenant and <dir>/stub-replies, leaves the rest of <dir>
    python3 -I evals/fixture.py <dir> --summary  the same, then prints the figures the cases are graded on, as JSON

Seller A1FIXTURESELLER, brand "Kettlewick" (kettles and tea and coffee tools). Today is 2026-11-10, a Tuesday. Two stores:
  US       ATVPDKIKX0DER  origin https://sellingpartnerapi-na.amazon.com  USD, stock in fulfilment centres QQA1 and QQB2
  Germany  A1PA6795UKMFR9 origin https://sellingpartnerapi-eu.amazon.com  EUR, Pan-European FBA (FR A13V1IB3VIYZZH,
           IT APJ6JRA9NG5V4, ES A1RKKUPIHCS9HS, NL A1805IZSGTT6HS); stock sits in QQD1 (DE), QQP1 (PL), QQC1 (CZ)
The seller's application holds the door's five roles; an AWD call (/awd/2024-05-09/...) is answered 403 Unauthorized.

<dir>/tenant is what the box holds after earlier sessions: an older getInventorySummaries (2026-10-15), September's storage
fee report and the seller's notes (catalog, AWD, warehouse, channels). <dir>/stub-replies is what Amazon answers "now", for
evals/cx, out of the run's sight: inventory summaries per store, listings items, inbound shipments (v0) and plans
(2024-03-20), fee estimates, order metrics, and report-sources/, the rows a requested report is cut from.

Every figure is invented. The shapes follow Amazon's models (fbaInventory, fulfillmentInbound v0 and 2024-03-20, reports
2021-06-30, listingsItems 2021-08-01, fulfillmentOutbound 2020-07-01 and 2026-07-04, sales, productFees) and the report column
lists the research printed (wt/research/method/sp-api-stock-surface.md, read 2026-11-10). Where the research gives no value
set (a report's Alert, stranded-reason, order-source; a ledger Date format), the value here is a guess, named in README.md.

Catalog, US (notes/catalog.md):
  KW-KETTLE-BLK   B0STOCK001  Gooseneck Kettle 1L Black   49.99  fulfillable 212, 300 inbound shipped, reserved 64
                                                                 (18 customer orders, 41 FC transfer, 5 FC processing),
                                                                 researching 6, unfulfillable 10; part of its stock in AWD
  KW-KETTLE-WHT   B0STOCK002  Gooseneck Kettle 1L White   49.99  ran out on 2026-10-17, restocked 2026-11-02
  KW-TEAPOT-GLS   B0STOCK003  Glass Teapot 1L (FBA)       29.99  and KW-TEAPOT-GLS-FBM, the same ASIN from the NJ warehouse
  KW-INFUSER-2PK  B0STOCK004  Tea Infuser 2-Pack          12.99  1,060 units, 480 over 180 days old
  KW-CADDY-TIN    B0STOCK005  Tea Caddy Tin Set of 3      19.99  86 units stranded (listing suppressed)
  KW-SCALE-DGT    B0STOCK006  Digital Coffee Scale        34.99  shipment FBA19KWSCL1: 600 shipped, 552 received, RECEIVING
  KW-POUROVER     B0STOCK007  Ceramic Pour-Over Dripper   22.99  18 fulfillable, 500 on the water; low-inventory fee applied
  KW-MUG-SET4     B0STOCK008  Double-Wall Mugs, Set of 4  27.99  19 unfulfillable (14 customer damaged)
  KW-FROTHER      B0STOCK009  Handheld Milk Frother       17.99  0 fulfillable today; 37 FC transfer, 120 receiving
Germany: KW-KETTLE-BLK-EU (B0STOCK001) 380 fulfillable in each Pan-EU marketplace's reply, of which 241 sit in DE, 88 in PL,
51 in CZ; KW-INFUSER-EU (B0STOCK004) 520.

SCENARIOS, two per skill. Each names its right answer and the research positions (wt/research/README.md) it rests on;
--summary prints the figures.

stock-position
  P1 total-with-awd (US). "API says totalQuantity 592 for the black kettle, Seller Central 212 available. How many do I have
     in all, AWD included?" totalQuantity counts the 300 inbound units (W2, W7); 212 fulfillable; reserved 64 is 18 customer
     orders, 41 FC transfer, 5 FC processing (W9), and whether FC-transfer units can be bought Amazon states two ways (W10);
     researching 6, all in the 1-10 day bucket (W14, W15); unfulfillable 10 = 7 customer damaged + 3 carrier damaged (W16).
     AWD cannot be read with the five roles: /awd/2024-05-09/inventory is answered 403 (W38); the AWD Inventory report is a
     Seller Central download (W39). No total including AWD is given as read.
  P2 pan-eu-sum (DE). "380 in DE, 380 FR, 380 IT, 380 ES: 1,520 kettles in Europe? How many sit in Germany?" The same sum
     comes back per Pan-EU marketplace (W18, developers' report, not in Amazon's guide), so 380, not 1,520; fulfillable is
     per marketplace, not physical (W6); GET_AFN_INVENTORY_DATA_BY_COUNTRY: DE 241, PL 88, CZ 51 for local fulfilment, no
     reserved or inbound (W19); where units sit is Amazon's call under Pan-EU (G1); stock in PL/CZ means VAT there (G3).

stock-cost
  C1 storage-rate-2027 (US). "October storage on the infusers looks high: am I paying the 2.40 everyone quotes, and what
     changes in 2027?" GET_FBA_STORAGE_FEE_CHARGES_DATA, month_of_charge 2026-10: base_rate 2.61, utilization_surcharge_rate
     0.69, storage_rate 3.30 per cubic foot, ratio 31.4 weeks (seller-level per size class, not per SKU); infuser 1,148 units
     average, 164.62 ft3, fee 543.25 (est_sus 113.59) (C1, C3, C41). The US surcharge ends 2027-01-31 (C4); from 2027-02-01
     the utilization surcharge goes and the aged surcharge folds into an age-based monthly rate (C21); 2027 rates are not
     readable (C22). September (the tree's report) read 0.84 + 0.44.
  C2 eu-storage-by-country (DE). "Why does my German storage report show three rates for the same kettle, what is my EU
     utilization surcharge, and does the 2027 change hit Germany?" Rows by fulfilment centre: DE 27.40 EUR, PL 104.50 PLN,
     CZ 612.00 CZK per cubic metre, billed where the unit sits (C34, C33); ratio 18.6 weeks computed once for DE/FR/IT/ES
     (C34), utilization_surcharge_rate 0 and est_sus 0 in October; the threshold is read from the Europe rate card, not
     carried (C5); the 2027 design is US and Canada only (C23); placement is Amazon's under Pan-EU (G1).

stock-out
  O1 censored-demand (US). "White kettle: 63 sold in 30 days = 2.1/day, plan on that?" The daily ledger shows a zero ending
     balance on 16 days, 2026-10-17..11-01, and 10-17 itself shipped 3 (O17: an end-of-day balance does not say when it ran
     out); in-stock 14 or 15 days, so 63/15 = 4.2 (63/14 = 4.5); a mean over stock-out days is a censored lower bound (O18);
     tools correct it in different ways (O19), a choice; lost sales are not in any SP-API read (O12).
  O2 zero-but-not-gone (US). "Frother shows 0 available; is there a 3-day grace period; should I open an FBM backup?"
     0 fulfillable with 37 FC transfer, 4 customer orders, 2 FC processing and 120 receiving (O1, W9); FC-transfer
     buyability stated two ways (W10); an out-of-stock offer cannot be featured and its ads stop (O8); no Amazon page states
     a grace period, the claim traces to 藏龙荟 2019 (O25, O20); FBM backup: practitioners disagree (O28).

restock
  R1 two-recommendations (US). "Restock report: 420 by 11-20; planning report: 260 by 11-14. Which is right?" Both are
     Amazon's, neither formula is published, sellers report they disagree (R3, R4); Total Days of Supply (62) counts the 300
     in transit (W7, R1); the Restock settings are Seller Central only (R5); a tool's shape is a set of choices (R18);
     shipped vs ordered units (R16); the Black Friday arrival dates (10-21 / 10-28) have passed (I24).
  R2 low-inventory-fee (US). "Pour-over got the low-inventory fee though 500 are on the water; what cover avoids it, and does
     that change in February?" Planning row: fee applied this week Y, exempt N, short-term 16 and long-term 23 days of
     historical supply, both under 28 (C12); inbound does not count (C13); from 2027-02-01 the two-sided test on shipments
     28 days before and after, charged about four weeks in arrears (C14); the per-unit amount has no report column (C11);
     28 is a fee boundary, not a holding rule; Amazon suggests four weeks (C42).

stock-inbound
  I1 shortfall-not-closed (US). "Amazon received 552 of 600 scales; file a claim?" FBA19KWSCL1 is RECEIVING, not CLOSED;
     a discrepancy is researched only after CLOSED, and CLOSED is not proof of receipt (I8); received units per SKU only from
     v0 getShipmentItems QuantityReceived and the ledger's Receipts (I3, W27): 300 (10-31), 180 (11-01), 72 (11-03); receiving
     is stages up to 18 days to available (R15); the US claim line is nine months after verified delivery (I21);
     FBA18KWMUG1 (200 shipped, 188 received) is CLOSED.
  I2 peak-placement (US). "400 more kettles for Black Friday: placement fee, and in time?" Plan wf…KWBLK2 ACTIVE, two
     placement options: Amazon-optimized (3 shipments) fee 0.00, minimal split (1 shipment) fee 112.00 USD (I15, C29);
     confirmPlacementOption cannot be reversed (I15); the 2026 BFCM arrival dates passed (I24); late arrivals are received
     but not guaranteed in time (I25). No write.

stuck-stock
  S1 stranded-vs-unfulfillable (US). "Caddies and mugs show unsellable; what is each, and what will Amazon do itself?" Caddy:
     86 stranded (listing suppressed, missing item_package_weight), date-stranded 2026-10-05, Date-to-take-auto-removal
     2026-12-04 (S1, S2, S3, S8); stranded stock keeps paying storage (C2). Mugs: 19 unfulfillable = 14 customer damaged,
     3 warehouse damaged, 2 defective (W16); customer damaged is not reimbursed (S13); with no return option set Amazon may
     dispose at its discretion (S14); the automated settings are not readable through the API (S15).
  S2 aged-ways-out (US). "1,060 infusers at 4 a day: remove, liquidate or discount before the fees?" Planning row: 420 in
     181-270 days, 60 in 271-365; estimated-ais next assessment 118.98 USD; excess 700; recommended removal 480; the aged
     surcharge is assessed on the 15th and an order by 11:59 PM Pacific on 2026-11-14 takes units out (C6); October's charge
     (LTSF report) 28.62; removal fee read from the removal detail report, 206.00 for 200 units in August (C31); liquidation
     5-10% gross less 15% and a per-item fee, not cancellable (S19); the 270-day texts disagree (S12, S11).

fbm-and-channels
  F1 both-offers-quantity (US). "I set the FBM teapot to 40 on Nov 3, the listing shows 25; set it to 60." The attribute
     holds the last submission (40), fulfillmentAvailability the live quantity (25) (F1), decremented by orders (F2); a write
     is a merge patch on /attributes/fulfillment_availability for DEFAULT (F4), ACCEPTED is not landed (F6); two SKUs on one
     ASIN are two offers (F19), one SKU with both records draws FBA first (F18). The stand-in refuses the write.
  F2 mcf-pool (US). "Seller Central shows 47 pour-overs; send a 30-unit MCF order for my Shopify customer." 18 fulfillable;
     26 FC transfer and 3 customer orders are in the 47 (F20); the preview says 12 cannot be filled (F22); fees are read from
     the preview (F27); createOrder is a write, refused; FILL_ALL_AVAILABLE ships what it can, the seller's choice (F24).
"""
import datetime as dt
import gzip
import json
import os
import shutil
import sys

if len(sys.argv) < 2:
    sys.exit("usage: python3 -I evals/fixture.py <dir> [--summary]")
root = os.path.abspath(sys.argv[1])
SUMMARY = "--summary" in sys.argv[2:]
T = os.path.join(root, "tenant")
S = os.path.join(root, "stub-replies")
for d in (T, S):
    if os.path.isdir(d):
        shutil.rmtree(d)

SELLER = "A1FIXTURESELLER"
US, DE, FR, IT, ES, NL = "ATVPDKIKX0DER", "A1PA6795UKMFR9", "A13V1IB3VIYZZH", "APJ6JRA9NG5V4", "A1RKKUPIHCS9HS", "A1805IZSGTT6HS"
NA_ORIGIN, EU_ORIGIN = "https://sellingpartnerapi-na.amazon.com", "https://sellingpartnerapi-eu.amazon.com"
TODAY = dt.date(2026, 11, 10)
D = dt.date.fromisoformat
FIRST, LAST = D("2026-08-01"), D("2026-11-09")
DAYS = [FIRST + dt.timedelta(n) for n in range((LAST - FIRST).days + 1)]


def put(base, rel, data, raw=False):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(data if raw else json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def r2(x):
    return round(x + 1e-9, 2)


# sku: (fnsku, asin, title, price, unit cost, (longest, median, shortest in), weight lb, fc)
CATALOG = {
    "KW-KETTLE-BLK": ("X00KWBLK01", "B0STOCK001", "Kettlewick Gooseneck Electric Kettle 1L, Matte Black", 49.99, 14.20, (12.6, 9.1, 7.9), 3.1, "QQA1"),
    "KW-KETTLE-WHT": ("X00KWWHT02", "B0STOCK002", "Kettlewick Gooseneck Electric Kettle 1L, Matte White", 49.99, 14.20, (12.6, 9.1, 7.9), 3.1, "QQA1"),
    "KW-TEAPOT-GLS": ("X00KWTPT03", "B0STOCK003", "Kettlewick Glass Teapot 1L with Removable Infuser", 29.99, 6.10, (9.4, 7.2, 6.3), 1.6, "QQB2"),
    "KW-INFUSER-2PK": ("X00KWINF04", "B0STOCK004", "Kettlewick Stainless Steel Tea Infuser, 2-Pack", 12.99, 1.85, (7.0, 6.0, 5.9), 0.4, "QQB2"),
    "KW-CADDY-TIN": ("X00KWCDY05", "B0STOCK005", "Kettlewick Airtight Tea Caddy Tins, Set of 3", 19.99, 4.40, (10.2, 4.1, 4.1), 1.2, "QQB2"),
    "KW-SCALE-DGT": ("X00KWSCL06", "B0STOCK006", "Kettlewick Digital Coffee Scale with Timer", 34.99, 7.90, (9.8, 7.4, 2.4), 1.3, "QQA1"),
    "KW-POUROVER": ("X00KWPOV07", "B0STOCK007", "Kettlewick Ceramic Pour-Over Coffee Dripper", 22.99, 4.05, (6.3, 6.3, 5.1), 1.1, "QQB2"),
    "KW-MUG-SET4": ("X00KWMUG08", "B0STOCK008", "Kettlewick Double-Wall Glass Mugs, Set of 4", 27.99, 7.10, (11.8, 8.3, 5.5), 2.6, "QQB2"),
    "KW-FROTHER": ("X00KWFRO09", "B0STOCK009", "Kettlewick Handheld Milk Frother", 17.99, 3.30, (10.0, 2.6, 2.2), 0.4, "QQA1"),
}
FBM_SKU = "KW-TEAPOT-GLS-FBM"
EU_SKUS = {
    "KW-KETTLE-BLK-EU": ("X00KWBLKE1", "B0STOCK001", "Kettlewick Schwanenhals-Wasserkocher 1 L, mattschwarz", 54.99),
    "KW-INFUSER-EU": ("X00KWINFE4", "B0STOCK004", "Kettlewick Teesieb Edelstahl, 2er-Pack", 13.99),
}

# getInventorySummaries today, US: fulfillable, (working, shipped, receiving), (customer orders, transshipment, fc processing),
# researching (1-10, 11-20, 21+), unfulfillable (customer, warehouse, distributor, carrier, defective, expired)
INV = {
    "KW-KETTLE-BLK": (212, (0, 300, 0), (18, 41, 5), (6, 0, 0), (7, 0, 0, 3, 0, 0)),
    "KW-KETTLE-WHT": (197, (0, 0, 0), (5, 0, 4), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
    "KW-TEAPOT-GLS": (64, (0, 0, 0), (2, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
    "KW-INFUSER-2PK": (1060, (0, 0, 0), (6, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
    "KW-CADDY-TIN": (86, (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
    "KW-SCALE-DGT": (618, (0, 0, 48), (9, 96, 12), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
    "KW-POUROVER": (18, (0, 500, 0), (3, 26, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
    "KW-MUG-SET4": (140, (0, 0, 0), (2, 0, 0), (0, 0, 0), (14, 3, 0, 0, 2, 0)),
    "KW-FROTHER": (0, (0, 0, 120), (4, 37, 2), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
}
INV_DE = {"KW-KETTLE-BLK-EU": (380, (0, 0, 0), (7, 22, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
          "KW-INFUSER-EU": (520, (0, 0, 0), (3, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0))}
BY_COUNTRY = {"KW-KETTLE-BLK-EU": (("DE", 241), ("PL", 88), ("CZ", 51)), "KW-INFUSER-EU": (("DE", 390), ("PL", 130))}


def total(row):
    f, inb, res, rsch, unf = row
    return f + sum(inb) + sum(res) + sum(rsch) + sum(unf)


def summary(sku, row, store, fnsku, asin, title, details, updated):
    f, (w, s, r), (pc, pt, fp), (r1, r2_, r3), u = row
    out = {"asin": asin, "fnSku": fnsku, "sellerSku": sku, "condition": "NewItem", "lastUpdatedTime": updated,
           "productName": title, "totalQuantity": total(row), "stores": [store]}
    if details:
        out["inventoryDetails"] = {
            "fulfillableQuantity": f, "inboundWorkingQuantity": w, "inboundShippedQuantity": s, "inboundReceivingQuantity": r,
            "reservedQuantity": {"totalReservedQuantity": pc + pt + fp, "pendingCustomerOrderQuantity": pc,
                                 "pendingTransshipmentQuantity": pt, "fcProcessingQuantity": fp},
            "researchingQuantity": {"totalResearchingQuantity": r1 + r2_ + r3, "researchingQuantityBreakdown": [
                {"name": "researchingQuantityInShortTerm", "quantity": r1}, {"name": "researchingQuantityInMidTerm", "quantity": r2_},
                {"name": "researchingQuantityInLongTerm", "quantity": r3}]},
            "unfulfillableQuantity": {"totalUnfulfillableQuantity": sum(u), "customerDamagedQuantity": u[0],
                                      "warehouseDamagedQuantity": u[1], "distributorDamagedQuantity": u[2],
                                      "carrierDamagedQuantity": u[3], "defectiveQuantity": u[4], "expiredQuantity": u[5]}}
    return out


def inv_reply(mkt, rows, cat, store, updated):
    return {"payload": {"granularity": {"granularityType": "Marketplace", "granularityId": mkt},
                        "inventorySummaries": [summary(k, v, store, cat[k][0], cat[k][1], cat[k][2], True, updated) for k, v in rows.items()]},
            "pagination": {}}


put(S, "getInventorySummaries-%s.json" % US, inv_reply(US, INV, CATALOG, "Amazon.com", "2026-11-10T07:41:12Z"))
for m in (DE, FR, IT, ES, NL):
    put(S, "getInventorySummaries-%s.json" % m, inv_reply(m, INV_DE, EU_SKUS, "Amazon.de", "2026-11-10T06:58:40Z"))
# the earlier session's read, 2026-10-15: the white kettle still had 9 units
OLD = dict(INV)
OLD.update({"KW-KETTLE-WHT": (9, (0, 240, 0), (3, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
            "KW-POUROVER": (141, (0, 0, 0), (4, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
            "KW-FROTHER": (96, (0, 160, 0), (3, 0, 0), (0, 0, 0), (0, 0, 0, 0, 0, 0)),
            "KW-KETTLE-BLK": (305, (0, 0, 0), (11, 8, 0), (0, 0, 0), (5, 0, 0, 3, 0, 0))})
put(T, "raw/amazon-sp-api/getInventorySummaries-%s-2026-10-15.json" % US, inv_reply(US, OLD, CATALOG, "Amazon.com", "2026-10-15T16:02:51Z"))
put(S, "getMarketplaceParticipations-na.json", {"payload": [
    {"marketplace": {"id": US, "countryCode": "US", "name": "Amazon.com", "defaultCurrencyCode": "USD", "defaultLanguageCode": "en_US", "domainName": "www.amazon.com"},
     "participation": {"isParticipating": True, "hasSuspendedListings": False}}]})
put(S, "getMarketplaceParticipations-eu.json", {"payload": [
    {"marketplace": {"id": m, "countryCode": c, "name": n, "defaultCurrencyCode": "EUR", "defaultLanguageCode": l, "domainName": "www." + n.lower()},
     "participation": {"isParticipating": True, "hasSuspendedListings": False}}
    for m, c, n, l in ((DE, "DE", "Amazon.de", "de_DE"), (FR, "FR", "Amazon.fr", "fr_FR"), (IT, "IT", "Amazon.it", "it_IT"),
                       (ES, "ES", "Amazon.es", "es_ES"), (NL, "NL", "Amazon.nl", "nl_NL"))]})

# ---- daily movements, US: shipments by day; receipts by day
def ship(sku, day):
    i = (day - FIRST).days
    wob = (i * 7) % 5 - 2
    if sku == "KW-KETTLE-WHT":
        if D("2026-10-18") <= day <= D("2026-11-01"):
            return 0
        if day >= D("2026-11-02"):
            return [4, 5, 4, 5, 4, 4, 4, 4][(day - D("2026-11-02")).days]
        if day >= D("2026-10-11"):
            return [4, 5, 4, 5, 4, 4, 3][(day - D("2026-10-11")).days]
        return max(0, 4 + (wob > 0))
    if sku == "KW-FROTHER" and day >= D("2026-11-08"):
        return {D("2026-11-08"): 3, D("2026-11-09"): 3}[day]
    base = {"KW-KETTLE-BLK": 5, "KW-TEAPOT-GLS": 2, "KW-INFUSER-2PK": 4, "KW-CADDY-TIN": 0, "KW-SCALE-DGT": 6,
            "KW-POUROVER": 3, "KW-MUG-SET4": 3, "KW-FROTHER": 3}[sku]
    if sku == "KW-CADDY-TIN":
        return 0 if day >= D("2026-10-05") else 2
    return max(0, base + (wob if base >= 3 else (wob > 0)))


RECEIPTS = {"KW-KETTLE-WHT": {D("2026-11-02"): 240}, "KW-SCALE-DGT": {D("2026-10-31"): 300, D("2026-11-01"): 180, D("2026-11-03"): 72},
            "KW-FROTHER": {D("2026-11-06"): 40}, "KW-MUG-SET4": {D("2026-09-24"): 120, D("2026-09-25"): 68},
            "KW-KETTLE-BLK": {D("2026-09-15"): 240}, "KW-POUROVER": {D("2026-08-20"): 200}}
END_SELLABLE = {k: v[0] + v[2][0] + v[2][2] for k, v in INV.items()}  # ending warehouse balance counts reserved but not transfer
IN_TRANSIT = {k: v[2][1] for k, v in INV.items()}
ADJ = {"KW-KETTLE-BLK": {D("2026-11-06"): ("M", -6)}}  # misplaced, now researching
UNSELL_IN = {"KW-MUG-SET4": {D("2026-10-09"): 5, D("2026-10-21"): 6, D("2026-11-04"): 3}}  # customer-damaged returns


def ledger():
    days = {}
    for sku in CATALOG:
        rec, adj = RECEIPTS.get(sku, {}), ADJ.get(sku, {})
        flows = [rec.get(d, 0) - ship(sku, d) + (adj[d][1] if d in adj else 0) for d in DAYS]
        bal = END_SELLABLE[sku] + IN_TRANSIT[sku] - sum(flows)
        rows = []
        for d, fl in zip(DAYS, flows):
            start = bal
            bal += fl
            tr = IN_TRANSIT[sku] if d >= D("2026-11-07") else 0
            rows.append({"date": d, "start": start - (IN_TRANSIT[sku] if d >= D("2026-11-08") else 0), "receipts": rec.get(d, 0),
                         "shipments": -ship(sku, d), "lost": adj[d][1] if d in adj else 0, "end": bal - tr, "transit": tr})
        assert min(r["end"] for r in rows) >= 0, sku
        days[sku] = rows
    return days


LEDGER = ledger()
WHT = LEDGER["KW-KETTLE-WHT"]
ZERO_DAYS = [r["date"].isoformat() for r in WHT if r["end"] == 0]
W30 = [d for d in DAYS if d >= D("2026-10-11")]
WHT_30 = sum(ship("KW-KETTLE-WHT", d) for d in W30)
assert ZERO_DAYS[0] == "2026-10-17" and ZERO_DAYS[-1] == "2026-11-01" and len(ZERO_DAYS) == 16 and WHT_30 == 63, (ZERO_DAYS, WHT_30)


def tsv_date(d):
    return d.strftime("%m/%d/%Y")


LS_HEAD = ["Date", "FNSKU", "ASIN", "MSKU", "Title", "Disposition", "Starting Warehouse Balance", "In Transit Between Warehouses",
           "Receipts", "Customer Shipments", "Customer Returns", "Vendor Returns", "Warehouse Transfer In/Out", "Found", "Lost",
           "Damaged", "Disposed", "Other Events", "Ending Warehouse Balance", "Unknown Events", "Location", "Store"]
ls_rows = []
for sku, rows in LEDGER.items():
    fn, asin, title = CATALOG[sku][:3]
    for r in rows:
        ls_rows.append({"Date": r["date"].isoformat(), "FNSKU": fn, "ASIN": asin, "MSKU": sku, "Title": title, "Disposition": "SELLABLE",
                        "Starting Warehouse Balance": r["start"], "In Transit Between Warehouses": r["transit"], "Receipts": r["receipts"],
                        "Customer Shipments": r["shipments"], "Customer Returns": 0, "Vendor Returns": 0, "Warehouse Transfer In/Out": 0,
                        "Found": 0, "Lost": r["lost"], "Damaged": 0, "Disposed": 0, "Other Events": 0,
                        "Ending Warehouse Balance": r["end"], "Unknown Events": 0, "Location": "US", "Store": "Amazon.com"})
for sku, unf in (("KW-MUG-SET4", INV["KW-MUG-SET4"][4]), ("KW-KETTLE-BLK", INV["KW-KETTLE-BLK"][4])):
    fn, asin, title = CATALOG[sku][:3]
    inflow = UNSELL_IN.get(sku, {})
    bal = sum(unf) - sum(inflow.values())
    for d in DAYS:
        st = bal
        bal += inflow.get(d, 0)
        ls_rows.append({"Date": d.isoformat(), "FNSKU": fn, "ASIN": asin, "MSKU": sku, "Title": title, "Disposition": "UNSELLABLE",
                        "Starting Warehouse Balance": st, "In Transit Between Warehouses": 0, "Receipts": 0, "Customer Shipments": 0,
                        "Customer Returns": inflow.get(d, 0), "Vendor Returns": 0, "Warehouse Transfer In/Out": 0, "Found": 0, "Lost": 0,
                        "Damaged": 0, "Disposed": 0, "Other Events": 0, "Ending Warehouse Balance": bal, "Unknown Events": 0,
                        "Location": "US", "Store": "Amazon.com"})

LD_HEAD = ["Date", "FNSKU", "ASIN", "MSKU", "Title", "Event Type", "Reference ID", "Quantity", "Fulfillment Center", "Disposition",
           "Reason", "Country", "Reconciled Quantity", "Unreconciled Quantity", "Date and Time", "Store"]
ld_rows = []
REF = {"KW-KETTLE-WHT": "FBA18KWWHT1", "KW-SCALE-DGT": "FBA19KWSCL1", "KW-FROTHER": "FBA19KWFRO1", "KW-MUG-SET4": "FBA18KWMUG1",
       "KW-KETTLE-BLK": "FBA18KWBLK1", "KW-POUROVER": "FBA18KWPOV1"}
for sku, rows in LEDGER.items():
    fn, asin, title, fc = CATALOG[sku][0], CATALOG[sku][1], CATALOG[sku][2], CATALOG[sku][7]
    for r in rows:
        d = r["date"]
        base = {"Date": d.isoformat(), "FNSKU": fn, "ASIN": asin, "MSKU": sku, "Title": title, "Fulfillment Center": fc,
                "Disposition": "SELLABLE", "Reason": "", "Country": "US", "Reconciled Quantity": "", "Unreconciled Quantity": "",
                "Store": "Amazon.com"}
        if r["receipts"]:
            ld_rows.append(dict(base, **{"Event Type": "Receipts", "Reference ID": REF[sku], "Quantity": r["receipts"],
                                         "Date and Time": d.isoformat() + "T14:22:05-07:00"}))
        if r["shipments"]:
            ld_rows.append(dict(base, **{"Event Type": "Shipments", "Reference ID": "Q%s%s" % (d.strftime("%m%d"), fn[-2:]),
                                         "Quantity": r["shipments"], "Date and Time": d.isoformat() + "T19:05:00-07:00"}))
        if r["lost"]:
            ld_rows.append(dict(base, **{"Event Type": "Adjustments", "Reference ID": "ADJ%s" % d.strftime("%m%d"), "Quantity": r["lost"],
                                         "Reason": "M", "Reconciled Quantity": 0, "Unreconciled Quantity": r["lost"],
                                         "Date and Time": d.isoformat() + "T09:12:44-08:00"}))
for d, q in UNSELL_IN["KW-MUG-SET4"].items():
    fn, asin, title = CATALOG["KW-MUG-SET4"][:3]
    ld_rows.append({"Date": d.isoformat(), "FNSKU": fn, "ASIN": asin, "MSKU": "KW-MUG-SET4", "Title": title, "Event Type": "CustomerReturns",
                    "Reference ID": "R%s08" % d.strftime("%m%d"), "Quantity": q, "Fulfillment Center": "QQB2", "Disposition": "CUSTOMER_DAMAGED",
                    "Reason": "", "Country": "US", "Reconciled Quantity": "", "Unreconciled Quantity": "",
                    "Date and Time": d.isoformat() + "T11:40:00-07:00", "Store": "Amazon.com"})
ld_rows.sort(key=lambda r: (r["Date"], r["MSKU"]))


# ---- report sources: {"kind", "gzip", "bom", "header", "rows", "date": column}
def source(rtype, mkt, header, rows, kind="snapshot", gz=False, date=None, bom=False):
    rows = [{c: r.get(c, "") for c in header} if isinstance(r, dict) else dict(zip(header, r)) for r in rows]
    put(S, "report-sources/%s-%s.json" % (rtype, mkt), {"reportType": rtype, "marketplaceId": mkt, "kind": kind, "gzip": gz,
                                                       "bom": bom, "header": header, "date": date, "rows": rows})


source("GET_LEDGER_SUMMARY_VIEW_DATA", US, LS_HEAD, ls_rows, kind="ledger-summary", gz=True, date="Date")
source("GET_LEDGER_DETAIL_VIEW_DATA", US, LD_HEAD, ld_rows, kind="ledger-detail", gz=True, date="Date")

MYI_HEAD = ["sku", "fnsku", "asin", "product-name", "condition", "your-price", "mfn-listing-exists", "mfn-fulfillable-quantity",
            "afn-listing-exists", "afn-warehouse-quantity", "afn-fulfillable-quantity", "afn-unsellable-quantity", "afn-reserved-quantity",
            "afn-total-quantity", "per-unit-volume", "afn-inbound-working-quantity", "afn-inbound-shipped-quantity",
            "afn-inbound-receiving-quantity", "afn-researching-quantity", "afn-reserved-future-supply", "afn-future-supply-buyable",
            "afn-fc-transfer-quantity", "afn-onhand-buyable-quantity", "store"]


def vol(sku):
    l, m, s = CATALOG[sku][5]
    return round(l * m * s / 1728, 4)


def myi(cat, inv, store, vol_of):
    out = []
    for sku, row in inv.items():
        f, (w, s, r), (pc, pt, fp), rs, u = row
        fn, asin, title, price = cat[sku][:4]
        out.append({"sku": sku, "fnsku": fn, "asin": asin, "product-name": title, "condition": "New", "your-price": price,
                    "mfn-listing-exists": "No", "mfn-fulfillable-quantity": "", "afn-listing-exists": "Yes",
                    "afn-warehouse-quantity": f + pc + pt + fp + sum(rs) + sum(u), "afn-fulfillable-quantity": f,
                    "afn-unsellable-quantity": sum(u), "afn-reserved-quantity": pc + pt + fp, "afn-total-quantity": total(row),
                    "per-unit-volume": vol_of(sku), "afn-inbound-working-quantity": w, "afn-inbound-shipped-quantity": s,
                    "afn-inbound-receiving-quantity": r, "afn-researching-quantity": sum(rs), "afn-reserved-future-supply": 0,
                    "afn-future-supply-buyable": 0, "afn-fc-transfer-quantity": pt, "afn-onhand-buyable-quantity": f, "store": store})
    return out


myi_us = myi(CATALOG, INV, "Amazon.com", vol)
myi_us.append({"sku": FBM_SKU, "fnsku": "", "asin": "B0STOCK003", "product-name": CATALOG["KW-TEAPOT-GLS"][2], "condition": "New",
               "your-price": 31.99, "mfn-listing-exists": "Yes", "mfn-fulfillable-quantity": 25, "afn-listing-exists": "No",
               "afn-warehouse-quantity": "", "afn-fulfillable-quantity": "", "afn-unsellable-quantity": "", "afn-reserved-quantity": "",
               "afn-total-quantity": "", "per-unit-volume": "", "afn-inbound-working-quantity": "", "afn-inbound-shipped-quantity": "",
               "afn-inbound-receiving-quantity": "", "afn-researching-quantity": "", "afn-reserved-future-supply": "",
               "afn-future-supply-buyable": "", "afn-fc-transfer-quantity": "", "afn-onhand-buyable-quantity": "", "store": "Amazon.com"})
source("GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA", US, MYI_HEAD, [r for r in myi_us if r["sku"] != "KW-CADDY-TIN"])
source("GET_FBA_MYI_ALL_INVENTORY_DATA", US, MYI_HEAD, myi_us)
EU_VOL = {"KW-KETTLE-BLK-EU": 0.0148, "KW-INFUSER-EU": 0.0070}  # cubic metres
source("GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA", DE, MYI_HEAD, myi(EU_SKUS, INV_DE, "Amazon.de", EU_VOL.get))

source("GET_AFN_INVENTORY_DATA_BY_COUNTRY", DE, ["seller-sku", "fulfillment-channel-sku", "asin", "condition-type", "country",
                                                 "quantity-for-local-fulfillment"],
       [[sku, EU_SKUS[sku][0], EU_SKUS[sku][1], "NewItem", c, q] for sku, cs in BY_COUNTRY.items() for c, q in cs])

RES_HEAD = ["sku", "fnsku", "asin", "product-name", "reserved_qty", "reserved_customerorders", "reserved_fc-processing", "reserved_staging", "program"]
source("GET_RESERVED_INVENTORY_DATA", US, RES_HEAD,
       [[sku, CATALOG[sku][0], CATALOG[sku][1], CATALOG[sku][2], sum(v[2]), v[2][0], v[2][2], 0, "FBA"] for sku, v in INV.items() if sum(v[2])])

# ---- Restock report (US)
RS_HEAD = ["Country", "Product Name", "FNSKU", "Merchant SKU", "ASIN", "Condition", "Supplier", "Supplier part no.", "Currency code",
           "Price", "Sales last 30 days", "Units Sold Last 30 Days", "Total Units", "Inbound", "Available", "FC transfer", "FC Processing",
           "Customer Order", "Unfulfillable", "Working", "Shipped", "Receiving", "Fulfilled by",
           "Total Days of Supply (including units from open shipments)", "Days of Supply at Amazon Fulfillment Network", "Alert",
           "Recommended replenishment qty", "Recommended ship date", "Recommended action", "Unit storage size"]
SOLD30 = {sku: sum(ship(sku, d) for d in W30) for sku in CATALOG}
# Amazon's own forward days of supply, recommended quantity and date, alert, action (invented, as Amazon's forecast is unseen)
RESTOCK = {"KW-KETTLE-BLK": (62, 29, "low_stock", 420, "2026-11-20", "Restock"),
           "KW-KETTLE-WHT": (38, 38, "low_stock", 180, "2026-11-24", "Restock"),
           "KW-TEAPOT-GLS": (35, 35, "", 0, "", ""),
           "KW-INFUSER-2PK": (262, 262, "", 0, "", ""),
           "KW-SCALE-DGT": (99, 92, "", 0, "", ""),
           "KW-POUROVER": (161, 7, "low_stock", 0, "", "Restock"),
           "KW-MUG-SET4": (49, 49, "", 0, "", ""),
           "KW-FROTHER": (40, 0, "out_of_stock", 60, "2026-11-12", "Restock")}
rs_rows = []
for sku, (tdos, adoss, alert, qty, date, action) in RESTOCK.items():
    fn, asin, title, price = CATALOG[sku][:4]
    f, (w, s, r), (pc, pt, fp), rs, u = INV[sku]
    rs_rows.append([ "US", title, fn, sku, asin, "New", "", "", "USD", price, r2(SOLD30[sku] * price), SOLD30[sku],
                     f + w + s + r + pc + pt + fp, w + s + r, f, pt, fp, pc, sum(u), w, s, r, "Amazon", tdos, adoss, alert, qty, date,
                     action, "Standard"])
source("GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT", US, RS_HEAD, rs_rows)

# ---- Planning report (US and DE)
AGE_COLS = ["inv-age-0-to-90-days", "inv-age-91-to-180-days", "inv-age-181-to-270-days", "inv-age-271-to-365-days"]
AIS = ["181-210", "211-240", "241-270", "271-300", "301-330", "331-365"]
PL_HEAD = (["snapshot-date", "sku", "fnsku", "asin", "product-name", "condition", "available", "fc-transfer", "pending-removal-quantity"]
           + AGE_COLS + ["currency", "units-shipped-t7", "units-shipped-t30", "units-shipped-t60", "units-shipped-t90", "alert",
           "your-price", "sales-price", "lowest-price-new-plus-shipping", "lowest-price-used", "recommended-action",
           "DEPRECATED healthy-inventory-level", "recommended-sales-price", "recommended-sale-duration-days", "recommended-removal-quantity",
           "estimated-cost-savings-of-recommended-actions", "sell-through", "item-volume", "volume-unit-measurement", "storage-type",
           "storage-volume", "marketplace", "product-group", "sales-rank", "days-of-supply", "estimated-excess-quantity",
           "weeks-of-cover-t30", "weeks-of-cover-t90", "featuredoffer-price", "sales-shipped-last-7-days", "sales-shipped-last-30-days",
           "sales-shipped-last-60-days", "sales-shipped-last-90-days", "inv-age-0-to-30-days", "inv-age-31-to-60-days",
           "inv-age-61-to-90-days", "inv-age-181-to-330-days", "inv-age-331-to-365-days", "estimated-storage-cost-next-month",
           "inbound-quantity", "inbound-working", "inbound-shipped", "inbound-received", "no-sale-last-6-months",
           "Total Reserved Quantity", "unfulfillable-quantity"]
           + [c for a in AIS for c in ("quantity-to-be-charged-ais-%s-days" % a, "estimated-ais-%s-days" % a)]
           + ["historical-days-of-supply", "fba-minimum-inventory-level", "fba-inventory-level-health-status",
              "Recommended ship-in quantity", "Recommended ship-in date", "Last updated date for Historical Days of Supply",
              "Exempted from Low-Inventory-Level fee?", "Low-Inventory-Level fee applied in current week?",
              "Short term historical days of supply", "Long term historical days of supply", "Inventory age snapshot date",
              "Inventory Supply at FBA", "Reserved FC Processing", "Reserved Customer Order", "Reserved Staging",
              "Total Days of Supply (including units from open shipments)", "supplier", "is-seasonal-in-next-3-months", "season-name",
              "season-start-date", "season-end-date", "Fulfillment Service and Programs", "inv-age-366-to-455-days",
              "inv-age-456-plus-days", "quantity-to-be-charged-ais-366-455-days", "estimated-ais-366-455-days",
              "quantity-to-be-charged-ais-456-plus-days", "estimated-ais-456-plus-days"])


def shipped(sku, n):
    return sum(ship(sku, LAST - dt.timedelta(k)) for k in range(n))


# per SKU: ages (0-90, 91-180, 181-270, 271-365), fine (0-30, 31-60, 61-90, 181-330, 331-365), ais quantities and amounts,
# hist DoS (short, long), fee exempt, fee applied, min level, health, ship-in qty and date, DoS, excess, action, removal qty
PLAN = {
    "KW-KETTLE-BLK": dict(age=(212 + 64, 0, 0, 0), fine=(150, 90, 36, 0, 0), hist=(41, 47), lif=("N", "N"), mil=190, health="Healthy",
                          shipin=(260, "2026-11-14"), dos=31, tdos=64, excess=0, action="No action required", remq=0),
    "KW-KETTLE-WHT": dict(age=(206, 0, 0, 0), fine=(206, 0, 0, 0, 0), hist=(29, 61), lif=("N", "N"), mil=120, health="Healthy",
                          shipin=(150, "2026-11-21"), dos=38, tdos=38, excess=0, action="No action required", remq=0),
    "KW-INFUSER-2PK": dict(age=(220, 360, 420, 60), fine=(70, 75, 75, 480, 0), hist=(266, 271), lif=("N", "N"), mil=60, health="Excess",
                           shipin=(0, ""), dos=262, tdos=262, excess=700, action="Create removal order", remq=480,
                           ais=((140, 25.20), (160, 34.56), (120, 31.32), (60, 27.90), (0, 0), (0, 0))),
    "KW-POUROVER": dict(age=(47, 0, 0, 0), fine=(47, 0, 0, 0, 0), hist=(16, 23), lif=("N", "Y"), mil=95, health="Low stock",
                        shipin=(0, ""), dos=7, tdos=161, excess=0, action="Restock", remq=0),
    "KW-SCALE-DGT": dict(age=(735, 0, 0, 0), fine=(735, 0, 0, 0, 0), hist=(94, 58), lif=("N", "N"), mil=160, health="Healthy",
                         shipin=(0, ""), dos=92, tdos=99, excess=0, action="No action required", remq=0),
    "KW-FROTHER": dict(age=(43, 0, 0, 0), fine=(43, 0, 0, 0, 0), hist=(9, 21), lif=("N", "N"), mil=80, health="Out of stock",
                       shipin=(60, "2026-11-12"), dos=0, tdos=40, excess=0, action="Restock", remq=0),
}
pl_rows = []
for sku, p in PLAN.items():
    fn, asin, title, price = CATALOG[sku][:4]
    f, (w, s, r), (pc, pt, fp), rs, u = INV[sku]
    a = p.get("ais", ((0, 0),) * 6)
    row = {"snapshot-date": "2026-11-09", "sku": sku, "fnsku": fn, "asin": asin, "product-name": title, "condition": "New",
           "available": f, "fc-transfer": pt, "pending-removal-quantity": 0, "currency": "USD",
           "units-shipped-t7": shipped(sku, 7), "units-shipped-t30": shipped(sku, 30), "units-shipped-t60": shipped(sku, 60),
           "units-shipped-t90": shipped(sku, 90), "alert": p["health"].lower().replace(" ", "_") if p["health"] != "Healthy" else "",
           "your-price": price, "sales-price": price, "lowest-price-new-plus-shipping": price, "lowest-price-used": "",
           "recommended-action": p["action"], "DEPRECATED healthy-inventory-level": "",
           "recommended-sales-price": 9.99 if sku == "KW-INFUSER-2PK" else "", "recommended-sale-duration-days": 14 if sku == "KW-INFUSER-2PK" else "",
           "recommended-removal-quantity": p["remq"], "estimated-cost-savings-of-recommended-actions": 118.98 if p["remq"] else 0,
           "sell-through": round(shipped(sku, 90) / max(1, (sum(p["age"]))), 2), "item-volume": vol(sku),
           "volume-unit-measurement": "cubic feet", "storage-type": "Standard", "storage-volume": round(vol(sku) * sum(p["age"]), 2),
           "marketplace": "US", "product-group": "Kitchen", "sales-rank": "", "days-of-supply": p["dos"],
           "estimated-excess-quantity": p["excess"], "weeks-of-cover-t30": round(f / max(1, shipped(sku, 30) / 30) / 7, 1),
           "weeks-of-cover-t90": round(f / max(1, shipped(sku, 90) / 90) / 7, 1), "featuredoffer-price": price,
           "sales-shipped-last-7-days": r2(shipped(sku, 7) * price), "sales-shipped-last-30-days": r2(shipped(sku, 30) * price),
           "sales-shipped-last-60-days": r2(shipped(sku, 60) * price), "sales-shipped-last-90-days": r2(shipped(sku, 90) * price),
           "inv-age-0-to-30-days": p["fine"][0], "inv-age-31-to-60-days": p["fine"][1], "inv-age-61-to-90-days": p["fine"][2],
           "inv-age-181-to-330-days": p["fine"][3], "inv-age-331-to-365-days": p["fine"][4],
           "estimated-storage-cost-next-month": r2(vol(sku) * sum(p["age"]) * 3.30), "inbound-quantity": w + s + r,
           "inbound-working": w, "inbound-shipped": s, "inbound-received": 0, "no-sale-last-6-months": 0,
           "Total Reserved Quantity": pc + pt + fp, "unfulfillable-quantity": sum(u),
           "historical-days-of-supply": max(p["hist"]), "fba-minimum-inventory-level": p["mil"],
           "fba-inventory-level-health-status": p["health"], "Recommended ship-in quantity": p["shipin"][0],
           "Recommended ship-in date": p["shipin"][1], "Last updated date for Historical Days of Supply": "2026-11-08",
           "Exempted from Low-Inventory-Level fee?": p["lif"][0], "Low-Inventory-Level fee applied in current week?": p["lif"][1],
           "Short term historical days of supply": p["hist"][0], "Long term historical days of supply": p["hist"][1],
           "Inventory age snapshot date": "2026-11-08", "Inventory Supply at FBA": f + pt + fp, "Reserved FC Processing": fp,
           "Reserved Customer Order": pc, "Reserved Staging": 0,
           "Total Days of Supply (including units from open shipments)": p["tdos"], "supplier": "",
           "is-seasonal-in-next-3-months": "N", "season-name": "", "season-start-date": "", "season-end-date": "",
           "Fulfillment Service and Programs": "FBA", "inv-age-366-to-455-days": 0, "inv-age-456-plus-days": 0,
           "quantity-to-be-charged-ais-366-455-days": 0, "estimated-ais-366-455-days": 0,
           "quantity-to-be-charged-ais-456-plus-days": 0, "estimated-ais-456-plus-days": 0}
    for c, v in zip(AGE_COLS, p["age"]):
        row[c] = v
    for band, (q, amt) in zip(AIS, a):
        row["quantity-to-be-charged-ais-%s-days" % band], row["estimated-ais-%s-days" % band] = q, amt
    pl_rows.append(row)
source("GET_FBA_INVENTORY_PLANNING_DATA", US, PL_HEAD, pl_rows, gz=True)
INFUSER_AIS = r2(sum(x[1] for x in PLAN["KW-INFUSER-2PK"]["ais"]))

# ---- Storage fee report: US September (in the tree) and October (stub), DE October
SF_HEAD = ["asin", "fnsku", "product_name", "fulfillment_center", "country_code", "longest_side", "median_side", "shortest_side",
           "measurement_units", "weight", "weight_units", "item_volume", "volume_units", "product_size_tier", "average_quantity_on_hand",
           "average_quantity_pending_removal", "estimated_total_item_volume", "month_of_charge", "storage_rate", "storage_utilization_ratio",
           "storage_utilization_ratio_units", "base_rate", "utilization_surcharge_rate", "avg_qty_for_sus", "est_vol_for_sus",
           "est_base_msf", "est_sus", "currency", "estimated_monthly_storage_fee", "dangerous_goods_storage_type",
           "eligible_for_inventory_discount", "qualifies_for_inventory_discount", "total_incentive_fee_amount",
           "breakdown_incentive_fee_amount", "average_quantity_customer_orders"]
RATES_US = {"2026-09": (0.84, 0.44, 28.9), "2026-10": (2.61, 0.69, 31.4)}


def avg_on_hand(sku, month):
    rows = [r for r in LEDGER[sku] if r["date"].strftime("%Y-%m") == month]
    return round(sum(r["end"] for r in rows) / len(rows), 2)


def sf_us(month):
    base, sus, ratio = RATES_US[month]
    out = []
    for sku in CATALOG:
        fn, asin, title, price, cost, (l, m, s), wt, fc = CATALOG[sku]
        q = avg_on_hand(sku, month)
        if sku == "KW-INFUSER-2PK" and month == "2026-10":
            q = 1148.0
        v = r2(q * vol(sku))
        out.append({"asin": asin, "fnsku": fn, "product_name": title, "fulfillment_center": fc, "country_code": "US", "longest_side": l,
                    "median_side": m, "shortest_side": s, "measurement_units": "inches", "weight": wt, "weight_units": "pounds",
                    "item_volume": vol(sku), "volume_units": "cubic feet", "product_size_tier": "Large Standard-Size",
                    "average_quantity_on_hand": q, "average_quantity_pending_removal": 0, "estimated_total_item_volume": v,
                    "month_of_charge": month, "storage_rate": r2(base + sus), "storage_utilization_ratio": ratio,
                    "storage_utilization_ratio_units": "weeks", "base_rate": base, "utilization_surcharge_rate": sus,
                    "avg_qty_for_sus": q, "est_vol_for_sus": v, "est_base_msf": r2(v * base), "est_sus": r2(v * sus), "currency": "USD",
                    "estimated_monthly_storage_fee": r2(v * base) + r2(v * sus), "dangerous_goods_storage_type": "--",
                    "eligible_for_inventory_discount": "N", "qualifies_for_inventory_discount": "N", "total_incentive_fee_amount": 0,
                    "breakdown_incentive_fee_amount": "", "average_quantity_customer_orders": 0})
        out[-1]["estimated_monthly_storage_fee"] = r2(out[-1]["estimated_monthly_storage_fee"])
    return out


sf_sep, sf_oct = sf_us("2026-09"), sf_us("2026-10")
source("GET_FBA_STORAGE_FEE_CHARGES_DATA", US, SF_HEAD, sf_sep + sf_oct, kind="range", date="month_of_charge")
INF_OCT = next(r for r in sf_oct if r["fnsku"] == "X00KWINF04")
# the earlier session downloaded September's report into the tree
sep_tsv = "\t".join(SF_HEAD) + "\n" + "".join("\t".join(str(r[c]) for c in SF_HEAD) + "\n" for r in sf_sep)
put(T, "raw/amazon-sp-api/reports/GET_FBA_STORAGE_FEE_CHARGES_DATA/ATVPDKIKX0DER_2026-09-01_2026-09-30/report.tsv", sep_tsv, raw=True)
put(T, "raw/amazon-sp-api/reports/GET_FBA_STORAGE_FEE_CHARGES_DATA/ATVPDKIKX0DER_2026-09-01_2026-09-30/receipt.json",
    {"reportType": "GET_FBA_STORAGE_FEE_CHARGES_DATA", "marketplaceIds": [US], "dataStartTime": "2026-09-01T00:00:00Z",
     "dataEndTime": "2026-09-30T23:59:59Z", "reportId": "52710018841", "reportDocumentId": "amzn1.spdoc.1.4.na.3f0c1e9a-77d2-4c1b-9b59-2a4e1d0f6c11",
     "read": "2026-10-15T16:04:10Z"})

EU_RATES = {"DE": ("QQD1", "EUR", 27.40), "PL": ("QQP1", "PLN", 104.50), "CZ": ("QQC1", "CZK", 612.00)}
sf_de = []
for sku, cs in BY_COUNTRY.items():
    fn, asin, title, price = EU_SKUS[sku]
    for c, q in cs:
        fc, cur, rate = EU_RATES[c]
        avg = round(q * 1.06, 2)
        v = round(avg * EU_VOL[sku], 4)
        sf_de.append({"asin": asin, "fnsku": fn, "product_name": title, "fulfillment_center": fc, "country_code": c,
                      "longest_side": 32.0 if "KETTLE" in sku else 17.8, "median_side": 23.1 if "KETTLE" in sku else 15.2,
                      "shortest_side": 20.1 if "KETTLE" in sku else 15.0, "measurement_units": "centimeters",
                      "weight": 1.41 if "KETTLE" in sku else 0.18, "weight_units": "kilograms", "item_volume": EU_VOL[sku],
                      "volume_units": "cubic meters", "product_size_tier": "Standard Parcel", "average_quantity_on_hand": avg,
                      "average_quantity_pending_removal": 0, "estimated_total_item_volume": v, "month_of_charge": "2026-10",
                      "storage_rate": rate, "storage_utilization_ratio": 18.6, "storage_utilization_ratio_units": "weeks",
                      "base_rate": rate, "utilization_surcharge_rate": 0, "avg_qty_for_sus": avg, "est_vol_for_sus": v,
                      "est_base_msf": r2(v * rate), "est_sus": 0, "currency": cur, "estimated_monthly_storage_fee": r2(v * rate),
                      "dangerous_goods_storage_type": "--", "eligible_for_inventory_discount": "N",
                      "qualifies_for_inventory_discount": "N", "total_incentive_fee_amount": 0, "breakdown_incentive_fee_amount": "",
                      "average_quantity_customer_orders": 0})
source("GET_FBA_STORAGE_FEE_CHARGES_DATA", DE, SF_HEAD, sf_de, kind="range", date="month_of_charge")
DE_KETTLE = {r["country_code"]: (r["storage_rate"], r["currency"], r["estimated_monthly_storage_fee"]) for r in sf_de if r["fnsku"] == "X00KWBLKE1"}

# DE planning report: no AIS 181-240 columns charged; low-inventory flags
de_pl = []
for sku, row in INV_DE.items():
    fn, asin, title, price = EU_SKUS[sku]
    de_pl.append({"snapshot-date": "2026-11-09", "sku": sku, "fnsku": fn, "asin": asin, "product-name": title, "condition": "New",
                  "available": row[0], "fc-transfer": row[2][1], "currency": "EUR", "marketplace": "DE", "volume-unit-measurement": "cubic meters",
                  "item-volume": EU_VOL[sku], "inv-age-0-to-90-days": row[0] + sum(row[2]), "days-of-supply": 58 if "KETTLE" in sku else 141,
                  "Exempted from Low-Inventory-Level fee?": "N", "Low-Inventory-Level fee applied in current week?": "N",
                  "Short term historical days of supply": 49, "Long term historical days of supply": 55, "historical-days-of-supply": 55,
                  "Inventory age snapshot date": "2026-11-08", "Fulfillment Service and Programs": "FBA, Pan-European FBA"})
source("GET_FBA_INVENTORY_PLANNING_DATA", DE, PL_HEAD, de_pl, gz=True)

# ---- aged surcharge charged on 2026-10-15 (US)
LT_HEAD = ["snapshot-date", "sku", "fnsku", "asin", "product-name", "condition", "per-unit-volume", "currency", "volume-unit", "country",
           "qty-charged", "amount-charged", "surcharge-age-tier", "rate-surcharge"]
LT = [("181-210", 300, 0.50), ("211-240", 80, 0.62)]
lt_rows = [["2026-10-15", "KW-INFUSER-2PK", "X00KWINF04", "B0STOCK004", CATALOG["KW-INFUSER-2PK"][2], "New", vol("KW-INFUSER-2PK"),
            "USD", "cubic feet", "US", q, r2(q * vol("KW-INFUSER-2PK") * rate), "Inv aged %s days" % tier, rate] for tier, q, rate in LT]
source("GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA", US, LT_HEAD, lt_rows, kind="range", date="snapshot-date")
LT_OCT = r2(sum(r[11] for r in lt_rows))

# ---- stranded (US)
ST_HEAD = ["primary-action", "date-stranded", "Date-to-take-auto-removal", "status-primary", "status-secondary", "error-message",
           "stranded-reason", "asin", "sku", "fnsku", "product-name", "condition", "fulfilled-by", "fulfillable-qty", "your-price",
           "unfulfillable-qty", "reserved-quantity", "inbound-shipped-qty"]
source("GET_STRANDED_INVENTORY_UI_DATA", US, ST_HEAD, [[
    "Fix listing", "2026-10-05", "2026-12-04", "Stranded", "Listing suppressed",
    "'item_package_weight' is required but not supplied.", "Listing suppressed", "B0STOCK005", "KW-CADDY-TIN", "X00KWCDY05",
    CATALOG["KW-CADDY-TIN"][2], "New", "Amazon", 86, 19.99, 0, 0, 0]])

# ---- removal orders (US)
RM_HEAD = ["request-date", "order-id", "order-source", "order-type", "service-speed", "order-status", "last-updated-date", "sku", "fnsku",
           "disposition", "requested-quantity", "cancelled-quantity", "disposed-quantity", "shipped-quantity", "in-process-quantity",
           "removal-fee", "currency"]
source("GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA", US, RM_HEAD, [
    ["2026-08-12T17:20:31-07:00", "KWRMV0812", "Seller-initiated Manual Removal", "Return", "Standard", "Completed",
     "2026-08-29T09:02:11-07:00", "KW-INFUSER-2PK", "X00KWINF04", "Sellable", 200, 0, 0, 200, 0, 206.00, "USD"],
    ["2026-06-03T10:11:00-07:00", "KWDSP0603", "Seller-initiated Manual Removal", "Disposal", "Standard", "Completed",
     "2026-06-10T08:45:30-07:00", "KW-MUG-SET4", "X00KWMUG08", "Customer Damaged", 9, 0, 9, 0, 0, 3.15, "USD"]],
    kind="range", date="request-date")

# ---- listings report (US): both teapot offers
LA_HEAD = ["item-name", "item-description", "listing-id", "seller-sku", "price", "quantity", "open-date", "image-url", "item-is-marketplace",
           "product-id-type", "zshop-shipping-fee", "item-note", "item-condition", "zshop-category1", "zshop-browse-path",
           "zshop-storefront-feature", "asin1", "asin2", "asin3", "will-ship-internationally", "expedited-shipping", "zshop-boldface",
           "product-id", "bid-for-featured-placement", "add-delete", "pending-quantity", "fulfillment-channel", "merchant-shipping-group",
           "status"]
la = []
for i, sku in enumerate(list(CATALOG) + [FBM_SKU]):
    c = CATALOG.get(sku, CATALOG["KW-TEAPOT-GLS"])
    fbm = sku == FBM_SKU
    la.append({"item-name": c[2], "listing-id": "1105KW%04dX" % (i + 1), "seller-sku": sku, "price": 31.99 if fbm else c[3],
               "quantity": 25 if fbm else "", "open-date": "2025-03-1%d 10:00:00 PDT" % (i % 9), "item-is-marketplace": "y",
               "product-id-type": 1, "item-condition": 11, "asin1": c[1], "will-ship-internationally": "", "expedited-shipping": "",
               "product-id": c[1], "add-delete": "", "pending-quantity": 0 if not fbm else 2,
               "fulfillment-channel": "DEFAULT" if fbm else "AMAZON_NA", "merchant-shipping-group": "Migrated Template" if fbm else "",
               "status": "Inactive" if sku == "KW-CADDY-TIN" else "Active"})
source("GET_MERCHANT_LISTINGS_ALL_DATA", US, LA_HEAD, la, bom=True)

# ---- listings items (US): the two teapot SKUs, the caddy, the pour-over
def item(sku, asin, title, status, attrs, avail, issues=(), price=None):
    return {"sku": sku, "summaries": [{"marketplaceId": US, "asin": asin, "productType": "TEAPOT" if "TEAPOT" in sku else "KITCHEN",
                                       "conditionType": "new_new", "status": status, "fnSku": CATALOG.get(sku, ("",))[0] or None,
                                       "itemName": title, "createdDate": "2025-03-12T17:00:00Z", "lastUpdatedDate": "2026-11-09T21:14:03Z"}],
            "attributes": attrs, "issues": list(issues), "offers": [{"marketplaceId": US, "offerType": "B2C",
                                                                     "price": {"currencyCode": "USD", "amount": str(price)}}] if price else [],
            "fulfillmentAvailability": avail, "procurement": [], "relationships": [], "productTypes": []}


put(S, "getListingsItem-%s-%s.json" % (FBM_SKU, US), item(FBM_SKU, "B0STOCK003", CATALOG["KW-TEAPOT-GLS"][2], ["BUYABLE", "DISCOVERABLE"], {
    "fulfillment_availability": [{"fulfillment_channel_code": "DEFAULT", "quantity": 40, "lead_time_to_ship_max_days": 2}],
    "purchasable_offer": [{"marketplace_id": US, "currency": "USD", "our_price": [{"schedule": [{"value_with_tax": 31.99}]}]}],
    "condition_type": [{"value": "new_new", "marketplace_id": US}]}, [{"fulfillmentChannelCode": "DEFAULT", "quantity": 25}], price=31.99))
put(S, "getListingsItem-%s-%s.json" % ("KW-TEAPOT-GLS", US), item("KW-TEAPOT-GLS", "B0STOCK003", CATALOG["KW-TEAPOT-GLS"][2], ["BUYABLE", "DISCOVERABLE"], {
    "fulfillment_availability": [{"fulfillment_channel_code": "AMAZON_NA"}],
    "purchasable_offer": [{"marketplace_id": US, "currency": "USD", "our_price": [{"schedule": [{"value_with_tax": 29.99}]}]}],
    "condition_type": [{"value": "new_new", "marketplace_id": US}]}, [{"fulfillmentChannelCode": "AMAZON_NA"}], price=29.99))
put(S, "getListingsItem-%s-%s.json" % ("KW-CADDY-TIN", US), item("KW-CADDY-TIN", "B0STOCK005", CATALOG["KW-CADDY-TIN"][2], [], {
    "fulfillment_availability": [{"fulfillment_channel_code": "AMAZON_NA"}]}, [{"fulfillmentChannelCode": "AMAZON_NA"}], issues=[{
        "code": "90220", "message": "'item_package_weight' is required but not supplied.", "severity": "ERROR",
        "attributeNames": ["item_package_weight"], "categories": ["MISSING_ATTRIBUTE"],
        "enforcements": {"actions": [{"action": "LISTING_SUPPRESSED"}], "exemption": {"status": "NOT_EXEMPT"}}, "marketplaceIds": [US]}]))
put(S, "getListingsItem-%s-%s.json" % ("KW-POUROVER", US), item("KW-POUROVER", "B0STOCK007", CATALOG["KW-POUROVER"][2], ["BUYABLE", "DISCOVERABLE"], {
    "fulfillment_availability": [{"fulfillment_channel_code": "AMAZON_NA"}]}, [{"fulfillmentChannelCode": "AMAZON_NA"}], price=22.99))

# ---- inbound, v0 (US)
ADDR = {"Name": "Kettlewick Supply", "AddressLine1": "1 Fixture Way", "City": "Newark", "StateOrProvinceCode": "NJ", "CountryCode": "US", "PostalCode": "07105"}
V0 = [("FBA19KWSCL1", "KW scale 2026-10", "QQA1", "RECEIVING", [("KW-SCALE-DGT", 600, 552)]),
      ("FBA19KWFRO1", "KW frother 2026-10", "QQA1", "RECEIVING", [("KW-FROTHER", 160, 40)]),
      ("FBA19KWBLK1", "KW black kettle 2026-10", "QQA1", "IN_TRANSIT", [("KW-KETTLE-BLK", 300, 0)]),
      ("FBA19KWPOV1", "KW pour-over 2026-10 sea", "QQB2", "SHIPPED", [("KW-POUROVER", 500, 0)]),
      ("FBA18KWWHT1", "KW white kettle 2026-09", "QQA1", "CLOSED", [("KW-KETTLE-WHT", 240, 240)]),
      ("FBA18KWMUG1", "KW mugs 2026-08", "QQB2", "CLOSED", [("KW-MUG-SET4", 200, 188)])]
put(S, "getShipments-%s.json" % US, {"payload": {"ShipmentData": [
    {"ShipmentId": sid, "ShipmentName": name, "ShipFromAddress": ADDR, "DestinationFulfillmentCenterId": fc, "ShipmentStatus": st,
     "LabelPrepType": "SELLER_LABEL", "AreCasesRequired": True, "BoxContentsSource": "INTERACTIVE"} for sid, name, fc, st, _ in V0]}})
for sid, name, fc, st, items in V0:
    put(S, "getShipmentItemsByShipmentId-%s.json" % sid, {"payload": {"ItemData": [
        {"ShipmentId": sid, "SellerSKU": sku, "FulfillmentNetworkSKU": CATALOG[sku][0], "QuantityShipped": q, "QuantityReceived": rcv,
         "QuantityInCase": 12 if sku == "KW-SCALE-DGT" else 8, "PrepDetailsList": []} for sku, q, rcv in items]}})

# ---- inbound, 2024-03-20 (US): the scale's plan (shipped) and the black-friday top-up (options offered, none confirmed)
SRC = {"addressLine1": "1 Fixture Way", "city": "Newark", "countryCode": "US", "name": "Kettlewick Supply", "postalCode": "07105",
       "stateOrProvinceCode": "NJ", "companyName": "Kettlewick LLC"}
P_SCL, P_BLK = "wf0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c01", "wf0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c02"
SH_SCL = "sh0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c11"
SH_BLK = ["sh0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c2%d" % i for i in (1, 2, 3)]
SH_BLK_MIN = "sh0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c29"
PO_OPT, PO_MIN = "pl0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c31", "pl0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c32"
plans = [{"createdAt": "2026-10-18T15:02:11Z", "inboundPlanId": P_SCL, "lastUpdatedAt": "2026-11-03T22:40:17Z", "marketplaceIds": [US],
          "name": "KW scale 2026-10", "sourceAddress": SRC, "status": "SHIPPED"},
         {"createdAt": "2026-11-09T18:31:45Z", "inboundPlanId": P_BLK, "lastUpdatedAt": "2026-11-09T18:44:02Z", "marketplaceIds": [US],
          "name": "KW black kettle BF top-up", "sourceAddress": SRC, "status": "ACTIVE"}]
put(S, "listInboundPlans.json", {"inboundPlans": plans, "pagination": {}})
put(S, "getInboundPlan-%s.json" % P_SCL, dict(plans[0], packingOptions=[], placementOptions=[{"placementOptionId": "pl0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c19", "status": "ACCEPTED"}],
                                              shipments=[{"shipmentId": SH_SCL, "status": "RECEIVING"}]))
put(S, "getInboundPlan-%s.json" % P_BLK, dict(plans[1], packingOptions=[], placementOptions=[{"placementOptionId": PO_OPT, "status": "OFFERED"},
                                              {"placementOptionId": PO_MIN, "status": "OFFERED"}],
                                              shipments=[{"shipmentId": s, "status": "UNCONFIRMED"} for s in SH_BLK + [SH_BLK_MIN]]))
put(S, "listInboundPlanItems-%s.json" % P_SCL, {"items": [{"asin": "B0STOCK006", "fnsku": "X00KWSCL06", "labelOwner": "SELLER", "msku": "KW-SCALE-DGT",
                                                         "prepInstructions": [], "quantity": 600}], "pagination": {}})
put(S, "listInboundPlanItems-%s.json" % P_BLK, {"items": [{"asin": "B0STOCK001", "fnsku": "X00KWBLK01", "labelOwner": "SELLER", "msku": "KW-KETTLE-BLK",
                                                         "prepInstructions": [], "quantity": 400}], "pagination": {}})


def fee(amount):
    return {"description": "Placement service fee", "target": "Placement Services", "type": "FEE", "value": {"amount": amount, "code": "USD"}}


put(S, "listPlacementOptions-%s.json" % P_BLK, {"placementOptions": [
    {"discounts": [], "expiration": "2026-11-17T18:44:02.000Z", "fees": [fee(0.00)], "placementOptionId": PO_OPT, "shipmentIds": SH_BLK, "status": "OFFERED"},
    {"discounts": [], "expiration": "2026-11-17T18:44:02.000Z", "fees": [fee(112.00)], "placementOptionId": PO_MIN, "shipmentIds": [SH_BLK_MIN], "status": "OFFERED"}],
    "pagination": {}})
put(S, "getShipment-%s.json" % SH_SCL, {"amazonReferenceId": "1KWSCL0X", "destination": {"destinationType": "AMAZON_OPTIMIZED", "warehouseId": "QQA1",
        "address": {"addressLine1": "100 Fixture Pkwy", "city": "Ontario", "countryCode": "US", "name": "QQA1", "postalCode": "91761", "stateOrProvinceCode": "CA"}},
    "name": "KW scale 2026-10", "placementOptionId": "pl0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c19", "selectedTransportationOptionId": "to0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c41",
    "shipmentConfirmationId": "FBA19KWSCL1", "shipmentId": SH_SCL, "source": {"sourceType": "SELLER_FACILITY", "address": SRC}, "status": "RECEIVING",
    "dates": {"readyToShipWindow": {"start": "2026-10-21T00:00:00Z", "end": "2026-10-23T00:00:00Z"}},
    "selectedDeliveryWindow": {"availabilityType": "AVAILABLE", "deliveryWindowOptionId": "dw0a1b2c3d-4e5f-4a6b-8c7d-0e1f2a3b4c51",
                               "startDate": "2026-10-28T00:00:00Z", "endDate": "2026-11-03T23:59:59Z"}})
put(S, "listShipmentItems-%s.json" % SH_SCL, {"items": [{"asin": "B0STOCK006", "fnsku": "X00KWSCL06", "labelOwner": "SELLER", "msku": "KW-SCALE-DGT",
                                                        "prepInstructions": [], "quantity": 600}], "pagination": {}})
for s in SH_BLK + [SH_BLK_MIN]:
    put(S, "getShipment-%s.json" % s, {"destination": {"destinationType": "AMAZON_OPTIMIZED"}, "placementOptionId": PO_MIN if s == SH_BLK_MIN else PO_OPT,
                                       "shipmentId": s, "source": {"sourceType": "SELLER_FACILITY", "address": SRC}, "status": "UNCONFIRMED"})

# ---- fee estimates (any catalog ASIN, US and DE) and order metrics (US, AFN)
FEES = {"B0STOCK001": (7.50, 6.38), "B0STOCK002": (7.50, 6.38), "B0STOCK003": (4.50, 5.02), "B0STOCK004": (1.95, 3.71),
        "B0STOCK005": (3.00, 4.48), "B0STOCK006": (5.25, 4.96), "B0STOCK007": (3.45, 4.62), "B0STOCK008": (4.20, 6.04), "B0STOCK009": (2.70, 3.71)}
put(S, "feesEstimate-table.json", {"US": {a: {"price": CATALOG[[k for k, v in CATALOG.items() if v[1] == a][0]][3], "referral": f[0], "fba": f[1]}
                                         for a, f in FEES.items()},
                                  "DE": {"B0STOCK001": {"price": 54.99, "referral": 8.25, "fba": 5.71}, "B0STOCK004": {"price": 13.99, "referral": 2.10, "fba": 3.39}}})
put(S, "orderMetrics-daily.json", {"note": "AFN units ordered per Pacific day, by SKU", "start": FIRST.isoformat(),
                                    "units": {sku: [ship(sku, d) for d in DAYS] for sku in CATALOG},
                                    "price": {sku: CATALOG[sku][3] for sku in CATALOG}, "asin": {sku: CATALOG[sku][1] for sku in CATALOG}})
# MCF: fees per unit by SKU for the previews; fulfillable comes from today's inventory
put(S, "mcf-fees.json", {"KW-POUROVER": {"FBAPerUnitFulfillmentFee": 7.96, "FBAPerOrderFulfillmentFee": 0.00},
                         "KW-KETTLE-BLK": {"FBAPerUnitFulfillmentFee": 10.42, "FBAPerOrderFulfillmentFee": 0.00},
                         "KW-TEAPOT-GLS": {"FBAPerUnitFulfillmentFee": 8.31, "FBAPerOrderFulfillmentFee": 0.00}})

# ---- the seller's notes
put(T, "notes/catalog.md", """# Kettlewick catalog (seller's own notes)

| SKU | ASIN | Item | Price | Landed unit cost |
|---|---|---|---|---|
""" + "".join("| %s | %s | %s | %.2f | %.2f |\n" % (k, v[1], v[2], v[3], v[4]) for k, v in CATALOG.items()) + """| KW-TEAPOT-GLS-FBM | B0STOCK003 | the same teapot, shipped from our NJ warehouse | 31.99 | 6.10 |

Europe (Pan-European FBA since 2025-06, home store Amazon.de): KW-KETTLE-BLK-EU (B0STOCK001) and KW-INFUSER-EU (B0STOCK004).
We allow storage in Poland and the Czech Republic.

Supplier (Ningbo): production 25 days after deposit; sea to Long Beach about 35 days door to door; air 9 days. Factory closed
for Chinese New Year 2027-02-01 to 2027-02-21.
""", raw=True)
put(T, "notes/awd.md", """# AWD

Black kettles (KW-KETTLE-BLK) go into AWD since 2026-08; auto-replenishment on. Last count I wrote down from the AWD page:
about 900 units on 2026-10-01. I never set up any API access for AWD.
""", raw=True)
put(T, "notes/channels.md", """# Channels

- Glass teapot: FBA SKU KW-TEAPOT-GLS and FBM SKU KW-TEAPOT-GLS-FBM from our NJ warehouse (handling 2 days). I set the FBM
  quantity to 40 on 2026-11-03 in Seller Central.
- Shopify store (kettlewick.example): orders shipped through Multi-Channel Fulfillment from FBA stock.
- Nobody else changes inventory settings; the automated removal settings were never opened.
""", raw=True)

if SUMMARY:
    print(json.dumps({
        "today": TODAY.isoformat(),
        "P1_total_with_awd": {"totalQuantity": total(INV["KW-KETTLE-BLK"]), "fulfillable": 212, "inbound": 300,
                              "reserved": {"customer": 18, "transfer": 41, "processing": 5}, "researching_1_10": 6,
                              "unfulfillable": {"customer_damaged": 7, "carrier_damaged": 3}, "awd": "403 Unauthorized"},
        "P2_pan_eu": {"per_marketplace_fulfillable": 380, "by_country": dict(BY_COUNTRY["KW-KETTLE-BLK-EU"]), "reserved": 29},
        "C1_storage_us_oct": {k: INF_OCT[k] for k in ("base_rate", "utilization_surcharge_rate", "storage_rate", "storage_utilization_ratio",
                                                      "average_quantity_on_hand", "estimated_total_item_volume", "est_sus", "estimated_monthly_storage_fee")},
        "C1_storage_us_sep": dict(zip(("base", "sus", "ratio"), RATES_US["2026-09"])),
        "C2_storage_de_oct_kettle": DE_KETTLE, "C2_ratio_weeks": 18.6,
        "O1_white_kettle": {"zero_ending_days": len(ZERO_DAYS), "first": ZERO_DAYS[0], "last": ZERO_DAYS[-1],
                            "shipped_on_first_zero_day": ship("KW-KETTLE-WHT", D("2026-10-17")), "units_30d": WHT_30,
                            "per_day_30": round(WHT_30 / 30, 2), "per_in_stock_day_15": round(WHT_30 / 15, 2), "per_in_stock_day_14": round(WHT_30 / 14, 2)},
        "O2_frother": {"fulfillable": 0, "transfer": 37, "customer": 4, "processing": 2, "receiving": 120},
        "R1_black_kettle": {"restock": {"qty": 420, "date": "2026-11-20", "total_dos": 62, "afn_dos": 29},
                            "planning": {"qty": 260, "date": "2026-11-14"}, "units_shipped_t30": shipped("KW-KETTLE-BLK", 30)},
        "R2_pourover": {"fee_applied": "Y", "short_hdos": 16, "long_hdos": 23, "inbound": 500, "fulfillable": 18},
        "I1_scale": {"shipped": 600, "received": 552, "status": "RECEIVING", "receipts": {"2026-10-31": 300, "2026-11-01": 180, "2026-11-03": 72},
                     "closed_with_shortfall": {"FBA18KWMUG1": [200, 188]}},
        "I2_placement": {"amazon_optimized": 0.00, "minimal_split": 112.00, "quantity": 400},
        "S1": {"caddy_stranded": 86, "date_stranded": "2026-10-05", "auto_removal": "2026-12-04",
               "mug_unfulfillable": {"customer_damaged": 14, "warehouse_damaged": 3, "defective": 2}},
        "S2_infuser": {"ages": PLAN["KW-INFUSER-2PK"]["age"], "estimated_ais_total": INFUSER_AIS, "excess": 700, "removal_qty": 480,
                       "ltsf_oct_charged": LT_OCT, "removal_fee_aug": [200, 206.00], "units_shipped_t30": shipped("KW-INFUSER-2PK", 30)},
        "F1_teapot_fbm": {"attribute_quantity": 40, "live_quantity": 25},
        "F2_pourover_mcf": {"fulfillable": 18, "transfer": 26, "customer": 3, "asked": 30, "unfillable": 12, "fee_per_unit": 7.96},
    }, indent=2, ensure_ascii=False))
