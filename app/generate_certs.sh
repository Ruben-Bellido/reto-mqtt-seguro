#!/bin/bash

# Ruta en la cual se generarán los certificados
DIR="./certs"
# Ruta de los certificados correspondientes al broker MQTT
CERTS="./mosquitto/config/certs"

# Crear directorios en los que se generarán los diferentes certificados
mkdir $DIR
mkdir $DIR/server
mkdir $DIR/sub_shell
mkdir $DIR/pub_shell
mkdir $DIR/sub_py
mkdir $DIR/pub_py
# Crear directorio de los certificados almacenados en mosquitto
mkdir $CERTS

# Dirección IP local (WSL)
IP=$(hostname -I | awk '{print $1}')

# Asunto de los diferentes certificados: C (País) / OU (nombre unitario organizacional) / CN (nombre común)
SUBJECT_CA="/C=ES/OU=CA/CN=$IP"
SUBJECT_SERVER="/C=ES/OU=Server/CN=$IP"
SUBJECT_CLIENT="/C=ES/OU=Client/CN=$IP"

# Extensión SAN (Subject Alt Name) con la dirección IP
SAN="subjectAltName=IP:$IP"

# Genera una clave privada de 2048 bits para la CA (autoridad de certificación)
openssl genrsa -des3 -out $DIR/ca.key 2048
# Genera el certificado raíz autofirmado de la CA válido durante un 1826 días
openssl req -new -x509 -days 1826 -key $DIR/ca.key -out $DIR/ca.crt -subj "$SUBJECT_CA" -addext $SAN

# Genera una clave de 2048 bits para la CSR (solicitud de firma de certificado) para el servidor MQTT
openssl genrsa -out $DIR/server/server.key 2048
# Genera la CSR para el servidor mqtt
openssl req -new -out $DIR/server/server.csr -key $DIR/server/server.key -subj "$SUBJECT_SERVER" -addext $SAN
# Usa la CSR y la CA para firmar la solicitud del servidor mqtt y obtener el certificado válido durante un año (sha256WithRSAEncryption)
openssl x509 -req -in $DIR/server/server.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/server/server.crt -days 365 -copy_extensions copy

# Copiar certificados requeridos para la configuración del broker MQTT TLS
cp $DIR/ca.crt $CERTS
cp $DIR/server/server.crt $CERTS
cp $DIR/server/server.key $CERTS

# Suscriptor de la línea de comandos
openssl genrsa -out $DIR/sub_shell/client.key 2048
openssl req -new -out $DIR/sub_shell/client.csr -key $DIR/sub_shell/client.key -subj "$SUBJECT_CLIENT" -addext $SAN
openssl x509 -req -in $DIR/sub_shell/client.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/sub_shell/client.crt -days 365 -copy_extensions copy

# Publicador de la línea de comandos
openssl genrsa -out $DIR/pub_shell/client.key 2048
openssl req -new -out $DIR/pub_shell/client.csr -key $DIR/pub_shell/client.key -subj "$SUBJECT_CLIENT" -addext $SAN
openssl x509 -req -in $DIR/pub_shell/client.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/pub_shell/client.crt -days 365 -copy_extensions copy

# Suscriptor de python
openssl genrsa -out $DIR/sub_py/client.key 2048
openssl req -new -out $DIR/sub_py/client.csr -key $DIR/sub_py/client.key -subj "$SUBJECT_CLIENT" -addext $SAN
openssl x509 -req -in $DIR/sub_py/client.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/sub_py/client.crt -days 365 -copy_extensions copy

# Publicador de python
openssl genrsa -out $DIR/pub_py/client.key 2048
openssl req -new -out $DIR/pub_py/client.csr -key $DIR/pub_py/client.key -subj "$SUBJECT_CLIENT" -addext $SAN
openssl x509 -req -in $DIR/pub_py/client.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/pub_py/client.crt -days 365 -copy_extensions copy