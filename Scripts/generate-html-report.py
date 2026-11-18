
import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path


def format_value(value):
    if isinstance(value, float):
        return f"{value:,.3f}"
    return str(value)


def generate_report(input_file, output_file, test_name):
    with open(input_file, "r", encoding="utf-8") as file:
        summary = json.load(file)

    metrics = summary.get("metrics", {})

    failed_thresholds = []
    threshold_rows = []

    for metric_name, metric in metrics.items():
        for threshold, passed in metric.get("thresholds", {}).items():
            threshold_rows.append((metric_name, threshold, passed))
            if not passed:
                failed_thresholds.append(
                    f"{metric_name}: {threshold}"
                )

    overall_status = "PASSED" if not failed_thresholds else "FAILED"

    metric_rows = []

    for metric_name, metric in metrics.items():
        values = metric.get("values", {})
        if not values:
            continue

        for value_name, value in values.items():
            metric_rows.append(
                (metric_name, value_name, format_value(value))
            )

    threshold_html = "".join(
        f"""
        <tr>
            <td>{html.escape(name)}</td>
            <td>{html.escape(threshold)}</td>
            <td class="{'pass' if passed else 'fail'}">
                {"PASSED" if passed else "FAILED"}
            </td>
        </tr>
        """
        for name, threshold, passed in threshold_rows
    )

    metric_html = "".join(
        f"""
        <tr>
            <td>{html.escape(name)}</td>
            <td>{html.escape(value_name)}</td>
            <td>{html.escape(value)}</td>
        </tr>
        """
        for name, value_name, value in metric_rows
    )

    checks = metrics.get("checks", {}).get("values", {})
    passed_checks = checks.get("passes", 0)
    failed_checks = checks.get("fails", 0)

    generated_at = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(test_name)} - Performance Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    color: #1f2937;
    margin: 0;
    padding: 25px;
}}
.container {{
    max-width: 1100px;
    margin: auto;
}}
header {{
    background: #111827;
    color: white;
    padding: 25px;
    border-radius: 10px;
}}
.card {{
    background: white;
    padding: 20px;
    margin-top: 20px;
    border-radius: 10px;
    overflow-x: auto;
}}
.status {{
    font-size: 22px;
    font-weight: bold;
}}
.pass {{ color: #15803d; }}
.fail {{ color: #b91c1c; }}
table {{
    width: 100%;
    border-collapse: collapse;
}}
th, td {{
    padding: 11px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}}
th {{ background: #f3f4f6; }}
footer {{
    margin-top: 25px;
    color: #64748b;
    font-size: 13px;
}}
</style>
</head>
<body>
<div class="container">

<header>
    <h1>AutoMarket Performance Testing</h1>
    <h2>{html.escape(test_name)}</h2>
    <p>Target: PakWheels Homepage</p>
    <p>Generated: {generated_at}</p>
    <p class="status {'pass' if overall_status == 'PASSED' else 'fail'}">
        Test status: {overall_status}
    </p>
</header>

<div class="card">
    <h2>Test Summary</h2>
    <p>Checks passed: {passed_checks}</p>
    <p>Checks failed: {failed_checks}</p>
</div>

<div class="card">
    <h2>Performance Metrics</h2>
    <table>
        <tr>
            <th>Metric</th>
            <th>Measurement</th>
            <th>Value</th>
        </tr>
        {metric_html}
    </table>
</div>

<div class="card">
    <h2>Threshold Results</h2>
    <table>
        <tr>
            <th>Metric</th>
            <th>Threshold</th>
            <th>Result</th>
        </tr>
        {threshold_html}
    </table>
</div>

<div class="card">
    <h2>Observations</h2>
    <p>
        Review response times, request failures, checks and thresholds
        before drawing performance conclusions.
    </p>
    <p>
        A passed report means the configured k6 thresholds passed.
        It does not independently establish overall production capacity.
    </p>
</div>

<footer>
    AutoMarket Performance Testing | Generated using k6 summary data
</footer>

</div>
</body>
</html>
"""

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"HTML report generated: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test-name", required=True)

    args = parser.parse_args()

    generate_report(
        args.input,
        args.output,
        args.test_name
    )
