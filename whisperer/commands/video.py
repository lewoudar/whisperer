import click

from whisperer.console import console
from whisperer.types import ModelType
from whisperer.utils import check_model_language_consistency, create_video_with_subtitles, extract_audio_from_video


@click.group()
def video():
    """Video related subcommands."""
    pass


@video.command('ea')
@click.argument('video_file', type=click.Path(exists=True, dir_okay=False))
@click.option(
    '-o',
    '--output',
    type=click.Path(dir_okay=False, writable=True),
    required=True,
    prompt='Output File',
    help='Output audio file.',
)
def extract_audio(video_file: str, output: str):
    """
    Extract audio from video file (VIDEO_FILE).

    Example usage:

    \b
    $ whp video ea video.mp4 -o audio.mp3
    """
    console.print(f'[info]Processing {video_file} :gear:')
    extract_audio_from_video(video_file, output)
    console.print('[success]Done! :party_popper:')


@video.command('subtitles')
@click.argument('video_file', type=click.Path(exists=True, dir_okay=False))
@click.option(
    '-o',
    '--output',
    type=click.Path(dir_okay=False, writable=True),
    required=True,
    prompt='Output File',
    help='Output video file.',
)
@click.option(
    '-l',
    '--language',
    help='Source language of the audio files. If not given, it will be detected automatically,'
    ' but it will take some time.',
)
@click.option(
    '-m',
    '--model',
    default='base',
    show_default=True,
    help='The Whisper model to use. The "*.en" versions are specific to the English language.',
    type=click.Choice(
        ['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large.en']
    ),
)
def add_subtitles_to_video(video_file: str, output: str, language: str | None, model: ModelType):
    """
    Creates a copy of the given video with subtitles added.

    Example usage:

    \b
    $ whp video subtitles video.mp4 -o video_with_subtitles.mp4

    \b
    # specify the whisper model to use and the source language of the video
    $ whp video subtitles video.mp4 -l en -m medium -o video_with_subtitles.mp4
    """
    check_model_language_consistency(model, language)
    create_video_with_subtitles(video_file, output, language, model)
