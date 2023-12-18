import os
import pathlib

import click

from whisperer.console import console
from whisperer.types import Format, ModelType
from whisperer.utils import check_model_language_consistency, transcribe_audio_file, write_files


@click.group()
def audio():
    """Audio related subcommands."""
    pass


@audio.command()
@click.argument('audio_files', type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path), nargs=-1)
@click.option(
    '-f',
    '--format',
    'formats',
    multiple=True,
    default=('all',),
    help='Formats supported for the output files. The special value "all" will write files for all formats.',
    show_default=True,
    type=click.Choice(['json', 'txt', 'srt', 'vtt', 'tsv', 'all']),
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
@click.option(
    '-d',
    '--directory',
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
    default=os.getcwd(),
    help='The directory where the transcribed files are stored. If not given, it will default to the current directory.',
)
@click.option('--translate', is_flag=True, help='Transcribe and directly translate to English language.')
@click.option('--verbose', is_flag=True, help='Print debug information about the file being processed.')
def transcribe(
    audio_files: list[pathlib.Path],
    formats: list[Format],
    model: ModelType,
    verbose: bool,
    language: str | None,
    translate: bool,
    directory: pathlib.Path,
) -> None:
    """
    Transcribe audio files (AUDIO_FILES) in different output formats.

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

    \b transcribe an audio file from german to english
    $ whp audio transcribe audio.mp3 -l de --translate
    """
    check_model_language_consistency(model, language)
    for audio_file in audio_files:
        console.print(f'[info]processing file {audio_file} :gear:')
        task = 'translate' if translate else 'transcribe'
        result = transcribe_audio_file(audio_file, model, language=language, verbose=verbose, task=task)
        write_files(audio_file, formats, result, directory)

    console.print('[success]Done! :party_popper:')
