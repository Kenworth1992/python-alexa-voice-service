# Clonar repo
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service

# Crear entorno virtual
python -m venv env
env\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Instalar ffmpeg (asegúrate que esté en PATH)
choco install ffmpeg
# Clonar repo
git clone https://github.com/Kenworth1992/python-alexa-voice-service.git
cd python-alexa-voice-service

# Crear entorno virtual
python3 -m venv env
source env/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Instalar ffmpeg
sudo apt install ffmpeg -y