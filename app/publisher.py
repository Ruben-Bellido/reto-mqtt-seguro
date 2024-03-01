import paho.mqtt.client as mqtt 
import time

broker_hostname = "172.29.74.232"
port = 8883
topic = "python"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado")
    else:
        print("No se pudo conectar, código devuelto:", reason_code)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username="client", password="1234")
client.tls_set(ca_certs="./certs/ca.crt", certfile="./certs/client.crt", keyfile="./certs/client.key")
client.on_connect = on_connect

client.connect(broker_hostname, port)
client.loop_start()

msg_count = 0

try:
    while client.is_connected():
        time.sleep(1)
        msg_count += 1
        result = client.publish(topic, msg_count)
        status = result[0]
        if status == 0:
            print("Mensaje Nº "+ str(msg_count) + " publicado al topic " + topic)
        else:
            print("No se ha podido publicar el mensaje al topic " + topic)
    print("Cliente desconectado, saliendo...")
except KeyboardInterrupt:
    print('Recepción de datos finalizada.')
finally:
    client.disconnect()
    client.loop_stop()