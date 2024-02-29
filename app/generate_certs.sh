#!/bin/bash

# Ruta en la cual se generarán los certificados
DIR="./certs"
# Certificados almacenados en mosquitto
CERTS="./mosquitto/config/certs"

# Dirección IP local
IP=$(hostname -I | awk '{print $1}')

# Identificador de los diferentes certificados
# C (País) / OU (nombre unitario organizacional) / CN (nombre común)
SUBJECT_CA="/C=ES/OU=CA/CN=$IP"
SUBJECT_SERVER="/C=ES/OU=Server/CN=$IP"
SUBJECT_CLIENT="/C=ES/OU=Client/CN=$IP"

# Genera una clave privada de 2048 bits para la CA (autoridad de certificación)
openssl genrsa -des3 -out $DIR/ca.key 2048
# Genera el certificado raíz autofirmado de la CA válido durante un 1826 días
openssl req -new -x509 -days 1826 -key $DIR/ca.key -out $DIR/ca.crt -subj "$SUBJECT_CA"

# Genera una clave de 2048 bits para la solicitud de firma de certificado (CSR) para el servidor mqtt
openssl genrsa -out $DIR/server.key 2048
# Genera la CSR para el servidor mqtt
openssl req -new -out $DIR/server.csr -key $DIR/server.key -subj "$SUBJECT_SERVER"
# Usa la CSR y la CA para firmar la solicitud del servidor mqtt y obtener el certificado válido durante un año
openssl x509 -req -in $DIR/server.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/server.crt -days 360

# Genera una clave de 2048 bits para la solicitud de firma de certificado (CSR) para el cliente mqtt
openssl genrsa -out $DIR/client.key 2048
# Genera la CSR para el cliente mqtt
openssl req -new -out $DIR/client.csr -key $DIR/client.key -subj "$SUBJECT_CLIENT"
# Usa la CSR y la CA para firmar la solicitud del cliente mqtt y obtener el certificado válido durante un año
openssl x509 -req -in $DIR/client.csr -CA $DIR/ca.crt -CAkey $DIR/ca.key -CAcreateserial -out $DIR/client.crt -days 360

# Copiar certificados requeridos para la configuración del broker mqtt tls
cp $DIR/ca.crt $CERTS
cp $DIR/server.crt $CERTS
cp $DIR/server.key $CERTS
