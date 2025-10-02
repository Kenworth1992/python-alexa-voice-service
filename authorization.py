python main.pypython auth_web.py{
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
───────────────────────────────────────────────https://developer.amazon.com/alexa/console/askconst https = require("https");

exports.handler = async (event) => {
    console.log("Request: ", JSON.stringify(event));

    let responseText = "No entendí bien lo que quieres.";

    if (event.request.type === "LaunchRequest") {
        responseText = "¡Hola! Soy Camila Gretel, tu asistente. ¿Qué quieres que haga?";
    }

    if (event.request.type === "IntentRequest") {
        const intentName = event.request.intent.name;

        if (intentName === "LightsIntent") {
            // Aquí simulas el encendido de luces
            await callWebhook("https://tu-webhook.com/lights/on");
            responseText = "Listo, las luces quedaron encendidas.";
        }

        if (intentName === "NotificationIntent") {
            await callWebhook("https://tu-webhook.com/notify");
            responseText = "Notificación enviada correctamente.";
        }

        if (intentName === "AMAZON.HelpIntent") {
            responseText = "Puedes pedirme que encienda luces o que mande una notificación.";
        }

        if (intentName === "AMAZON.CancelIntent" || intentName === "AMAZON.StopIntent") {
            responseText = "Adiós, estaré aquí cuando me necesites.";
        }
    }

    return buildResponse(responseText);
};

// 👉 Función auxiliar para mandar requests a tu API/Webhook
function callWebhook(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            console.log(`Webhook status: ${res.statusCode}`);
            resolve();
        }).on("error", (e) => {
            console.error(`Error webhook: ${e}`);
            reject(e);
        });
    });
}

// 👉 Respuesta para Alexa
function buildResponse(outputText) {
    return {
        version: "1.0",
        response: {
            outputSpeech: {
                type: "PlainText",
                text: outputText,
            },
            shouldEndSession: false,
        },
    };
}const https = require("https");

exports.handler = async (event) => {
    console.log("Request: ", JSON.stringify(event));

    let responseText = "No entendí bien lo que quieres.";

    if (event.request.type === "LaunchRequest") {
        responseText = "¡Hola! Soy Camila Gretel, tu asistente. ¿Qué quieres que haga?";
    }

    if (event.request.type === "IntentRequest") {
        const intentName = event.request.intent.name;

        if (intentName === "LightsIntent") {
            // Aquí simulas el encendido de luces
            await callWebhook("https://tu-webhook.com/lights/on");
            responseText = "Listo, las luces quedaron encendidas.";
        }

        if (intentName === "NotificationIntent") {
            await callWebhook("https://tu-webhook.com/notify");
            responseText = "Notificación enviada correctamente.";
        }

        if (intentName === "AMAZON.HelpIntent") {
            responseText = "Puedes pedirme que encienda luces o que mande una notificación.";
        }

        if (intentName === "AMAZON.CancelIntent" || intentName === "AMAZON.StopIntent") {
            responseText = "Adiós, estaré aquí cuando me necesites.";
        }
    }

    return buildResponse(responseText);
};

// 👉 Función auxiliar para mandar requests a tu API/Webhook
function callWebhook(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            console.log(`Webhook status: ${res.statusCode}`);
            resolve();
        }).on("error", (e) => {
            console.error(`Error webhook: ${e}`);
            reject(e);
        });
    });
}

// 👉 Respuesta para Alexa
function buildResponse(outputText) {
    return {
        version: "1.0",
        response: {
            outputSpeech: {
                type: "PlainText",
                text: outputText,
            },
            shouldEndSession: false,
        },
    };
}"""
Based on code written by sammachin.

See https://github.com/sammachin/AlexaCHIP for the original code

"""


import cherrypy
import os
from cherrypy.process import servers
import requests
import json
import threading
import urllib.parse

import helper

class Start(object):
    def __init__(self, config):
        self.config = config

    def index(self):
        sd = json.dumps({
            "alexa:all": {
                "productID": self.config['ProductID'],
                "productInstanceAttributes": {
                    "deviceSerialNumber": "123456"
                }
            }
        })
        callback = cherrypy.url() + "code"
        payload = {
            "client_id": self.config['Client_ID'],
            "scope": "alexa:all",
            "scope_data": sd,
            "response_type": "code",
            "redirect_uri": callback
        }
        req = requests.Request('GET', "https://www.amazon.com/ap/oa", params=payload)
        p = req.prepare()
        raise cherrypy.HTTPRedirect(p.url)

    def code(self, var=None, **params):
        code = urllib.parse.quote(cherrypy.request.params['code'])
        callback = cherrypy.url()
        payload = {
            "client_id": self.config['Client_ID'],
            "client_secret": self.config['Client_Secret'],
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": callback
        }
        url = "https://api.amazon.com/auth/o2/token"
        r = requests.post(url, data=payload)
        resp = r.json()

        self.config['refresh_token'] = resp['refresh_token']
        helper.write_dict('config.dict',self.config)

        threading.Timer(1, lambda: cherrypy.engine.exit()).start()

        return "Authentication successful! Please return to the program."

    index.exposed = True
    code.exposed = True


def get_authorization():
    # Load configuration dictionary
    config = helper.read_dict('config.dict')

    cherrypy.config.update({'server.socket_host': '0.0.0.0', })
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')), })
    cherrypy.quickstart(Start(config))
