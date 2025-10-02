./setup_alexa_5.0.shchmod +x setup_alexa_5.0.sh#!/bin/bash
# =========================
# Setup Alexa Voice Service Python 5.0 - Legendaria
# =========================

# ----------- CONFIGURA TUS CREDENCIALES AQUÍ -----------
CLIENT_ID="TU_CLIENT_ID"
CLIENT_SECRET="TU_CLIENT_SECRET"
PRODUCT_ID="TU_PRODUCT_ID"
# Opcional: token Telegram para notificaciones
TELEGRAM_TOKEN="TU_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID="TU_CHAT_ID"
# ---------------------------------------------------------

LOG_FILE="alexa.log"
PANEL_PORT=5000

echo "🔹 Actualizando sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🔹 Instalando dependencias básicas..."
sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg xdg-utils swig libatlas-base-dev libffi-dev

echo "🔹 Clonando repo..."
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service || { echo "❌ No se pudo entrar al directorio"; exit 1; }

echo "🔹 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "🔹 Instalando librerías Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/Lukasa/hyper.git
pip install "snowboy==1.3.0" flask requests || echo "⚠️ Revisa dependencias"

echo "🔹 Configurando credenciales Alexa automáticamente..."
cat > config.dict <<EOL
{
  "product_id": "$PRODUCT_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "refresh_token": ""
}
EOL

echo "🔹 Autenticación Alexa..."
python auth_web.py &

echo "💡 Autentícate y copia tu refresh_token"
read -p "➡ Pega aquí tu refresh_token: " REFRESH_TOKEN
sed -i "s/\"refresh_token\": \"\"/\"refresh_token\": \"$REFRESH_TOKEN\"/" config.dict

# ------------------- Panel Web + Notificaciones -----------------------
cat > panel_legendaria.py <<EOL
from flask import Flask, render_template_string, request
import subprocess, os, requests

app = Flask(__name__)
LOG_FILE = "$LOG_FILE"
TELEGRAM_TOKEN = "$TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID = "$TELEGRAM_CHAT_ID"

def push_notify(msg):
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={msg}")

@app.route('/')
def index():
    logs = open(LOG_FILE).read() if os.path.exists(LOG_FILE) else "No logs yet."
    return render_template_string("""
        <h2>Alexa Legendaria Panel</h2>
        <pre>{{logs}}</pre>
        <form action='/restart' method='post'>
        <button type='submit'>Reiniciar Alexa</button>
        </form>
    """, logs=logs)

@app.route('/restart', methods=['POST'])
def restart():
    subprocess.Popen(["pkill", "-f", "main.py"])
    subprocess.Popen(["nohup", "python3", "main.py", "--wakeword", "alexa", "--daemonize", "--log", LOG_FILE, "&"])
    push_notify("Alexa reiniciada desde panel!")
    return "Alexa reiniciada!"

if __name__ == '__main__':
    push_notify("Alexa Legendaria lista y corriendo!")
    subprocess.Popen(["nohup", "python3", "main.py", "--wakeword", "alexa", "--daemonize", "--log", LOG_FILE, "&"])
    app.run(host='0.0.0.0', port=$PANEL_PORT)
EOL

echo "🔹 Lanzando panel Legendaria + Alexa..."
nohup python panel_legendaria.py &

echo "✅ Setup Legendaria completado!"
echo "Accede al panel web: http://localhost:$PANEL_PORT"
echo "Alexa está escuchando continuamente, logs activos y notificaciones push configuradas."https://developer.amazon.com/./setup_alexa_4.0.shchmod +x setup_alexa_4.0.sh#!/bin/bash
# =========================
# Setup Alexa Voice Service Python 4.0 - Panel Master
# =========================

# ----------- CONFIGURA TUS CREDENCIALES AQUÍ -----------
CLIENT_ID="TU_CLIENT_ID"
CLIENT_SECRET="TU_CLIENT_SECRET"
PRODUCT_ID="TU_PRODUCT_ID"
# ---------------------------------------------------------

LOG_FILE="alexa.log"
PANEL_PORT=5000

echo "🔹 Actualizando sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🔹 Instalando dependencias básicas..."
sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg xdg-utils swig libatlas-base-dev libffi-dev

echo "🔹 Clonando repo..."
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service || { echo "❌ No se pudo entrar al directorio"; exit 1; }

echo "🔹 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "🔹 Instalando librerías Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/Lukasa/hyper.git
pip install "snowboy==1.3.0" flask || echo "⚠️ Instala Flask si falla manualmente"

echo "🔹 Configurando credenciales Alexa automáticamente..."
cat > config.dict <<EOL
{
  "product_id": "$PRODUCT_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "refresh_token": ""
}
EOL

echo "🔹 Autenticación Alexa..."
python auth_web.py &

echo "💡 Autentícate y copia tu refresh_token"
read -p "➡ Pega aquí tu refresh_token: " REFRESH_TOKEN

sed -i "s/\"refresh_token\": \"\"/\"refresh_token\": \"$REFRESH_TOKEN\"/" config.dict

# ------------------- Panel Web -----------------------
echo "🔹 Configurando panel web..."
cat > panel.py <<EOL
from flask import Flask, render_template_string
import subprocess
import os

app = Flask(__name__)
LOG_FILE = "$LOG_FILE"

@app.route('/')
def index():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = f.read()
    else:
        logs = "No logs yet."
    return render_template_string("""
        <h2>Alexa Voice Service Panel</h2>
        <pre>{{logs}}</pre>
        <form action='/restart' method='post'>
        <button type='submit'>Reiniciar Alexa</button>
        </form>
    """, logs=logs)

@app.route('/restart', methods=['POST'])
def restart():
    subprocess.Popen(["pkill", "-f", "main.py"])
    subprocess.Popen(["nohup", "python3", "main.py", "--wakeword", "alexa", "--daemonize", "--log", "$LOG_FILE", "&"])
    return "Alexa reiniciada!"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=$PANEL_PORT)
EOL

echo "🔹 Lanzando Alexa y panel web..."
nohup python main.py --wakeword "alexa" --daemonize --log "$LOG_FILE" &
nohup python panel.py &

echo "✅ Setup Panel Master completado!"
echo "Accede al panel desde tu navegador: http://localhost:$PANEL_PORT"
echo "Alexa seguirá escuchando, logs disponibles y puedes reiniciarla desde el panel."chmod +x setup_alexa_3.0.sh#!/bin/bash
# =========================
# Setup Alexa Voice Service Python 3.0 Ultra Pro
# =========================

# ----------- CONFIGURA TUS CREDENCIALES AQUÍ -----------
CLIENT_ID="TU_CLIENT_ID"
CLIENT_SECRET="TU_CLIENT_SECRET"
PRODUCT_ID="TU_PRODUCT_ID"
# ---------------------------------------------------------

LOG_FILE="alexa.log"

echo "🔹 Actualizando sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🔹 Instalando dependencias básicas..."
sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg xdg-utils swig libatlas-base-dev libffi-dev

echo "🔹 Clonando repo..."
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service || { echo "❌ No se pudo entrar al directorio"; exit 1; }

echo "🔹 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "🔹 Instalando librerías Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/Lukasa/hyper.git
pip install "snowboy==1.3.0" || echo "⚠️ Si falla, instala manual: https://github.com/Kitt-AI/snowboy"

echo "🔹 Configurando credenciales Alexa automáticamente..."
cat > config.dict <<EOL
{
  "product_id": "$PRODUCT_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "refresh_token": ""
}
EOL

echo "🔹 Autenticación Alexa..."
python auth_web.py &

echo "💡 Autentícate y copia tu refresh_token"
read -p "➡ Pega aquí tu refresh_token: " REFRESH_TOKEN

sed -i "s/\"refresh_token\": \"\"/\"refresh_token\": \"$REFRESH_TOKEN\"/" config.dict

echo "🔹 Lanzando Alexa en segundo plano con wake word y auto-reconexión..."
echo "🎙️ Alexa se ejecutará como daemon y guardará logs en $LOG_FILE"
nohup python main.py --wakeword "alexa" --daemonize --log "$LOG_FILE" &

echo "✅ Setup Ultra Pro completado!"
echo "Puedes cerrar la terminal, Alexa seguirá escuchando y respondiendo al wake word 'Alexa'."
echo "Logs disponibles en $LOG_FILE"#!/bin/bash
# =========================
# Setup Alexa Voice Service Python 2.0 - Wake Word + Escucha continua
# =========================

# ----------- CONFIGURA TUS CREDENCIALES AQUÍ -----------
CLIENT_ID="TU_CLIENT_ID"
CLIENT_SECRET="TU_CLIENT_SECRET"
PRODUCT_ID="TU_PRODUCT_ID"
# ---------------------------------------------------------

echo "🔹 Actualizando sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🔹 Instalando dependencias básicas..."
sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg xdg-utils swig libatlas-base-dev libffi-dev

echo "🔹 Clonando repo..."
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service || { echo "❌ No se pudo entrar al directorio"; exit 1; }

echo "🔹 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "🔹 Instalando librerías Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/Lukasa/hyper.git

echo "🔹 Instalando wake word engine (snowboy)..."
pip install "snowboy==1.3.0" || echo "⚠️ Si falla, instala manual: https://github.com/Kitt-AI/snowboy"

echo "🔹 Configurando credenciales Alexa automáticamente..."
cat > config.dict <<EOL
{
  "product_id": "$PRODUCT_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "refresh_token": ""
}
EOL

echo "🔹 Abriendo navegador para autenticación Alexa..."
python auth_web.py &

echo "💡 Autentícate y copia tu refresh_token"
read -p "➡ Pega aquí tu refresh_token: " REFRESH_TOKEN

# Guardamos refresh_token en config.dict
sed -i "s/\"refresh_token\": \"\"/\"refresh_token\": \"$REFRESH_TOKEN\"/" config.dict

echo "🔹 Activando Alexa con wake word y escucha continua..."
echo "🎙️ Di 'Alexa' y empieza a interactuar"

# Ejecuta main.py en modo wake word
python main.py --wakeword "alexa"chmod +x setup_alexa_final.sh#!/bin/bash
# =========================
# Setup final Alexa Voice Service Python
# =========================

# ----------- CONFIGURA TUS CREDENCIALES AQUÍ -----------
CLIENT_ID="TU_CLIENT_ID"
CLIENT_SECRET="TU_CLIENT_SECRET"
PRODUCT_ID="TU_PRODUCT_ID"
# ---------------------------------------------------------

echo "🔹 Actualizando sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🔹 Instalando dependencias básicas..."
sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg xdg-utils

echo "🔹 Clonando repo..."
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service || { echo "❌ No se pudo entrar al directorio"; exit 1; }

echo "🔹 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "🔹 Instalando librerías Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/Lukasa/hyper.git

echo "🔹 Configurando credenciales Alexa automáticamente..."
cat > config.dict <<EOL
{
  "product_id": "$PRODUCT_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "refresh_token": ""
}
EOL

echo "🔹 Abriendo navegador para autenticación Alexa..."
python auth_web.py &

echo "💡 Por favor, autentícate en la ventana que se abrió y copia tu refresh_token"
read -p "➡ Pega aquí tu refresh_token: " REFRESH_TOKEN

# Guardamos refresh_token en config.dict
sed -i "s/\"refresh_token\": \"\"/\"refresh_token\": \"$REFRESH_TOKEN\"/" config.dict

echo "🔹 Ejecutando Alexa automáticamente..."
python main.py./setup_alexa_ultra.shchmod +x setup_alexa_ultra.sh#!/bin/bash
# =========================
# Setup ultra completo Alexa Voice Service Python
# =========================

# ----------- CONFIGURA TUS CREDENCIALES AQUÍ -----------
CLIENT_ID="TU_CLIENT_ID"
CLIENT_SECRET="TU_CLIENT_SECRET"
PRODUCT_ID="TU_PRODUCT_ID"
# ---------------------------------------------------------

echo "🔹 Actualizando sistema..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "🔹 Instalando dependencias básicas..."
sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg xdg-utils

echo "🔹 Clonando repo..."
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service || { echo "❌ No se pudo entrar al directorio"; exit 1; }

echo "🔹 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "🔹 Instalando librerías Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install git+https://github.com/Lukasa/hyper.git

echo "🔹 Configurando credenciales Alexa automáticamente..."
cat > config.dict <<EOL
{
  "product_id": "$PRODUCT_ID",
  "client_id": "$CLIENT_ID",
  "client_secret": "$CLIENT_SECRET",
  "refresh_token": ""
}
EOL

echo "🔹 Abriendo navegador para autenticación Alexa..."
python auth_web.py &

echo "💡 Por favor, autentícate en la ventana que se abrió y copia tu refresh_token"
read -p "➡ Pega aquí tu refresh_token: " REFRESH_TOKEN

# Guardamos refresh_token en config.dict
sed -i "s/\"refresh_token\": \"\"/\"refresh_token\": \"$REFRESH_TOKEN\"/" config.dict

echo "🔹 Setup completado, compa! 🎉"
echo "Ahora solo corre: python main.py"
echo "y tu Alexa debería responder a tu voz 🔊🎙️"import os
import platform
import subprocess
import sys
import time

REPO_URL = "https://github.com/Kenworth1992/python-alexa-voice-service.git"
PROJECT_DIR = "python-alexa-voice-service"

def run(cmd):
    subprocess.check_call(cmd, shell=True)

def install_ffmpeg():
    system = platform.system()
    if system == "Windows":
        print("Verifica que ffmpeg esté en PATH. Si no, instalar desde https://ffmpeg.org/download.html")
    else:
        print("Instalando ffmpeg en Linux...")
        run("sudo apt update && sudo apt install -y ffmpeg")

def setup_python_env():
    if platform.system() == "Windows":
        run(f"python -m venv env && env\\Scripts\\activate && pip install --upgrade pip")
        run(f"env\\Scripts\\pip install -r {PROJECT_DIR}\\requirements.txt")
    else:
        run(f"python3 -m venv env && source env/bin/activate && pip install --upgrade pip")
        run(f"pip install -r {PROJECT_DIR}/requirements.txt")

def clone_repo():
    if not os.path.exists(PROJECT_DIR):
        print("Clonando repo...")
        run(f"git clone {REPO_URL}")
    else:
        print("Repositorio ya existe. Actualizando...")
        os.chdir(PROJECT_DIR)
        run("git pull")
        os.chdir("..")

def create_config():
    cfg_path = os.path.join(PROJECT_DIR, "config.dict")
    if not os.path.exists(cfg_path):
        with open(cfg_path, "w") as f:
            f.write(
"""[DEFAULT]
client_id = TU_CLIENT_ID
client_secret = TU_CLIENT_SECRET
device_type = my_python_device
product_id = PythonAlexa001
""")
        print(f"Archivo config.dict creado en {cfg_path}. Reemplaza TU_CLIENT_ID y TU_CLIENT_SECRET")
    else:
        print("Archivo config.dict ya existe. Revisa tus credenciales.")

def main():
    clone_repo()
    install_ffmpeg()
    setup_python_env()
    create_config()

    print("\n¡Setup completado! Para iniciar Alexa:")
    print(f"1. Entrar al entorno virtual:")
    if platform.system() == "Windows":
        print("   env\\Scripts\\activate")
    else:
        print("   source env/bin/activate")
    print(f"2. Ejecutar:\n   python {PROJECT_DIR}/main.py")
    print("\nElige Always Listening o Push to Talk al iniciar.\n")

if __name__ == "__main__":
    main()AlexaInstaller/
│
├─ install.py      # Script principal que hace todo
└─ README.md       # Instrucciones resumidaspython setup.py   # Instala librerías y ffmpeg
python main.py    # Inicia Alexa# Alexa Python Ultra Plug & Play

## Setup rápido

1. Reemplaza TU_CLIENT_ID y TU_CLIENT_SECRET en config.dict
2. Ejecuta setup.py:
   Windows / Linux:
   python setup.py
3. Ejecuta Alexa:
   python main.py
4. Elige modo: Always Listening o Push to Talkimport os
import platform
import time
from alexa import AlexaService  # Módulo original

CONFIG_FILE = "config.dict"
alexa = AlexaService(config_file=CONFIG_FILE)

def always_listening():
    print("Alexa lista, modo always listening...")
    try:
        while True:
            alexa.listen()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Saliendo...")

def push_to_talk():
    print("Presiona Enter para hablar con Alexa")
    while True:
        input()
        alexa.listen()

if __name__ == "__main__":
    print("Selecciona modo:\n1 - Always Listening\n2 - Push to Talk")
    choice = input("Opción (1 o 2): ")
    if choice.strip() == "2":
        push_to_talk()
    else:
        always_listening()import os
import platform
import subprocess
import sys

def install_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_ffmpeg():
    system = platform.system()
    if system == "Windows":
        print("Verifica que ffmpeg esté en PATH. Si no, instalar desde https://ffmpeg.org/download.html")
    else:
        print("Instalando ffmpeg en Linux...")
        subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])

if __name__ == "__main__":
    install_packages()
    install_ffmpeg()
    print("¡Setup completado! Ejecuta python main.py para iniciar Alexa.")AlexaPythonUltra/
│
├─ main.py
├─ config.dict
├─ setup.py          # Instala dependencias y ffmpeg automáticamente
├─ requirements.txt
└─ README.md# Alexa Voice Service en Python – Plug & Play

## Setup

### Windows
1. python -m venv env
2. env\Scripts\activate
3. pip install -r requirements.txt
4. python main.py

### Linux / Raspberry Pi
1. python3 -m venv env
2. source env/bin/activate
3. pip install -r requirements.txt
4. sudo apt install ffmpeg -y
5. python3 main.py

## Configuración
- Editar config.dict con tu Client ID y Client Secret de Amazonimport os
import platform
import time

# Suponiendo que el módulo AlexaService está en el repo original
from alexa import AlexaService  

IS_WINDOWS = platform.system() == "Windows"
CONFIG_FILE = "config.dict"
alexa = AlexaService(config_file=CONFIG_FILE)

def always_listening():
    print("Alexa lista, modo always listening...")
    try:
        while True:
            alexa.listen()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Saliendo...")

def push_to_talk():
    print("Presiona Enter para hablar con Alexa")
    while True:
        input()
        alexa.listen()

if __name__ == "__main__":
    MODE = "always"  # Cambia a "push" si quieres push-to-talk
    if MODE == "always":
        always_listening()
    else:
        push_to_talk()AlexaPythonReady/
│
├─ main.py
├─ config.dict
├─ requirements.txt
└─ README.mdpython3 -m venv env
source env/bin/activate
pip install -r requirements.txt
sudo apt install ffmpeg -y
python3 main.pypython -m venv env
env\Scripts\activate
pip install -r requirements.txt
python main.pycherrypy
requests
hyper
pyaudio
SpeechRecognitionimport os
import platform
import time
from alexa import AlexaService  # Suponiendo que existe el módulo original

# Detectar SO
IS_WINDOWS = platform.system() == "Windows"

# Configuración
CONFIG_FILE = "config.dict"

# Inicializar Alexa
alexa = AlexaService(config_file=CONFIG_FILE)

def always_listening():
    print("Alexa lista, modo always listening...")
    try:
        while True:
            alexa.listen()  # Función que activa reconocimiento de voz
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Saliendo...")

def push_to_talk():
    print("Presiona Enter para hablar con Alexa")
    while True:
        input()
        alexa.listen()

if __name__ == "__main__":
    # Elegir modo según preferencia (default: always listening)
    MODE = "always"  # "push" para push-to-talk
    if MODE == "always":
        always_listening()
    else:
        push_to_talk()python-alexa-voice-service/
│
├─ main.py              # Script principal modificado
├─ config.dict          # Configuración de ejemplo
├─ requirements.txt     # Librerías necesarias
└─ README.md            # Instrucciones rápidaspython-alexa-voice-service/
│
├─ main.py              # Script principal modificado
├─ config.dict          # Configuración de ejemplo
├─ requirements.txt     # Librerías necesarias
└─ README.md            # Instrucciones rápidashttps://developer.amazon.com/alexa/console/avs/home[DEFAULT]
client_id = TU_CLIENT_ID
client_secret = TU_CLIENT_SECRET
device_type = my_python_device
product_id = PythonAlexa001# Clonar repo
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service

# Crear entorno virtual
python3 -m venv env
source env/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Instalar ffmpeg
sudo apt install ffmpeg -yPowershell# Clonar repo
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service

# Crear entorno virtual
python -m venv env
env\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Instalar ffmpeg (asegúrate que esté en PATH)
choco install ffmpegpython main.pypython auth_web.pycp config_example.dict config.dict{
  "product_id": "TuProductID",
  "client_id": "TuClientID",
  "client_secret": "TuClientSecret",
  "refresh_token": ""
}pip install git+https://github.com/Lukasa/hyper.gitpip install -r requirements.txtpython3 -m venv venv
source venv/bin/activate   # en Linux/Mac
venv\Scripts\activate      # en Windows# Python Alexa Voice Service

This project is a Python implementation of Amazon's Alexa Voice Service (AVS). The goal of this project is to create cross-platform example Alexa device that is completely compatible with the current AVS API (v20160207). This is a work in progress.

## Requirements
- [Python 3.5+](https://www.python.org/)
	- [cherrypy](http://www.cherrypy.org/)
    - [requests](http://docs.python-requests.org/en/master/)
    - [hyper](https://hyper.readthedocs.org/en/latest/) (developer branch)
	- [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/)
	- [speech_recognition](https://github.com/Uberi/speech_recognition#readme)
- [ffmpeg](https://ffmpeg.org/)
- [Microphone](http://amzn.to/1rvSxuS) and speaker

## Getting Started

Install the necessary requirements and clone the repository.

``
git clone https://github.com/nicholasjconn/python-alexa-voice-service
``

``
cd python-alexa-voice-service
``

Extract and copy the ffmpeg folder to the project's folder. Rename to ffmpeg, so that the ffmpeg command is located in python-alexa-voice-service/ffmpeg/bin/ffmpeg.

Follow the directions from Amazon on how to get your Client ID, Client Secret, and ProductID (parts of Chapter 3 and Chapter 6).

[https://github.com/amzn/alexa-avs-raspberry-pi](https://github.com/amzn/alexa-avs-raspberry-pi)

Rename config_example.dict to config.dict. Then open the file and update the Client ID, Client Secret, and ProductID values to your own values

Run the main.py script. If you run into any errors, chances are that you have missed one of the requirements.

``
python3 main.py
``

## Using the Code

This is a command line based program. You will be receive notices and prompts via the command line. Start a voice command by pressing enter. The software is not always listening (I am waiting on a response from Amazon before enabling this), so a button press is required to active the microphone.

When you would like to close the program, press 'q' and then enter.

Errors and other text may be printed out if anything goes wrong. This is a work in progress.

#### Example Alexa Commands
* "What time is it?"
* "Set an alarm."
* "Where am I?"
* "What is the weather tomorrow?"
* "Are you a robot?"

If you have the Wink hub or any other supported home automation devices, you can connect them via the [Android Alexa App](https://play.google.com/store/apps/details?id=com.amazon.dee.app&hl=en). Once connected, you can say things like "turn on bedroom lights" or "set bedroom lights to 50%".

Have fun!

## Cross-Platform

This code has only been tested on Windows. This project will eventually support Linux and hopefully OS X. The final goal is for this project to work out of the box on a Raspberry Pi.

## Alexa Voice Service

The following link has all of the information needed to understand the Alexa Voice Service API:

[https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/content/avs-api-overview](https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/content/avs-api-overview)

## Bugs

If you run into any bugs, please create an issue on GitHub. Don't hesitate to submit bugs for the README.md as well! I can't promise that I will get to it quickly, but I will do my best to keep this project as bug free as possible (given the time I have to work on it).

## Contributing

Feel free contribute to the code! I will be actively adding new feature until it is full-featured. If you get 
to a feature before me, I may be able to use your code!

## License
MIT - [See LICENSE](./license.txt)

## Future Work
Please feel free to add functionality or fix any bugs that you find. I will be working on this project whenever I have time, so stay tuned for updates.

Currently, only the SpeechRecognizer and SpeechSynthesizer interfaces are supported. More will be added in the near future.

## Change Log
* Version 0.2 - Added Alert (alarm and timer) functionality, and updated README.md
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-servicehttp://localhost:5000───────────────────────────────────────────────
            Modern Gradient Background
     (Animated floating elements – subtle)
───────────────────────────────────────────────

                  [Profile Card – Glass]
           ┌─────────────────────────────┐
           │       Profile Photo          │
           │   Name: José Arturo Ríos    │
           │        Stats / Bio          │
           └─────────────────────────────┘
        (Hover lift, subtle shadow, blur effect)

───────────────────────────────────────────────
               Social Media Buttons
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │Instagram │ │Facebook  │ │TikTok    │
       └──────────┘ └──────────┘ └──────────┘
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │YouTube   │ │Website   │ │Portfolio │
       └──────────┘ └──────────┘ └──────────┘
  (Hover scale + shadow, target="_blank", fade-in on load)

───────────────────────────────────────────────
        Optional Section / Future Extensions
   (Extra links, newsletter signup, mini-bio, etc.)
───────────────────────────────────────────────https://developer.amazon.com/alexa/console/ask