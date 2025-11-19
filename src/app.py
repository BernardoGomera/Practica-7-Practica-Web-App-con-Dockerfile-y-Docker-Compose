from flask import Flask
import os
import mysql.connector

app = Flask(__name__)

def get_db_now():
    host = os.environ.get('DB_HOST')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    database = os.environ.get('DB_NAME')
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            connection_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT NOW();")
        row = cursor.fetchone()
        if row:
            val = row[0]
            try:
                return val.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return str(val)
        return 'desconocida'
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


@app.route('/')
def index():
    now = get_db_now()
    return f"Hola mundo desde Docker + MySQL — Fecha y hora: {now}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
