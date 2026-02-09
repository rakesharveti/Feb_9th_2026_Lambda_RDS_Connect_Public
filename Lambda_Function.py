import os
import pymysql

# Database settings from environment variables
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
new_db_name = os.environ['DB_NAME']
table_name = "mytable"

# Establish a database connection
def connect_to_rds():
    return pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        connect_timeout=5,   # added timeout (good practice)
        cursorclass=pymysql.cursors.DictCursor
    )

# Lambda function handler
def lambda_handler(event, context):
    connection = None  # 🔥 IMPORTANT FIX

    try:
        connection = connect_to_rds()

        with connection.cursor() as cursor:

            # Create database if not exists
            create_db_sql = f"CREATE DATABASE IF NOT EXISTS {new_db_name};"
            cursor.execute(create_db_sql)

            # Select the new database
            cursor.execute(f"USE {new_db_name};")

            # Create table if not exists
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_sql)

            connection.commit()

            print(f"Database '{new_db_name}' and table '{table_name}' created successfully.")

            return {
                'statusCode': 200,
                'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
            }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        if connection is not None:   # 🔥 SAFE CLOSE
            connection.close()
