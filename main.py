import requests
import os
from dotenv import load_dotenv

load_dotenv()

REGISTRY = {
    "ETH":   {"risk_level": 10},
    "WETH":  {"risk_level": 10},
    "WBTC":  {"risk_level": 20},
    "USDC":  {"risk_level": 25},
    "USDT":  {"risk_level": 30},
    "DAI":   {"risk_level": 20},
    "ARB":   {"risk_level": 40},
    "OP":    {"risk_level": 40},
    "MATIC": {"risk_level": 40},
    "CRV":   {"risk_level": 45},
    "DEFAULT": {"risk_level": 50},
}

CHAIN_RISK = {
    "ethereum": 10,
    "arbitrum": 25,
    "optimism": 25,
    "polygon":  35,
    "bsc":      45,
}

WALLET = "0x6cd68e8f04490cd1a5a21cc97cc8bc15b47dc9eb"
headers = {"X-SIM-API-Key": os.getenv("SIM_API_KEY")}

response = requests.get(
    f"https://api.sim.dune.com/v1/evm/balances/{WALLET}?chain_ids=1,42161,10,137",
    headers=headers
).json()

balances = response["balances"]
balances = [t for t in balances if t.get("value_usd") is not None]
total = sum(t["value_usd"] for t in balances)

CR = PR = CoR = ChR = 0.0

for token in balances:
    sym   = (token.get("symbol") or token.get("token_symbol") or "DEFAULT").upper()
    chain = (token.get("chain") or "unknown").lower()
    info  = REGISTRY.get(sym, REGISTRY["DEFAULT"])
    pct   = token["value_usd"] / total

    CR  += info["risk_level"] * pct
    PR  += info["risk_level"] * pct
    CoR += 100 * pct if pct > 0.5 else 0
    ChR += CHAIN_RISK.get(chain, 50) * pct

    print(f"[{sym}] chain={chain} | {round(pct*100,2)}% | risk={info['risk_level']}")

portfolio_risk = 0.35*CR + 0.25*PR + 0.25*CoR + 0.15*ChR

print(f"\nCR:  {round(CR,2)}")
print(f"PR:  {round(PR,2)}")
print(f"CoR: {round(CoR,2)}")
print(f"ChR: {round(ChR,2)}")
print(f"==> Portfolio Risk Score: {round(portfolio_risk,2)}")

import json
from datetime import datetime, timezone

report = {
    "wallet": WALLET,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "scores": {
        "CR": round(CR, 2),
        "PR": round(PR, 2),
        "CoR": round(CoR, 2),
        "ChR": round(ChR, 2),
        "portfolio_risk": round(portfolio_risk, 2)
    },
    "risk_label": "🟢 LOW" if portfolio_risk < 30 else "🟡 MEDIUM" if portfolio_risk < 60 else "🔴 HIGH",
    "tokens": []
}

for token in balances:
    sym = (token.get("symbol") or "DEFAULT").upper()
    report["tokens"].append({
        "symbol": sym,
        "chain": token.get("chain", "unknown"),
        "value_usd": round(token["value_usd"], 4),
        "percent": round((token["value_usd"] / total) * 100, 2)
    })

with open("risk_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"\n✅ Report saved → risk_report.json")
