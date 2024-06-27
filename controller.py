# TODO: fix false positives

import pyaudio
import scipy.fftpack
import numpy
import keyboard
import time

DELAY = 2.0

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

# UP, DOWN, LEFT, RIGHT, Z, X
NOTES = ["low e", "a", "d", "g", "high e", "10b"]
NOTE_FREQ = [129.1992, 107.660, 150.7324, 193.7988, 172.2656, 215.332]

# initialize pyAudio
p = pyaudio.PyAudio()

# open stream for note listening
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

THRESHOLD = 100


# convert notes to keys
def keyboard_input():
    last_pressed = time.time()
    while True:
        data = stream.read(CHUNK)
        audio_data = numpy.frombuffer(data, dtype=numpy.int16)
        fft_data = numpy.abs(scipy.fftpack.fft(audio_data))
        freq = scipy.fftpack.fftfreq(len(fft_data), 1.0 / RATE)

        fft_data = fft_data[1:]
        freq = freq[1:]

        peak_idx = numpy.argmax(fft_data)
        peak_freq = freq[peak_idx]

        current_time = time.time()
        if current_time - last_pressed > DELAY:
            match abs(peak_freq):
                case _ if numpy.isclose(peak_freq, NOTE_FREQ[0], atol=0.5):
                    keyboard.press_and_release("up")
                    print(f"{NOTES[0]} - Pressed up")
                case _ if numpy.isclose(peak_freq, NOTE_FREQ[1], atol=0.5):
                    keyboard.press_and_release("down")
                    print(f"{NOTES[1]} - Pressed down")
                case _ if numpy.isclose(peak_freq, NOTE_FREQ[2], atol=0.5):
                    keyboard.press_and_release("left")
                    print(f"{NOTES[2]} - Pressed left")
                case _ if numpy.isclose(peak_freq, NOTE_FREQ[3], atol=0.5):
                    keyboard.press_and_release("right")
                    print(f"{NOTES[3]} - Pressed right")
                case _ if numpy.isclose(peak_freq, NOTE_FREQ[4], atol=0.5):
                    keyboard.press_and_release("z")
                    print(f"{NOTES[4]} - Pressed z")
                case _ if numpy.isclose(peak_freq, NOTE_FREQ[5], atol=0.5):
                    keyboard.press_and_release("x")
                    print(f"{NOTES[5]} - Pressed x")


# find frequency of notes
def detect_note():
    while True:
        data = stream.read(CHUNK)
        audio_data = numpy.frombuffer(data, dtype=numpy.int16)
        fft_data = numpy.abs(scipy.fftpack.fft(audio_data))
        freq = scipy.fftpack.fftfreq(len(fft_data), 1.0 / RATE)

        fft_data = fft_data[1:]
        freq = freq[1:]

        peak_idx = numpy.argmax(fft_data)
        peak_freq = freq[peak_idx]

        if abs(peak_freq) > THRESHOLD and abs(peak_freq) < THRESHOLD + 200:
            print(f"Detected frequency: {abs(peak_freq)} Hz")


# try:
#     detect_note()
# except KeyboardInterrupt:
#     pass

try:
    print("listening")
    keyboard_input()
except KeyboardInterrupt:
    pass

stream.stop_stream()
stream.close()
p.terminate()
