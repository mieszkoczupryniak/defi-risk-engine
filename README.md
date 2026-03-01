# DeFi Risk Engine

Portfolio risk scoring engine for on-chain wallets.
Calculates CR, PR, CoR, ChR components and outputs a composite Portfolio Risk Score.

## Risk Components
- **CR** – Contract Risk (token-level smart contract risk)
- **PR** – Protocol Risk (weighted average across positions)
- **CoR** – Concentration Risk (flags single-asset exposure >50%)
- **ChR** – Chain Risk (risk score per blockchain)

## Stack
- Python 3.14
- Dune SIM API (on-chain balances)
- python-dotenv, requests

## Usage
```bash
pip install requests python-dotenv
python main.py
```

## Output
Generates `risk_report.json` with full breakdown per token and final Portfolio Risk Score.

## Status
🚧 MVP v0.1 – active development
