import argparse
import cv2
import mss
import numpy
from pynput import keyboard
import threading
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import soundcard as sc
import soundfile as sf

# Set up the screen capture.
# Adjust this to your screen resolution.
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss.mss()
keep_listening = True
video_output = "tempVideo.mp4"  # The output file.

# Audio capture settings
audio_output = "tempAudio.wav"
SAMPLE_RATE = 48000  # [Hz]. sampling rate.
gain = 2.0  # Adjust this gain factor to increase the audio volume


def on_key_press(key):
    global keep_listening
    try:
        if key.char == 'q':
            print('The key "q" is pressed. Stopping the program...')
            keep_listening = False
    except AttributeError:
        pass


def on_key_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def capture_audio():
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        frames = []
        while keep_listening:
            data = mic.record(numframes=SAMPLE_RATE // 10)
            data = data * gain
            frames.append(data)

        frames = numpy.concatenate(frames)
        sf.write(file=audio_output, data=frames, samplerate=SAMPLE_RATE)


# Set up the argument parser
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-o', '--output', type=str, default='output.mp4',
                    help='The path and name of the output video file.')

args = parser.parse_args()

# Set up the video writer.
# You can experiment with different codecs.
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = 30.0  # Adjust this to your desired frames per second.
video_writer = cv2.VideoWriter(
    video_output, fourcc, fps, (monitor["width"], monitor["height"]))

# Set up the keyboard listener.
listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
listener.start()

# Start audio capture in a separate thread
audio_thread = threading.Thread(target=capture_audio)
audio_thread.start()

print("Capturing screen...")

# Capture the screen and encode the frames to video.
while keep_listening:
    # Get the screen image.
    img = sct.grab(monitor)
    # MSS returns images in BGRA format, so we'll convert it to BGR.
    img_bgra = numpy.array(img)
    img_bgr = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2BGR)

    # Write the frame to the video file.
    video_writer.write(img_bgr)

# Wait for audio capture to finish
audio_thread.join()

print("Releasing resources...")

# Release the resources.
video_writer.release()
cv2.destroyAllWindows()

video = VideoFileClip(video_output)
audio = AudioFileClip(audio_output)

# Set the audio of the video clip
video = video.set_audio(audio)

# Write the final output to a file
video.write_videofile(args.output, codec="libx264", audio_codec="aac")
os.remove(video_output)
os.remove(audio_output)
