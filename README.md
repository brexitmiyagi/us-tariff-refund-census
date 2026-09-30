# us-tariff-refund-census

This is the data and code behind my posts "Who Gets The Refund" and "Drip In, Lump Out" (The Istanbul Macro Brief, September 2026), and my Seeking Alpha pieces on G-III Apparel and Walmart.

The short version. In the second quarter of 2026 Treasury's cash books show US tariffs raising minus $3.5 billion. The national accounts show $81.6 billion. The difference is the IEEPA refund. This repo rebuilds the refund from Treasury's tables, shows how the national accounts treat it, sweeps the filings of every SEC filer that mentions it (698 companies by my 29 September run) for where the money went, uses each refund as a measure of the tariff bill to test who passed it on, and checks what happened to prices after the tariff came down.

The newest part. 22 big US retailers booked $7.4 billion of refunds in the quarter to early August. That was two thirds of their gross-profit growth. Without it their combined gross margin was below the same quarter of 2024, before any IEEPA tariff.

## How to run it

Python 3, standard library only. From anywhere:

```
python3 scripts/tieout.py
python3 scripts/net_customs.py
python3 scripts/three_ledgers.py
python3 scripts/regime_runrate.py
python3 scripts/incidence_split.py
python3 scripts/incidence_roundtrip.py
python3 scripts/census_summary.py
python3 scripts/census.py
python3 scripts/five_below.py
python3 scripts/interest_cost.py
python3 scripts/dts_crosscheck.py
python3 scripts/giii_refund_forensics.py
python3 scripts/giii_valuation.py
python3 scripts/nipa_incidence.py
python3 scripts/tariff_cut_chain.py
python3 scripts/refund_season.py
python3 scripts/passthrough.py
python3 scripts/z1_split.py
python3 scripts/wmt_fiscal2028.py
```

`scripts/edgar_census.py` re-runs the SEC sweep itself. It needs network access and a User-Agent (set `SEC_USER_AGENT` to your name and email, which the SEC asks for). It takes a while.

My own run is saved in `results/`.

## What each script gives you

- `tieout.py` checks that the monthly rows add up to Treasury's own fiscal-year-to-date rows. It fails loudly if they don't. Run it first.
- `net_customs.py`: gross up 70.2%, net up 1.3%, 98.2% of the extra gross refunded, the three negative months (minus $34.1 billion, June minus $25.6 billion), and the refund record. Full-year refunds FY2015 to FY2025 ran $1.6 billion to $7.5 billion. FY2026 to August is $125.2 billion.
- `three_ledgers.py`: the same quarter three ways. Q2 2026 Treasury net customs minus $3.5 billion, national-accounts customs duties $81.6 billion, and the refund sitting in Q1 2026 as a $166.4 billion federal capital transfer (Q1 capital transfers $807.9 billion annualized against $142.2 billion in Q4 2025).
- `regime_runrate.py`: monthly gross before the tariffs ($7.8 billion), under IEEPA ($30.9 billion) and after ($23.6 billion), and the FY2027 estimate of about $244.5 billion.
- `incidence_split.py`: the $166 billion split by who carried it. About $16.6 billion foreign sellers, at least $49.8 billion consumers, at most $99.6 billion US businesses.
- `incidence_roundtrip.py`: after the ruling. November 2025 to August 2026, import prices ex fuel +4.9%, the dollar -2.1%, core goods CPI +0.4%, landed cost of the basket +0.3% once the tariff drops from 15% to 10%. Import prices ex fuel were +5.47% year on year in August.
- `census_summary.py`: the 39 largest disclosures I pulled out of the sweep, $9.9 billion as stated, and how much of it is held for customers ($1.27 billion outright at FedEx, UPS and Power Solutions). American Eagle's claim sale works out at 27 cents on the dollar.
- `census.py`: the first nine disclosures I checked by hand, with each as a share of market value.
- `five_below.py`: the refund as 18.4% of Five Below's FY2026 GAAP EPS guidance midpoint.
- `interest_cost.py`: CBP's refund interest rates (6% for corporations to March 2026, 5% after) against three-month bills, and $2.0 billion to $6.0 billion of interest on $166 billion using the rates companies actually disclosed.
- `giii_refund_forensics.py`: G-III Apparel, the company my Seeking Alpha piece is about. Of its $139.5 million refund, $23.6 million stays inside non-GAAP ($0.36 a share, 16% of the $2.25 guidance midpoint). In Q1 that was 3.2 of the 3.5 points of adjusted gross margin gain. In Q2 it was $0.10 of the $0.26 non-GAAP EPS. The $133.9 million of refund cash was 27% of the roughly $500 million Marc Jacobs investment.
- `giii_valuation.py`: the fiscal 2028 bridge (my estimates), peer multiples on Nasdaq consensus, and the three cases. Base $1.86 a share, weighted value $20.64 against $27.13.
- `nipa_incidence.py`: who ate the tariff, from the national accounts, which leave the refund out of profits by design. Wholesale trade profits averaged 22% below 2024 across the four tariff quarters (trough -30% in Q3 2025, about $65 billion in all); retail trade profits were 0.4% above. All domestic nonfinancial profits came up $86 billion short, inside the at-most $99.6 billion on US businesses from `incidence_split.py`.
- `tariff_cut_chain.py`: what happened after the IEEPA duties ended. Duties/imports 10.8% (Oct 2025) to 6.5% (Jul 2026), about 13-14% to 8.3% excluding AI-related imports. Import prices before duty for consumer goods ex autos +2.1% Feb-Aug 2026 (record level, fastest six months since 2008); apparel/footwear/household +4.5% (record, fastest since 2011) after -3.1% under the tariff. Dollar +0.8%, Brent $71 to $117 (Apr) to $91, cotton +20%. PPI trade margins: general merchandise retailers +10-12% y/y Feb-May 2026. Core goods CPI +0.2%.
- `refund_season.py`: the quarter to July/August 2026 for 22 retailers (Walmart, Target, Home Depot, Lowe's, TJX, Ross, Gap, Dollar Tree, Five Below, American Eagle, Williams-Sonoma, Abercrombie, Urban Outfitters, lululemon, Academy, Bath & Body Works, Kohl's, Ollie's, Macy's, Best Buy, Burlington, Dillard's). Refunds booked in cost of sales $7.4 billion, 66% of combined gross-profit growth. Gross profit +11.7% reported, +4.0% without the refund, on sales +5.8%. Combined gross margin without the refund 28.27%, against 28.76% a year earlier and 28.82% in 2024.
- `passthrough.py`: the refund equals the IEEPA duty a company paid, so it measures the tariff bill. For 40 recipients: whole refund as a share of tariff-year sales (Walmart 0.41%, Home Depot 0.44%, Target 0.95%, median 1.24%, G-III 4.72%), and gross margin in the tariff year against the year before. Margin change regressed on duty/sales: slope +0.10, standard error 0.32, where eating the duty would be -1. Margin dollars given up were about a quarter of the duty; passing it on at cost would have cost about 34%. Run it with an argument (0.6 or 0.9) to change the share of each refund assumed to hit that year's cost of goods (0.74 is G-III's disclosed split).
- `z1_split.py`: the Fed's Financial Accounts (11 Sep 2026) put the refund in 2026 Q1: $141.5 billion to nonfinancial corporations, $24.75 billion to noncorporate business, nothing to households. The 98 largest disclosures in SEC filings add up to $16.9 billion, 10% of it.
- `wmt_fiscal2028.py`: the Walmart piece. It splits the $2.9 billion refund using the change in Walmart's own guidance from February to August (more than $2.0 billion to fuel, $0.06 billion to Vibe, a $0.61 billion leftover that is mostly price). It measures what a dollar of NY Harbor wholesale diesel costs Walmart three ways from its own statements (2022 Q1, US only, $0.92 billion a year; 2026 Q1 $0.71 billion; the FY27 guide $1.39 billion, a floor; mid $1.01 billion) and checks it against Walmart's own fleet (1 billion miles at 6.7 mpg, about $0.15 billion). On the CME strip of 29 September 2026 (fiscal 2028 $3.62), consensus of $3.22 needs $37.4 billion of operating income: 12.5% on fiscal 2027 as reported, 23.3% without the refund, and 14.9% to 18.1% on any fiscal 2027 base from 7% to 10% underlying growth, however the leftover splits between price and other costs. It prints a three-statement summary through fiscal 2029 (gross margin bridge, SG&A, interest at 4.5% on new debt, cash flow, debt, equity), quarterly EPS for Q3 FY27 to Q4 FY28 against consensus, the three cases, fair value today on fiscal 2028 ($94.40) and the 12-month target on fiscal 2029 ($105.16), an owner-earnings cross-check, and the freight, EV/EBITDA and options numbers. Operating income is forecast top-down, and the gross profit and SG&A lines in the summary split that total. Section 13 rebuilds it bottom-up as a check: gross margin gets only last year's mix gain (24.13% to 24.21%, 8 basis points), SG&A grows with sales plus depreciation above sales, less the leverage (0.11% of sales) needed to land fiscal 2027 on guidance. That gives $0.56 billion less operating income in fiscal 2028 and $0.88 billion less in fiscal 2029, EPS of $2.86 and $3.17, and a target of $102.46, so the top-down figures are the kinder ones. Section 14 shows the target at 6% to 11% base-case underlying growth: $102.34 to $108.05.
- `sweep_filers.py`: reruns the EDGAR full-text searches behind the 698-company sweep and writes `data/sweep_filers.csv`. Needs network access and `SEC_USER_AGENT`.
- `dts_crosscheck.py`: the Daily Treasury Statement against the monthly one, and CBP outflows this year running $145.5 billion above last year, 37% of net corporate income tax over the same days.

## Data

- `data/mts_customs_monthly.csv`, `data/mts_customs_fytd_fy2026.csv`, `data/mts_customs_fy_history.csv`: Monthly Treasury Statement Table 4, Customs Duties. https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
- `data/dts_customs_monthly.csv`: Daily Treasury Statement, customs deposits and CBP withdrawals. https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/
- `data/nipa_quarterly.csv`: FRED series W020RC1Q027SBEA (federal capital transfer payments), B235RC1Q027SBEA (customs duties), CP (corporate profits after tax).
- `data/prices_monthly.csv`: FRED series IREXFUELS (import prices ex fuels), DTWEXBGS (broad dollar, monthly average), CUSR0000SACL1E (core goods CPI).
- `data/census_edgar.csv`: the 39 disclosures in the census table, each with the filing it came from and how I classified it.
- `data/refund_census.csv`: the first nine, hand-checked, with market values.
- `data/giii_inputs.csv`, `data/giii_peers.csv`: G-III figures from its 10-K, 10-Qs, 8-K releases and the Q2 call, and peer prices and consensus from Nasdaq on 28-29 September 2026.
- `data/nipa_profits_by_industry.csv`: BEA NIPA Table 6.16D, profits with inventory valuation adjustment by industry, SAAR, read 29 Sep 2026.
- `data/fred_chain_monthly.csv`: FRED pulls on 29 Sep 2026: BLS import price indexes by end use and origin, CPI, PPI trade margin indexes, dollar, yuan, Brent, cotton.
- `data/tracker_tariff_monthly.csv`: Census imports, duties/imports and AI-related imports, as published by the Trade War Tracker (tradewartracker.github.io/state-of-us-trade), July 2026 edition.
- `data/retail_q2_2026.csv`: revenue and gross profit for the same quarter in 2024, 2025 and 2026 (SEC XBRL company facts) and the refund each 10-Q says went into cost of sales that quarter.
- `data/xbrl_quarterly_margins.csv`: quarterly revenue and gross profit, 2023 to 2026, for the 40 refund recipients (SEC XBRL company facts API).
- `data/refund_duty_inputs.csv`: each company's refund, or IEEPA duty paid where the filing gives it, with what the number measures.
- `data/census_listed_refunds.csv`: the 98 largest refund disclosures I read in 10-Qs and 10-Ks, with where each says the money goes.
- `data/refund_uses.csv`: the cases where a filing says part of the refund went to suppliers, staff, claim buyers, business customers or prices.
- `data/z1_capital_transfers.csv`: FRED series BOGZ1FU315410005Q, BOGZ1FU105400005Q, BOGZ1FU115400005Q, BOGZ1FU155400005Q, BOGZ1FU265400005Q, BOGZ1FU795400005Q, 2024 Q1 to 2026 Q2.
- `data/wmt_history_segments_freight.csv`: NY Harbor ULSD monthly averages for 2022 and 2026, Walmart's 2022 fuel statement, adjusted operating income growth for fiscal 2021 to 2026, first-guidance prices and EPS midpoints for fiscal 2023 to 2027, segment sales and operating income, balance sheet, buybacks, and the freight indicators, each with its source.
- `data/wmt_futures_cashflow.csv`: Walmart's first-quarter fuel figure, the full-year fuel guidance, Sam's Club operating income with and without fuel, the CME ULSD settlements of 28 Sep 2026, operating cash flow, D&A, dividend and 52-week range.
- `data/wmt_quarterly_peers.csv`: Walmart's quarterly adjusted EPS for fiscal 2026 and the first half of fiscal 2027, quarterly consensus, and two assumptions of mine (4.5% on new debt, and 0.15 points a year of gross-margin mix used only to split the top-down operating income into gross profit and SG&A).
- `data/wmt_fy26_statements.csv`: Walmart's fiscal 2026 income statement, balance sheet and cash flow lines from SEC XBRL company facts, plus first-half fiscal 2027 items the model uses and fiscal 2025 sales and cost of sales for the bottom-up check.
- `data/wmt_market_29sep.csv`: the 29 September 2026 close for Walmart and peers, the CME ULSD settlements of that day (they replace the 28 September strip), Walmart's fleet miles, FHWA truck fuel economy, trailing EV/EBITDA from S&P Global via StockAnalysis, and the November option quotes.
- `data/wmt_fuel_peers.csv`: Walmart's refund and guidance figures, consensus, shares, tax rate, peer prices and consensus, free cash flow and short interest.
- `data/inputs.csv`: every outside number the scripts use, with its source.

## Sources

1. Treasury, Monthly Treasury Statement. https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
2. Treasury, Daily Treasury Statement. https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/
3. BEA, how the IEEPA refunds are recorded. https://bea.gov/help/faq/1488
4. CBO, Monthly Budget Review for August 2026. https://www.cbo.gov/system/files/2026-09/61984-MBR.pdf
5. CBO, updated tariff projections, 20 Aug 2026. https://www.cbo.gov/publication/62704
6. Treasury, borrowing estimates, 3 Aug 2026. https://home.treasury.gov/news/press-releases/sb0584
7. TBAC minutes, 4 Aug 2026. https://home.treasury.gov/news/press-releases/sb0592
8. CBP, IEEPA refunds and CAPE. https://www.cbp.gov/trade/programs-administration/trade-remedies/ieepa-duty-refunds
9. CBP, customs interest rates. https://www.federalregister.gov/documents/2026/05/18/2026-09871/quarterly-irs-interest-rates-used-in-calculating-interest-on-overdue-accounts-and-refunds-of-customs
10. C.H. Robinson on CBP's September update. https://www.chrobinson.com/en-us/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/
11. CNBC on CBP's court filing ($166 billion, 330,000 importers). https://www.cnbc.com/2026/03/06/trump-trade-tariffs-refunds-customs-border-protection.html
12. AP via Fast Company on the government's Federal Circuit brief. https://www.fastcompany.com/91588641/tariff-refund-government-appeal
13. NY Fed, Who Is Paying for the 2025 U.S. Tariffs? https://libertystreeteconomics.newyorkfed.org/2026/02/who-is-paying-for-the-2025-u-s-tariffs/
14. Federal Reserve Board, The Slow Climb. https://www.federalreserve.gov/econres/notes/feds-notes/the-slow-climb-how-tariffs-gradually-raised-retail-prices-in-2025-20260305.html
15. 26 U.S.C. 6416. https://www.law.cornell.edu/uscode/text/26/6416
16. Case 199/82, San Giorgio. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:61982CJ0199
17. H.R. 7822, Tariff Relief for Consumers Act. https://www.govinfo.gov/content/pkg/BILLS-119hr7822ih/html/BILLS-119hr7822ih.htm
18. Hedgeweek on the claims market. https://hedgeweek.com/news/tariff-refunds-how-hedge-funds-are-structuring-a-new-short-duration-credit-trade
19. Holland & Knight on the consumer class actions. https://www.hklaw.com/en/insights/publications/2026/08/ieepa-tariff-consumer-class-actions-litigation-update
20. Proclamation 11012. https://www.federalregister.gov/documents/2026/02/25/2026-03824/imposing-a-temporary-import-surcharge-to-address-fundamental-international-payments-problems
21. Global Trade Alert on the switch to Section 301. https://globaltradealert.org/blog/us-import-tariffs-24-july-2026
22. SEC EDGAR full-text search. https://efts.sec.gov/LATEST/search-index?q=%22IEEPA%22%20%22refund%22&forms=10-Q,10-K
23. SEC XBRL company facts API. https://data.sec.gov/api/xbrl/companyfacts/
24. Federal Reserve, Financial Accounts of the United States, Z.1, 11 Sep 2026. https://www.federalreserve.gov/releases/z1/
25. Federal Reserve, FOMC statement, 16 Sep 2026. https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
26. Nintendo, financial results explanatory material, Q1 FY2027. https://www.nintendo.co.jp/ir/pdf/2026/260806_2e.pdf
27. EIA Short-Term Energy Outlook, 9 Sep 2026. https://www.eia.gov/outlooks/steo/
28. Walmart Q2 FY27 earnings call transcript, 20 Aug 2026. https://stock.walmart.com/
29. Macrotrends, Walmart P/E history. https://www.macrotrends.net/stocks/charts/WMT/walmart/pe-ratio
30. CME Group, NY Harbor ULSD futures settlements, 28 Sep 2026. https://www.cmegroup.com/markets/energy/refined-products/heating-oil.settlements.html
31. FRED, DDFUELNYH (NY Harbor ULSD spot) and GASDESW (US retail diesel). https://fred.stlouisfed.org/
32. Walmart Q1 FY27 earnings call and presentation, 21 May 2026. https://stock.walmart.com/
33. Walmart Form 10-K for the year to 31 Jan 2026 (Item 7A, market risk). https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm
34. FRED, DGS3MO (three-month Treasury yield). https://fred.stlouisfed.org/series/DGS3MO
35. Walmart Q1 FY23 earnings call transcript, 17 May 2022. https://stock.walmart.com/
36. Walmart Q4 earnings releases FY21-FY26 (8-K). https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000104169
37. Walmart Form 10-Q for the quarter to 31 Jul 2026. https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm
38. J.B. Hunt Form 10-Q for the quarter to 30 Jun 2026. https://www.sec.gov/Archives/edgar/data/728535/000143774926024397/jbht20260630_10q.htm
39. FRED: PCU484121484121 (truckload PPI), FRGEXPUSM649NCIS and FRGSHPUSM649NCIS (Cass Freight Index). https://fred.stlouisfed.org/
40. BLS Beyond the Numbers, 'As crude oil plunges, retail gasoline margins spike, then retreat'. https://www.bls.gov/opub/btn/volume-4/as-crude-oil-plunges-retail-gasoline-margins-spike-then-retreat.htm
41. Consensus on guidance days: CNBC (17 Feb 2022, 19 Feb 2026), Fox Business/Reuters (21 Feb 2023), eMarketer (20 Feb 2025).
42. Walmart careers, private fleet (16,000 drivers, 1 billion miles a year). https://careers.walmart.com/us/en/home/careers-areas/supply-chain-and-transportation/drivers
43. FHWA Highway Statistics 2023, Table VM-1. https://www.fhwa.dot.gov/policyinformation/statistics/2023/vm1.cfm
44. StockAnalysis (S&P Global data), statistics pages for WMT, COST, AMZN, BJ, DG, TGT, KR, 30 Sep 2026. https://stockanalysis.com/stocks/wmt/statistics/
45. Nasdaq option chain, WMT, 30 Sep 2026. https://www.nasdaq.com/market-activity/stocks/wmt/option-chain
46. Kroger Q2 2026 release (8-K) and call. https://www.sec.gov/Archives/edgar/data/56873/000110465926106890/tm2625060d1_ex99-1.htm and https://www.fool.com/earnings/call-transcripts/2026/09/11/kroger-kr-q2-2026-earnings-call-transcript/
47. Dollar General Q2 2026 release (8-K). https://www.sec.gov/Archives/edgar/data/29534/000110465926101918/tm2623914d1_ex99.htm
48. Target Q2 2026 release (8-K). https://www.sec.gov/Archives/edgar/data/27419/000002741926000034/a2026q2ex-99.htm

## Things to be careful with

- The pass-through test is 40 companies and one year of margins. Year-to-year margin moves with no tariff in them average about 1.4 points, and the median tariff bill is about 1.2% of sales, so any single company's number is noise. The regression across all 40 is the finding, and Nike, lululemon, Baxter and GE HealthCare had big margin moves for their own reasons (dropping them gives a slope of -0.08).
- "Passed on" in the test means recovered from customers or suppliers. Gap, Williams-Sonoma and VF say vendors carried part of it.
- The retail refund numbers are what each 10-Q booked in cost of sales that quarter. American Eagle's and Burlington's are for 26 weeks. Kohl's recognized about $100 million of the $150 million it received in cost of sales.
- The 98-company census is the largest disclosures, read by hand. Smaller ones are in the filings the sweep script finds but are not added up here.
- NIPA profits with the inventory adjustment are profits from current production. Book profits fell less, because firms sold pre-tariff stock at post-tariff prices. Retail trade in the national accounts includes Amazon's whole business. Profits move for reasons other than tariffs.
- After February 2026 the tariff cut overlaps an oil shock (Brent $71 to $117) and a 20% cotton rise. The factory-price rise is part cost, part exporters rebuilding price; the scripts do not split it.
- The ex-fuel import price index is driven by industrial supplies and AI-related capital goods. Use the consumer goods index for anything about shelf prices.
- The Walmart fuel sensitivity comes from three Walmart figures that run from $0.71 billion to $1.39 billion a dollar, and the 2022 one is US only. I measure against NY Harbor wholesale diesel, which is what the futures trade, not what Walmart's fleet actually pays. Walmart's February plan may have assumed a forward curve rather than February's spot price. Sam's Club fuel profit is left out.
- The G-III fiscal 2028 bridge is four estimates of mine, not company guidance. The consensus I compare against is a single analyst estimate.
- The sweep is a keyword search. A company that booked a refund without using the word "refund" near "IEEPA" is missed, and the pass-back count depends on how filings are worded. I counted 16 companies disclosing refunds owed to customers after dropping four keyword false positives by hand.
- The census amounts are as each filing states them. Some are recognized, some received, some expected, some claims submitted. They are not one consistent measure.
- The incidence split joins two studies with different scopes. The consumer share is a floor measured on Chinese goods.
- The price comparison uses indexes with different baskets. CBO's effective rate is weighted by 2024 imports. The landed-cost figure is a rough check, not a measurement.
- The interest range comes from two companies' disclosures. The true average could sit outside it.
- The FY2027 estimate assumes gross collections hold near the March to August pace and that the whole tail is paid in FY2027. A Federal Circuit ruling on refunds, Section 122 or Section 301 changes that.
- DTS and MTS don't match exactly. Headline numbers use MTS.
- The Walmart segment numbers for fiscal 2028 are mine. Walmart only gives fuel and the refund in total, so the segments are underlying and fuel and rollbacks come off the total. I couldn't find the day-of consensus for two of the five guidance days (fiscal 2023 and 2025).

## Corrections

None so far.
