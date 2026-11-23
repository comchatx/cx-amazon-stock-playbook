# Changelog

## 0.1.4

- The tile's mark on the Plugins page is the signed drawing.

## 0.1.3

- Each template's body is its description, word for word, then the seller's own words: `stock-position`, `restock-plan`, `stock-cost`, `stuck-stock` and `stockout-review`. Typing `/stock-cost` sends "Work out what holding my Amazon stock cost last month."; typing `/stuck-stock SKU-1` sends that template's sentence, then "SKU-1".

## 0.1.2

- The README no longer names another plugin; what the playbook builds on is its `comchatx.builds`, each with its reason, as signed on 2026-11-18. The sentence "To see what each product earns after fees, also install [Amazon Finance Playbook](…)." and its Chinese are gone; `@comchatx/cx-amazon-finance-playbook` is an optional entry with the reason 「用于算出每个商品扣掉费用后赚了多少。」 / "Works out what each product earns after fees."
- "What it uses" names the account, not the plugin: 「**你的亚马逊卖家账户**：cx 在这里读取库存、报告和货件。」 / "**Your Amazon seller account:** cx reads your inventory, reports and shipments there."
- `cx-amazon-seller` is a new optional entry, with the reason 「用于让 cx 从第一条消息起就知道你在亚马逊开店。」 / "Tells cx from the start that you sell on Amazon."
- Four templates' English reads as the seller's own message, as signed on 2026-11-17: `stock-cost`, `stock-position`, `stockout-review` and `stuck-stock` say "my" where they said "your". Their Chinese, and `restock-plan`, stay.

## 0.1.1

- The card's name is the one signed on 2026-11-17: "Amazon Stock Playbook" on the English page (`comchatx.name`) and 「亚马逊库存分析手册」 on the Chinese page (`comchatx.nameZh`).
- The README, in English and Chinese, calls each plugin of ours it names by the card's name signed on 2026-11-17.
- The README names each other plugin it speaks of by the card's name in its own language, a link to that plugin's page on npm, never by the npm name.

## 0.1.0

- The first version: seven skills on a seller's Amazon stock over `cx-amazon-sp-api` (`stock-position`, `stock-cost`, `stock-out`, `restock`, `stock-inbound`, `stuck-stock`, `fbm-and-channels`) and five templates (`/stock-position`, `/restock-plan`, `/stock-cost`, `/stuck-stock`, `/stockout-review`). Every line of the skills cites one of the 283 positions in `research/README.md`.
