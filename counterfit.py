from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT  # Importa el sensor de temperatura y humedad
from counterfit_shims_grove.grove_led import GroveLed
import paho.mqtt.client as mqtt
import json
import time


CounterFitConnection.init("localhost", 5000)# Inicializa la conexión con CounterFit

sensor_temp_hum = DHT("11",0)# Inicializa el sensor de temperatura y humedad (puerto 0)


id = "c12fb10d-f9c8-47f0-8a6e-f591d670152f"# Configuración del cliente MQTT
nombre_cliente = id + "ProyectoTemperatura"
mqtt_cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,nombre_cliente)
mqtt_cliente.connect("localhost")
mqtt_cliente.loop_start()
if mqtt_cliente.is_connected:
    print("Conectado al servidor")
else:
    print("Hubo un problema al conectarse")
    
cliente_telemetria_topico = id + "/plantas"# Definición de tópicos MQTT


while True:#loop para leer datos y enviarlos por MQTT
    temperatura, humedad = sensor_temp_hum.read()
    # print(f"Temperatura: {temperatura} °C, Humedad: {humedad} %")
    telemetria = json.dumps({"temperatura": temperatura, "humedad": humedad})
    print(f"Temperatura enviada:  {telemetria} ")
    mqtt_cliente.publish("plantas", telemetria)
    time.sleep(15)


