import click
from click_didyoumean import DYMGroup

from whisperer.commands.audio import audio
from whisperer.commands.completion import install_completion
from whisperer.commands.video import video


@click.version_option('0.1.0', message='%(prog)s version %(version)s')
@click.group(cls=DYMGroup, context_settings={'help_option_names': ['-h', '--help']})
def cli():
    """
    A command line interface to transcribe your audio files and create subtitles for your videos.

    \b
    Note that you will need ffmpeg (https://ffmpeg.org/) installed on your machine to run this command.

    Example usage:

    \b
    # transcribe an audio file in spanish in all formats supported
    # this will create many files like audio.json, audio.srt, etc...
    $ whp audio transcribe audio.mp3 -l es

    \b
    # transcribe multiple audio files. They must have the same source language.
    $ whp audio transcribe audio1.mp3 audio2.wav -l es

    \b
    # transcribe an audio file using the medium model
    $ whp audio transcribe audio.mp3 -l en -m medium

    \b
    # transcribe an audio file in json and srt formats
    # this will create files audio.json and audio.srt
    $ whp audio transcribe audio.mp3 -f json -f srt

    \b
    # extract an audio file from a video file
    $ whp video ea video.mp4 -o audio.mp3

    \b
    # create video with subtitles
    $ whp video subtitles video.mp4 -o video_with_subtitles.mp4

    \b
    # specify the whisper model to use and the source language of the video
    $ whp video subtitles video.mp4 -l en -m medium -o video_with_subtitles.mp4
    """


for command in [install_completion, audio, video]:
    cli.add_command(command)

if __name__ == '__main__':
    cli()
