from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Database connection settings
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:88005553535@db/metrics_db')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/metrics', methods=['POST'])
def ingest_metrics():
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO user_metrics (
                user_id, session_id, timestamp, talked_time,
                microphone_used, speaker_used, voice_sentiment,
                device_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data['user_id'], data['session_id'], datetime.now(),
                data.get('talked_time'), data.get('microphone_used'),
                data.get('speaker_used'), data.get('voice_sentiment'),
                data.get('device_type')
            )
        )

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"status": "failure", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)