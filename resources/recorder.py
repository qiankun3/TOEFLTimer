import pyaudio
import wave
import argparse

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 45
#TIME_STARTRECORD = re.sub('[^A-Za-z0-9]+', '', str(datetime.datetime.now()))
#WAVE_OUTPUT_FILENAME =  TIME_STARTRECORD[:14] + ".wav"

parser = argparse.ArgumentParser()
parser.add_argument('duration', type=int, help='set how long it last')
parser.add_argument('filename', type=str, help='customize the filename')
args = parser.parse_args()

#def record(time = RECORD_SECONDS, filename = WAVE_OUTPUT_FILENAME):
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * args.duration)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(args.filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
