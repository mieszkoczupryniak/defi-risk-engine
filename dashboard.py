import json
from datetime import datetime

with open("risk_report.json") as f:
    data = json.load(f)

scores = data["scores"]
tokens = data["tokens"]
wallet = data["wallet"]
timestamp = data["timestamp"]
risk_label = data["risk_label"]

top_tokens = [t for t in tokens if t["percent"] >= 0.5]
other_pct = sum(t["percent"] for t in tokens if t["percent"] < 0.5)
portfolio_value = sum(t["value_usd"] for t in tokens)

pie_labels = [f"{t['symbol']} ({t['chain']})" for t in top_tokens]
pie_values = [t["percent"] for t in top_tokens]
if other_pct > 0:
    pie_labels.append("Other")
    pie_values.append(round(other_pct, 2))

pie_labels_js = str(pie_labels).replace("'", '"')
pie_values_js = str(pie_values)

token_rows = ""
for t in tokens:
    if t["value_usd"] == 0:
        continue
    risk_val = 10
    from main import REGISTRY
    sym = t["symbol"].upper()
    risk_val = REGISTRY.get(sym, REGISTRY["DEFAULT"])["risk_level"]
    if risk_val <= 25:
        badge = f'<span class="badge low">LOW {risk_val}</span>'
    elif risk_val <= 55:
        badge = f'<span class="badge mid">MED {risk_val}</span>'
    else:
        badge = f'<span class="badge high">HIGH {risk_val}</span>'

    token_rows += f"""
    <tr>
        <td><b>{t['symbol']}</b></td>
        <td>{t['chain']}</td>
        <td>${t['value_usd']:,.4f}</td>
        <td>{t['percent']}%</td>
        <td>{badge}</td>
    </tr>"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DeFi Risk Report — {wallet[:8]}...</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e0e0e0; padding: 32px; }}
  h1 {{ font-size: 22px; color: #fff; margin-bottom: 4px; }}
  .sub {{ color: #888; font-size: 13px; margin-bottom: 32px; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }}
  .card {{ background: #1a1d27; border-radius: 12px; padding: 20px; }}
  .card h3 {{ font-size: 12px; color: #888; text-transform: uppercase; margin-bottom: 8px; }}
  .card .val {{ font-size: 28px; font-weight: 700; color: #fff; }}
  .card .label {{ font-size: 13px; color: #aaa; margin-top: 4px; }}
  .section {{ background: #1a1d27; border-radius: 12px; padding: 24px; margin-bottom: 24px; }}
  .section h2 {{ font-size: 15px; color: #ccc; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 1px; }}
  .risk-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }}
  .risk-item {{ background: #12141e; border-radius: 8px; padding: 14px; }}
  .risk-item .name {{ font-size: 11px; color: #666; margin-bottom: 4px; }}
  .risk-item .score {{ font-size: 22px; font-weight: 700; color: #7c83ff; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ text-align: left; padding: 10px 12px; color: #666; font-weight: 500; border-bottom: 1px solid #2a2d3a; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #1e2030; }}
  tr:hover td {{ background: #12141e; }}
  .badge {{ padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; }}
  .badge.low {{ background: #1a3a2a; color: #4caf82; }}
  .badge.mid {{ background: #3a2e1a; color: #f0a500; }}
  .badge.high {{ background: #3a1a1a; color: #f05050; }}
  .chart-wrap {{ max-width: 360px; margin: 0 auto; }}
</style>
</head>
<body>
<h1>🛡️ DeFi Risk Report</h1>
<div class="sub">Wallet: {wallet} &nbsp;|&nbsp; Generated: {timestamp[:19].replace('T',' ')} UTC</div>

<div class="grid">
  <div class="card">
    <h3>Portfolio Value</h3>
    <div class="val">${portfolio_value:,.2f}</div>
    <div class="label">across all chains</div>
  </div>
  <div class="card">
    <h3>Unified Risk Score</h3>
    <div class="val">{scores.get('unified_risk', scores['portfolio_risk'])}</div>
    <div class="label">{risk_label}</div>
  </div>
  <div class="card">
    <h3>Token Count</h3>
    <div class="val">{len([t for t in tokens if t['value_usd'] > 0])}</div>
    <div class="label">active positions</div>
  </div>
  <div class="card">
    <h3>DeFi Risk</h3>
    <div class="val">{scores.get('defi_risk', 0)}</div>
    <div class="label">positions score</div>
  </div>
</div>

<div class="section">
  <h2>Risk Breakdown</h2>
  <div class="risk-row">
    <div class="risk-item"><div class="name">CR — Concentration Risk</div><div class="score">{scores['CR']}</div></div>
    <div class="risk-item"><div class="name">PR — Protocol Risk</div><div class="score">{scores['PR']}</div></div>
    <div class="risk-item"><div class="name">CoR — Correlation Risk</div><div class="score">{scores['CoR']}</div></div>
    <div class="risk-item"><div class="name">ChR — Chain Risk</div><div class="score">{scores['ChR']}</div></div>
  </div>
</div>

<div class="section">
  <h2>Exposure Chart</h2>
  <div class="chart-wrap">
    <canvas id="pie"></canvas>
  </div>
</div>

<div class="section">
  <h2>Assets</h2>
  <table>
    <tr><th>Symbol</th><th>Chain</th><th>Value USD</th><th>% Portfolio</th><th>Risk</th></tr>
    {token_rows}
  </table>
</div>

<script>
new Chart(document.getElementById('pie'), {{
  type: 'doughnut',
  data: {{
    labels: {pie_labels_js},
    datasets: [{{ data: {pie_values_js}, backgroundColor: [
      '#7c83ff','#4caf82','#f0a500','#f05050','#a78bfa',
      '#38bdf8','#fb923c','#e879f9','#34d399','#f472b6','#94a3b8'
    ], borderWidth: 0 }}]
  }},
  options: {{ plugins: {{ legend: {{ labels: {{ color: '#aaa', font: {{ size: 11 }} }} }} }}, cutout: '65%' }}
}});
</script>
</body>
</html>"""

with open("report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ report.html saved")
