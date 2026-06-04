# Nifty 50 Evening Tally — 2026-06-04

**Run boundary:** Post-market after 17:00 IST  
**Market status:** **OPEN — tally executed.** NSE showed an actual Nifty 50 close print for **04-Jun-2026 15:30**, and NSE clearing schedule also listed **04-Jun-2026** as a trade date with settlement on **05-Jun-2026**. ([nseindia.com](https://www.nseindia.com/resources/exchange-communication-holidays/))

## 1. Actual Post-Market Data Used

| Item | Actual |
|---|---:|
| Previous close | 23,405.60 |
| Open | 23,282.45 |
| High | 23,465.30 |
| Low | 23,247.30 |
| Close | 23,416.55 |
| Day range | 218.00 pts |
| Close vs open | **Above open** by 134.10 pts |
| Close vs previous close | +10.95 pts / +0.05% |

The actual open was confirmed at **23,282.45**; the intraday range was reported as **23,247.30–23,465.30**; and the close was **23,416.55**. ([newsarenaindia.com](https://newsarenaindia.com/economy/sensex-nifty-open-lower-amid-west-asia-tensions/79036?utm_source=openai))

**India VIX:** Closed at **15.89**, down **2.41%**, versus the morning report’s prior VIX reference of **16.28**. ([business-standard.com](https://www.business-standard.com/markets/capital-market-news/nifty-holds-23-400-amid-rbi-policy-caution-broader-market-ends-firm-126060400835_1.html?utm_source=openai))

**Macro / context:** The session stayed choppy and cautious ahead of the RBI policy decision on **05-Jun-2026**; Brent was around **$96.70**, USD/INR was around **95.8350**, the India 10-year yield was around **7.005%**, and the US 10-year yield was around **4.477%** in the post-market recap. ([business-standard.com](https://www.business-standard.com/markets/capital-market-news/nifty-holds-23-400-amid-rbi-policy-caution-broader-market-ends-firm-126060400835_1.html?utm_source=openai))

**Institutional flow status:** Final/provisional **04-Jun-2026 FII/DII cash flow was not source-confirmed in the fetched post-market results**. NSE’s FII/FPI-DII page notes that such trade data is provisional and that final FII/FPI data should be checked through NSDL/CDSL. ([nseindia.com](https://www.nseindia.com/reports/fii-dii?os=dio&utm_source=openai))

---

## 2. Section-Wise Morning Report Audit

| Morning section / claim | Verdict | Tally comment |
|---|---:|---|
| **Market-open verification / reference prices** | **Hit** | Previous close **23,405.60** and open **23,282.45** were correct. |
| **VIX Risk Envelope: 22,924–23,641** | **Contained** | Actual low/high **23,247.30–23,465.30** stayed inside the broad VIX envelope. This is risk containment, not precision by itself. |
| **Expected Day Range: 23,155–23,505** | **Hit** | Actual low and high both stayed inside the primary expected range. |
| **Expected High Zone: 23,420–23,505** | **Hit** | Actual high **23,465.30** landed inside the expected high zone. |
| **Expected Low Zone: 23,155–23,225** | **Tolerance hit** | Actual low **23,247.30** was **22.30 pts above** the zone’s upper edge, within the ±50 pt tolerance. |
| **Range precision rule** | **Hit** | High-zone error **0.00**; low-zone error **22.30**; no precision miss. |
| **Close vs open: Close above open** | **Hit** | Actual close **23,416.55** was above open **23,282.45**. |
| **Opening execution map** | **Good** | Open sat inside the chop band. Short trigger below **23,215** did not fire; later acceptance above **23,375** worked and reached target 1 **23,445**, but not target 2 **23,525**. |
| **Scenario mapping** | **Hit** | The realised session matched the “fragile gap-down recovery / VIX cooling” path better than a clean trend day. |
| **Risk invalidations** | **Useful** | Neither **23,150** downside invalidation nor **23,530** upside breakout invalidation fired. VIX spike risk did not materialise; VIX cooled. |
| **Trader-specific desk plan** | **Mostly useful** | Best fit was disciplined long/futures/option-buyer trigger execution after reclaim; non-directional sellers needed caution because price moved from gap-down support to upside target zone. |

---

## 3. Key Scoring Outcomes

- **Direction hit:** Yes — predicted and actual were both **above_open**.
- **Expected range contained:** Yes.
- **Range precision hit:** Yes.
- **High zone error:** **0.00 pts**.
- **Low zone error:** **22.30 pts**, within tolerance.
- **Execution map score:** **82/100** — trigger logic was useful; target 1 worked; target 2 did not.
- **Overall tally score:** **86/100**.

---

## 4. Calibration / Auto-Healing Result

**Bounded auto-healing processed in scorecard only. No core skill logic rewrite.**

Processed bounded updates:

1. Add one positive observation to binary close-direction hit rate.
2. Add one positive observation to primary expected-range containment.
3. Add one positive observation to high/low zone precision.
4. Add pattern observation: `gap_down_low_at_open_vix_cool_reversal` because the day opened gap-down, the short trigger did not fire, VIX cooled, and price recovered above open.
5. Apply a **small +1 confidence offset** to the already-bounded gap-down-recovery calibration bucket only when all conditions are present: low near open, short trigger not fired, VIX cooling, and upside trigger later confirms.
6. Add a source reliability note: official NSE close was available, but high/low were taken from a public technical recap because the official OHLC CSV was not accessible in the fetched crawl. Automation should prefer NSE/NiftyIndices CSV when reachable.

**Disallowed changes not performed:** no CPR rewrite, no probability-model replacement, no removal of risk warnings, no leverage/position-size aggressiveness, and no core skill-logic rewrite.
