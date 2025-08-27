import re

# Только те символы, которые точно требуют экранирования в MarkdownV2
MDV2_SPECIAL_CHARS = r'_*[]()~`>#+-=|{}!'

_escape_regex = re.compile(f"([{re.escape(MDV2_SPECIAL_CHARS)}])")

def escape(content: str) -> str:
    """Escape special characters for Telegram MarkdownV2"""
    return _escape_regex.sub(r"\\\1", content)
