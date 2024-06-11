import cv2
import mss
import numpy

# Set up the screen capture.
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # Adjust this to your screen resolution.
sct = mss.mss()

# Set up the video writer.
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # You can experiment with different codecs.
fps = 30.0  # Adjust this to your desired frames per second.
out_file = "output.mp4"  # The output file.
video_writer = cv2.VideoWriter(out_file, fourcc, fps, (monitor["width"], monitor["height"]))

# Capture the screen and encode the frames to video.
while True:
    # Get the screen image.
    img = sct.grab(monitor)
    img_rgb = numpy.array(img)  # MSS returns images in BGR format, so we'll convert it to RGB.
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)

    # Write the frame to the video file.
    video_writer.write(img_rgb)

    # Break the loop if the 'q' key is pressed.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the resources.
video_writer.release()
cv2.destroyAllWindows()