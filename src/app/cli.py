from app.reader import load_text_files
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(description = "Load text files from a specified path.")
    parser.add_argument("-i", "--input-path", help="Path to a .md or .txt file, or a directory containing such files.")
    args = parser.parse_args()
    documents = load_text_files(args.input_path)

    for file_path, text in documents:
        print(f"Loaded file: {file_path}, Content length: {len(text)} characters")