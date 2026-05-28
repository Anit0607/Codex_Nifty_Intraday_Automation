# Nifty 50 Intraday Desk Report

Analysis Date: 2026-05-26  
Mode: BACKTEST  
Generated As Of: 2026-05-26 09:20 IST  

Reference Prices:  
Previous Close: 24,031.70  
Today's Open: 24,004.10  

Expected Day Range: 23,625 - 24,383  
Expected Range Confidence: 56%  

Actionable Desk Range: 23,950 - 24,135  
Actionable Range Confidence: 67%  

Close vs Open Direction:  
Expected Bias: Near open to mildly positive if 24,000 holds  
Direction Confidence: 57%  

Overall Report Confidence: 68%

## 1. Market Summary

Nifty opened with a flat-to-soft gap of about -0.11% and started inside the CPR, which keeps the first bias balanced rather than directional. CPR width is very narrow at 28.70 points, so expansion is possible if price accepts outside 23,950 or 24,085. VIX cooled to 16.70 but remains elevated enough for expiry whipsaws. FII and DII were both net buyers on 25 May, while global cues were mixed-positive but Brent near USD 98 and USD/INR near 95 remain macro caps.  

Section Confidence: 72%

## 2. Key Levels

| Level Type | Level | Interpretation | Confidence |
|---|---:|---|---:|
| Strong Resistance | 24,135 - 24,150 | R2/round-zone extension; trend confirmation only above this | 82% |
| Immediate Resistance | 24,054 - 24,083 | Previous high to R1 supply zone | 86% |
| Strong Support | 23,870 - 23,885 | S2 and lower round-zone defence | 82% |
| Immediate Support | 23,950 - 23,989 | S1 to CPR lower edge | 88% |
| Pivot | 24,003.00 | Opening balance almost exactly at pivot | 92% |
| CPR Zone | 23,988.65 - 24,017.35 | Open inside CPR; balanced start | 92% |
| Previous Day High | 24,054.45 | First meaningful upside test | 90% |
| Previous Day Low | 23,922.85 | Breakdown support reference | 90% |
| Previous Day Close | 24,031.70 | Carry-forward bullish reference | 92% |
| Breakout Level | 24,085 - 24,100 | Sustained hold above R1 confirms upside expansion | 78% |
| Breakdown Level | 23,950 - 23,920 | Loss of S1/prior low confirms bearish turn | 78% |
| Expected Intraday Range | 23,625 - 24,383 | VIX statistical envelope, not a trade target | 56% |
| R1 | 24,083.15 | First pivot resistance | 92% |
| R2 | 24,134.60 | Second pivot resistance | 92% |
| S1 | 23,951.55 | First pivot support | 92% |
| S2 | 23,871.40 | Second pivot support | 92% |

Section Confidence: 87%

## 3. Probability Model

From current day open of 24,004.10:

Upside Probability: 36%  
Downside Probability: 24%  
Sideways Probability: 40%  
Total: 100%  
Section Confidence: 64%

The leading scenario is sideways with a constructive lean because price opened inside CPR after a strong previous-day close above 24,000. Institutional flows were supportive, VIX was cooling, and US futures/Asia were not risk-off. The bullish case needs acceptance above 24,085; without that, expiry gravity around 24,000 can keep the market pinned. Downside becomes serious only below 23,950 and especially below 23,922.

## 4. Factor Scoring Table

| Factor | Observation | Bias | Weight | Impact | Confidence |
|---|---|---|---:|---|---:|
| Price Action & Gap Context | Flat-to-soft open inside narrow CPR after bullish close | Sideways/Constructive | 35% | Balance with breakout potential | 76% |
| India VIX / Volatility | VIX previous close 16.70, down 6.76% | Constructive but volatile | 20% | Lower fear, but expiry swing risk | 74% |
| Derivatives Logic | Simulated expiry pin near 24,000; call supply 24,100/24,200; put support 23,900/24,000 | Sideways | 20% | Range/pin risk dominates early | 58% |
| Global & Macro Cues | US closed, US futures strong, Asia mixed-positive, Brent near 98, rupee near 95.23 | Mixed constructive | 15% | Supports dips, caps euphoria | 66% |
| Institutional Flow | FII +822 Cr, DII +3,857 Cr on 25 May | Bullish liquidity | 10% | Dips likely defended | 80% |
| Markov Regime Overlay | Recent close above prior range but not enough full model data in this run | Calibration layer | Bounded | Mild upside/sideways support | 50% |

Section Confidence: 68%

## 5. Scenario Mapping

Bullish Case (36%)  
Price must sustain above: 24,085, then 24,100  
VIX behaviour: VIX should stay below 17 and ideally cool toward 16  
Breakout confirmation: 15-minute hold above R1 with no rejection below 24,054  
Upside targets: 24,135 - 24,150 -> 24,200  
Confidence: 63%

Bearish Case (24%)  
Price must fail below: 23,950  
VIX behaviour: VIX rises above 17.2 while price loses prior low  
Breakdown confirmation: sustained trade below 23,922  
Downside targets: 23,871 -> 23,800  
Confidence: 57%

Sideways Case (40%)  
Range to hold: 23,950 - 24,085  
Option writer defence zone: 24,000 pivot/max-pain area; 23,900/24,100 outer strikes  
Confirming behaviour: repeated mean reversion around 24,000 with no 15-minute acceptance outside range  
Mean reversion target: 24,003 - 24,032  
Confidence: 68%

Section Confidence: 65%

## 6. Assumptions Made

Missing Data Assumptions:

- Exact 09:20 live option-chain OI/PCR snapshot was not reconstructed; derivatives logic is simulated.
- Full Markov transition matrix was not rebuilt in this chat run; regime overlay is treated as a bounded proxy.
- US cash-market close for 25 May was unavailable because US markets were closed for Memorial Day.

Simulated Derivatives Assumptions:

- Call writing zones assumed at 24,100, 24,150, and 24,200.
- Put writing zones assumed at 24,000, 23,950, and 23,900.
- Max pain estimate: 24,000.
- PCR assumption: neutral to mildly put-heavy while spot holds 24,000.

Macro Assumptions:

- Brent near USD 98 is treated as a cap, not a panic trigger.
- USD/INR near 95.23 is a structural FII-pressure risk under the framework.
- FII/DII buying from 25 May supports dip defence but may not be enough for a one-way expiry trend.

Markov/Quant Assumptions:

- Recent regime is treated as sideways-to-bullish after the 25 May breakout close.
- Markov overlay adjusts confidence only; it does not override CPR/open structure.

Section Confidence: 78%

## 7. Invalidations / Risk Factors

| Risk Factor | Trigger | Consequence | Primary View Invalidated | Confidence |
|---|---|---|---|---:|
| Bullish confirmation | 15-min hold above 24,100 | Range thesis weakens; upside extension opens | Sideways | 78% |
| Bearish confirmation | 15-min hold below 23,922 | Dip-buying thesis weakens; expiry selling can accelerate | Bullish/sideways | 78% |
| Expiry gamma | Fast 60-100 point reversal near 24,000 | SLs can trigger both sides; avoid chasing | Directional trades | 74% |
| VIX spike | VIX above 17.2 with price below 23,950 | Premium expands; option sellers lose comfort | Range-selling | 72% |
| Macro shock | Crude spike / rupee weakness headline | Risk-off pressure returns | Buy-on-dip | 66% |
| Watch window | 09:20 - 10:15 IST | First acceptance outside CPR decides bias | Morning view | 82% |

Section Confidence: 71%

## 8. Trader-Specific Desk Plan

### Option Non-Directional Seller

- Suitable / avoid: Suitable only after the first 30 minutes if 23,950 - 24,085 holds.
- Preferred structure: Intraday short strangle/iron fly around 24,000 with strict SL; avoid overnight carry.
- Strike or range logic: Short premium around 24,000 only if spot mean-reverts; outer risk levels 23,900 and 24,100.
- Entry condition: Two failed attempts outside CPR/range and VIX not rising.
- Stop/invalidation: Exit if spot sustains above 24,100 or below 23,922; also exit if VIX spikes above 17.2.
- Time window: 10:00 - 13:45; avoid fresh positions late in expiry.
- Confidence: 62%

### Option Directional Seller

- Suitable / avoid: Suitable only after rejection confirmation; avoid initiating at the open.
- Preferred side: Put selling above 24,000 if spot holds; call selling only after rejection below 24,085.
- Strike logic: For bullish sell-side, 23,950/23,900 PE only after support confirmation. For bearish sell-side, 24,100 CE after failed breakout.
- Entry condition: Spot holds above pivot/CPR with falling VIX for PE sell; spot rejects R1 for CE sell.
- Stop/invalidation: PE sell invalid below 23,950; CE sell invalid above 24,100.
- Time window: 09:45 - 12:30 after first direction is clear.
- Confidence: 60%

### Option Buyer

- Suitable / avoid: Avoid blind buying because expiry theta and pin risk are high.
- Calls or puts: Calls only above 24,100; puts only below 23,922.
- Entry condition: Momentum candle plus retest hold; no entry inside 23,950 - 24,085.
- Stop/invalidation: Re-entry into the range after breakout/breakdown.
- Target logic: Call target 24,135/24,200; put target 23,871/23,800.
- Time window: First 90 minutes if breakout is clean; otherwise wait.
- Confidence: 55%

### Future Intraday Trader

- Suitable / avoid: Wait for range break; avoid middle-zone trades.
- Entry zone: Long above 24,100; short below 23,922.
- Stop: Long SL below 24,045; short SL above 23,975.
- Targets: Long 24,135 then 24,200; short 23,871 then 23,800.
- Timing: 09:45 onward after opening whipsaw settles.
- Confidence: 59%

Section Confidence: 61%

## 9. Trading Desk Interpretation

Classification: Range-selling day with conditional upside breakout.

Option sellers can work around 24,000 only after confirming range behaviour and must use strict SLs because monthly expiry can create sharp gamma moves. Option buyers and futures traders should wait for 24,100 upside acceptance or 23,922 downside breakdown; the middle zone is a no-trade area.

Bottom line: Treat 26 May 2026 as a 24,000-pivot expiry session; favour range tactics early, but flip bullish only above 24,100 and defensive below 23,922.

Section Confidence: 67%

Backtest Integrity: This analysis was generated using only data available as of/before approximately 09:20 IST on 26 May 2026. The actual 26 May 2026 closing price and intraday outcome were not referenced while forming the morning view.

