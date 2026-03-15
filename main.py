import requests
import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
from defi_positions import get_defi_positions

load_dotenv()

REGISTRY = {
    "ETH":     {"risk_level": 10},
    "WETH":    {"risk_level": 10},
    "WBTC":    {"risk_level": 20},
    "USDC":    {"risk_level": 15},
    "USDT":    {"risk_level": 20},
    "DAI":     {"risk_level": 15},
    "SUSD":    {"risk_level": 25},
    "AUSD":    {"risk_level": 25},
    "MKUSD":   {"risk_level": 20},
    "CRV":     {"risk_level": 45},
    "3CRV":    {"risk_level": 35},
    "ARB":     {"risk_level": 40},
    "OP":      {"risk_level": 40},
    "MATIC":   {"risk_level": 40},
    "SYRUP":   {"risk_level": 50},
    "PERQ":    {"risk_level": 55},
    "SHFL":    {"risk_level": 65},
    "DJIA":    {"risk_level": 60},
    "GBR":     {"risk_level": 70},
    "TREE":    {"risk_level": 70},
    "PEANUT":  {"risk_level": 80},
    "GME":     {"risk_level": 85},
    "DOGENES": {"risk_level": 85},
    "REMILIA": {"risk_level": 80},
    "TISM":    {"risk_level": 80},
    "SHINSHU": {"risk_level": 80},
    "DEFAULT": {"risk_level": 75},
}

CHAIN_RISK = {
    "ethereum": 10,
    "arbitrum": 25,
    "optimism": 25,
    "polygon":  35,
    "bsc":      45,
}

def load_last_report(wallet: str) -> dict | None:
    if not os.path.exists("reports"):
        return None
    slug = wallet[:8]
    files = sorted([f for f in os.listdir("reports") if slug in f])
    if len(files) < 2:
        return None
    with open(f"reports/{files[-2]}") as f:  # -2 bo -1 to właśnie zapisany
        return json.load(f)

WALLET = "0x6cd68e8f04490cd1a5a21cc97cc8bc15b47dc9eb"
headers     = {"X-SIM-API-Key": os.getenv("SIM_API_KEY")}
headers_sim = {"X-Sim-Api-Key": os.getenv("SIM_API_KEY")}

last_report = load_last_report(WALLET)

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

print("\n--- DeFi Positions ---")
defi = get_defi_positions(WALLET, headers_sim)
DR   = defi["DR_score"]

if defi["total_usd"] > 0:
    token_weight = total / (total + defi["total_usd"])
    defi_weight  = defi["total_usd"] / (total + defi["total_usd"])
    unified_risk = round(portfolio_risk * token_weight + DR * defi_weight, 2)
else:
    unified_risk = round(portfolio_risk, 2)

print(f"\n{'='*40}")
print(f"Token Portfolio Risk:  {round(portfolio_risk,2)}")
print(f"DeFi Positions Risk:   {DR}")
print(f"==> UNIFIED RISK v0.2: {unified_risk}")
print(f"{'='*40}")

# === TREND ===
if last_report:
    prev = last_report["scores"]
    def delta(key, curr):
        d = round(curr - prev.get(key, curr), 2)
        arrow = "▲" if d > 0 else "▼" if d < 0 else "="
        return f"{arrow} {abs(d)}"

    print(f"\n--- Trend vs last scan ({last_report['timestamp'][:16]}) ---")
    print(f"Unified Risk: {unified_risk}  ({delta('unified_risk', unified_risk)})")
    print(f"CR:           {round(CR,2)}  ({delta('CR', round(CR,2))})")
    print(f"CoR:          {round(CoR,2)}  ({delta('CoR', round(CoR,2))})")
    print(f"ChR:          {round(ChR,2)}  ({delta('ChR', round(ChR,2))})")
else:
    print("\n--- Trend: brak poprzedniego raportu ---")

# === SAVE ===
report = {
    "wallet": WALLET,
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "scores": {
        "CR": round(CR, 2),
        "PR": round(PR, 2),
        "CoR": round(CoR, 2),
        "ChR": round(ChR, 2),
        "portfolio_risk": round(portfolio_risk, 2),
        "defi_risk": DR,
        "unified_risk": unified_risk,
    },
    "risk_label": "🟢 LOW" if portfolio_risk < 30 else "🟡 MEDIUM" if portfolio_risk < 60 else "🔴 HIGH",
    "tokens": [
        {
            "symbol": (t.get("symbol") or "DEFAULT").upper(),
            "chain":  t.get("chain", "unknown"),
            "value_usd": round(t["value_usd"], 4),
            "percent":   round((t["value_usd"] / total) * 100, 2),
        }
        for t in balances
    ],
}

with open("risk_report.json", "w") as f:
    json.dump(report, f, indent=2)

os.makedirs("reports", exist_ok=True)
slug = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
history_path = f"reports/{slug}_{WALLET[:8]}.json"
with open(history_path, "w") as f:
    json.dump(report, f, indent=2)

print(f"\n✅ Report saved → risk_report.json")
print(f"📁 History saved → {history_path}")
