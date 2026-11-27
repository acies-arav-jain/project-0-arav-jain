# FastAPI Documentation Corpus Chunker

A small Python CLI that reads Markdown and text documents, normalizes their
content, divides it into overlapping word chunks, and saves the chunks as JSON.
The repository includes a FastAPI documentation corpus under `corpus/`.

## Problem

Documentation is useful to search and process only when it is available in
consistent, manageable units. This project prepares a local document corpus for
downstream uses such as retrieval, indexing, and language-model workflows. It
handles file discovery, text cleanup, chunk boundaries, source metadata, and
JSON serialization; it does not create embeddings, call a model, or write to a
vector database.

The CLI is intended for developers preparing documentation or similar
`.md`/`.txt` collections. It processes supported files recursively from the
input folder and records each chunk's source so it can be traced back to its
document.

## Design

The processing path is:

1. **Read** — `reader.py` walks the input folder recursively and reads `.md`
   and `.txt` files as UTF-8. It yields each file's path and text.
2. **Clean** — `cleaner.py` removes emoji and normalizes whitespace in
   Markdown prose while preserving the internal layout of fenced code blocks.
3. **Chunk** — `chunker.py` splits the cleaned text on whitespace into
   overlapping chunks. The default is 200 words per chunk with a 40-word
   overlap.
4. **Model** — `models.py` validates chunk settings and represents each chunk
   with an ID, source path, zero-based position, text, and word count.
5. **Write** — `cli.py` serializes the chunk records to an indented UTF-8 JSON
   array. It creates the output directory if needed and prints a completion
   summary.

Chunk IDs use the form `<source path>#<position>`, for example
`corpus/tutorial/index.md#0`. Chunk positions start at zero for each source
document.

## Cleaning policy

- Emoji sequences are removed with the Python `emoji` package, including emoji
  inside fenced code blocks.
- Outside fenced code blocks, runs of spaces and tabs are reduced to one space.
  Trailing whitespace is stripped, and three or more consecutive line breaks
  are reduced so that at most one blank line separates paragraphs.
- Fenced code blocks opened with Markdown backtick or tilde fences retain their
  internal spacing and line structure; trailing whitespace is still removed.
  The chunker later tokenizes all content by whitespace, so a saved chunk does
  not preserve the original Markdown layout.
- Corpus include directives such as
  `{* ../../docs_src/first_steps/tutorial001.py *}` are retained literally.
  Their referenced code files are not included in this corpus, and the reader
  does not resolve external references. Keeping the directive preserves the
  source path for traceability, but it may appear as text in a generated
  chunk.

## Trade-offs

- **Word-based rather than semantic chunks:** fixed-size splitting is simple,
  deterministic, and inexpensive, but it can split a sentence, table, or code
  example across chunks.
- **Overlap for continuity:** neighboring chunks repeat 40 words by default.
  This can retain context at boundaries, at the cost of duplicate text and a
  larger output.
- **Whole-file processing:** files and all output chunks are held in memory.
  This keeps the implementation straightforward for the current corpus, but
  very large corpora may need a streaming design.
- **Whitespace normalization:** prose becomes more consistent, but formatting
  that depends on repeated spaces may change. Code-block formatting is
  protected during cleaning, although word chunking still flattens whitespace.
- **No include expansion:** referenced source files are not fetched or merged.
  This keeps processing local and reproducible, while leaving unresolved
  directives in the text.

Chunk size must be greater than zero. Overlap must be non-negative and smaller
than chunk size; these settings are validated before processing.

## Results

The current `corpus/` inventory contains **158 supported documents**: 157
Markdown files and 1 text file. This is an input inventory count, not a count of
generated chunks.

No benchmark or retrieval-quality evaluation results are recorded yet; the
`evals/` directory currently contains only its placeholder. The number of
chunks and output size depend on the input contents and the selected chunk size
and overlap. The repository has focused tests for chunking, text cleaning, and
model validation, but no measured performance or quality claims are made here.

## How to run

### Requirements

- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/)

Install the project and its runtime dependencies from the repository root:

```bash
uv sync
```

### Process the corpus

The CLI accepts an input **folder** and requires an output JSON path:

```bash
uv run chunker corpus --out output/chunks.json
```

The output directory is created if it does not already exist. The command
prints the number of chunks and source files written. Use the defaults of 200
words per chunk and 40 words of overlap, or set both options explicitly:

```bash
uv run chunker corpus --out output/chunks.json --size 300 --overlap 60
```

Run `uv run chunker --help` to display the command-line options. When scanning
the input folder, the reader processes `.md` and `.txt` files and ignores files
with other extensions.

The JSON output is an array of records with this shape:

```json
[
  {
    "id": "corpus/tutorial/index.md#0",
    "source": "corpus/tutorial/index.md",
    "position": 0,
    "text": "Text from the first chunk...",
    "word_count": 200
  }
]
```

### Run focused tests

Pytest is not a runtime dependency, so include it for a one-off test run:

```bash
uv run --with pytest pytest tests/test_cleaner.py tests/test_chunker.py tests/test_models.py
```
