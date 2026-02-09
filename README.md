# Feb_9th_2026_Lambda_RDS_Connect_Public
Lambda-RDS Connect and Create DB and Table


🚀 AWS Lambda + RDS (MySQL) Public Connection Setup

This project demonstrates how to connect AWS Lambda (Python 3.11) to Amazon RDS MySQL (Public Access) using a custom PyMySQL Lambda Layer, while avoiding the cryptography dependency issue.

📌 1️⃣ Create IAM Role for Lambda

Go to IAM → Roles → Create Role

Select:

Trusted entity type: AWS Service

Use case: Lambda

Attach policy:

AdministratorAccess (for demo purposes)

Click Create Role

📌 2️⃣ Create RDS (MySQL)

Go to RDS → Create Database

Select:

Engine: MySQL

Configure:

DB Name

Master Username

Master Password

Set:

Public Access: Yes (for demo setup)

Click Create Database

📌 3️⃣ Update Security Group (Important)

After RDS is created:

Go to RDS → Connectivity & Security

Click associated Security Group

Edit Inbound Rules

Add rule:

Type	Port	Source
MySQL/Aurora	3306	0.0.0.0/0

⚠️ Note: This is only for public testing.
In production, restrict access properly.

🔐 Fix MySQL Authentication (Avoid cryptography Dependency)

MySQL 8 uses caching_sha2_password by default, which requires the cryptography package in Lambda.

To avoid this dependency, change authentication method to mysql_native_password.

Step 1: Connect to RDS

Connect using:

EC2

MySQL Workbench

CloudShell

Example:

mysql -h your-rds-endpoint -u admin -p

Step 2: Check Authentication Plugin
SELECT user, host, plugin FROM mysql.user;


You will likely see:

caching_sha2_password

Step 3: Change Authentication Method
ALTER USER 'your_db_user'@'%' 
IDENTIFIED WITH mysql_native_password 
BY 'your_password';

FLUSH PRIVILEGES;


Replace:

your_db_user

your_password

Step 4: Redeploy Lambda

After updating authentication:

Redeploy Lambda

No need for cryptography

Only pymysql is required

📦 Create PyMySQL Lambda Layer

Go to Lambda → Layers

Click Create Layer

Upload pymysql_layer.zip

Example Layer File:

https://github.com/rakesharveti/Feb_9th_2026_Lambda_RDS_Connect_Public/blob/main/pymysql_layer.zip


Create Layer

Copy the Layer ARN

⚙️ Create Lambda Function

Go to Lambda → Create Function

Select:

Author from scratch

Runtime: Python 3.11

Attach previously created IAM Role

Paste your Lambda code

Click Deploy

➕ Attach PyMySQL Layer

Go to:

Lambda → Configuration → Layers


Click Add Layer

Select custom layer

Choose PyMySQL layer

Add

🌍 Configure Environment Variables

Go to:

Lambda → Configuration → Environment Variables


Add required keys:

Key	Value (Example)
DB_HOST	your-rds-endpoint
DB_NAME	your-db-name
DB_PASS	your-password
DB_USER	your-username

Example:

DB_HOST = lambda-rds-connect.cczc0aqowmei.us-east-1.rds.amazonaws.com
DB_NAME = Rakesh
DB_PASS = admin123
DB_USER = admin


⚠️ Use your own credentials.

⏱ Update Lambda Timeout

Go to:

Configuration → General Configuration


Set:

Timeout: 5 minutes

🏗 Architecture Flow
Lambda (Python 3.11)
        ↓
PyMySQL Layer
        ↓
RDS MySQL (Public)
        ↓
Authentication using mysql_native_password

✅ Summary

Created IAM Role for Lambda

Created RDS MySQL (Public Access)

Updated Security Group (Port 3306)

Fixed MySQL authentication method

Created and attached PyMySQL Layer

Configured environment variables

Successfully connected Lambda to RDS
