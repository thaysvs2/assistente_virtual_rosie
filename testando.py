import speech_recognition as sr
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from gtts import gTTS


#### Configuracoes #####
hotword = 'rose'

####Funcoes Principais ####

def monitora_microfone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Aguardando o comando: ")
            audio = microfone.listen(source)
            try:
                trigger = microfone.recognize_google(audio, language='pt-BR')
                trigger = trigger.lower()

                if hotword in trigger:
                    print('Comando: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google Speech to Text could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech to Text service; {0}".format(e))

    return trigger

def responde(arquivo):
    playsound('audios/' + arquivo + '.mp3')

def cria_audio(mensagem):
    tts = gTTS(mensagem, lang='pt-br')
    tts.save('audios/mensagem.mp3')
    playsound('audios/mensagem.mp3')  # WINDOWS

def executa_comandos(trigger):
    if 'noticias' in trigger:
        ultimas_noticias()

####Funcoes Comandos ####

def ultimas_noticias():
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt - 419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    for item in noticias.findAll('item')[:5]:
        mensagem = item.title.text
        print(mensagem)
        cria_audio(mensagem)

def main():
    while True:
        monitora_microfone()

main()

#ultimas_noticias()