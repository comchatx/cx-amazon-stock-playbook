/** The words Jack signed on 2026-11-11 for the Plugins page: the card's name and line, each template's and each skill's. */
export const NAME = "Amazon Stock Playbook";
export const LINE = { en: "Shows where your Amazon stock is, and when to restock.", zh: "看清亚马逊库存都在哪，算出何时补货、补多少。" } as const;
export const SKILL_WORDS = {
  "stock-position": { zh: "查清库存在哪、处于什么状态、能卖多少。", en: "Where your stock is, its state, and what can sell now." },
  "stock-cost": { zh: "算出仓储、库龄等压库存的费用。", en: "What holding stock costs: storage, aged stock and more." },
  "stock-out": { zh: "分析断货的影响和被低估的需求。", en: "What a stock-out stops, and the demand it hides." },
  "restock": { zh: "读懂补货建议，算出发多少、何时发。", en: "Amazon's restock advice, and how much to send when." },
  "stock-inbound": { zh: "跟踪在途库存，查收货短缺和入库费用。", en: "Stock on its way: when it sells, shortfalls and fees." },
  "stuck-stock": { zh: "找出卡住的库存，以及每条出路的代价。", en: "Stuck stock, and what each way out costs." },
  "fbm-and-channels": { zh: "管理自发货数量、多渠道配送和站外库存。", en: "Your own-fulfilled quantity, MCF and stock elsewhere." },
} as const;
export const PROMPT_WORDS = {
  "stock-position": { zh: "盘点亚马逊库存：在哪、能卖多少、哪些卡住了。", en: "See where your Amazon stock is and what shoppers can buy now.", body: "Take stock of my Amazon inventory: where my units are, what shoppers can buy now, what is on its way and what is stuck, and say where each figure comes from." },
  "restock-plan": { zh: "看看哪些商品该补货，发多少、何时发。", en: "See which products need more stock, and how much to send and when.", body: "Tell me which of my products need more stock: what Amazon recommends, what I already have on its way, and how much you would send and when, with your reasons." },
  "stock-cost": { zh: "算出上个月在亚马逊压库存花了多少钱。", en: "Work out what holding your Amazon stock cost last month.", body: "Work out what holding my stock at Amazon cost me last month: storage, aged stock, low stock and capacity charges, which products drive them, and where each rate comes from." },
  "stuck-stock": { zh: "找出滞留、冗余、超龄和不可售的库存及其出路。", en: "Find your stuck stock and what each way out costs.", body: "Find my stuck stock at Amazon: stranded, excess, aged and unsellable units, what each way out costs, and which cannot be undone." },
  "stockout-review": { zh: "复盘最近的断货：断了多久、为什么断。", en: "Look back at your recent stock-outs and what they likely cost.", body: "Look back at my recent stock-outs: how long each lasted, what sales it likely cost and how you estimated that, and where in the chain it started." },
} as const;
/** The signed Overview, each README whole. */
export const OVERVIEW = {
  "README.md": "cx reads your stock in Amazon's warehouses: where each product is, what shoppers can buy now, what it costs to hold, what is stuck and when to restock. It cannot read AWD, and changes nothing at Amazon unless you ask.\n\nSome things you can ask:\n\n- Which products will run out before the stock on its way is received?\n- Why did my storage charge go up last month?\n- How many units of last week's delivery were received short?\n\nTo see what each product earns after fees, also install cx-amazon-finance-playbook.\n\n## What it uses\n\n- **Amazon SP-API:** your Amazon selling account, connected on the Amazon SP-API plugin. cx reads your inventory, reports and shipments there.\n",
  "README.zh-CN.md": "cx 读取你放在亚马逊仓库里的库存：每个商品在哪、买家现在能买多少、压着要花多少钱、哪些卡住了，以及什么时候该补货、补多少。AWD 里的库存读不到。除非你开口，cx 不会在亚马逊做任何改动。\n\n你可以这样问：\n\n- 哪些商品撑不到在途的货入仓就会断货？\n- 上个月的仓储费为什么涨了？\n- 上周送到的那批货少收了多少件？\n\n如果想知道每个商品扣掉费用后赚了多少，再装上 cx-amazon-finance-playbook。\n\n## 用到的数据\n\n- **Amazon SP-API**：你的亚马逊卖家账户，在 Amazon SP-API 插件里连接。cx 在这里读取库存、报告和货件。\n",
} as const;
