#!/bin/bash

# Instalar componentes necesarios
apt-get update
apt install python3-pip  
pip install paho-mqtt
snap install mosquitto