from collections.abc import Iterator
from pathlib import Path
import argparse

def load_text_files(input_path: str | Path) -> Iterator[tuple[str, str]]:
    input_path = Path(input_path)

    if input_path.is_file() and input_path.suffix.lower() in ['.md', '.txt']:
        text = input_path.read_text(encoding='utf-8')
        yield (input_path.name, text)

    elif input_path.is_dir():
        for file_path in input_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.md', '.txt']:
                text = file_path.read_text(encoding='utf-8')
                yield (str(file_path), text)

    else:
        raise ValueError(f"Invalid input path: {input_path}. Must be a .md or .txt file, or a directory containing such files.")