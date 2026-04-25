CREATE DATABASE IF NOT EXISTS log_monitoring_db;
USE log_monitoring_db;

CREATE TABLE log_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    total_logs INT,
    errors INT,
    warnings INT,
    error_rate FLOAT,
    top_error VARCHAR(255)
);