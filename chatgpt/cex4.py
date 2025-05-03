from .algorithms import DECODING_ALGORITHMS, ENCODING_ALGORITHMS, HASHING_ALGORITHMS


def encoding_algos() -> list[str]:
    """Return a list of available encoding algorithm names."""
    return list(ENCODING_ALGORITHMS.keys())


def decoding_algos() -> list[str]:
    """Return a list of available decoding algorithm names."""
    return list(DECODING_ALGORITHMS.keys())


def hashing_algos() -> list[str]:
    """Return a list of available hashing algorithm names."""
    return list(HASHING_ALGORITHMS.keys())


def has_encoding_algo(algo: str) -> bool:
    """Check if the given algorithm exists in the encoding algorithms."""
    return algo.lower().strip() in ENCODING_ALGORITHMS


def has_decoding_algo(algo: str) -> bool:
    """Check if the given algorithm exists in the decoding algorithms."""
    return algo.lower().strip() in DECODING_ALGORITHMS


def has_hashing_algo(algo: str) -> bool:
    """Check if the given algorithm exists in the hashing algorithms."""
    return algo.lower().strip() in HASHING_ALGORITHMS


def encode(text: str | bytes, algo: str) -> str:
    """Encode the given text using the specified algorithm."""
    if isinstance(text, str):
        text = text.encode()
    encoding_fn = ENCODING_ALGORITHMS[algo.lower().strip()]
    return encoding_fn(text).decode()


def decode(text: str | bytes, algo: str) -> str:
    """Decode the given text using the specified algorithm."""
    if isinstance(text, str):
        text = text.encode()
    decoding_fn = DECODING_ALGORITHMS[algo.lower().strip()]
    return decoding_fn(text).decode()


def hash_val(text: str | bytes, algo: str) -> str:
    """Hash the given text using the specified algorithm."""
    if isinstance(text, str):
        text = text.encode()
    hashing_fn = HASHING_ALGORITHMS[algo.lower().strip()]
    return hashing_fn(text).hexdigest()
