\# Production Log Monitoring System



An event-driven, serverless log monitoring system built on AWS that

analyzes application logs in near real-time to detect error patterns,

calculate metrics, and trigger automated alerts.



\## Architecture



App Logs → S3 (logs/raw/) → Lambda (triggered automatically)

↓

┌──────────────────┐

│  Parse Logs      │

│  Detect Errors   │

│  Calculate Rate  │

│  Find Top Error  │

└──────────────────┘

↓

┌─────────────────────────┐

│                         │

SNS Alert               RDS MySQL

(Email sent)           (Metrics stored)



\## Features



\- Event-driven processing — S3 upload automatically triggers Lambda, no manual intervention

\- Configurable thresholds — error rate limits stored in a config file, not hardcoded

\- Real-time alerting — instant SNS email alert when error rate exceeds threshold

\- Error pattern detection — automatically identifies the most frequently occurring error

\- Structured metrics storage — all results saved to RDS MySQL for trend analysis

\- Fully serverless — no servers to manage, scales automatically



\## Tech Stack



AWS S3 | AWS Lambda | Amazon SNS | Amazon RDS | CloudWatch | Python | GitHub | Version control 



\## Project Structure



production-log-monitoring-system/

├── lambda/

│   └── log\_processor.py       # Core Lambda function

├── config/

│   └── config.json            # Configurable error thresholds

├── sample\_logs/

│   └── app\_logs.txt           # Sample log file for testing

├── sql/

│   └── schema.sql             # RDS MySQL table schema

└── README.md



\## How It Works



1\. Application logs are uploaded to S3 under logs/raw/

2\. The S3 upload event automatically triggers the Lambda function

3\. Lambda reads and parses the log file line by line

4\. Calculates total logs, error count, warning count, and error rate

5\. Identifies the most frequently occurring error message

6\. Loads the error threshold dynamically from config/config.json stored in S3

7\. If error rate exceeds the threshold, SNS instantly sends an email alert

8\. Full metrics summary is printed to CloudWatch for observability

9\. Metrics are stored in RDS MySQL for downstream dashboarding

