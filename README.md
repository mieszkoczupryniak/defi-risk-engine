# Nexus — DeFi Portfolio Risk Intelligence Engine

Analyze any on-chain wallet and get a unified risk score, trend tracking, and automated alerts — in seconds.

---

## What it does

Nexus scans any EVM wallet across multiple chains and detects:

- **Portfolio risk** — weighted risk score across all held tokens
- **DeFi exposure** — LP positions, vaults, lending protocols
- **Concentration risk** — dangerous overexposure to a single asset
- **Risk spikes** — sudden risk increases vs previous scan
- **Trend tracking** — delta vs last historical snapshot

---

## Features

- Multi-chain wallet analysis (Ethereum, Arbitrum, Optimism, Polygon)
- DeFi position detection (vaults, LP, lending)
- Unified risk scoring (tokens + DeFi combined)
- Historical risk tracking (auto-saved snapshots)
- Risk alerts engine (spike / high risk / concentration)
- CLI wallet scanner

---

## Example output

\```
==> UNIFIED RISK v0.2: 33.52

--- Trend vs last scan (2026-03-15T14:41) ---
Unified Risk: 33.52  (▲ 0.04)
CR:           24.27  (▼ 0.79)
CoR:          69.71  (▲ 0.82)

--- Alerts ---
⚠️  CONCENTRATION RISK (ETH 69.71%)
\```

---

## How to run

\```bash
git clone https://github.com/mieszkoczupryniak/defi-risk-engine
cd defi-risk-engine
pip install -r requirements.txt
\```

Add your API key to `.env`:

\```
SIM_API_KEY=your_key_here
\```

Run:

\```bash
python main.py --wallet 0xYOUR_WALLET
\```

---

## Risk Score

| Score | Label | Meaning |
|-------|-------|---------|
| 0–29  | 🟢 LOW | Conservative portfolio |
| 30–59 | 🟡 MEDIUM | Moderate risk exposure |
| 60+   | 🔴 HIGH | High risk — review positions |

---

## Roadmap

- [x] v0.5 — CLI flags
- [x] v0.6 — trend tracking
- [x] v0.7 — risk alerts
- [x] v0.8 — multi-wallet scanning
- [ ] v1.0 — REST API

---

## Tech stack

Python · Dune SIM API · JSON · argp
