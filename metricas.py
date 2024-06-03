import pandas as pd
import requests
import random
import time
from threading import Thread
import matplotlib.pyplot as plt

def escenario_carga_intervalo(url, solicitudes, tiempos_intervalo, tiempos_respuesta):
    for solicitud in solicitudes:
        start_time = time.time()
        response = requests.post(url, json=solicitud)
        end_time = time.time()
        tiempos_respuesta.append(end_time - start_time)
        print(f"Solicitud enviada: {solicitud}")
        time.sleep(random.choice(tiempos_intervalo))  # Esperar un tiempo aleatorio entre solicitudes

def escenario_carga_simultanea(url, solicitudes, tiempos_simultanea, tiempos_respuesta):
    threads = []
    for solicitud in solicitudes:
        thread = Thread(target=enviar_solicitud, args=(url, solicitud, tiempos_respuesta))
        threads.append(thread)
        thread.start()
        time.sleep(random.choice(tiempos_simultanea))  # Esperar un tiempo aleatorio entre solicitudes
    for thread in threads:
        thread.join()

def enviar_solicitud(url, solicitud, tiempos_respuesta):
    start_time = time.time()
    response = requests.post(url, json=solicitud)
    end_time = time.time()
    tiempos_respuesta.append(end_time - start_time)
    print(f"Solicitud enviada: {solicitud}")

if __name__ == "__main__":
    URL = "http://localhost:4000/solicitud"
    DATASET_PATH = "amazon_categories.csv"
    TIEMPOS_INTERVALO = [1, 2, 3]  # Intervalos de tiempo en segundos
    TIEMPOS_SIMULTANEA = [0.5, 1, 1.5]  # Intervalos de tiempo en segundos

    # Cargar datos del archivo CSV
    dataset = pd.read_csv(DATASET_PATH)

    # Seleccionar solo 100 datos o 1000 datos según lo deseado
    solicitudes_100 = dataset.head(100).to_dict(orient="records")
    solicitudes_1000 = dataset.head(1000).to_dict(orient="records")

    # Crear listas para almacenar los tiempos de respuesta
    tiempos_respuesta_intervalo_100 = []
    tiempos_respuesta_intervalo_1000 = []
    tiempos_respuesta_simultanea_100 = []
    tiempos_respuesta_simultanea_1000 = []

    # Ejecutar los escenarios de carga y recopilar los tiempos de respuesta
    thread_intervalo_100 = Thread(target=escenario_carga_intervalo, args=(URL, solicitudes_100, TIEMPOS_INTERVALO, tiempos_respuesta_intervalo_100))
    thread_intervalo_100.start()

    thread_simultanea_100 = Thread(target=escenario_carga_simultanea, args=(URL, solicitudes_100, TIEMPOS_SIMULTANEA, tiempos_respuesta_simultanea_100))
    thread_simultanea_100.start()

    thread_intervalo_1000 = Thread(target=escenario_carga_intervalo, args=(URL, solicitudes_1000, TIEMPOS_INTERVALO, tiempos_respuesta_intervalo_1000))
    thread_intervalo_1000.start()

    thread_simultanea_1000 = Thread(target=escenario_carga_simultanea, args=(URL, solicitudes_1000, TIEMPOS_SIMULTANEA, tiempos_respuesta_simultanea_1000))
    thread_simultanea_1000.start()

    # Esperar a que todos los threads terminen
    thread_intervalo_100.join()
    thread_simultanea_100.join()
    thread_intervalo_1000.join()
    thread_simultanea_1000.join()

    # Graficar los resultados
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 2, 1)
    plt.hist(tiempos_respuesta_intervalo_100, bins=20, alpha=0.5, color='b', label='100 solicitudes')
    plt.hist(tiempos_respuesta_intervalo_1000, bins=20, alpha=0.5, color='r', label='1000 solicitudes')
    plt.title('Distribución de tiempos de respuesta (Intervalo de tiempo)')
    plt.xlabel('Tiempo de respuesta (segundos)')
    plt.ylabel('Frecuencia')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.hist(tiempos_respuesta_simultanea_100, bins=20, alpha=0.5, color='b', label='100 solicitudes')
    plt.hist(tiempos_respuesta_simultanea_1000, bins=20, alpha=0.5, color='r', label='1000 solicitudes')
    plt.title('Distribución de tiempos de respuesta (Simultánea)')
    plt.xlabel('Tiempo de respuesta (segundos)')
    plt.ylabel('Frecuencia')
    plt.legend()

    plt.tight_layout()
    plt.show()

