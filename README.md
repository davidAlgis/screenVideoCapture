# Screen and Audio Recorder

This Python script captures the screen and audio, allowing users to specify various options such as output file path, video codec, bitrate, and frame rate. It also offers an option to enable or disable audio recording.
 
__The project is still under development there is a problem of synchronization of audio and video. However, it should works normally if you only capturing video.__

## Installation

To run this script, you'll need to ensure you have the required Python libraries. Install them using the `requirements.txt` file provided in this repository.

```
pip install -r requirements.txt
```


## Usage

Ensure you have Python 3.6 or newer installed on your system. Clone this repository or download the script and `requirements.txt` file. Then, install the required libraries as mentioned above.

To use the script, run it from the command line with the desired options:

```
python screenVideoCapture.py [options]
```

## Options

- `-o`, `--output` <output_file>: Specify the path and name of the output video file. Default is `output.mp4`.
- `-a`, `--audio` <true/false>: Indicate if audio should be recorded. Default is `true`.
- `-c`, `--codec` <codec>: The codec to use for video compression. Options are `h264` and `h265`. Default is `h264`.
- `-b`, `--bitrate` <bitrate>: The bitrate for video compression in bits per second. Default is `1000000`.
- `-f`, `--fps` <frames_per_second>: The frames per second of the video. Default is `30`.
- `-d`, `--duration` <seconds>: The duration for which the recording should run in seconds. Default is None, it will only stop after user has press `q` key.
- `-h`, `--help`: Display help information showing all command-line options.

## Example

To capture the screen and audio, saving the video to `MyOutput.mp4` with the H.265 codec, a bitrate of 500,000 bits per second, and a frame rate of 15 frames per second, you can use the following command:

```
python screenVideoCapture.py -o "MyOutput.mp4" -a true -c h265 -b 500000 -f 15
```


To capture the screen without audio, using the H.264 codec and default settings, you can use:

```
python screenVideoCapture.py -a false
```

## Issues

If you encounter any issues or have suggestions for improvements, please submit them to the GitHub issue tracker for this project.