"""Function to normalize whitespace in a string."""


def normalize_space(v: str):
    return ' '.join(v.split()).strip()
