# reto-mqtt-seguro

## Pasos seguidos
- Investigación: cómo montar un servicio MQTT en docker (mosquitto)
- Desarrollo de la estructura inicial del proyecto
- Configuración inicial de mosquitto y pruebas a través de la línea de comandos
- Configuración de seguridad para añadir usuario + contraseña y pruebas a través de la línea de comandos
- Investigación: cómo añadir conexión segura al servicio MQTT
- Replanteamiento de la estructura del proyecto
- Configuración TLS de mosquitto
- Desarrollo del shell script encargado de generar los certificados de seguridad y pruebas a través de la línea de comandos
- Desarrollo de los scripts de publicador y suscriptor de Python
- Configuración del nombre de asunto alternativo (SAN) para los certificados de seguridad
- Pruebas a través de los scripts de Python
- Implementación de extras
- Desarrollo del shell script encargado de instalar todo lo necesario para que el proyecto funcione

## Instrucciones de uso
- Instalar requisitos: $ sudo sh requirements.sh
- Generar certificados: $ sh generate_certs.sh
- Cambio de contraseña: $ docker exec -it mosquitto mosquitto_passwd -c /mosquitto/config/mosquitto.passwd "usr"
- Visualización de logs: sudo cat ./mosquitto/log/mosquitto.log
### Mediante línea de comandos
- Suscribirse al topic: $ mosquitto_sub -h "IP local" -p 8883 -u client --pw 1234 --cafile ./certs/ca.crt --cert ./certs/sub_shell/client.crt --key ./certs/sub_shell/client.key -t "topic"
- Publicar al topic: $ mosquitto_pub -h "IP local" -p 8883 -u client --pw 1234 --cafile ./certs/ca.crt --cert ./certs/pub_shell/client.crt --key ./certs/pub_shell/client.key -t "topic" -m "mensaje"
- Para comprobar la IP local: $ hostname -I
### Mediante Pyhon
- Suscribirse al topic: $ python3 subscriber.py
- Publicar al topic: $ python3 publisher.py
- Usuario: client
- Contraseña: 1234

## Posibles vías de mejora
- Hacer uso del hostname en vez de la dirección IP para conectarse al broker (sería más práctico)
- Datos enviados a través del programa de Python más elaborados
- Generación de certificados más sencilla frente a los permisos de usuario

## Problemas / Retos encontrados
- Generación de certificados
- Configuración TLS
- Uso del nombre común para el nombre del host desaprobado
- Permisos de usuario: usuario local, root y mosquitto

## Alternativas posibles
- Apache Pulsar en lugar de MQTT
- HiveMQ como alternativa a Mosquitto
