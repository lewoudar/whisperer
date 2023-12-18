from pathlib import Path
from typing import Literal

import torch
from whisper import load_model, utils

from whisperer.console import console
from whisperer.types import Format, ModelType, TaskType


def _get_fp16_option() -> bool:
    """
    Prevents a UserWarning because by default Whisper tries to use the torch.float16
    which is only useful in CUDA (GPU) architectures.
    """
    return torch.cuda.is_available()


def transcribe_audio_file(
        audio_file: str,
        model_name: ModelType,
        language: str | None = None,
        task: TaskType = 'transcribe',
        verbose: bool | None = None,
) -> dict:
    model = load_model(model_name)
    return model.transcribe(str(audio_file), verbose=verbose, language=language, task=task, fp16=_get_fp16_option())


WRITER_MAPPING = {
    'json': utils.WriteJSON,
    'tsv': utils.WriteTSV,
    'vtt': utils.WriteVTT,
    'srt': utils.WriteSRT,
    'txt': utils.WriteTXT,
}


def _write_file(
        audio_file: Path, format_: Literal['json', 'tsv', 'vtt', 'tsv', 'srt'], output_directory: str, result: dict
) -> None:
    console.print(f'writing {audio_file.stem}.{format_} file')
    writer_class = WRITER_MAPPING[format_]
    writer = writer_class(output_directory)
    writer(result, str(audio_file))


def write_files(audio_file: str, formats: list[Format], result: dict, output_directory: str) -> None:
    audio_file = Path(audio_file)
    match formats:
        case ('all', *_):
            for format_ in WRITER_MAPPING:
                _write_file(audio_file, format_, output_directory, result)
        case _:
            for format_ in formats:
                _write_file(audio_file, format_, output_directory, result)
