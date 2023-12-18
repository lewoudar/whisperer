import shutil
import subprocess  # nosec
import tempfile
from pathlib import Path
from typing import Literal

from whisper import load_model
from whisper.utils import WriteSRT


def run_command(command_list: list[str]) -> str:
    try:
        result = subprocess.run(command_list, check=True, text=True, capture_output=True)  # nosec
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"The command '{command_list}' failed with error:\n{e!s}")
        print(e.stdout)


def extract_audio_from_video(video_path: str, temp_dir: str) -> Path:
    directory = Path(temp_dir)
    audio_file = directory / 'audio.wav'
    command = ['ffmpeg', '-i', video_path, '-vn', '-ab', '192k', '-ar', '48000', '-y', str(audio_file)]
    print(run_command(command))
    return audio_file


def get_text_from_audio(
    audio_file: Path,
    temp_dir: str,
    model_name: Literal['tiny', 'base', 'small', 'medium', 'large'] = 'small',
    verbose: bool | None = None,
) -> Path:
    model = load_model(model_name)
    result = model.transcribe(str(audio_file), verbose=verbose)

    # write SRT file
    text_file = Path(temp_dir) / 'text.srt'
    WriteSRT(temp_dir).write_result(result, text_file.open('w', encoding='utf-8'))
    return text_file


def create_video_with_subtitles(
    video_path: str, srt_file: Path, output_dir: str | None = None, output_file: str = 'output.mp4'
) -> None:
    current_dir = Path(__file__).parent
    output_dir = current_dir if output_dir is None else Path(output_dir)
    output_file = output_dir / Path(output_file).name
    copy_srt_file = Path(shutil.copy(srt_file, current_dir))
    command = ['ffmpeg', '-i', video_path, '-vf', f'subtitles={copy_srt_file.name}', '-y', str(output_file)]
    print(run_command(command))
    copy_srt_file.unlink()


def main(video_path: str) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_file = extract_audio_from_video(video_path, temp_dir)
        text_file = get_text_from_audio(audio_file, temp_dir)
        create_video_with_subtitles(video_path, text_file)


if __name__ == '__main__':
    import sys

    main(sys.argv[1])
