import speech_recognition as sr
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from gtts import gTTS
import webbrowser as browser
from paho.mqtt import publish
import json
import os
import random

##### CONFIGURAÇÕES #####
hotword = 'rose'


##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o Comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google(audio, language='pt-BR')
                trigger = trigger.lower()

                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))
    return trigger


def responde(arquivo):
    playsound('audios/' + arquivo + '.mp3')


def cria_audio(mensagem):
    try:
        tts = gTTS(mensagem, lang='pt-br')
        tts.save('audios/mensagem.mp3')
        print('Tallud:\n    ' + mensagem)
        playsound('audios/mensagem.mp3')  # windows
        os.remove('audios/mensagem.mp3')

        # Permission in Windows 10 is denied
    except PermissionError:
        numero = random.randint(0, 1000000000000)
        tts = gTTS(mensagem, lang='pt-br')
        tts.save('audios/mensagem' + str(numero) + '.mp3')
        print('Tallud:\n    ' + mensagem)
        playsound('audios/mensagem' + str(numero) + '.mp3')  # windows
        os.remove('audios/mensagem' + str(numero) + '.mp3')


def executa_comandos(trigger):
    if 'notícias' in trigger:
        ultimas_noticias()

    elif 'toca' in trigger and 'bee gees' in trigger:
        playlists('bee_gees')

    elif 'toca' in trigger and 'system' in trigger:
        playlists('soad')

    elif 'tempo agora' in trigger:
        previsao_tempo(tempo=True)

    elif 'temperatura hoje' in trigger:
        previsao_tempo(minmax=True)

    elif 'liga a iluminação' in trigger:
        publica_mqtt('office/iluminacao/status', '1')

    elif 'desativa a iluminação' in trigger:
        publica_mqtt('office/iluminacao/status', '0')

    else:
        mensagem = trigger.strip(hotword)
        cria_audio(mensagem)
        print('C. INVÁLIDO', mensagem)
        responde('comando_invalido')


##### FUNÇÕES COMANDOS #####

def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt - 419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:2]:
        mensagem = item.title.text
        cria_audio(mensagem)


def playlists(album):
    if album == 'bee_gees':
        browser.open('https://open.spotify.com/track/2xSXw1EqGSAKc1e4TPaQvV')
    elif album == 'soad':
        browser.open('https://open.spotify.com/track/2DlHlPMa4M17kufBvI2lEN')


def previsao_tempo(tempo=False, minmax=False):
    site = get(
        'http://api.openweathermap.org/data/2.5/weather?id=3451190&APPID=baae195fdfc14d8b2de4ac91d936c538&units=metric&lang=pt')
    clima = site.json()
    # print(json.dumps(clima, indent=4))
    temperatura = clima['main']['temp']
    minima = clima['main']['temp_min']
    maxima = clima['main']['temp_max']
    descricao = clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}'

    if minmax:
        mensagem = f'Mínima de {minima} e máxima de {maxima}'

    cria_audio(mensagem)


def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=1, retain=True, hostname="soldier.cloudmqtt.com",
                   port=13890, client_id="rosie", auth={'username': 'rjkusnef', 'password': 'ALOKzIIzW09O'})
    if payload == '1':
        mensagem = 'Iluminação ligada!'
    elif payload == '0':
        mensagem = 'Iluminação desligada!'
    cria_audio(mensagem)


def main():
    while True:
        monitora_audio()

main()
