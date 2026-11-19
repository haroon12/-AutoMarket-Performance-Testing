
import argparse
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def format_value(value):
    if isinstance(value, float):
        return f"{value:,.3f}"
    return str(value)


def collect_checks(group):
    """Collect checks recursively from the k6 root group."""
    results = []

    for check_name, check_data in group.get("checks", {}).items():
        results.append({
            "name": check_name,
            "passes": check_data.get("passes", 0),
            "fails": check_data.get("fails", 0),
        })

    for child in group.get("groups", {}).values():
        results.extend(collect_checks(child))

    return results


def evaluate_threshold(metric, expression):
    """
    Evaluate common k6 threshold expressions using actual measurements.
    For Rate metrics, k6 exports the measured rate under 'value'.
    """

    match = re.fullmatch(
        r"\s*(avg|min|med|max|p\(\d+(?:\.\d+)?\)|rate|count|value)"
        r"\s*(<=|>=|<|>|==|!=)\s*(-?\d+(?:\.\d+)?)\s*",
        expression
    )

    if not match:
        return None

    selector, operator, limit = match.groups()

    # k6 Rate metrics such as http_req_failed store their rate in "value".
    if selector == "rate":
        actual = metric.get("rate", metric.get("value"))
    else:
        actual = metric.get(selector)

    if actual is None:
        return None

    try:
        actual = float(actual)
        limit = float(limit)
    except (TypeError, ValueError):
        return None

    operations = {
        "<": actual < limit,
        "<=": actual <= limit,
        ">": actual > limit,
        ">=": actual >= limit,
        "==": actual == limit,
        "!=": actual != limit,
    }

    return operations[operator]


def generate_report(input_file, output_file, test_name):

    with open(input_file, "r", encoding="utf-8") as file:
        summary = json.load(file)

    metrics = summary.get("metrics", {})

    # Collect checks
    checks = collect_checks(summary.get("root_group", {}))

    passed_checks = sum(item["passes"] for item in checks)
    failed_checks = sum(item["fails"] for item in checks)

    check_rows = ""

    for item in checks:
        status = "PASSED" if item["fails"] == 0 else "FAILED"
        css_class = "pass" if item["fails"] == 0 else "fail"

        check_rows += f"""
        <tr>
            <td>{html.escape(item["name"])}</td>
            <td>{item["passes"]}</td>
            <td>{item["fails"]}</td>
            <td class="{css_class}">{status}</td>
        </tr>
        """

    # Performance metrics
    selected_metrics = [
        "http_reqs",
        "http_req_duration",
        "http_req_failed",
        "http_req_waiting",
        "http_req_connecting",
        "http_req_tls_handshaking",
        "iteration_duration",
        "iterations",
        "vus",
        "vus_max",
        "data_received",
        "data_sent",
    ]

    metric_rows = ""

    for metric_name in selected_metrics:
        metric = metrics.get(metric_name)

        if not metric:
            continue

        # Display HTTP failure rate clearly as a percentage.
        if metric_name == "http_req_failed":
            failure_rate = metric.get("value")

            if failure_rate is not None:
                metric_rows += f"""
                <tr>
                    <td>HTTP failure rate</td>
                    <td>percentage</td>
                    <td>{float(failure_rate) * 100:.2f}%</td>
                </tr>
                """
            continue

        for measurement, value in metric.items():

            if measurement == "thresholds":
                continue

            if measurement in ("passes", "fails"):
                continue

            if isinstance(value, (int, float)):
                metric_rows += f"""
                <tr>
                    <td>{html.escape(metric_name)}</td>
                    <td>{html.escape(measurement)}</td>
                    <td>{format_value(value)}</td>
                </tr>
                """

    # Evaluate thresholds from actual measurements
    threshold_rows = []
    failed_thresholds = []
    unevaluated_thresholds = []

    for metric_name, metric in metrics.items():

        for expression in metric.get("thresholds", {}):

            result = evaluate_threshold(metric, expression)

            if result is None:
                status = "NOT EVALUATED"
                css_class = "warning"
                unevaluated_thresholds.append(
                    f"{metric_name}: {expression}"
                )

            else:
                status = "PASSED" if result else "FAILED"
                css_class = "pass" if result else "fail"

                if not result:
                    failed_thresholds.append(
                        f"{metric_name}: {expression}"
                    )

            threshold_rows.append(f"""
            <tr>
                <td>{html.escape(metric_name)}</td>
                <td>{html.escape(expression)}</td>
                <td class="{css_class}">{status}</td>
            </tr>
            """)

    # Overall status
    if failed_checks > 0 or failed_thresholds:
        overall_status = "FAILED"

    elif unevaluated_thresholds:
        overall_status = "REVIEW REQUIRED"

    else:
        overall_status = "PASSED"

    status_class = (
        "pass" if overall_status == "PASSED"
        else "fail" if overall_status == "FAILED"
        else "warning"
    )

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
.warning {{ color: #b45309; }}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th, td {{
    padding: 11px;
    text-align: left;
    border-bottom: 1px solid #e5e7eb;
}}

th {{
    background: #f3f4f6;
}}

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

    <p class="status {status_class}">
        Test status: {overall_status}
    </p>
</header>

<div class="card">
    <h2>Test Summary</h2>
    <p>Checks passed: {passed_checks}</p>
    <p>Checks failed: {failed_checks}</p>
    <p>Total checks: {passed_checks + failed_checks}</p>
</div>

<div class="card">
    <h2>Check Results</h2>

    <table>
        <tr>
            <th>Check</th>
            <th>Passed</th>
            <th>Failed</th>
            <th>Result</th>
        </tr>
        {check_rows}
    </table>
</div>

<div class="card">
    <h2>Performance Metrics</h2>

    <table>
        <tr>
            <th>Metric</th>
            <th>Measurement</th>
            <th>Value</th>
        </tr>
        {metric_rows}
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
        {''.join(threshold_rows)}
    </table>
</div>

<div class="card">
    <h2>Observations</h2>
    <p>
        Review response times, HTTP failures, checks and thresholds
        before drawing performance conclusions.
    </p>
    <p>
        A passed report indicates that the evaluated checks and
        configured thresholds passed for this test run.
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
    print(f"Test status: {overall_status}")
    print(f"Checks passed: {passed_checks}")
    print(f"Checks failed: {failed_checks}")


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
