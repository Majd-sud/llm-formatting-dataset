"""
HEDShell
Date: 10/18/2022
License: MIT
Language: Python 3.10
"""

from time import sleep
from colorama import Fore as f

from shell.api import (
    decode,
    decode as decode_text,
    decoding_algos,
    encode,
    encoding_algos,
    has_decoding_algo,
    has_encoding_algo,
    has_hashing_algo,
    hash_val,
    hashing_algos,
)
from shell.core import add_command, run_shell

# Startup banner
STARTUP_DOC = f"""{f.YELLOW}
    HEDShell
    License: MIT
    Language: {f.CYAN}Python 3.10{f.YELLOW}
    Description: A tool to hash, encode, and decode text.
    Commands: hash, encode, decode, help, exit
"""

# Command usage examples
ENCODING_DOC = f"""
    Syntax: Encode <InputText> < {" | ".join(encoding_algos())} >
"""

DECODING_DOC = f"""
    Syntax: Decode <InputText> < {" | ".join(decoding_algos())} >
"""

HASHING_DOC = f"""
    Syntax: Hash <InputText> < {" | ".join(hashing_algos())} >
"""

HELP_DOC = """
    Usage:
        To encode/decode:
            Encode/Decode <Text> <Algorithm>
            Encode/Decode only for help.
        To hash:
            Hash <Text> <Algorithm>
            Hash only for help.
"""


def exit_shell(_: list[str]) -> None:
    """Gracefully exit the shell."""
    for dots in [".", "..", "..."]:
        print(f"  Exiting{dots}", end="\r")
        sleep(1)
    exit(0)


def help_shell(_: list[str]) -> None:
    """Display help information."""
    print(HELP_DOC)


def process_hash(args: list[str]) -> None:
    """Process hashing command."""
    if len(args) != 2:
        print(HASHING_DOC)
        return

    text, algo = args
    if not has_hashing_algo(algo):
        print(f"Unknown algorithm name: {algo}")
        print(HASHING_DOC)
        return

    print(hash_val(text, algo))


def process_decode(args: list[str]) -> None:
    """Process decode command."""
    if len(args) != 2:
        print(DECODING_DOC)
        return

    text, algo = args
    if not has_decoding_algo(algo):
        print(f"Unknown algorithm name: {algo}")
        print(DECODING_DOC)
        return

    print(decode_text(text, algo))


def process_encode(args: list[str]) -> None:
    """Process encode command."""
    if len(args) != 2:
        print(ENCODING_DOC)
        return

    text, algo = args
    if not has_encoding_algo(algo):
        print(f"Unknown algorithm name: {algo}")
        print(ENCODING_DOC)
        return

    print(encode(text, algo))


def main() -> None:
    """Main entry point of HEDShell."""
    add_command("exit", exit_shell)
    add_command("help", help_shell)
    add_command("hash", process_hash)
    add_command("encode", process_encode)
    add_command("decode", process_decode)

    print(STARTUP_DOC)
    run_shell()


if __name__ == "__main__":
    main()
