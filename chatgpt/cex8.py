ENCODE, DECODE = 0, 1


def EncodingManager(func: callable, op: int) -> callable:
    """
    Returns an encoding or decoding function based on the specified operation.

    Args:
        func: The encoding or decoding function to wrap.
        op: Operation type (0 for ENCODE, 1 for DECODE).

    Returns:
        A callable that takes a string or bytes and returns a decoded string.

    Raises:
        AssertionError: If op is not 0 or 1, or if input types are invalid.
    """
    assert op in [ENCODE, DECODE], (
        f"This operation is not implemented or incorrect! index [{op}]"
    )

    if op == ENCODE:
        def wrapped(s: str | bytes) -> str:
            assert isinstance(s, (str, bytes)), (
                f"Cannot encode object of type {type(s)}"
            )
            if isinstance(s, str):
                s = s.encode()
            return func(s).decode()

    elif op == DECODE:
        def wrapped(s: str | bytes) -> str:
            assert isinstance(s, str), (
                f"Cannot decode object of type {type(s)}"
            )
            return func(s.encode()).decode()

    return wrapped
