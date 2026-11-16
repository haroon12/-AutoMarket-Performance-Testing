# AutoMarket Performance Testing

A performance testing project built using **Grafana k6** and JavaScript to evaluate the responsiveness, stability, and performance of the AutoMarket web application's homepage.

## Project Overview

This project covers three types of performance testing:

- Smoke Testing
- Load Testing
- Stress Testing

## Project Structure

```text
AutoMarket-Performance-Testing/
│
├── Config/
│   └── .env
│
├── Scripts/
│   ├── homepage.js
│   ├── homepage-load.js
│   └── homepage-stress.js
│
├── .gitignore
└── README.md
```

## Testing Scenarios

### 1. Smoke Testing

File: `Scripts/homepage.js`

- Validates homepage availability.
- Verifies HTTP status code 200.
- Checks response time below 1000 ms.
- Validates that the response body is not empty.
- Executes one virtual user and one iteration.

### 2. Load Testing

File: `Scripts/homepage-load.js`

Includes six load testing scenarios:

| Test ID | Scenario |
|---|---|
| LT-01 | Gradual Load Testing |
| LT-02 | Constant Load Testing |
| LT-03 | Ramp-up Load Testing |
| LT-04 | Peak Load Testing |
| LT-05 | Low Load Testing |
| LT-06 | Step Load Testing |

Load testing thresholds:
- 95th percentile response time below 2000 ms.
- HTTP request failure rate below 1%.

### 3. Stress Testing

File: `Scripts/homepage-stress.js`

Includes four stress testing scenarios:

| Test ID | Scenario |
|---|---|
| ST-01 | Gradual Stress Testing |
| ST-02 | Spike Stress Testing |
| ST-03 | Sustained Stress Testing |
| ST-04 | Recovery Testing |

Stress testing thresholds:
- 95th percentile response time below 3000 ms.
- HTTP request failure rate below 5%.

## Prerequisites

- Grafana k6
- JavaScript knowledge
- Access to the authorized AutoMarket test environment

## Configuration

The scripts require a `BASE_URL` environment variable.

Set the environment variable when executing k6:

```powershell
$env:BASE_URL="https://your-test-environment.com"
```

Do not commit credentials or private environment configuration to GitHub.

## Execution Commands

### Run Smoke Test

```bash
k6 run Scripts/homepage.js
```

### Run Load Tests

```bash
k6 run Scripts/homepage-load.js
```

### Run Stress Tests

```bash
k6 run Scripts/homepage-stress.js
```

## Performance Metrics

The framework validates and measures:

- HTTP response time
- 95th percentile response time (p95)
- HTTP request failure rate
- HTTP status codes
- Virtual user execution
- Response body validation

## Tools & Technologies

- Grafana k6
- JavaScript
- Visual Studio Code
- PowerShell

## Author

Haroon Rasheed

QA Engineer | Software Quality Assurance | Performance Testing | Test Automation