import pyaudio
import wave
import speech_recognition as sr
import sys
from firebase import firebase

form1 = pyaudio.paInt16
chans = 1
sampRate = 44100
chunk = 4096
recordSecs = 6
deviceIndex = 1
fileName = 'outwav.wav'

audio = pyaudio.PyAudio()
stream = audio.open(format = form1, rate = sampRate,
                    channels = chans, input_device_index = deviceIndex,
                    input = True, frames_per_buffer=chunk)
print('recording')
frames = []
for i in range(0, int((sampRate/chunk)*recordSecs)):
    data = stream.read(chunk, exception_on_overflow = False)
    frames.append(data)
print('recording Finnish!')
stream.stop_stream()
stream.close()
audio.terminate()

wavefile = wave.open(fileName,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form1))
wavefile.setframerate(sampRate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

filename = "outwav.wav"
r = sr.Recognizer()
dataBase = firebase.FirebaseApplication("https://assist-1b2c0-default-rtdb.europe-west1.firebasedatabase.app/")

with sr.AudioFile(filename) as source:
    audioData = r.record(source)
    text = r.recognize_google(audioData)
    print(text)
    data = {'audio': text}
    dataBase.post("webData/uploadedText", data)