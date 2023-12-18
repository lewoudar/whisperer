# Whisperer

It is a fun project I started to complement this article where I introduce
the [whisper](https://github.com/openai/whisper) project.

It is a command line you can use to transcribe audio files or create subtitles for your videos.

## Installation

You will need **Python3.10** or higher to play with the project. You should also have all the dependencies need
to build binary dependencies like [gcc](https://gcc.gnu.org/) for Linux/Unix systems
or [Visual Studio](https://visualstudio.microsoft.com/) with C/C++
support for Windows.
Last but not least, you will need [ffmpeg](https://ffmpeg.org/) installed on your machine.

Once all the prerequisites have been met, you can run one of the following commands.

```shell
# with pip
$ pip install git+https://github.com/lewoudar/whisperer

# with poetry
$ poetry add git+https://github.com/lewoudar/whisperer

# with pipx
$ pipx install git+https://github.com/lewoudar/whisperer
```

## Usage

The usage is simple. Hopefully, you will understand by just reading the command documentation :)

```shell
$ whp --help
Usage: whp [OPTIONS] COMMAND [ARGS]...

  A command line interface to transcribe your audio files and create subtitles
  for your videos.

  Note that you will need ffmpeg (https://ffmpeg.org/) installed on your machine to run this command.

  Example usage:

  # transcribe an audio file in spanish in all formats supported
  # this will create many files like audio.json, audio.srt, etc...
  $ whp audio transcribe audio.mp3 -l es

  # transcribe multiple audio files. They must have the same source language.
  $ whp audio transcribe audio1.mp3 audio2.wav -l es

  # transcribe an audio file using the medium model
  $ whp audio transcribe audio.mp3 -l en -m medium

  # transcribe an audio file in json and srt formats
  # this will create files audio.json and audio.srt
  $ whp audio transcribe audio.mp3 -f json -f srt

  # extract an audio file from a video file
  $ whp video ea video.mp4 -o audio.mp3

  # create video with subtitles
  $ whp video subtitles video.mp4 -o video_with_subtitles.mp4

  # specify the whisper model to use and the source language of the video
  $ whp video subtitles video.mp4 -l en -m medium -o video_with_subtitles.mp4

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  audio               Audio related subcommands.
  install-completion  Install completion script for bash, zsh and fish...
  video               Video related subcommands.
```