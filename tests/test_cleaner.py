from app.cleaner import clean_text


def test_clean_text_removes_emoji_sequences_including_inside_code_blocks():
    text = "Hello 👋🏽!\n```python\nprint('👨‍👩‍👧‍👦')\n```"

    assert clean_text(text) == "Hello !\n```python\nprint('')\n```"
