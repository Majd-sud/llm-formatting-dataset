from typing import Callable
from colorama import Fore as f

# Shell input prompt formatting
SHELL_HEADER = f"  {f.YELLOW}[*] {f.CYAN}-> {f.WHITE}"

# Dictionary mapping commands to their respective functions
COMMANDS: dict[str, Callable[[list[str]], None]] = {}


def add_command(command: str, function: Callable[[list[str]], None]) -> None:
    """
    Register a new command with its corresponding function.

    Args:
        command: The command keyword.
        function: A function that takes a list of arguments and performs the command.
    """
    COMMANDS[command] = function


def execute(command: str, arguments: list[str]) -> None:
    """
    Execute a registered command with given arguments.

    Args:
        command: The command to execute.
        arguments: The list of arguments for the command.
    """
    if command in COMMANDS:
        COMMANDS[command](arguments)


def parse_command_string(command_string: str) -> tuple[str, list[str]]:
    """
    Parse a full command string into a command and argument list.

    Args:
        command_string: Raw string input from the user.

    Returns:
        A tuple (command, arguments) where:
            - command: lowercase string of the command
            - arguments: list of argument strings
    """
    command_parts = command_string.split()

    if not command_parts:
        return "", []

    command = command_parts[0].lower().strip()
    arguments = [part.strip() for part in command_parts[1:]]

    return command, arguments


def shell_input() -> tuple[str, list[str]]:
    """
    Prompt the user for input and parse the result.

    Returns:
        A tuple (command, arguments) parsed from the input.
    """
    user_input = input(SHELL_HEADER)
    return parse_command_string(user_input)


def run_shell() -> None:
    """
    Run the interactive shell loop, waiting for and executing commands.
    """
    while True:
        command, arguments = shell_input()
        execute(command, arguments)
