import string

_ALPHABET = string.ascii_uppercase


def index_to_item(idx: int) -> str:
    """Преобразует индекс (0-based) в буквенный код Excel: 0=A, 25=Z, 26=AA."""
    if idx < 0:
        raise ValueError("Index must be non-negative")
    result = ""
    n = idx
    while True:
        n, remainder = divmod(n, 26)
        result = _ALPHABET[remainder] + result
        if n == 0:
            break
        n -= 1
    return result
