from kafka import KafkaProducer
import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/solicitud', methods=['POST'])
def create_solicitud():
    solicitud = request.json
    solicitud['id'] = int(time.time())
    producer.send('solicitud_topic', solicitud)
    return jsonify(solicitud), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
