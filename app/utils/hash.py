import hashlib

def hash_string(text: str) -> str:
    """
    Returns a SHA-256 hash of the input string.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
