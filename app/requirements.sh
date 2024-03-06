#!/bin/bash

# Instalar componentes necesarios
apt-get update
snap install mosquitto
apt install python3-pip  
pip install paho-mqtt
apt-get install python3-tk