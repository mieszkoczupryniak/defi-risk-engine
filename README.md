# 🛡️ DeFi Risk Engine

On-chain portfolio risk scoring engine for any EVM wallet.
Analyzes token holdings and DeFi positions across multiple chains and returns a unified risk score with HTML dashboard.

## Features
- **Multi-chain support** — Ethereum, Arbitrum, Optimism, Polygon
- **4 risk components** — CR, PR, CoR, ChR → Unified Risk Score
- **DeFi positions** — Vaults, LP, Lending (Aave, Uniswap, ERC4626)
- **Spam filter** — blacklist + $500k position cap
- **HTML dashboard** — dark theme, exposure chart, assets table

## Risk Components
| Score | Name | Description |
|---|---|---|
| CR | Concentration Risk | Single-asset exposure |
| PR | Protocol Risk | Token-level smart contract risk |
| CoR | Correlation Risk | Flags >50% in one asset |
| ChR | Chain Risk | Risk score per blockchain |

## Stack
- Python 3.14
- Dune SIM API
- python-dotenv, requests, Chart.js

## Usage
```bash
cp .env.example .env  # add your SIM_API_KEY
pip install requests python-dotenv
python main.py        # generates risk_report.json
python dashboard.py   # generates report.html

## Status
🚧 v0.3 — active development | Roadmap
