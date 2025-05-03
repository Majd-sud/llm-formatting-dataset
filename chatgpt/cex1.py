"""
Author: Hossin Azmoud (Moody0101)
Date: 10/18/2022
License: MIT
Language: Python 3.10
"""

from time import sleep
from colorama import Fore as f
from UtilPackage import (
    Shell,
    Command,
    ENCODING,
    HASHING,
    EncodingManager,  # EncodingManager(Func: callable, s: str | bytes, Op: int)
    ENCODE,
    DECODE,
    Hasher  # Hasher(HashingFunc: callable, s: str | bytes) -> str
)

DOC = f"""{f.YELLOW}

Author: Hossin Azmoud (Moody0101)
Date: 10/18/2022
License: MIT
Language: {f.CYAN}Python 3.10{f.YELLOW}
Description: A tool to hash, encode, decode text.
Commands: hash, encode, decode, help, exit

Usage:
    To encode/decode:
        Encode/Decode <Text> <Algorithm>
        Encode/Decode only for help.
    To hash:
        Hash <Text> <Algorithm>
        Hash only for help.
"""


class Interface:
    """An interface that handles user interactions with the shell program."""

    def __init__(self) -> None:
        self.shell = Shell()

        self.default_commands = {
            'EXIT': self.exit_program,
            'HELP': self.help_text,
            'HASH': self.hash_doc,
            'DECODE': self.decode_doc,
            'ENCODE': self.encode_doc
        }

        self.commands = {
            'HASH': self.hash_value,
            'DECODE': self.decode,
            'ENCODE': self.encode
        }

    def hash_doc(self):
        """Displays documentation for hashing."""
        return HASHING["Doc"]

    def decode_doc(self):
        """Displays documentation for decoding."""
        return ENCODING["Doc"][DECODE]

    def encode_doc(self):
        """Displays documentation for encoding."""
        return ENCODING["Doc"][ENCODE]

    def encode(self, text, encoder_name):
        encoder_key = encoder_name.upper().strip()
        if encoder_key not in ENCODING:
            print(f"\n  Invalid algorithm name: {encoder_name}")
            print("  Available algorithms:")
            for key in ENCODING:
                print(f"    {key}")
            return

        func = ENCODING[encoder_key][ENCODE]
        encoder = EncodingManager(func, ENCODE)
        return encoder(text)

    def decode(self, text, decoder_name):
        decoder_key = decoder_name.upper().strip()
        if decoder_key not in ENCODING:
            print(f"\n  Invalid algorithm name: {decoder_name}")
            print("  Available algorithms:")
            for key in ENCODING:
                print(f"    {key}")
            return

        func = ENCODING[decoder_key][DECODE]
        decoder = EncodingManager(func, DECODE)
        return decoder(text)

    def hash_value(self, text, hasher_name):
        hasher_key = hasher_name.upper().strip()
        if hasher_key not in HASHING:
            print(f"\n  Invalid algorithm name: {hasher_name}")
            print("  Available algorithms:")
            for key in HASHING:
                print(f"    {key}")
            return

        return Hasher(HASHING[hasher_key], text)

    def set_text(self, text=None):
        self.text = text

    def exit_program(self) -> None:
        for dots in ['.', '..', '...']:
            print(f"  Exiting{dots}", end='\r')
            sleep(1)
        exit(0)

    def help_text(self):
        """Returns help instructions."""
        return """
To encode/decode:
    Encode/Decode <Text> <Algorithm>
    Encode/Decode only for help.
To hash:
    Hash <Text> <Algorithm>
    Hash only for help.
"""

    def execute(self, command: Command) -> None:
        """Execute given command with arguments if available."""
        if command.CMD in self.default_commands:
            if command.argv:
                print(self.commands[command.CMD](*command.argv))
            else:
                print(self.default_commands[command.CMD]())
        elif command.CMD in self.commands:
            if command.argv:
                print(self.commands[command.CMD](*command.argv))
            else:
                print(self.commands[command.CMD]())

    def run(self) -> None:
        print(DOC)
        while True:
            command = self.shell.shellInput()
            if command:
                self.execute(command)


def main():
    interface = Interface()
    interface.run()


if __name__ == '__main__':
    main()
