import PyPDF2
from time import sleep
import gtts
import pyglet
import os

def reader(file):
    pdfFileObj = open(f'files/{file}', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    output = pageObj.extractText()
    print(output)
    tts = gtts.gTTS(output)
    filename = 'temp.mp3'
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()

    sleep(music.duration)  # prevent from killing
    os.remove(filename)  # remove temperory file