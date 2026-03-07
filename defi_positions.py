import requests
import os
from dotenv import load_dotenv

load_dotenv()

POSITION_RISK = {
    "Erc4626":   {"risk_level": 30, "label": "Vault"},
    "UniswapV2": {"risk_level": 45, "label": "LP V2"},
    "UniswapV3": {"risk_level": 50, "label": "LP V3"},
    "AaveV2":    {"risk_level": 35, "label": "Lending"},
    "AaveV3":    {"risk_level": 30, "label": "Lending"},
    "DEFAULT":   {"risk_level": 60, "label": "Unknown"},
}

def get_defi_positions(wallet: str, headers: dict) -> dict:
    response = requests.get(
        f"https://api.sim.dune.com/beta/evm/defi/positions/{wallet}",
        headers=headers
    ).json()

    positions = response.get("positions", [])
    positions = [p for p in positions if (p.get("usd_value") or 0) > 0]

    total_usd = sum(p.get("usd_value", 0) or 0 for p in positions)

    result = {
        "total_usd": total_usd,
        "positions": [],
        "DR_score": 0.0  # DeFi Risk score
    }

    if total_usd == 0:
        return result

    DR_total = 0.0

    for pos in positions:
        pos_type   = pos.get("type", "DEFAULT")
        usd_value  = pos.get("usd_value", 0) or 0
        pct        = usd_value / total_usd
        info       = POSITION_RISK.get(pos_type, POSITION_RISK["DEFAULT"])

        token0 = pos.get("token0_symbol", "?")
        token1 = pos.get("token1_symbol", "?")
        symbol = pos.get("token_symbol") or f"{token0}/{token1}"

        DR_total += info["risk_level"] * pct

        result["positions"].append({
            "type":      pos_type,
            "label":     info["label"],
            "symbol":    symbol,
            "chain_id":  pos.get("chain_id"),
            "usd_value": round(usd_value, 2),
            "percent":   round(pct * 100, 2),
            "risk":      info["risk_level"],
        })

        print(f"[{info['label']}] {symbol} | ${round(usd_value,2)} | {round(pct*100,2)}% | risk={info['risk_level']}")

    result["DR_score"] = round(DR_total, 2)
    return result


if __name__ == "__main__":
    WALLET = "0x3ddfa8ec3052539b6c9549f12cea2c295cff5296"
    headers = {"X-Sim-Api-Key": os.getenv("SIM_API_KEY")}
    result = get_defi_positions(WALLET, headers)
    print(f"\nDeFi positions total: ${round(result['total_usd'], 2)}")
    print(f"DR Score: {result['DR_score']}")
