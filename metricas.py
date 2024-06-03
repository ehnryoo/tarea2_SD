import pandas as pd
import requests
import random
import time
from threading import Thread

def escenario_carga_intervalo(url, solicitudes, tiempos_intervalo):
    for solicitud in solicitudes:
        response = requests.post(url, json=solicitud)
        print(f"Solicitud enviada: {solicitud}")
        time.sleep(random.choice(tiempos_intervalo))  # Esperar un tiempo aleatorio entre solicitudes

def escenario_carga_simultanea(url, solicitudes, tiempos_simultanea):
    threads = []
    for solicitud in solicitudes:
        thread = Thread(target=enviar_solicitud, args=(url, solicitud))
        threads.append(thread)
        thread.start()
        time.sleep(random.choice(tiempos_simultanea))  # Esperar un tiempo aleatorio entre solicitudes
    for thread in threads:
        thread.join()

def enviar_solicitud(url, solicitud):
    response = requests.post(url, json=solicitud)
    print(f"Solicitud enviada: {solicitud}")

if __name__ == "__main__":
    URL = "http://localhost:4000/solicitud"
    DATASET_PATH = "amazon_categories.csv"
    TIEMPOS_INTERVALO = [1, 2, 3]  # Intervalos de tiempo en segundos
    TIEMPOS_SIMULTANEA = [0.5, 1, 1.5]  # Intervalos de tiempo en segundos

    # Cargar datos del archivo CSV
    dataset = pd.read_csv(DATASET_PATH)
    solicitudes = dataset.to_dict(orient="records")

    print("Escenario de carga por intervalo de tiempo")
    thread_intervalo = Thread(target=escenario_carga_intervalo, args=(URL, solicitudes, TIEMPOS_INTERVALO))
    thread_intervalo.start()

    print("Escenario de carga simultánea")
    thread_simultanea = Thread(target=escenario_carga_simultanea, args=(URL, solicitudes, TIEMPOS_SIMULTANEA))
    thread_simultanea.start()

    thread_intervalo.join()
    thread_simultanea.join()
