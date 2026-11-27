from app.chunker import chunk_words


def test_normal_chunking_with_overlap():
    text = "a b c d e f"

    result = chunk_words(text, size=4, overlap=2)

    assert result == ["a b c d", "c d e f"]


def test_no_overlap():
    text = "a b c d e f"

    result = chunk_words(text, size=3, overlap=0)

    assert result == ["a b c", "d e f"]


def test_text_shorter_than_one_chunk():
    text = "a b"

    result = chunk_words(text, size=4, overlap=1)

    assert result == ["a b"]


def test_empty_text():
    text = ""

    result = chunk_words(text, size=4, overlap=1)

    assert result == []


def test_no_redundant_tail_chunk():
    text = "a b c d e f"

    result = chunk_words(text, size=4, overlap=2)

    assert result == ["a b c d", "c d e f"]


def test_invalid_overlap():
    text = "a b c d"

    try:
        chunk_words(text, size=4, overlap=4)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError when overlap equals size"