# Developing cx-amazon-stock-playbook

The README is written for a seller, in English (`README.md`) and Chinese (`README.zh-CN.md`); the Plugins page draws it. These are the notes for whoever works on the package.

A [pi](https://pi.dev) package for a seller's Amazon stock, read through SP-API: where every unit is and what can be bought now, what holding it costs, running out, restocking, stock on its way, stuck stock and its ways out, and stock fulfilled by the seller or outside Amazon. It is written for the assistant in a [ComChatX](https://comchatx.com) seller's box, and reads the seller's account through the box's `cx` command and the [`cx-amazon-sp-api`](https://github.com/comchatx/cx-amazon-sp-api) package.

It is text only: no script, no extension, no dependency. Its changes are in [CHANGELOG.md](CHANGELOG.md). Every line of the skills ends with the position it rests on, as `(W8)` or `(C21, G4)`, and the positions are in [`research/README.md`](research/README.md); a line without one only points to another file. The research stays in the repository and does not ship.

## What it holds

| | What the model reads | Positions |
|---|---|---|
| `skills/stock-position` | Every stock state and what can be bought now, the reports and the ledger and where they do not tie, freshness; the shared homes for every read and its role (`references/reads-and-roles.md`), programs and regions (`references/programs-and-regions.md`) and what only Seller Central shows (`references/seller-central-only.md`) | W, A, G, Q |
| `skills/stock-cost` | Every holding charge: its rule, its dated history, its differences by store, the 2027 US change, and where each value is read | C |
| `skills/stock-out` | What out of stock is in Amazon's data, Amazon's stated consequences, what is and is not measured, censored demand | O, T |
| `skills/restock` | Amazon's recommendation reports and what moves them, the settings the API cannot see, lead time, and the methods as the seller's choices | R, T |
| `skills/stock-inbound` | Stock on its way as a position: when it becomes sellable, receiving and shortfalls, the writes' charges and what they fix in place | I |
| `skills/stuck-stock` | Stranded, excess, aged and unsellable stock, and every way out with what it makes permanent | S |
| `skills/fbm-and-channels` | Seller-fulfilled quantity, an item with both offers, Multi-Channel Fulfillment, stock outside Amazon | F |
| `prompts/*.md` | `/stock-position`, `/restock-plan`, `/stock-cost`, `/stuck-stock`, `/stockout-review`: each hands the seller's words to cx | |

Each template's `description:` is one English sentence; its Chinese is `comchatx.prompts.<name>.zh` in `package.json`, beside each skill's words in `comchatx.skills`, as the Plugins page reads them.

How a call is made and how a report is asked for and landed is the `amazon-sp-api` skill's (`references/door.md`), never this package's. A value that differs by store or year (a fee rate, a band, a capacity limit, a claim window, a date of the year) is in no skill line: the line states the rule and where the seller's own value is read. The research's ten lines of its own seat enter no skill.

Two other packages own facts beside these: `cx-listing-playbook` owns why a listing's sales moved and whether a change to it worked, and reads a stock-out as a confounder; `@comchatx/cx-amazon-finance-playbook` owns how a holding charge posts to the seller's money. Nothing of theirs is written here.

## What the README no longer says

The README's words were signed on 2026-11-11. These parts of the earlier README left it then and are kept here whole, in both languages: a first paragraph that said "every unit" where AWD stock cannot be read, named SP-API (now under "What it uses") and said cx reads the seller's own stores only; two questions, one now asked in a seller's words and one that the `/stuck-stock` template already asks; and the heading "What it needs".

> cx reads your Amazon stock through SP-API: where every unit is and which of it shoppers can buy now, what holding it costs you, what is stuck and how it can leave, and when more must land. It reads your own stores only, and changes nothing at Amazon unless you ask.
>
> - Which of my products will run out before the shipment on its way arrives?
> - What is stranded or aged in my inventory, and what would each way out cost?
>
> ## What it needs

> cx 通过 SP-API 读取你的亚马逊库存：每一件在哪、哪些买家现在能买，压着要花多少钱，哪些卡住了、可以怎么处理，以及什么时候必须补货。它只读你自己的店铺，除非你开口，不会在亚马逊做任何改动。
>
> 你可以问：
>
> - 我哪些商品会在途中那批货到仓之前断货？
> - 我的库存里哪些滞留或超龄了，每条出路要花多少？
>
> ## 需要什么

## What it needs

pi, and in the box the `cx` command with the Amazon SP-API source. It reaches no network itself.

## Install

```bash
pi install npm:@comchatx/cx-amazon-stock-playbook
```

On ComChatX, a seller installs it from the Plugins page.

## Develop

```bash
npm ci
npm run typecheck
npm test               # pi at the pin loads the package and its tarball and expands every template;
                       # every line of the skills cites a position that exists, each of the 283 is cited,
                       # and none restates the seat's own; each SKILL.md body is at most 371 words; no line of
                       # a skill file carries a fee amount, rate, share, band, capacity limit, claim window or
                       # date of the year
```

The skills were measured with Anthropic's `skill-creator`; the cases, the fixture and the stand-in `cx` are in [`evals/`](evals/README.md), and nothing there ships.

## Release

A tag `v<version>` on `main`, the version in `package.json`, runs `.github/workflows/release.yml`, which publishes through npm trusted publishing. WRITING-A-PACKAGE.md, "Shipping it", gives the steps before the first release.
