import emoji
import re


def clean_text(text: str) -> str:

    text = emoji.replace_emoji(text, replace="")

    cleaned_lines = []

    in_code_block = False
    fence_character = None
    fence_length = 0

    for line in text.splitlines():

        fence_match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)

        if not in_code_block and fence_match:
            fence_character = fence_match.group(1)[0]
            fence_length = len(fence_match.group(1))
            in_code_block = True

            cleaned_lines.append(line.rstrip())
            continue

        if in_code_block:

            cleaned_lines.append(line.rstrip())

            close_match = re.match(r"^ {0,3}(`{3,}|~{3,})\s*$", line)

            if (
                close_match
                and close_match.group(1)[0] == fence_character
                and len(close_match.group(1)) >= fence_length
            ):
                in_code_block = False
                fence_character = None
                fence_length = 0

            continue

        line = re.sub(r"[ \t]+", " ", line)

        line = line.rstrip()

        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    cleaned_text = cleaned_text.strip()

    return cleaned_text