import pyaudio
import scipy.fftpack
import numpy
import keyboard
import pyautogui
import pydirectinput
import time
from collections import Counter

DELAY = 1.0

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1

# UP, DOWN, LEFT, RIGHT, Z, X
NOTES = ["low e", "a", "d", "g", "high e", "10b"]
NOTE_FREQ = [129.1992, 107.660, 150.7324, 193.7988, 172.2656, 215.332]

# initialize pyAudio
p = pyaudio.PyAudio()

# open stream for note listening
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

THRESHOLD = 100
TOLERANCE = 0.5


# convert notes to keys
def keyboard_input():
    freq_arr = []
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

        freq_arr.append(abs(peak_freq))

        current_time = time.time()
        if current_time - last_pressed > RECORD_SECONDS:
            m_c_freq = Counter(freq_arr).most_common(1)[0][0]
            for i, note_freq in enumerate(NOTE_FREQ):
                if numpy.isclose(m_c_freq, note_freq, atol=TOLERANCE):
                    key_pressed = {NOTE_FREQ[0]: "up", NOTE_FREQ[1]: "down", NOTE_FREQ[2]: "left", NOTE_FREQ[3]: "right", NOTE_FREQ[4]: "z", NOTE_FREQ[5]: "x"}[note_freq]
                    # keyboard.press_and_release(key_pressed)
                    # pyautogui.press(key_pressed)
                    pydirectinput.press(key_pressed)
                    print(f"{NOTES[i]} - Pressed {key_pressed}")
                    last_pressed = time.time()
            freq_arr = []


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
#     print("listening")
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
