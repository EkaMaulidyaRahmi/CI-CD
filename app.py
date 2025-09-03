from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

def wait_for_db(host, user, password, database, retries=5, delay=3):
    for i in range(retries):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            conn.close()
            return True
        except:
            time.sleep(delay)
    return False

@app.route('/')
def hello():
    db_host = os.getenv("DATABASE_HOST", "db")
    db_user = os.getenv("DATABASE_USER", "root")
    db_pass = os.getenv("DATABASE_PASSWORD", "root")
    db_name = os.getenv("DATABASE_NAME", "mydb")

    if not wait_for_db(db_host, db_user, db_pass, db_name):
        return "Error: Cannot connect to MySQL database"

    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE();")
    record = cursor.fetchone()
    return f"Hello from Flask! Connected to MySQL database: {record}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
