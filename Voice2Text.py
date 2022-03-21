#All imports for audio, audio files, sppech recognition and database
import pyaudio
import wave
import speech_recognition as sr
import sys
from firebase import firebase

#Audio parameters
form1 = pyaudio.paInt16 #audio is 16bit format
chans = 1 #Each frame has 1 sample
sampRate = 44100 #Number of samples recorded per second
chunk = 4096 #Number of frames
recordSecs = 6 #Recording time
deviceIndex = 1 #USB Device location
fileName = 'outwav.wav' #Filename to store audio

audio = pyaudio.PyAudio()
stream = audio.open(format = form1, rate = sampRate,
                    channels = chans, input_device_index = deviceIndex, #inputting audio parameters
                    input = True, frames_per_buffer=chunk)
print('recording')
frames = []
for i in range(0, int((sampRate/chunk)*recordSecs)):
    data = stream.read(chunk, exception_on_overflow = False) #Looping through and recording each frame
    frames.append(data)
print('recording Finnish!')
stream.stop_stream()
stream.close()
audio.terminate() #Closing PyAudio

#Saving the audio recording as a .wav file with audio parameters
wavefile = wave.open(fileName,'wb')
wavefile.setnchannels(chans)
wavefile.setsampwidth(audio.get_sample_size(form1))
wavefile.setframerate(sampRate)
wavefile.writeframes(b''.join(frames))
wavefile.close()

#Database and speach recognition parameters
filename = "outwav.wav"
r = sr.Recognizer()
dataBase = firebase.FirebaseApplication("https://assist-1b2c0-default-rtdb.europe-west1.firebasedatabase.app/")

with sr.AudioFile(filename) as source:
    audioData = r.record(source)
    text = r.recognize_google(audioData) #Converting audioData to text
    print(text)
    data = {'audio': text} 
    dataBase.post("webData/uploadedText", data) #Uploading text data to Database