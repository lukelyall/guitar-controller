# Guitar Controller
This program integrates audio processing with Python's PyAudio library. It detects guitar notes through Fourier analysis and maps each detected note to a keyboard input. This allows the guitar to act as a keyboard, turning played notes into key presses.
# Usage
To use this program, you need to run the following command in your terminal:
```
pip install pyaudio numpy scipy pydirectinput
```
With that installed, you now need to edit and find the frequencies of your own guitar notes using the detect_note() function and update the NOTE_FREQ list. Once that is finished, you can run the program with the following:
```
python controller.py
```
