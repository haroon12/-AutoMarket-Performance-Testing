# AutoMarket Performance Testing Framework

A performance testing framework developed using **Grafana k6 and JavaScript** to evaluate the performance, responsiveness, stability, and reliability of the AutoMarket web application.

The project includes Smoke, Load, Stress, Breakpoint, Recovery, Soak, and Login Smoke testing.

## Project Overview

This framework is designed to validate application performance under different workload conditions and identify potential performance bottlenecks.

### Testing Coverage

| Testing Type | Description |
|---|---|
| Homepage Smoke Testing | Validates homepage availability and basic response behavior |
| Load Testing | Evaluates application performance under expected workloads |
| Stress Testing | Evaluates system behavior under increased workloads |
| Breakpoint Testing | Explores the workload at which performance begins to degrade |
| Recovery Testing | Evaluates application recovery after increased load |
| Soak Testing | Evaluates application stability under sustained load |
| Login Smoke Testing | Validates the basic login workflow |

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
│   ├── homepage-stress.js
│   ├── homepage-breakpoint.js
│   ├── homepage-recovery.js
│   ├── homepage-soak.js
│   └── login-smoke.js
│
├── .gitignore
└── README.md
```

## Test Scripts

### 1. Homepage Smoke Testing

**File:** `Scripts/homepage.js`

Validates basic homepage functionality and availability.

Checks include:
- HTTP status code 200
- Response time below 1000 ms
- Response body is not empty
- Single virtual user execution

### 2. Homepage Load Testing

**File:** `Scripts/homepage-load.js`

Includes six load testing scenarios:

| Test ID | Scenario |
|---|---|
| LT-01 | Gradual Load Testing |
| LT-02 | Constant Load Testing |
| LT-03 | Ramp-up Load Testing |
| LT-04 | Peak Load Testing |
| LT-05 | Low Load Testing |
| LT-06 | Step Load Testing |

**Performance Thresholds:**
- 95th percentile response time below 2000 ms
- HTTP request failure rate below 1%

### 3. Homepage Stress Testing

**File:** `Scripts/homepage-stress.js`

Includes four stress testing scenarios:

| Test ID | Scenario |
|---|---|
| ST-01 | Gradual Stress Testing |
| ST-02 | Spike Stress Testing |
| ST-03 | Sustained Stress Testing |
| ST-04 | Recovery Testing |

**Performance Thresholds:**
- 95th percentile response time below 3000 ms
- HTTP request failure rate below 5%

### 4. Homepage Breakpoint Testing

**File:** `Scripts/homepage-breakpoint.js`

Designed to investigate the workload level at which application performance begins to degrade.

### 5. Homepage Recovery Testing

**File:** `Scripts/homepage-recovery.js`

Designed to evaluate application behavior and recovery after increased workload.

### 6. Homepage Soak Testing

**File:** `Scripts/homepage-soak.js`

Designed to evaluate application stability during sustained workload over an extended period.

### 7. Login Smoke Testing

**File:** `Scripts/login-smoke.js`

Designed to validate the basic login workflow and its expected behavior.

## Prerequisites

- Grafana k6
- JavaScript
- Visual Studio Code
- PowerShell
- Access to an authorized test environment

## Environment Configuration

The test scripts use the `BASE_URL` environment variable.

Configure your target environment in PowerShell:

```powershell
$env:BASE_URL="https://your-test-environment.com"
```

Replace the example with your authorized test environment URL.

**Important:** Keep credentials and sensitive configuration in your local `.env` file. Never upload actual credentials to GitHub.

## Running Performance Tests

Run the following commands from the project root directory.

### Homepage Smoke Test

```bash
k6 run Scripts/homepage.js
```

### Homepage Load Testing

```bash
k6 run Scripts/homepage-load.js
```

### Homepage Stress Testing

```bash
k6 run Scripts/homepage-stress.js
```

### Homepage Breakpoint Testing

```bash
k6 run Scripts/homepage-breakpoint.js
```

### Homepage Recovery Testing

```bash
k6 run Scripts/homepage-recovery.js
```

### Homepage Soak Testing

```bash
k6 run Scripts/homepage-soak.js
```

### Login Smoke Testing

```bash
k6 run Scripts/login-smoke.js
```

## Performance Metrics

The framework uses k6 metrics and checks to evaluate:

- HTTP response time
- 95th percentile response time (p95)
- HTTP request failure rate
- HTTP status codes
- Virtual user execution
- Response body validation
- Application stability under different workloads

## Tools & Technologies

- **Performance Testing:** Grafana k6
- **Programming Language:** JavaScript
- **IDE:** Visual Studio Code
- **Version Control:** Git and GitHub
- **Terminal:** Windows PowerShell

## Author

**Haroon Rasheed**

Software Quality Assurance Engineer

Skills: Manual Testing | Automation Testing | Performance Testing | Selenium | Python | Pytest | JavaScript | Grafana k6

GitHub: https://github.com/haroon12