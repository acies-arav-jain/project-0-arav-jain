import argparse
import json
from pathlib import Path

from app.reader import load_text_files
from app.cleaner import clean_text
from app.chunker import chunk_words
from app.models import Chunk, Settings


def process_input(
    input_path: str | Path,
    settings: Settings | None = None
) -> list[Chunk]:
    """
    Read, clean, chunk and model text documents.

    Accepts either a single .md/.txt file or a directory
    containing .md/.txt files.

    Returns a list of Chunk objects with metadata.
    """

    # 1. Use default settings if the user hasn't provided any
    if settings is None:
        settings = Settings()

    # 2. Convert the input path to a Path object
    input_path = Path(input_path)

    # 3. Create a list to store all the chunks
    all_chunks = []

    # 4. Read all supported text files
    documents = load_text_files(input_path)

    # 5. Process each document
    for file_path, text in documents:

        # 5a. Clean the text
        cleaned_text = clean_text(text)

        # 5b. Split the cleaned text into chunks
        text_chunks = chunk_words(
            cleaned_text,
            size=settings.size,
            overlap=settings.overlap
        )

        # 5c. Use the original file path as the source
        source = str(file_path)

        # 5d. Create a Chunk model for every text chunk
        for position, chunk_text in enumerate(text_chunks):

            chunk = Chunk(
                id=f"{source}#{position}",
                source=source,
                position=position,
                text=chunk_text,
                word_count=len(chunk_text.split())
            )

            # 5e. Add the Chunk model to our list
            all_chunks.append(chunk)

    # 6. Return all Chunk objects
    return all_chunks


def write_chunks_to_json(
    chunks: list[Chunk],
    output_path: str | Path
) -> None:
    """
    Save Chunk objects to a JSON file.
    """

    # 1. Convert each Chunk object into a dictionary
    chunk_data = [
        chunk.model_dump()
        for chunk in chunks
    ]

    # 2. Convert the list of dictionaries into JSON
    json_data = json.dumps(
        chunk_data,
        indent=2,
        ensure_ascii=False
    )

    # 3. Convert the output path into a Path object
    output_path = Path(output_path)

    # 4. Create the parent folder if it doesn't exist
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # 5. Write the JSON data to the file
    output_path.write_text(
        json_data,
        encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Load, clean, and chunk text files."
    )

    # Input folder
    parser.add_argument(
        "folder",
        help="Folder containing .md and .txt documents."
    )

    # Output JSON file path
    parser.add_argument(
        "--out",
        required=True,
        help="Path where the output JSON file will be saved."
    )

    # Chunk size
    parser.add_argument(
        "--size",
        type=int,
        default=200,
        help="Number of words per chunk (default: 200)."
    )

    # Overlap
    parser.add_argument(
        "--overlap",
        type=int,
        default=40,
        help="Number of overlapping words between chunks (default: 40)."
    )

    # Parse the arguments entered in the terminal
    args = parser.parse_args()

    # Create Settings object to validate chunk size and overlap
    settings = Settings(
        size=args.size,
        overlap=args.overlap
    )

    # Process all files in the input folder
    chunks = process_input(
        input_path=args.folder,
        settings=settings
    )

    # Save the generated chunks to the specified output file
    write_chunks_to_json(
        chunks=chunks,
        output_path=args.out
    )

    # Calculate the number of unique files processed
    files_processed = len(
        {chunk.source for chunk in chunks}
    )

    # Display the summary
    print(
        f"Wrote {len(chunks):,} chunks from "
        f"{files_processed:,} files to {args.out}"
    )


if __name__ == "__main__":
    main()