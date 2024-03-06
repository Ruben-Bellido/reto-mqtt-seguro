import paho.mqtt.client as mqtt
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

# Establecer el nombre del hostname y el puerto
broker_hostname = subprocess.getoutput("hostname -I | awk '{print $1}'")
port = 8883
topic = ""

# Función ejecutada una vez el cliente se conecta al broker MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado")
        client.subscribe(topic)
    else:
        print("No se pudo conectar, código devuelto:", reason_code)
        client.failed_connect = True

# Función ejecutada cada vez que se recibe un mensaje
def on_message(client, userdata, message):
    print("Mensaje recibido: ", str(message.payload.decode("utf-8")))

# Función que abre un diálogo para seleccionar un archivo
def seleccionar_archivo(message):
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana de Tkinter
    ruta_al_archivo = filedialog.askopenfilename(title=message)  # Abre el diálogo para seleccionar archivo
    return ruta_al_archivo

# Se crea el cliente y se solicitan el usuario, la contraseña, los certificados y el topic
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
username = input("Introduce el nombre de usuario: ")
password = input("Introduce la contraseña: ")
client.username_pw_set(username=username, password=password)
ca_certs = seleccionar_archivo("Selecciona el certificado de la CA (ca.crt)")
certfile = seleccionar_archivo("Selecciona el certificado del cliente (client.crt)")
keyfile = seleccionar_archivo("Selecciona las clave del cliente (client.key)")
client.tls_set(ca_certs=ca_certs, certfile=certfile, keyfile=keyfile)
topic = input("Introduce el topic al cual deseas suscribirte: ")
client.on_connect = on_connect
client.on_message = on_message
client.failed_connect = False

# Iniciar conexión con el broker MQTT
client.connect(broker_hostname, port) 
client.loop_start()

try:
    # Recibir datos cada segundo
    while client.failed_connect == False:
        time.sleep(1)
    # Comprobar si el cliente no consigue conectarse
    if client.failed_connect == True:
        print("Conexión fallida, saliendo...")
# Ctrl + C para finalizar el envío de datos
except KeyboardInterrupt:
    print("Recepción de datos finalizada")
finally:
    # Finalizar la conexión
    client.disconnect()
    client.loop_stop()