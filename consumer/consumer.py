import os
from kafka import KafkaConsumer, KafkaProducer
import json
import time
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from threading import Thread
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

consumer = KafkaConsumer(
    'solicitud_topic',
    bootstrap_servers='kafka:9092',
    group_id='solicitud_processors',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

solicitud_statuses = ["recibido", "procesando", "finalizado"]
solicitudes = {}
notificaciones = []  # Inicializa como una lista vacía

default_email = "default@example.com"  # Correo electrónico predeterminado

def process_solicitud(solicitud):
    for status in solicitud_statuses:
        solicitud['estado'] = status
        producer.send('solicitud_updates', solicitud)
        print(f"Proceso: {solicitud}")
        solicitudes[solicitud['id']] = solicitud
        print(f"Solicitud almacenada: {solicitud}")
        notify_solicitud(solicitud)
        if status != solicitud_statuses[-1]:
            time.sleep(5)  # Espera 5 segundos antes de cambiar de estado
        else:
            time.sleep(10)  # Espera 10 segundos antes de que se marque como finalizado
            print(f"Solicitud {solicitud['id']} finalizada")

def notify_solicitud(solicitud):
    msg = MIMEText(f"Solicitud {solicitud['id']} está ahora {solicitud['estado']}")
    msg['Subject'] = f"Solicitud Update: {solicitud['estado']}"
    msg['From'] = "prueba.sistedistri@gmail.com"

    # Verifica si la solicitud tiene información de correo electrónico, de lo contrario, usa el correo predeterminado
    correo_destino = solicitud.get('correo', default_email)
    msg['To'] = correo_destino

    smtp_user = "prueba.sistedistri@gmail.com"
    smtp_password = "axtm cfyo qmpd dqha"

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print(f"Notificado: {solicitud}")
        notificaciones.append({"id": solicitud['id'], "estado": solicitud['estado'], "correo": correo_destino, "timestamp": time.time()})  # Agrega la notificación a la lista

def consume_messages():
    for msg in consumer:
        solicitud = msg.value
        print(f"Mensaje recibido: {solicitud}")
        process_solicitud(solicitud)

@app.route('/solicitud/<int:solicitud_id>', methods=['GET'])
def get_solicitud(solicitud_id):
    solicitud = solicitudes.get(solicitud_id)
    if solicitud:
        return jsonify(solicitud)
    else:
        return jsonify({'error': 'Solicitud not found'}), 404

@app.route('/notificaciones', methods=['GET'])
def get_notificaciones():
    return jsonify(notificaciones)

if __name__ == "__main__":
    consumer_thread = Thread(target=consume_messages)
    consumer_thread.start()
    app.run(host='0.0.0.0', port=4000)
