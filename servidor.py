from counterfit_connection import CounterFitConnection
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.subscribeoptions as subscribeOptions
import time
import json
import csv
from os import path
from datetime import datetime



id = "c12fb10d-f9c8-47f0-8a6e-f591d670152f"# Configuración del cliente MQTT
nombre_cliente = id + "ProyectoTemperatura2"


# cliente_telemetria_topico = id + "/plantas"
# cliente_telemetria_comando = id + "/apagar"
mqtt_cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, nombre_cliente, protocol=mqtt.MQTTv311)
mqtt_cliente.connect("localhost",1883)

nombre_archivo_log= "temperatura.csv"
columnas =["fechayhora","temperatura", "humedad"]

if not path.exists(nombre_archivo_log):
    with open(nombre_archivo_log, mode="+w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columnas)
        writer.writeheader()
        
def temperatura_recibida(cliente,informacion, msj):
        msj= json.loads(msj.payload.decode())
        print("Mensaje recibido:",msj)
        
        with open(nombre_archivo_log, mode="a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columnas)
            writer.writerow({"fechayhora":datetime.now(),"temperatura": msj["temperatura"],"humedad": msj["humedad"]})
        
    
mqtt_cliente.on_message = temperatura_recibida
mqtt_cliente.subscribe("plantas",qos=1)
mqtt_cliente.loop_forever()


