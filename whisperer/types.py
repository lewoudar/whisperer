from typing import Literal, TypeAlias

ModelType: TypeAlias = Literal[
    'tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 'medium', 'medium.en', 'large', 'large.en'
]
TaskType: TypeAlias = Literal['translate', 'transcribe']
Format: TypeAlias = Literal['all', 'txt', 'json', 'tsv', 'vtt', 'srt']
