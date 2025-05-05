from shell.core import run_shell
from shell.commands import load_default_commands


def main() -> None:
    """
    Entry point of the shell application.
    Loads default commands and starts the interactive shell.
    """
    load_default_commands()
    run_shell()


if __name__ == "__main__":
    main()
