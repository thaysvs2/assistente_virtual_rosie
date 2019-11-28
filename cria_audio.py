from gtts import gTTS
#from subprocess import call   # MAC / LINUX
from playsound import playsound  # WINDOWS

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/comando_invalido.mp3')

    #call(['afplay', 'audios/hello.mp3']) #OSX
    #call(['aplay', 'audios/hello.mp3']) #LINUX
    playsound('audios/comando_invalido.mp3')  # WINDOWS

cria_audio('Eu não sou paga para isso!')