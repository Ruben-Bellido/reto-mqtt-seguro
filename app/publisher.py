import paho.mqtt.client as mqtt 
import subprocess
import time
import tkinter as tk
from tkinter import filedialog

# Establecer el nombre del hostname y el puerto
broker_hostname = subprocess.getoutput("hostname -I | awk '{print $1}'")
port = 8883

# Función ejecutada una vez el cliente se conecta al broker MQTT
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado")
    else:
        print("No se pudo conectar, código devuelto:", reason_code)

# Función que abre un diálogo para seleccionar un archivo
def seleccionar_archivo(message):
    root = tk.Tk()
    root.withdraw()
    dir = filedialog.askopenfilename(title=message)
    return dir

# Se crea el cliente y se solicitan el usuario, la contraseña, los certificados y el topic
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
username = input("Introduce el nombre de usuario: ")
password = input("Introduce la contraseña: ")
client.username_pw_set(username=username, password=password)
ca_certs = seleccionar_archivo("Selecciona el certificado de la CA (ca.crt)")
certfile = seleccionar_archivo("Selecciona el certificado del cliente (client.crt)")
keyfile = seleccionar_archivo("Selecciona las clave del cliente (client.key)")
client.tls_set(ca_certs=ca_certs, certfile=certfile, keyfile=keyfile)
topic = input("Introduce el topic al cual deseas publicar datos: ")
client.on_connect = on_connect

# Iniciar conexión con el broker MQTT
client.connect(broker_hostname, port)
client.loop_start()

msg_count = 0

try:
    # Publicar un mensaje cada segundo
    while True:
        time.sleep(1)
        msg_count += 1
        result = client.publish(topic, msg_count)
        status = result[0]
        # Comprobar que el mensaje se haya podido publicar correctamente
        if status == 0:
            print("Mensaje Nº "+ str(msg_count) + " publicado al topic " + topic)
        else:
            print("No se ha podido publicar el mensaje al topic " + topic)
        # Comprobar si el cliente se ha desconectado
        if not client.is_connected():
            print("Cliente desconectado, saliendo...")
            break
# Ctrl + C para finalizar el envío de datos
except KeyboardInterrupt:
    print("Envío de datos finalizado")
finally:
    # Finalizar la conexión
    client.disconnect()
    client.loop_stop()