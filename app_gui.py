import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import keyboard
import subprocess as sub
import os
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
import threading as tr

#VENTANA
main_window = Tk()
main_window.title("Samira AV")
main_window.geometry("1080x920")
main_window.resizable(0, 0)
main_window.configure(bg='#41295a')

comandos = """
            Comandos que puedes ejecutar:
            - Reproduce: Video en YT
            - Busca: Contenido en wikipedia
            - Abre: Pagina web
            - Hora: Muestra la hora actual
            - Fecha: Muestra la fecha actual
            - Programa: Ejecuta un programa
            - Escribe: Escribe un txt
            - Stop: Samira deja de escuhar
"""

label_title = Label(main_window, text="Samira AV", bg="#2E1437", fg="white",
                    font=('Arial', 40, 'bold'))
label_title.pack(pady=10)

canvas_comandos = Canvas(bg="#2E1437", height=200, width=300)
canvas_comandos.place(x=700, y=700)
canvas_comandos.create_text(100, 100, text=comandos,
                            fill="white", font='Arial 12')

samira_photo = ImageTk.PhotoImage(Image.open("AV.jpg"))
window_photo = Label(main_window, image=samira_photo)
window_photo.pack(pady=0.1)


#VOZ DEL ASISTENTE
def spanish_voice():
    change_voice(0)


def english_voice():
    change_voice(1)


def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine. setProperty('rate', 145)
    talk("Hola soy Samira!")


#LINEAS DE CODIGO PARA EL RECONOCIMIENTO DE VOZ
name = 'samira'
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine. setProperty('rate', 145)

#RUTAS PARA ACCEDER A SITIOS Y PROGRAMAS
sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'twitter': 'twitter.com',
    'ups': 'ups.edu.ec',
    'whatsapp': 'web.whatsapp.com',
}

files = {
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    'excel': r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    'epic': r"D:\EpicGames\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
    'netbeans': r"C:\Program Files\NetBeans 8.2\bin\netbeans64.exe",
    'visio': r"C:\Program Files\Microsoft Office\root\Office16\VISIO.EXE"

}


#CODIGO ASISTENTE
def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            talk("Esperando ordenes")
            voice = listener.listen(source)
            rec = listener.recognize_google(voice, language='es-ES')
            rec = rec.lower()

            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec


def run_samira():
    while True:
        rec = listen()
        if 'hola' in rec:
            hola = rec.replace('hola', '')
            talk("Hola soy tu asistente virtual, Me llamo samira ")
            talk("¿En que te puedo ayudar?")
        elif 'comandos' in rec:
            csamira = rec.replace('comandos', '')
            talk("Los comandos que puedo ejecutar son los siguientes:")
            talk("Reproduce: reproduzco un video en youtube")
            talk("Busca: busco contenido en wikipedia")
            talk("Abre: abro una pagina web")
            talk("Hora: muestro la hora actual")
            talk("Fecha: muestro la fecha actual")
            talk("Programa: ejecuto un programa")
            talk("Escribe: escribo un bloc de notas")
            talk("Stop: dejo de escucharte!")
        elif 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            talk('Reproduciendo ' + music)
            pywhatkit.playonyt(music)
        elif 'hora' in rec:
            hora = datetime.datetime.now().strftime('%I:%M %p')
            talk("Son las " + hora)
        elif 'fecha' in rec:
            fecha = datetime.datetime.now().strftime('%d/%m/%Y')
            talk("Hoy es " + fecha)
        elif 'busca' in rec:
            order = rec.replace('busca', '')
            wikipedia.set_lang("es")
            info = wikipedia.summary(order, 1)
            print(order + ": " + info)
            talk(info)
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
        elif 'programa' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("anotaciones.txt", 'a') as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
        elif 'stop' in rec:
            talk('Samira se ha desconectado!')
            break


def write(f):
    talk("¿Que escribo?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, revisalo")
    sub.Popen("anotaciones.txt", shell=True)


button_voice_es = Button(main_window, text="Voz España", fg="white", bg="#2E1437",
                         font=("Arial", 14, "bold"), command=spanish_voice)
button_voice_es.place(x=200, y=750, width=150, height=40)
button_voice_us = Button(main_window, text="Voz USA", fg="white", bg="#2E1437",
                         font=("Arial", 14, "bold"), command=english_voice)
button_voice_us.place(x=200, y=800, width=150, height=40)
button_listen = Button(main_window, text="Escuchar", fg="white", bg="#870000",
                       font=("Arial", 20, "bold"), command=run_samira)
button_listen.pack(pady=10)


main_window.mainloop()
