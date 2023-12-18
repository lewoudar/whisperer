import click

from whisperer.console import console
from whisperer.utils import extract_audio_from_video


@click.group()
def video():
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
