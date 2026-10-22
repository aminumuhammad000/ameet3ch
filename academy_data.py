"""
Ameetech Business & Economics Academy | Comprehensive Curriculum & Content Database
Contains categories, courses, lessons, quizzes, formulas, and study guides.
"""

CATEGORIES = [
    {
        "id": "economics-fundamentals",
        "name": "Economics Fundamentals",
        "slug": "economics-fundamentals",
        "icon": "fa-chart-line",
        "color": "#6C2BD9",
        "summary": "Master core economic principles: scarcity, opportunity cost, supply and demand, elasticity, market equilibrium, and macroeconomic policies.",
        "level": "Beginner to Advanced",
        "order": 1
    },
    {
        "id": "accounting-financial-literacy",
        "name": "Accounting and Financial Literacy",
        "slug": "accounting-financial-literacy",
        "icon": "fa-calculator",
        "color": "#10B981",
        "summary": "Understand revenue vs profit, margins, break-even mechanics, working capital, cash flow, financial statements, and taxation.",
        "level": "Beginner to Intermediate",
        "order": 2
    },
    {
        "id": "business-models-strategy",
        "name": "Business Models and Strategy",
        "slug": "business-models-strategy",
        "icon": "fa-chess",
        "color": "#3B82F6",
        "summary": "Architect durable competitive advantages, analyze economies of scale, network effects, switching costs, and market positioning.",
        "level": "Intermediate to Advanced",
        "order": 3
    },
    {
        "id": "marketing-consumer-behaviour",
        "name": "Marketing and Consumer Behaviour",
        "slug": "marketing-consumer-behaviour",
        "icon": "fa-bullseye",
        "color": "#F59E0B",
        "summary": "Measure Customer Acquisition Cost (CAC), Lifetime Value (LTV), retention cohorts, conversion funnels, and pricing psychology.",
        "level": "Beginner to Intermediate",
        "order": 4
    },
    {
        "id": "entrepreneurship-startups",
        "name": "Entrepreneurship and Startups",
        "slug": "entrepreneurship-startups",
        "icon": "fa-rocket",
        "color": "#EC4899",
        "summary": "Validate ideas, construct Minimum Viable Products (MVPs), reach Product-Market Fit, and navigate bootstrapping vs venture capital in Africa.",
        "level": "Beginner to Advanced",
        "order": 5
    },
    {
        "id": "finance-investment-risk",
        "name": "Finance, Investment and Risk",
        "slug": "finance-investment-risk",
        "icon": "fa-coins",
        "color": "#8B5CF6",
        "summary": "Explore time value of money, compound interest, ROI, liquidity ratios, capital allocation, and risk management frameworks.",
        "level": "Intermediate to Advanced",
        "order": 6
    },
    {
        "id": "operations-business-growth",
        "name": "Operations and Business Growth",
        "slug": "operations-business-growth",
        "icon": "fa-gears",
        "color": "#14B8A6",
        "summary": "Streamline procurement, inventory control (EOQ & Safety Stock), capacity planning, process automation, and operational efficiency.",
        "level": "Intermediate",
        "order": 7
    },
    {
        "id": "digital-business-technology-economics",
        "name": "Digital Business and Technology Economics",
        "slug": "digital-business-technology-economics",
        "icon": "fa-laptop-code",
        "color": "#6366F1",
        "summary": "Unpack SaaS metrics (MRR, ARR, Churn, NRR), two-sided marketplace economics, platform network effects, and AI product cost structures.",
        "level": "Intermediate to Advanced",
        "order": 8
    }
]

# Curriculum Lessons
LESSONS = [
    # ── 1. Economics Fundamentals ──
    {
        "slug": "scarcity-and-opportunity-cost",
        "category_id": "economics-fundamentals",
        "title": "Scarcity, Trade-offs, and Opportunity Cost in Business Decisions",
        "summary": "Every commercial choice requires choosing one alternative over another. Learn how scarcity governs allocation and how calculating true opportunity cost protects capital.",
        "level": "Beginner",
        "reading_time": "9 min",
        "order": 1,
        "objectives": [
            "Define scarcity and recognize its role as the fundamental economic problem.",
            "Distinguish between accounting cost (cash outflows) and economic opportunity cost.",
            "Apply the Production Possibilities Frontier (PPF) concept to business resource allocation.",
            "Calculate trade-offs in operational decision-making with practical African market scenarios."
        ],
        "content_sections": [
            {
                "heading": "1. What is Scarcity and Why Does it Govern Business?",
                "body": """
Scarcity is the condition where human desires and operational demands exceed the finite productive resources (time, capital, skilled labor, and raw materials) available to fulfill them. Because resources are never unlimited, every enterprise must continuously solve the fundamental economic questions: **what to produce**, **how to produce**, and **for whom to allocate capital**.

In a commercial environment, ignoring scarcity leads to overexpansion, fragmented focus, and liquidity crises. Recognizing scarcity forces leadership to establish strict prioritization criteria based on expected return and strategic alignment.
"""
            },
            {
                "heading": "2. Opportunity Cost Explained for Beginners",
                "body": """
**Opportunity cost** is the value of the next best alternative that is forgone when a choice is made. It is not the sum of all other alternatives, but specifically the single highest-valued option surrendered.

Unlike accounting expenses recorded in ledgers, opportunity cost is an **economic cost**. When a business owner commits ₦10,000,000 to purchase excess raw inventory that sits in a warehouse for 12 months, the cost is not merely the purchase price and storage fees. The true economic cost includes the lost return that capital could have generated had it been invested in a high-yielding treasury bill, dedicated marketing campaign, or software automation system.
"""
            },
            {
                "heading": "3. The Formula for Opportunity Cost",
                "body": """
Opportunity cost can be mathematically expressed when comparing mutual options:

$$\\text{Opportunity Cost} = \\text{Return on Best Forgone Option (FO)} - \\text{Return on Chosen Option (CO)}$$

Where:
* **FO (Forgone Option):** Expected net cash benefit or utility from the top unselected alternative.
* **CO (Chosen Option):** Expected net cash benefit or utility realized from the chosen alternative.

If $\\text{Opportunity Cost} > 0$, the decision maker forfeited a superior commercial alternative.
"""
            },
            {
                "heading": "4. Step-by-Step Worked Business Example (Nigerian Logistics Context)",
                "body": """
**Scenario:** A delivery business in Kano has ₦15,000,000 in surplus working capital. The management must decide between two mutually exclusive expansions:

* **Option A (Chosen):** Purchase 3 new delivery vans. Projected annual net return after maintenance and fuel = ₦4,200,000 (28% annual return).
* **Option B (Next Best Alternative):** Invest in automated sorting software and dispatch route optimization that reduces fleet idle time across all existing 20 vehicles. Projected annual operating cost savings and revenue lift = ₦5,700,000 (38% annual return).

**Step 1: Calculate the returns:**
$$\\text{Return (A)} = ₦4,200,000$$
$$\\text{Return (B)} = ₦5,700,000$$

**Step 2: Calculate the Opportunity Cost of choosing Option A:**
$$\\text{Opportunity Cost} = ₦5,700,000 - ₦4,200,000 = ₦1,500,000 \\text{ per annum}$$

By selecting physical vans over workflow optimization software, the company effectively leaves ₦1,500,000 of annual economic value on the table.
"""
            },
            {
                "heading": "5. Common Misconceptions",
                "body": """
* **Misconception 1: Opportunity cost only applies to money.** In reality, **management time** is frequently a company's scarcest resource. Six weeks spent by senior software engineers building a custom CRM represents the lost opportunity of improving the company's core client-facing product.
* **Misconception 2: Sunk costs are part of opportunity cost.** Sunk costs (money already spent and unrecoverable) must never influence forward-looking decisions. Opportunity cost concerns only prospective, forward choices.
"""
            },
            {
                "heading": "6. Strategic Business Applications",
                "body": """
1. **Capital Budgeting:** Compare internal project hurdle rates against safe risk-free sovereign instruments (such as Nigerian Treasury Bills yielding 16-20%).
2. **Make vs. Buy Decisions:** Evaluate whether hiring in-house developers or using cloud APIs (such as payment gateways like Paystack/Moniepoint) frees technical talent for core value creation.
3. **Inventory Management:** Carrying zero-margin inventory carries holding cost and capital lockup that starves faster-turning product lines.
"""
            }
        ],
        "takeaways": [
            "Scarcity makes every business decision an exercise in prioritization.",
            "Opportunity cost reflects the highest-valued forgone choice, not merely accounting expenditure.",
            "Managers must evaluate capital, time, and talent against their highest-yielding prospective use.",
            "Never allow past sunk costs to distort opportunity cost calculations."
        ],
        "quiz": [
            {
                "question": "An entrepreneur invests ₦5,000,000 in inventory generating ₦800,000 profit. A commercial bank deposit would have paid 18% guaranteed return (₦900,000). What is the opportunity cost of investing in inventory?",
                "options": [
                    "₦5,000,000",
                    "₦100,000 in forgone return",
                    "₦800,000",
                    "Zero, because the business made a profit"
                ],
                "answer_index": 1,
                "explanation": "The opportunity cost is the difference between the return on the best forgone alternative (₦900,000) and the chosen option (₦800,000), resulting in an economic shortfall of ₦100,000."
            },
            {
                "question": "Which resource in an early-stage company typically has the highest, most overlooked opportunity cost?",
                "options": [
                    "Office furniture",
                    "Founders' and senior engineers' focus and time",
                    "Social media follower count",
                    "Utility bills"
                ],
                "answer_index": 1,
                "explanation": "Founder and engineering hours are finite and non-renewable; deploying them on non-essential tasks creates massive opportunity losses compared to customer discovery and product iteration."
            }
        ],
        "related_slugs": ["supply-demand-market-equilibrium", "break-even-analysis-contribution-margin"]
    },

    {
        "slug": "supply-demand-market-equilibrium",
        "category_id": "economics-fundamentals",
        "title": "Supply, Demand, and Price Elasticity in Real Markets",
        "summary": "How buyer willingness to pay interacts with producer cost to determine equilibrium pricing, market clearing, and revenue elasticity.",
        "level": "Beginner to Intermediate",
        "reading_time": "11 min",
        "order": 2,
        "objectives": [
            "Explain the Law of Demand and the Law of Supply.",
            "Identify market clearing equilibrium and diagnose shortages versus surpluses.",
            "Calculate Price Elasticity of Demand (PED) using the midpoint formula.",
            "Use elasticity to predict whether price increases will raise or lower total revenue."
        ],
        "content_sections": [
            {
                "heading": "1. Mechanics of Supply, Demand, and Equilibrium",
                "body": """
In competitive markets, price serves as an informational signal coordinating consumption and production:

* **Law of Demand:** Ceteris paribus (all else held equal), as the unit price of a good rises, consumer quantity demanded falls, and vice versa.
* **Law of Supply:** As market price rises, suppliers are willing to produce and sell more units to capture higher marginal profits.
* **Market Equilibrium:** The price point ($P^*$) where quantity demanded equals quantity supplied ($Q_d = Q_s$). At this price, the market clears without excess inventory (surplus) or unfulfilled buyer queues (shortage).
"""
            },
            {
                "heading": "2. Price Elasticity of Demand (PED)",
                "body": """
**Price Elasticity of Demand (PED)** measures the responsiveness of customer demand to changes in price:

$$\\text{PED} = \\frac{\\% \\Delta Q_d}{\\% \\Delta P} = \\frac{(Q_2 - Q_1) / \\left(\\frac{Q_1 + Q_2}{2}\\right)}{(P_2 - P_1) / \\left(\\frac{P_1 + P_2}{2}\\right)}$$

### Interpreting Elasticity Values:
1. **$|\\text{PED}| > 1$ (Elastic Demand):** Consumers are highly price-sensitive. A 10% price hike causes sales volume to drop by more than 10%. **Raising prices will decrease Total Revenue.**
2. **$|\\text{PED}| < 1$ (Inelastic Demand):** Consumers have few substitutes or the product is an essential necessity. A 10% price hike causes volume to fall by less than 10%. **Raising prices will increase Total Revenue.**
3. **$|\\text{PED}| = 1$ (Unitary Elasticity):** Percentage changes in price and volume are identical; Total Revenue remains constant.
"""
            },
            {
                "heading": "3. African Market Case Study: Food Staples vs. Luxury Services",
                "body": """
Consider consumer behavior in urban Nigeria:

* **Inelastic Good:** Petroleum fuel or fundamental staple grains (rice/garri). Because substitutes are limited and everyday survival relies on energy/food, when prices rose sharply post-subsidy removal in 2023, consumption dropped only modestly ($|\\text{PED}| \\approx 0.35$). Total merchant revenue rose despite lower physical volume.
* **Elastic Good:** Fine dining restaurants or designer shoes. When inflation compressed consumer disposable income, discretionary spending on fine dining dropped drastically ($|\\text{PED}| \\approx 2.4$), prompting restaurateurs to offer discounted lunch bowls to preserve customer volume.
"""
            },
            {
                "heading": "4. Step-by-Step Elasticity Calculation",
                "body": """
**Problem:** An e-commerce platform in Lagos sells a wireless phone accessory.
* Original: Price $P_1 = ₦10,000$, Units sold $Q_1 = 1,200$ monthly. Total Revenue = $1,200 \\times ₦10,000 = ₦12,000,000$.
* New: Price increases to $P_2 = ₦12,000$, Units sold fall to $Q_2 = 900$ monthly. Total Revenue = $900 \\times ₦12,000 = ₦10,800,000$.

**Step 1: Calculate percentage changes using the midpoint formula:**
$$\\% \\Delta Q = \\frac{900 - 1200}{(900 + 1200) / 2} = \\frac{-300}{1050} = -28.57\\%$$
$$\\% \\Delta P = \\frac{12000 - 10000}{(12000 + 10000) / 2} = \\frac{2000}{11000} = +18.18\\%$$

**Step 2: Calculate PED:**
$$\\text{PED} = \\frac{-28.57\\%}{+18.18\\%} = -1.57$$

**Interpretation:**
Because $|\\text{PED}| = 1.57 > 1$, the product is **price-elastic**. The price increase caused volume to drop significantly, cutting monthly revenue from ₦12.0M to ₦10.8M. The company should reconsider this price hike or differentiate the product to reduce price sensitivity.
"""
            }
        ],
        "takeaways": [
            "Market equilibrium is where quantity demanded equals quantity supplied.",
            "Elastic products ($|\\text{PED}| > 1$) lose total revenue when prices rise.",
            "Inelastic products ($|\\text{PED}| < 1$) gain total revenue when prices rise.",
            "Pricing decisions must evaluate customer substitutes, switching costs, and necessity."
        ],
        "quiz": [
            {
                "question": "If a software firm increases subscription rates by 15% and user cancellations cause subscriber count to fall by only 3%, what is the demand elasticity?",
                "options": [
                    "Elastic (|PED| = 5.0)",
                    "Inelastic (|PED| = 0.20)",
                    "Unitary (|PED| = 1.0)",
                    "Perfectly elastic"
                ],
                "answer_index": 1,
                "explanation": "|PED| = 3% / 15% = 0.20. Since it is below 1, demand is inelastic, and total recurring revenue will expand following the price adjustment."
            }
        ],
        "related_slugs": ["scarcity-and-opportunity-cost", "pricing-strategies-customer-psychology"]
    },

    # ── 2. Accounting and Financial Literacy ──
    {
        "slug": "revenue-gross-operating-net-profit",
        "category_id": "accounting-financial-literacy",
        "title": "Demystifying Profit: Revenue, Gross, Operating, and Net Profit Margins",
        "summary": "Never confuse top-line turnover with actual wealth creation. Master the four tiers of profit, calculate operating margins, and distinguish markup from margin.",
        "level": "Beginner to Intermediate",
        "reading_time": "12 min",
        "order": 1,
        "objectives": [
            "Distinguish Revenue from Gross, Operating, and Net Profit.",
            "Compute Cost of Goods Sold (COGS) and Operating Expenses (OPEX).",
            "Calculate profit margins versus markups without mathematical error.",
            "Analyze a multi-step Income Statement with practical African business metrics."
        ],
        "content_sections": [
            {
                "heading": "1. The Four Tiers of the Income Statement",
                "body": """
A commercial organization records earnings across four distinct tiers:

1. **Gross Revenue (Top Line):** Total invoice value or cash received from goods sold and services delivered before any deductions.
2. **Gross Profit:** Revenue minus direct Cost of Goods Sold (COGS). Measures production efficiency and product unit margins.
3. **Operating Profit (EBIT):** Gross Profit minus operational expenditures (OPEX) such as administrative salaries, rent, software, and marketing. Measures core business profitability.
4. **Net Profit (The Bottom Line):** Operating Profit minus finance expenses (interest on debt), foreign exchange losses, and corporate income taxes. Represents the actual profit belonging to equity owners.
"""
            },
            {
                "heading": "2. The Mathematical Formulas",
                "body": """
$$\\text{Gross Profit} = \\text{Revenue} - \\text{COGS}$$
$$\\text{Gross Margin} = \\left( \\frac{\\text{Gross Profit}}{\\text{Revenue}} \\right) \\times 100\\%$$

$$\\text{Operating Profit (EBIT)} = \\text{Gross Profit} - \\text{Operating Expenses (OPEX)}$$
$$\\text{Operating Margin} = \\left( \\frac{\\text{Operating Profit}}{\\text{Revenue}} \\right) \\times 100\\%$$

$$\\text{Net Profit} = \\text{Operating Profit} - \\text{Interest} - \\text{Taxes} - \\text{Extraordinary Losses}$$
$$\\text{Net Margin} = \\left( \\frac{\\text{Net Profit}}{\\text{Revenue}} \\right) \\times 100\\%$$
"""
            },
            {
                "heading": "3. Markup vs. Margin: The Critical Distinction",
                "body": """
Confusing **Markup** with **Margin** is one of the most fatal financial blunders made by growing SME operators:

* **Markup:** The percentage added directly to the Cost of Goods Sold to arrive at the selling price:
$$\\text{Markup} = \\frac{\\text{Selling Price} - \\text{Cost}}{\\text{Cost}} \\times 100\\%$$

* **Margin:** The percentage of the final selling price that remains as profit:
$$\\text{Margin} = \\frac{\\text{Selling Price} - \\text{Cost}}{\\text{Selling Price}} \\times 100\\%$$

**Worked Comparison:**
If you buy an item for ₦6,000 and sell it for ₦10,000:
* Profit = ₦4,000
* $\\text{Markup} = \\frac{4,000}{6,000} = 66.67\\%$
* $\\text{Margin} = \\frac{4,000}{10,000} = 40.00\\%$

*Warning:* A 50% markup is NOT a 50% margin. If your retail cost is ₦1,000 with a 50% markup, you sell at ₦1,500. Your margin is $\\frac{500}{1,500} = 33.3\\%$. If overheads are 40% of sales, you are losing money on every unit!
"""
            },
            {
                "heading": "4. Complete Worked Multi-Step Financial Statement",
                "body": """
**Case Study: Apex Manufacturing Ltd (Kaduna & Abuja)**

| Income Statement Line Item | Amount (₦) | % of Revenue |
| :--- | :--- | :--- |
| **Gross Revenue** | **₦50,000,000** | **100.0%** |
| Less: Direct Raw Materials & Labor (COGS) | (₦28,000,000) | 56.0% |
| **Gross Profit** | **₦22,000,000** | **44.0%** |
| Less: Sales & Marketing | (₦5,000,000) | 10.0% |
| Less: Office Rent, Generator Fuel & Utilities | (₦4,200,000) | 8.4% |
| Less: Administrative & Tech Salaries | (₦6,000,000) | 12.0% |
| **Operating Profit (EBIT)** | **₦6,800,000** | **13.6%** |
| Less: Bank Loan Interest (18% on overdraft) | (₦1,200,000) | 2.4% |
| Profit Before Tax (PBT) | ₦5,600,000 | 11.2% |
| Less: Company Income Tax (CIT at 30%) | (₦1,680,000) | 3.36% |
| **Net Profit After Tax (PAT)** | **₦3,920,000** | **7.84%** |

*Takeaway:* Despite generating ₦50M in sales, the business retains ₦3.92M (7.84%) in net distributable cash.
"""
            }
        ],
        "takeaways": [
            "Revenue is vanity, profit is sanity, cash flow is reality.",
            "Gross margin measures manufacturing and fulfillment efficiency.",
            "Operating margin measures operational leverage and overhead control.",
            "Markup is calculated on cost; margin is calculated on selling price."
        ],
        "quiz": [
            {
                "question": "A merchant buys a gadget for ₦15,000 and sells it for ₦20,000. What is the merchant's gross profit margin?",
                "options": [
                    "33.3%",
                    "25.0%",
                    "20.0%",
                    "50.0%"
                ],
                "answer_index": 1,
                "explanation": "Gross profit = ₦20,000 - ₦15,000 = ₦5,000. Gross Margin = (₦5,000 / ₦20,000) * 100% = 25.0%. (The markup on cost is 33.3%)."
            }
        ],
        "related_slugs": ["break-even-analysis-contribution-margin", "cash-flow-working-capital-liquidity"]
    },

    {
        "slug": "break-even-analysis-contribution-margin",
        "category_id": "accounting-financial-literacy",
        "title": "Break-Even Analysis, Fixed vs Variable Costs, and Contribution Margin",
        "summary": "Determine the exact sales volume required to cover fixed overheads. Learn how contribution margin powers profitable pricing and scenario planning.",
        "level": "Intermediate",
        "reading_time": "10 min",
        "order": 2,
        "objectives": [
            "Differentiate between Fixed Costs and Variable Costs.",
            "Compute Unit Contribution Margin and Contribution Margin Ratio.",
            "Calculate Break-Even Point in physical units and currency value.",
            "Perform 'Margin of Safety' calculations to assess commercial risk."
        ],
        "content_sections": [
            {
                "heading": "1. Cost Structures: Fixed vs Variable",
                "body": """
All business expenditures divide into two operational categories:

* **Fixed Costs (FC):** Expenses that do not fluctuate with production volume in the short term. Examples: Office rent, core administrative salaries, property insurance, software subscription licenses, and equipment depreciation.
* **Variable Costs (VC):** Expenses that increase directly in proportion to each unit produced and delivered. Examples: Raw materials, packaging boxes, delivery courier fees, payment gateway transaction fees (e.g. 1.5% Paystack charge), and sales commission.
"""
            },
            {
                "heading": "2. Contribution Margin Mechanics",
                "body": """
**Unit Contribution Margin (CM)** is the portion of selling price remaining after covering variable costs that goes directly toward paying down fixed overheads:

$$\\text{Unit CM} = \\text{Selling Price per Unit (P)} - \\text{Variable Cost per Unit (VC)}$$

$$\\text{Contribution Margin Ratio (CMR)} = \\frac{\\text{Unit CM}}{\\text{Selling Price (P)}} = \\frac{\\text{Total Contribution Margin}}{\\text{Total Revenue}}$$
"""
            },
            {
                "heading": "3. The Break-Even Formula",
                "body": """
The **Break-Even Point (BEP)** is the operational milestone where Total Revenue equals Total Costs (Profit = 0):

$$\\text{Break-Even Units (Q)} = \\frac{\\text{Total Fixed Costs}}{\\text{Selling Price} - \\text{Variable Cost per Unit}} = \\frac{\\text{Fixed Costs}}{\\text{Unit CM}}$$

$$\\text{Break-Even Revenue (₦)} = \\frac{\\text{Total Fixed Costs}}{\\text{Contribution Margin Ratio (CMR)}}$$
"""
            },
            {
                "heading": "4. Practical Worked Example: Commercial Bakery in Ibadan",
                "body": """
**Data:**
* Selling price per loaf of specialty bread ($P$) = ₦1,200
* Ingredients & packaging per loaf ($VC$) = ₦700
* Monthly bakery rent, manager salary, and generator fuel ($FC$) = ₦1,500,000

**Step 1: Calculate Unit Contribution Margin:**
$$\\text{Unit CM} = ₦1,200 - ₦700 = ₦500$$
$$\\text{CMR} = \\frac{₦500}{₦1,200} = 41.67\\%$$

**Step 2: Calculate Break-Even Units:**
$$\\text{Break-Even Units} = \\frac{₦1,500,000}{₦500} = 3,000 \\text{ loaves monthly}$$

**Step 3: Calculate Break-Even Revenue:**
$$\\text{Break-Even Revenue} = 3,000 \\times ₦1,200 = ₦3,600,000$$

**Target Profit Planning:**
If the bakery desires a monthly net profit of ₦1,000,000:
$$\\text{Target Volume} = \\frac{\\text{Fixed Costs} + \\text{Target Profit}}{\\text{Unit CM}} = \\frac{₦1,500,000 + ₦1,000,000}{₦500} = 5,000 \\text{ loaves}$$
"""
            }
        ],
        "takeaways": [
            "Fixed costs remain constant regardless of output; variable costs scale with unit volume.",
            "Contribution margin pays down fixed costs first; after break-even, it flows straight into operating profit.",
            "High fixed-cost structures create high operational leverage (huge profits in boom times, severe danger in downturns)."
        ],
        "quiz": [
            {
                "question": "A digital consultancy has fixed costs of ₦2,000,000 per month. They bill clients ₦250,000 per audit and incur ₦50,000 in direct cloud and data fees per audit. How many audits must they complete to break even?",
                "options": [
                    "8 audits",
                    "10 audits",
                    "15 audits",
                    "20 audits"
                ],
                "answer_index": 1,
                "explanation": "Unit CM = ₦250,000 - ₦50,000 = ₦200,000. Break-Even Units = ₦2,000,000 / ₦200,000 = 10 audits."
            }
        ],
        "related_slugs": ["revenue-gross-operating-net-profit", "cash-flow-working-capital-liquidity"]
    },

    {
        "slug": "cash-flow-working-capital-liquidity",
        "category_id": "accounting-financial-literacy",
        "title": "Cash Flow vs Profit: Working Capital and Liquidity Survival",
        "summary": "Why profitable businesses fail from cash insolvency. Master the cash conversion cycle, accounts receivable aging, and working capital buffers.",
        "level": "Intermediate",
        "reading_time": "11 min",
        "order": 3,
        "objectives": [
            "Distinguish between accounting profitability and liquid cash flow.",
            "Understand the three sections of the Cash Flow Statement.",
            "Calculate Net Working Capital and the Cash Conversion Cycle (CCC).",
            "Implement defensive strategies against debtor defaults and inflation erosion."
        ],
        "content_sections": [
            {
                "heading": "1. Why 'Profitable' Companies Go Bankrupt",
                "body": """
Under accrual accounting, revenue is recognized when an invoice is issued upon delivery of goods, not when cash hits the bank. A business can report ₦20,000,000 in monthly net profit on paper while having zero cash in its commercial account because corporate clients pay on 90-day credit terms.

If supplier invoices, generator fuel, and staff salaries must be paid on day 30, the business collapses from **cash insolvency** despite a healthy income statement.
"""
            },
            {
                "heading": "2. Net Working Capital Formula",
                "body": """
$$\\text{Net Working Capital (NWC)} = \\text{Current Assets} - \\text{Current Liabilities}$$

* **Current Assets:** Cash, inventory, and accounts receivable (money owed by customers within 12 months).
* **Current Liabilities:** Accounts payable (money owed to vendors), short-term bank overdrafts, and accrued payroll.

If $\\text{NWC} < 0$, the business is illiquid and risks defaulting on immediate obligations.
"""
            },
            {
                "heading": "3. The Cash Conversion Cycle (CCC)",
                "body": """
$$\\text{CCC} = \\text{DIO} + \\text{DSO} - \\text{DPO}$$

Where:
* **DIO (Days Inventory Outstanding):** Average days stock sits before sale.
* **DSO (Days Sales Outstanding):** Average days taken to collect cash from customers.
* **DPO (Days Payables Outstanding):** Average days taken to pay vendors.

The shorter the CCC, the less external working capital financing the business requires. If CCC is negative (as achieved by Amazon or retail supermarkets who receive cash upfront from shoppers but pay suppliers in 60 days), customer cash finances company expansion.
"""
            }
        ],
        "takeaways": [
            "Cash pays salaries and debts, not booked paper profits.",
            "Track Operating Cash Flow separately from net accounting profit.",
            "Shorten Days Sales Outstanding (DSO) through upfront payment incentives.",
            "Always maintain at least 3 to 6 months of operational runway in liquid funds."
        ],
        "quiz": [
            {
                "question": "If a distributor takes 40 days to sell inventory (DIO), 45 days to collect customer payment (DSO), and pays suppliers in 30 days (DPO), what is the Cash Conversion Cycle?",
                "options": [
                    "115 days",
                    "55 days",
                    "25 days",
                    "85 days"
                ],
                "answer_index": 1,
                "explanation": "CCC = 40 (DIO) + 45 (DSO) - 30 (DPO) = 55 days. The business must finance 55 days of operations out of working capital."
            }
        ],
        "related_slugs": ["revenue-gross-operating-net-profit", "break-even-analysis-contribution-margin"]
    },

    # ── 3. Business Models and Strategy ──
    {
        "slug": "competitive-advantage-economic-moats",
        "category_id": "business-models-strategy",
        "title": "Competitive Advantage and Economic Moats: Defending Market Share",
        "summary": "How exceptional companies protect high profit margins from competitive imitation. Analyze network effects, switching costs, scale, and intangible assets.",
        "level": "Intermediate to Advanced",
        "reading_time": "13 min",
        "order": 1,
        "objectives": [
            "Define economic moats and sustainable competitive advantage.",
            "Classify the four primary types of economic moats (Network Effects, Switching Costs, Cost Advantages, Intangible Assets).",
            "Evaluate Porter's Five Forces in African emerging markets.",
            "Formulate defensible strategy against commoditization."
        ],
        "content_sections": [
            {
                "heading": "1. What is an Economic Moat?",
                "body": """
Coined by Warren Buffett, an **economic moat** is a structural advantage that protects a company's high Return on Invested Capital (ROIC) from competitive erosion. In standard microeconomic theory, supernormal profits attract competitors who introduce substitute products, drive down prices, and reduce margins to the cost of capital. A moat prevents this regression.
"""
            },
            {
                "heading": "2. The Four Pillars of Structural Moats",
                "body": """
1. **Network Effects:** The product becomes exponentially more valuable to existing users as new users join.
   * *Example:* WhatsApp in Nigeria or Moniepoint's POS agent distribution network.
2. **High Switching Costs:** The monetary, technical, operational, or psychological cost of leaving for a competitor exceeds the benefit.
   * *Example:* Enterprise ERP software (SAP, Oracle) or banking payment rails embedded in an e-commerce checkout.
3. **Cost Advantages (Scale & Process):** Ability to produce at lower unit cost through massive volume or proprietary logistics.
   * *Example:* Dangote Cement's vertical integration with limestone quarries and dedicated logistics fleet.
4. **Intangible Assets:** Brands that command price premiums, patents, government regulatory licenses, or zoning permits.
   * *Example:* Commercial banking licenses issued by the Central Bank of Nigeria (CBN).
"""
            }
        ],
        "takeaways": [
            "Without an economic moat, competitors will eventually compete away above-average margins.",
            "Network effects create 'winner-takes-most' market dynamics.",
            "High customer switching costs yield pricing power and predictable recurring cash flows."
        ],
        "quiz": [
            {
                "question": "Which of the following represents a switching cost moat?",
                "options": [
                    "A brand offering a temporary 20% discount",
                    "A business running TV commercials",
                    "An ERP software where migrating customer historical data and retraining 500 staff takes 9 months",
                    "A product that is cheaper than all competitors"
                ],
                "answer_index": 2,
                "explanation": "High migration friction, data integration, and employee retraining costs create structural switching barriers that prevent client defection."
            }
        ],
        "related_slugs": ["scarcity-and-opportunity-cost", "saas-metrics-mrr-arr-churn"]
    },

    # ── 4. Marketing and Consumer Behaviour ──
    {
        "slug": "cac-ltv-unit-economics",
        "category_id": "marketing-consumer-behaviour",
        "title": "Mastering CAC and LTV: The Math of Sustainable Customer Acquisition",
        "summary": "Customer Acquisition Cost (CAC) and Lifetime Value (LTV) govern company survival. Discover how to compute the LTV:CAC ratio and calculate payback periods.",
        "level": "Intermediate",
        "reading_time": "12 min",
        "order": 1,
        "objectives": [
            "Calculate fully-loaded Customer Acquisition Cost (CAC).",
            "Calculate Customer Lifetime Value (LTV) using retention and gross margins.",
            "Assess business viability with the LTV:CAC ratio benchmark (3:1).",
            "Compute the CAC Payback Period to manage marketing working capital."
        ],
        "content_sections": [
            {
                "heading": "1. What is Customer Acquisition Cost (CAC)?",
                "body": """
**Customer Acquisition Cost (CAC)** represents the total cost required to acquire one net new paying customer over a given timeframe:

$$\\text{CAC} = \\frac{\\text{Total Sales \\& Marketing Expenditure (Ad spend, agency fees, sales salaries, software)}}{\\text{Number of Net New Customers Acquired}}$$

*Crucial Rule:* CAC must be **fully loaded**. Do not count ad spend alone; include sales rep commissions, marketing team payroll, CRM tools, and promotional giveaways.
"""
            },
            {
                "heading": "2. Customer Lifetime Value (LTV) Formula",
                "body": """
**Customer Lifetime Value (LTV)** measures the total gross profit contribution an enterprise expects to earn from a customer relationship over its entire duration:

$$\\text{LTV} = \\frac{\\text{Average Revenue Per User (ARPU)} \\times \\text{Gross Margin (\\%)}}{\\text{Customer Churn Rate (\\%)}}$$

Alternatively:
$$\\text{LTV} = \\text{Average Purchase Value} \\times \\text{Annual Purchase Frequency} \\times \\text{Average Lifespan (Years)} \\times \\text{Gross Margin (\\%)}$$
"""
            },
            {
                "heading": "3. The Golden Ratios: LTV:CAC and Payback Period",
                "body": """
* **$\\text{LTV:CAC} < 1:1$:** Destructive business model. Spending more to acquire customers than they ever return.
* **$\\text{LTV:CAC} = 3:1$:** The healthy, gold-standard benchmark for sustainable growth.
* **$\\text{LTV:CAC} > 5:1$:** Under-investing in marketing; competitors can outspend you to capture market share.

**CAC Payback Period:**
$$\\text{Payback Months} = \\frac{\\text{CAC}}{\\text{Monthly Gross Profit Contribution Per Customer}}$$
*Target:* Healthy companies recover CAC within **6 to 12 months** to avoid burning through working capital.
"""
            }
        ],
        "takeaways": [
            "Always compute fully-loaded CAC including team salaries and tools.",
            "LTV must be based on Gross Profit contribution, never top-line gross revenue.",
            "Maintain an LTV:CAC ratio near 3:1 with payback under 12 months."
        ],
        "quiz": [
            {
                "question": "A fintech spends ₦10,000,000 on ads and sales salaries in a month, acquiring 2,000 active users. What is the fully loaded CAC?",
                "options": [
                    "₦5,000",
                    "₦2,000",
                    "₦10,000",
                    "₦500"
                ],
                "answer_index": 0,
                "explanation": "CAC = Total Marketing & Sales Costs / Total New Customers = ₦10,000,000 / 2,000 = ₦5,000 per user."
            }
        ],
        "related_slugs": ["saas-metrics-mrr-arr-churn", "break-even-analysis-contribution-margin"]
    },

    # ── 5. Entrepreneurship and Startups ──
    {
        "slug": "mvp-idea-validation-product-market-fit",
        "category_id": "entrepreneurship-startups",
        "title": "MVP, Idea Validation, and Product-Market Fit in Frontier Markets",
        "summary": "How to validate business hypotheses before burning capital. Build true Minimum Viable Products and identify genuine retention-driven product-market fit.",
        "level": "Beginner to Intermediate",
        "reading_time": "11 min",
        "order": 1,
        "objectives": [
            "Define the Minimum Viable Product (MVP) according to Lean Startup methodology.",
            "Distinguish genuine consumer demand signals from polite feedback.",
            "Recognize qualitative and quantitative signs of Product-Market Fit (PMF).",
            "Adapt lean validation strategies to African infrastructure and payment habits."
        ],
        "content_sections": [
            {
                "heading": "1. What is an MVP (and What is it Not)?",
                "body": """
An **MVP (Minimum Viable Product)** is the simplest version of a product that allows a team to collect the maximum amount of validated learning about customers with the least effort and capital.

It is **not** a broken or low-quality product; rather, it is a focused solution that addresses the single core pain point of an early adopter.
"""
            },
            {
                "heading": "2. The 'Smoke Test' and Pre-Selling",
                "body": """
Never write code or lease warehouses before validating customer willingness to pay. In frontier markets, customers frequently express verbal enthusiasm for an idea but refuse to part with cash when launched.

**True validation signals:**
* Pre-orders with non-refundable deposits (via bank transfer, card, or escrow).
* Signed letters of intent (LOI) from corporate B2B clients.
* Waitlists where users provide their WhatsApp number or commit to a pilot trial.
"""
            }
        ],
        "takeaways": [
            "An MVP is a learning tool to test assumptions, not an incomplete final product.",
            "Willingness to pay cash is the only undisputed validation signal.",
            "Product-Market Fit is characterized by retention cohorts flattening above zero."
        ],
        "quiz": [
            {
                "question": "Which indicator provides the strongest evidence that a startup has validated its business hypothesis?",
                "options": [
                    "1,000 followers on social media",
                    "50 prospective clients pre-paying a 20% deposit before product delivery",
                    "Praise from family and university colleagues",
                    "A certificate of business registration from the Corporate Affairs Commission (CAC)"
                ],
                "answer_index": 1,
                "explanation": "Cash commitment (pre-orders or non-refundable deposits) is the ultimate market validation of customer willingness to pay."
            }
        ],
        "related_slugs": ["cac-ltv-unit-economics", "competitive-advantage-economic-moats"]
    },

    # ── 6. Finance, Investment and Risk ──
    {
        "slug": "time-value-of-money-compound-interest",
        "category_id": "finance-investment-risk",
        "title": "Time Value of Money, Discounting, and Compound Interest",
        "summary": "Why a naira today is worth more than a naira tomorrow. Calculate Present Value, Future Value, Net Present Value (NPV), and internal hurdle rates.",
        "level": "Intermediate",
        "reading_time": "12 min",
        "order": 1,
        "objectives": [
            "Understand the core principle of the Time Value of Money (TVM).",
            "Calculate Future Value (FV) with compound interest.",
            "Discount future commercial cash flows to calculate Present Value (PV) and Net Present Value (NPV).",
            "Adjust investment hurdles for high-inflation macroeconomic environments."
        ],
        "content_sections": [
            {
                "heading": "1. Core Principle of Time Value of Money",
                "body": """
Money available at the present time is worth more than the identical sum in the future due to its potential earning capacity (interest and investment yields) and the eroding effect of inflation.
"""
            },
            {
                "heading": "2. The Mathematical Formulas",
                "body": """
$$\\text{Future Value (FV)} = \\text{PV} \\times (1 + r)^n$$
$$\\text{Present Value (PV)} = \\frac{\\text{FV}}{(1 + r)^n}$$

Where:
* **PV:** Present Value (starting principal).
* **FV:** Future Value after compounding.
* **$r$:** Annual interest rate or discount rate per period.
* **$n$:** Number of compounding periods (years).

$$\\text{Net Present Value (NPV)} = \\sum_{t=1}^{n} \\frac{CF_t}{(1 + r)^t} - \\text{Initial Investment}$$
If $\\text{NPV} > 0$, the project generates value in excess of the alternative hurdle rate and should be undertaken.
"""
            }
        ],
        "takeaways": [
            "A currency unit today is worth more than one in the future due to inflation and reinvestment return.",
            "Compound interest accelerates capital growth exponentially over long investment horizons.",
            "Discount future project cash flows using a rate that reflects inflation and commercial risk."
        ],
        "quiz": [
            {
                "question": "If you invest ₦1,000,000 at a compound interest rate of 20% per year, what is the value after 2 years?",
                "options": [
                    "₦1,400,000",
                    "₦1,440,000",
                    "₦1,200,000",
                    "₦1,500,000"
                ],
                "answer_index": 1,
                "explanation": "FV = PV * (1 + r)^n = ₦1,000,000 * (1 + 0.20)^2 = ₦1,000,000 * 1.44 = ₦1,440,000."
            }
        ],
        "related_slugs": ["scarcity-and-opportunity-cost", "revenue-gross-operating-net-profit"]
    },

    # ── 7. Operations and Business Growth ──
    {
        "slug": "inventory-management-eoq-safety-stock",
        "category_id": "operations-business-growth",
        "title": "Inventory Management: EOQ, Safety Stock, and Working Capital",
        "summary": "Balance stockout risks against expensive storage and capital lockup. Compute Economic Order Quantity (EOQ) and Reorder Points.",
        "level": "Intermediate",
        "reading_time": "11 min",
        "order": 1,
        "objectives": [
            "Distinguish between ordering costs and holding/carrying costs.",
            "Calculate Economic Order Quantity (EOQ).",
            "Establish Reorder Points (ROP) with safety stock buffers.",
            "Prevent dead inventory while avoiding revenue-destroying stockouts."
        ],
        "content_sections": [
            {
                "heading": "1. The Inventory Dilemma: Holding Costs vs. Stockouts",
                "body": """
Inventory represents cash sitting on shelves. Excessive inventory ties up working capital, incurs warehouse rent, risks spoilage or obsolescence, and incurs holding costs. In contrast, insufficient inventory causes stockouts, lost sales, and damaged customer trust.
"""
            },
            {
                "heading": "2. Economic Order Quantity (EOQ) Formula",
                "body": """
The **EOQ** identifies the optimal order batch size that minimizes the sum of inventory ordering costs and carrying costs:

$$\\text{EOQ} = \\sqrt{\\frac{2 \\times D \\times S}{H}}$$

Where:
* **$D$:** Annual customer demand in units.
* **$S$:** Fixed order placement cost (freight, inspection, bank transfer charges per order).
* **$H$:** Annual holding/carrying cost per unit (rent, insurance, shrinkage, financing interest).
"""
            },
            {
                "heading": "3. Reorder Point (ROP) with Safety Stock",
                "body": """
$$\\text{Reorder Point (ROP)} = (\\text{Daily Demand Rate} \\times \\text{Lead Time in Days}) + \\text{Safety Stock}$$

If average lead time to receive stock from port to store is 14 days, and daily sales are 50 units, with a 200-unit safety stock buffer:
$$\\text{ROP} = (50 \\times 14) + 200 = 700 + 200 = 900 \\text{ units}$$
When warehouse stock reaches 900 units, the inventory system triggers a purchase order.
"""
            }
        ],
        "takeaways": [
            "EOQ minimizes the total cost of ordering and carrying stock.",
            "Safety stock protects against unpredictable supplier lead times and sudden demand spikes.",
            "Audit slow-moving inventory regularly to free trapped cash."
        ],
        "quiz": [
            {
                "question": "What happens if a company doubles its order batch size without an increase in customer demand?",
                "options": [
                    "Holding costs increase, while annual order placement frequency decreases",
                    "Total inventory cost is guaranteed to drop",
                    "Safety stock becomes zero",
                    "Cash flow immediately improves"
                ],
                "answer_index": 0,
                "explanation": "Larger order batches mean fewer annual orders (saving ordering cost), but higher average warehouse inventory (increasing annual holding costs)."
            }
        ],
        "related_slugs": ["cash-flow-working-capital-liquidity", "break-even-analysis-contribution-margin"]
    },

    # ── 8. Digital Business and Technology Economics ──
    {
        "slug": "saas-metrics-mrr-arr-churn",
        "category_id": "digital-business-technology-economics",
        "title": "SaaS Economics: MRR, ARR, Churn, and Net Revenue Retention (NRR)",
        "summary": "Understand subscription software metrics. Learn how compounding Monthly Recurring Revenue, customer churn, and expansion revenue drive technology company valuation.",
        "level": "Intermediate to Advanced",
        "reading_time": "13 min",
        "order": 1,
        "objectives": [
            "Calculate Monthly Recurring Revenue (MRR) and Annual Recurring Revenue (ARR).",
            "Differentiate Gross Churn from Net Revenue Retention (NRR).",
            "Understand why negative net revenue churn creates exponential software enterprise value.",
            "Model subscription cohort decay and customer lifespan."
        ],
        "content_sections": [
            {
                "heading": "1. The Recurring Revenue Engine",
                "body": """
Unlike traditional retail or custom service software firms that must resell to customers every single month, Software-as-a-Service (SaaS) charges a recurring subscription fee. This changes the economics: initial customer acquisition cost is high, but marginal delivery cost is near zero.
"""
            },
            {
                "heading": "2. MRR Components and Formula",
                "body": """
$$\\text{Net New MRR} = \\text{New MRR} + \\text{Expansion MRR} - \\text{Contraction MRR} - \\text{Churned MRR}$$

$$\\text{Annual Recurring Revenue (ARR)} = \\text{MRR} \\times 12$$
"""
            },
            {
                "heading": "3. Net Revenue Retention (NRR) Formula",
                "body": """
$$\\text{NRR} = \\frac{\\text{Starting MRR} + \\text{Expansion} - \\text{Contraction} - \\text{Churn}}{\\text{Starting MRR}} \\times 100\\%$$

If $\\text{NRR} > 100\\%$, the software company grows its revenue from existing cohorts even if it acquires zero new customers! World-class enterprise SaaS companies achieve $\\text{NRR} \\ge 120\\%$.
"""
            }
        ],
        "takeaways": [
            "MRR measures predictable, contracted monthly recurring subscription revenue.",
            "High customer churn acts as a leaky bucket that destroys acquisition ad spend.",
            "Net Revenue Retention (NRR) above 100% indicates strong product expansion and customer stickiness."
        ],
        "quiz": [
            {
                "question": "A SaaS startup starts January with ₦5,000,000 MRR from 100 clients. In January, existing clients upgrade by ₦800,000 (expansion), downgrades are ₦100,000, and cancellations are ₦200,000. What is their NRR?",
                "options": [
                    "90%",
                    "110%",
                    "100%",
                    "125%"
                ],
                "answer_index": 1,
                "explanation": "NRR = (5,000,000 + 800,000 - 100,000 - 200,000) / 5,000,000 = 5,500,000 / 5,000,000 = 110%."
            }
        ],
        "related_slugs": ["cac-ltv-unit-economics", "competitive-advantage-economic-moats"]
    }
]

# Quick helper lookups
CATEGORY_MAP = {c["id"]: c for c in CATEGORIES}
LESSON_MAP = {l["slug"]: l for l in LESSONS}
