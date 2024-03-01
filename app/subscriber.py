import paho.mqtt.client as mqtt
import time

broker_hostname = "172.29.74.232"
port = 8883
topic = "python"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado")
        client.subscribe(topic)
    else:
        print("No se pudo conectar, código devuelto:", reason_code)
        client.failed_connect = True


def on_message(client, userdata, message):
    print("Mensaje recibido: ", str(message.payload.decode("utf-8")))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="client", password="1234")
client.tls_set(ca_certs="./certs/ca.crt", certfile="./certs/client.crt", keyfile="./certs/client.key")
client.on_connect = on_connect
client.on_message = on_message
client.failed_connect = False

client.connect(broker_hostname, port) 
client.loop_start()

try:
    while client.failed_connect == False:
        time.sleep(1)
    if client.failed_connect == True:
        print("Conexión fallida, saliendo...")
except KeyboardInterrupt:
    print('Recepción de datos finalizada.')
finally:
    client.disconnect()
    client.loop_stop()