import cv2
import mss
import numpy
from pynput import keyboard

# Set up the screen capture.
# Adjust this to your screen resolution.
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
sct = mss.mss()
keep_listening = True


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


# Set up the video writer.
# You can experiment with different codecs.
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = 30.0  # Adjust this to your desired frames per second.
out_file = "output.mp4"  # The output file.
video_writer = cv2.VideoWriter(
    out_file, fourcc, fps, (monitor["width"], monitor["height"]))

# Set up the keyboard listener.
listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
listener.start()

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

print("Releasing resources...")

# Release the resources.
video_writer.release()
cv2.destroyAllWindows()
