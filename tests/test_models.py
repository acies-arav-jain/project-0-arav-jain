import pytest

from app.models import Chunk, Settings


def test_default_settings():
    settings = Settings()

    assert settings.size == 200
    assert settings.overlap == 40


def test_custom_settings():
    settings = Settings(size=100, overlap=20)

    assert settings.size == 100
    assert settings.overlap == 20


def test_invalid_overlap():
    with pytest.raises(ValueError):
        Settings(size=4, overlap=4)


def test_negative_overlap():
    with pytest.raises(ValueError):
        Settings(size=4, overlap=-1)


def test_zero_size():
    with pytest.raises(ValueError):
        Settings(size=0, overlap=0)


def test_chunk_model():
    chunk = Chunk(
        id="tutorial/first-steps.md#0",
        source="tutorial/first-steps.md",
        position=0,
        text="Hello world",
        word_count=2,
    )

    assert chunk.position == 0
    assert chunk.word_count == 2
    assert chunk.text == "Hello world"


def test_negative_position():
    with pytest.raises(ValueError):
        Chunk(
            id="tutorial/first-steps.md#-1",
            source="tutorial/first-steps.md",
            position=-1,
            text="Hello world",
            word_count=2,
        )