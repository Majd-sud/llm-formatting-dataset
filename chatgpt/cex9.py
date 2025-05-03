def Hasher(hashing_func: callable, s: str | bytes) -> str:
    """
    Applies a hashing function to the given string or bytes input.

    Args:
        hashing_func: A callable that accepts bytes and returns a hash object.
        s: The input data to hash (as str or bytes).

    Returns:
        The hexadecimal digest of the hash.

    Raises:
        AssertionError: If the input is not str or bytes.
    """
    assert isinstance(s, (str, bytes)), (
        f"Cannot hash object of type {type(s)}"
    )

    if isinstance(s, str):
        s = s.encode()

    return hashing_func(s).hexdigest()
