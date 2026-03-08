# DeFi Risk Engine — Roadmap

## ✅ v0.1 — Token Risk Scoring
- Multi-chain balances (ETH / ARB / OP / Polygon)
- Risk registry (CR, PR, CoR, ChR)
- JSON report

## ✅ v0.2 — Unified Risk Score
- DeFi positions module
- Spam filter (blacklist + $500k cap)
- Unified risk score (tokens + DeFi)

## ✅ v0.3 — HTML Dashboard
- Dark theme dashboard
- Exposure doughnut chart
- Assets table with risk badges

## 🔜 v0.4 — Historical Tracking
- Auto-save reports to reports/YYYY-MM-DD_wallet.json
- Risk score trend chart
- Portfolio value over time

## 🔜 v0.5 — Multi-Wallet Support
- wallets = ["0x...", "0x..."]
- Global portfolio view
- Combined risk score

## 🔜 v0.6 — Alerts
- Threshold-based triggers (risk_score > 60)
- Telegram / email / webhook
- Scheduled monitoring (cron)

## 🔜 v0.7 — API
- FastAPI: GET /risk/{wallet}
- JSON response with portfolio + risk
- Foundation for SaaS
