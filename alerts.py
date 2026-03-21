def check_alerts(unified_risk: float, last_report: dict | None, tokens: list) -> list[str]:
    alerts = []

    # Alert 1: Risk Spike
    if last_report:
        prev_risk = last_report["scores"].get("unified_risk", unified_risk)
        delta = round(unified_risk - prev_risk, 2)
        if delta > 10:
            alerts.append(f"⚠️  RISK SPIKE DETECTED (+{delta})")

    # Alert 2: High Risk Portfolio
    if unified_risk >= 60:
        alerts.append(f"🚨 HIGH RISK PORTFOLIO (risk: {unified_risk})")

    # Alert 3: Concentration Risk
    for token in tokens:
        if token["percent"] > 50:
            alerts.append(f"⚠️  CONCENTRATION RISK ({token['symbol']} {token['percent']}%)")

    return alerts
