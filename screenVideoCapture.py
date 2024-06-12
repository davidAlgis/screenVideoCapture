import argparse
import cv2
import mss
import numpy as np
from pynput import keyboard
import threading
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import soundcard as sc
import soundfile as sf


class ScreenRecorder:
    def __init__(self, monitor, video_output, audio_output, sample_rate, gain, record_audio):
        """
        Initializes the ScreenRecorder with monitor settings, output file paths, sample rate, gain, and audio recording flag.
        """
        self.monitor = monitor
        self.video_output = video_output
        self.audio_output = audio_output
        self.sample_rate = sample_rate
        self.gain = gain
        self.keep_listening = True
        self.sct = mss.mss()
        self.video_writer = self._setup_video_writer()
        self.record_audio = record_audio

    def _setup_video_writer(self):
        """
        Sets up the video writer with specified codec and frame rate.
        """
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = 30.0  # Adjust this to your desired frames per second.
        return cv2.VideoWriter(
            self.video_output, fourcc, fps,
            (self.monitor["width"], self.monitor["height"])
        )

    def on_key_press(self, key):
        """
        Handles key press events to stop the program when 'q' is pressed.
        """
        try:
            if key.char == 'q':
                print('Stopping recording...')
                self.keep_listening = False
        except AttributeError:
            pass

    def on_key_release(self, key):
        """
        Handles key release events to stop the listener when 'esc' is released.
        """
        if key == keyboard.Key.esc:
            return False

    def capture_audio(self):
        """
        Captures audio using the soundcard library with loopback from the default speaker.
        """
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.sample_rate) as mic:
            frames = []
            while self.keep_listening:
                data = mic.record(numframes=self.sample_rate // 10)
                data = data * self.gain
                frames.append(data)

            frames = np.concatenate(frames)
            sf.write(file=self.audio_output, data=frames,
                     samplerate=self.sample_rate)

    def capture_screen(self):
        """
        Captures the screen and writes the frames to the video file.
        """
        while self.keep_listening:
            img = self.sct.grab(self.monitor)
            img_bgra = np.array(img)
            img_bgr = cv2.cvtColor(img_bgra, cv2.COLOR_BGRA2BGR)
            self.video_writer.write(img_bgr)

    def release_resources(self):
        """
        Releases the resources used by the video writer and closes all OpenCV windows.
        """
        self.video_writer.release()
        cv2.destroyAllWindows()

    def combine_audio_video(self, output_file):
        """
        Combines the captured audio and video into a single file.
        """
        video = VideoFileClip(self.video_output)
        if self.record_audio:
            audio = AudioFileClip(self.audio_output)
            video = video.set_audio(audio)
        video.write_videofile(output_file, codec="libx264", audio_codec="aac")
        os.remove(self.video_output)
        if self.record_audio:
            os.remove(self.audio_output)


def str2bool(v):
    """
    Converts a string argument to a boolean value.
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def ensure_directory_exists(file_path):
    """
    Ensures the directory for the given file path exists, creates it if it does not.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def main(args):
    """
    Main function to set up the ScreenRecorder and start the capturing process.
    """
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    video_output = "tempVideo.mp4"
    audio_output = "tempAudio.wav"
    sample_rate = 48000
    gain = 2.0

    recorder = ScreenRecorder(monitor, video_output,
                              audio_output, sample_rate, gain, args.audio)

    listener = keyboard.Listener(
        on_press=recorder.on_key_press, on_release=recorder.on_key_release)
    listener.start()

    if args.audio:
        audio_thread = threading.Thread(target=recorder.capture_audio)
        audio_thread.start()

    print("Press 'q' to stop capture.")
    print("Capturing screen...")
    recorder.capture_screen()

    if args.audio:
        audio_thread.join()

    print("Releasing resources...")
    recorder.release_resources()

    ensure_directory_exists(args.output)
    recorder.combine_audio_video(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Screen and audio recorder.')
    parser.add_argument('-o', '--output', type=str, default='output.mp4',
                        help='The path and name of the output video file.')
    parser.add_argument('-a', '--audio', type=str2bool, nargs='?', const=True, default=True,
                        help='Indicate if audio should be recorded. (default is true)')

    args = parser.parse_args()
    main(args)
