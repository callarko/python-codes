import os
from flask import Flask, jsonify
import snowflake.connector
import getpass

app = Flask(__name__)

def create_snowflake_connection():
    account = os.getenv('SNOWFLAKE_ACCOUNT') or input('Enter Snowflake account: ')
    user = os.getenv('SNOWFLAKE_USER') or input('Enter Snowflake user: ')
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE') or input('Enter Snowflake warehouse: ')
    database = os.getenv('SNOWFLAKE_DATABASE') or input('Enter Snowflake database: ')
    role = os.getenv('SNOWFLAKE_ROLE') or input('Enter Snowflake role: ')
    access_token = os.getenv('SNOWFLAKE_ACCESS_TOKEN') or getpass.getpass('Enter Snowflake access token: ')

    conn = snowflake.connector.connect(
        user=user,
        host=account,
        token=access_token,
        role=role,
        account=account,
        warehouse=warehouse,
        database=database,
        authenticator='oauth',
        client_session_keep_alive=True,
        max_connection_pool=100,
        login_timeout=300,
        network_timeout=300,
        socket_timeout=300
    )
    return conn

@app.route('/query')
def run_query():
    conn = create_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
