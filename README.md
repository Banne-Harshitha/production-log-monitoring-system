## Production Log Monitoring System

An event-driven, serverless log monitoring system built on AWS that analyzes
application logs in near real-time to detect error patterns, calculate metrics,
and trigger automated alerts.

---

## Architecture
App Logs
|
v
AWS S3 (logs/raw/)
|
v
AWS Lambda
|-- Parse Logs
|
|-- Detect Errors
|
|-- Calculate Error Rate
|
|-- Find Top Error
|
+-------------------+
|                   |
v                   v
Amazon SNS          Amazon RDS
(Email Alert)       (Metrics Stored)

---

## Features

- Event-driven processing — S3 upload automatically triggers Lambda, no manual intervention
- Configurable thresholds — error rate limits stored in a config file, not hardcoded
- Real-time alerting — instant SNS email alert when error rate exceeds threshold
- Error pattern detection — automatically identifies the most frequently occurring error
- Structured metrics storage — all results saved to RDS MySQL for trend analysis
- Fully serverless — no servers to manage, scales automatically

---

## Tech Stack

| Service | Purpose |
|---------|---------|
| AWS S3 | Log file storage (raw and processed) |
| AWS Lambda | Serverless log processing engine |
| Amazon SNS | Real-time email alerting |
| Amazon RDS | Structured metrics storage (MySQL) |
| Amazon CloudWatch | Logs and observability |
| Python 3.12 | Core processing logic |
| GitHub | Version control |

---

## Project Structure
production-log-monitoring-system/
|
|-- lambda/
|   |-- log_processor.py       (Core Lambda function)
|
|-- config/
|   |-- config.json            (Configurable error thresholds)
|
|-- sample_logs/
|   |-- app_logs.txt           (Sample log file for testing)
|
|-- sql/
|   |-- schema.sql             (RDS MySQL table schema)
|
|-- README.md

---

## How It Works

1. Application logs are uploaded to S3 under logs/raw/
2. The S3 upload event automatically triggers the Lambda function
3. Lambda reads and parses the log file line by line
4. Calculates total logs, error count, warning count, and error rate
5. Identifies the most frequently occurring error message
6. Loads the error threshold dynamically from config/config.json stored in S3
7. If error rate exceeds the threshold, SNS instantly sends an email alert
8. Full metrics summary is printed to CloudWatch for observability
9. Metrics are stored in RDS MySQL for downstream dashboarding

---

## S3 Bucket Structure

mdm-log-monitoring-bucket/
|
|-- logs/
|   |-- raw/                   (upload log files here)
|   |-- processed/             (for future processed output)
|
|-- config/
|   |-- config.json            (threshold configuration)

---

## Database Schema

```sql
CREATE TABLE log_metrics (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    timestamp   DATETIME,
    total_logs  INT,
    errors      INT,
    warnings    INT,
    error_rate  FLOAT,
    top_error   VARCHAR(255)
);
```

---

## Project Status
- S3 bucket configured
- IAM role created
- Lambda function deployed
- SNS alerts working
- RDS database connected
- End-to-end test passed — alert email received

---

## Future Improvements
- Auto-insert metrics from Lambda into RDS after each run
- Power BI dashboard for error trend visualization
- Kinesis Data Streams for real-time log streaming
- CI/CD pipeline using GitHub Actions
- Infrastructure as Code using Terraform