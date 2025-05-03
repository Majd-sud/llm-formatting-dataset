from colorama import Fore as f
from dataclasses import dataclass


@dataclass
class Command:
    """Represents a parsed shell command with its arguments."""
    CMD: str
    argv: list[str]

    def __repr__(self) -> str:
        return f"<cmd: {self.CMD}, args: {self.get_arg_str()} arglen: {len(self.argv)}>"

    def __str__(self) -> str:
        return self.__repr__()

    def get_arg_str(self) -> str:
        return ', '.join(f"{arg}" for arg in self.argv)


class Shell:
    """A basic shell interface for handling command input and parsing."""

    def shell_input(self, tool: str = None) -> Command | bool:
        """
        Prompts the user for input and returns a parsed Command object.
        
        Args:
            tool: Optional tool name to display in the prompt.
        
        Returns:
            A Command object if input is valid, False otherwise.
        """
        prompt = f"  {f.YELLOW}[*][{tool}] {f.CYAN}-> {f.WHITE}" if tool else f"  {f.YELLOW}[*] {f.CYAN}-> {f.WHITE}"
        user_input = input(prompt)
        return self.parse_cmd(user_input)

    def parse_cmd(self, cmd: str) -> Command | bool:
        """
        Parses a raw input string into a Command object.

        Args:
            cmd: Raw input command string.

        Returns:
            A Command object or False if input is empty.
        """
        parts = cmd.strip().split()

        if not parts:
            return False

        command = parts[0].upper()
        arguments = parts[1:] if len(parts) > 1 else []
        return Command(command, arguments)
