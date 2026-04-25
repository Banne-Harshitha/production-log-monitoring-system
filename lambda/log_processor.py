import boto3
import json
import datetime

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_ARN"  # You'll replace this in Phase 5

def lambda_handler(event, context):
    try:
        # Step 1: Get the uploaded file info from the S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        print(f"Processing file: s3://{bucket}/{key}")

        # Step 2: Read the log file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        logs = response['Body'].read().decode('utf-8').splitlines()
        
        # Step 3: Parse logs
        error_count = 0
        warning_count = 0
        error_messages = {}

        for line in logs:
            if "ERROR" in line:
                error_count += 1
                msg = line.split("ERROR")[1].strip()
                error_messages[msg] = error_messages.get(msg, 0) + 1
            elif "WARNING" in line:
                warning_count += 1

        # Step 4: Calculate metrics
        total_logs = len(logs)
        error_rate = round(error_count / total_logs, 2) if total_logs > 0 else 0
        top_error = max(error_messages, key=error_messages.get) if error_messages else "None"

        # Step 5: Load threshold config from S3
        config_obj = s3.get_object(Bucket=bucket, Key="config/config.json")
        config = json.loads(config_obj['Body'].read().decode('utf-8'))
        threshold = config.get("error_threshold", 0.2)

        # Step 6: Build result summary
        result = {
            "timestamp": str(datetime.datetime.utcnow()),
            "file_processed": key,
            "total_logs": total_logs,
            "errors": error_count,
            "warnings": warning_count,
            "error_rate": error_rate,
            "top_error": top_error
        }

        print("Processed Result:", json.dumps(result, indent=2))

        # Step 7: Send alert if error rate exceeds threshold
        if error_rate > threshold:
            alert_message = (
                f"HIGH ERROR RATE ALERT\n\n"
                f"File: {key}\n"
                f"Error Rate: {error_rate * 100:.1f}%\n"
                f"Threshold: {threshold * 100:.1f}%\n"
                f"Total Errors: {error_count} out of {total_logs} logs\n"
                f"Top Error: {top_error}\n"
                f"Time: {result['timestamp']}"
            )
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Log Monitor Alert - High Error Rate Detected",
                Message=alert_message
            )
            print("Alert sent via SNS!")

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }

    except Exception as e:
        print(f"Lambda Error: {str(e)}")
        raise e