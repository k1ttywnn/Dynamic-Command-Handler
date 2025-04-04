import sys
from typing import Callable, Any, Dict, Optional
import inspect
import random
import json
import os
from datetime import datetime


class CommandHandler:
    def __init__(self, prefix: str = "!", library_file: str = "command_library.json"):
        """Initialize the CommandHandler with a prefix and persistent library.

        Args:
            prefix (str): Command prefix (default: '!').
            library_file (str): File to store custom commands.
        """
        self.prefix = prefix
        self.library_file = library_file
        self.commands: Dict[str, Dict[str, Any]] = {}
        self.load_library()  # Load saved commands on startup

    def load_library(self) -> None:
        """Load commands from the library file."""
        if os.path.exists(self.library_file):
            try:
                with open(self.library_file, "r") as f:
                    library = json.load(f)
                for cmd, details in library.items():
                    if "custom" in details and details["custom"]:
                        # Rebuild custom commands
                        func = self._create_function(details["source"])
                        self.commands[cmd] = {
                            "function": func,
                            "description": details["description"],
                            "signature": inspect.signature(func),
                            "custom": True,
                            "source": details["source"],
                        }
                    else:
                        # Skip built-in commands (they'll be re-added)
                        continue
                print(f"Loaded {len(self.commands)} custom commands from library.")
            except Exception as e:
                print(f"Error loading library: {e}")

    def save_library(self) -> None:
        """Save custom commands to the library file."""
        library = {}
        for cmd, details in self.commands.items():
            if details.get("custom", False):
                library[cmd] = {
                    "description": details["description"],
                    "source": details["source"],
                    "custom": True,
                }
        try:
            with open(self.library_file, "w") as f:
                json.dump(library, f, indent=4)
            print("Command library saved.")
        except Exception as e:
            print(f"Error saving library: {e}")

    def add_command(
        self,
        command: str,
        function: Callable,
        description: str = "No description provided",
        aliases: list[str] = None,
        custom: bool = False,
        source: str = None,
    ) -> None:
        """Add a command to the handler.

        Args:
            command (str): Command name.
            function (Callable): Function to execute.
            description (str): Command description.
            aliases (list[str]): Optional aliases.
            custom (bool): Whether this is a user-defined command.
            source (str): Source code if custom.
        """
        if not callable(function):
            raise ValueError(f"Function for command '{command}' must be callable.")
        command = command.lower()
        self.commands[command] = {
            "function": function,
            "description": description,
            "signature": inspect.signature(function),
            "custom": custom,
            "source": source if custom else None,
        }
        if aliases:
            for alias in aliases:
                self.commands[alias.lower()] = self.commands[command]

    def _create_function(self, source: str) -> Callable:
        """Create a function from user-provided source code."""
        try:
            # Basic safety: restrict imports and dangerous builtins
            safe_globals = {"print": print, "random": random, "int": int, "str": str}
            local_vars = {}
            exec(source, safe_globals, local_vars)
            func_name = source.split("def ")[1].split("(")[0].strip()
            func = local_vars[func_name]
            return func
        except Exception as e:
            raise ValueError(f"Invalid function definition: {e}")

    def execute(self, command: str, *args: Any) -> Optional[Any]:
        """Execute a command with arguments."""
        command = command.lower()
        if command in self.commands:
            cmd_info = self.commands[command]
            try:
                expected_params = len(cmd_info["signature"].parameters)
                if len(args) != expected_params:
                    raise TypeError(
                        f"'{command}' expects {expected_params} argument(s), got {len(args)}"
                    )
                result = cmd_info["function"](*args)
                return result
            except TypeError as e:
                print(f"Error: {e}. Usage: {command} {cmd_info['signature']}")
            except Exception as e:
                print(f"Error executing '{command}': {e}")
        else:
            print(f"Command '{command}' not found. Type '{self.prefix}help'.")
        return None

    def list_commands(self) -> None:
        """List all available commands."""
        if not self.commands:
            print("No commands available.")
        else:
            print("Available commands:")
            seen = set()
            for cmd, details in sorted(self.commands.items()):
                if cmd not in seen:
                    seen.add(cmd)
                    signature = (
                        str(details["signature"]).replace("(", "").replace(")", "")
                    )
                    custom_tag = "[custom]" if details.get("custom") else ""
                    print(
                        f"  {self.prefix}{cmd:<15} : {details['description']} {custom_tag} (usage: {cmd} {signature})"
                    )

    def get_command_help(self, command: str) -> None:
        """Provide detailed help for a command."""
        command = command.lower()
        if command in self.commands:
            cmd_info = self.commands[command]
            signature = str(cmd_info["signature"]).replace("(", "").replace(")", "")
            print(f"'{self.prefix}{command}': {cmd_info['description']}")
            print(f"Usage: {self.prefix}{command} {signature}")
            if cmd_info.get("custom"):
                print(f"Source:\n{cmd_info['source']}")
        else:
            print(f"No help found for '{command}'. Type '{self.prefix}help'.")


# Built-in commands
def greet(name: str) -> str:
    """Greets the user by name."""
    return f"Hello, {name}!"


def add_numbers(a: str, b: str) -> int:
    """Adds two numbers."""
    return int(a) + int(b)


def subtract_numbers(a: str, b: str) -> int:
    """Subtracts the second number from the first."""
    return int(a) - int(b)


def echo(text: str) -> str:
    """Echoes back the provided text."""
    return text


def roll_dice(dice: str = "1d6") -> str:
    """Rolls dice in the format 'NdM' (e.g., '2d6' for two six-sided dice). Defaults to 1d6.

    Args:
        dice (str): Dice notation (e.g., '2d6' for 2 six-sided dice).

    Returns:
        str: Result of the dice roll.
    """
    try:
        if "d" not in dice:
            raise ValueError("Format must be 'NdM' (e.g., '2d6').")
        num, sides = map(int, dice.split("d"))
        if num <= 0 or sides <= 0:
            raise ValueError("Number of dice and sides must be positive.")
        if num > 100:
            raise ValueError("Cannot roll more than 100 dice at once.")
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls)
        return f"Rolled {dice}: {rolls} = {total}"
    except ValueError as e:
        return f"Error: {e}"


def add_command_handler(handler: CommandHandler, name: str, source: str) -> str:
    """Dynamically add a command from user input."""
    try:
        func = handler._create_function(source)
        signature = inspect.signature(func)
        param_count = len(signature.parameters)
        if param_count > 5:
            return "Error: Custom commands can have up to 5 parameters."
        description = (
            f"Custom command defined on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        handler.add_command(name, func, description, custom=True, source=source)
        handler.save_library()
        return f"Command '{handler.prefix}{name}' added successfully!"
    except Exception as e:
        return f"Error adding command: {e}"


def main():
    handler = CommandHandler(prefix="!")

    # Add built-in commands
    handler.add_command("greet", greet, "Greets the user by name.", aliases=["hello"])
    handler.add_command("add", add_numbers, "Adds two numbers.", aliases=["sum"])
    handler.add_command(
        "roll", roll_dice, "Rolls dice (e.g., '2d6').", aliases=["dice"]
    )
    handler.add_command(
        "addcmd",
        lambda name, source: add_command_handler(handler, name, source),
        "Add a custom command (e.g., '!addcmd square def square(x):\\n    return int(x) ** 2')",
        aliases=["newcmd"],
    )

    print(
        f"Welcome to CommandHandler! Use '{handler.prefix}'. Type '{handler.prefix}help' or '{handler.prefix}exit'."
    )
    print("Add custom commands with '!addcmd <name> <source>' (use \\n for newlines).")

    while True:
        try:
            user_input = input("> ").strip()
            if not user_input:
                continue

            if not user_input.startswith(handler.prefix):
                print(
                    f"Commands must start with '{handler.prefix}'. Type '{handler.prefix}help'."
                )
                continue

            user_input = user_input[len(handler.prefix) :]
            if user_input == "exit":
                handler.save_library()
                print("Goodbye!")
                sys.exit(0)

            if user_input == "help":
                handler.list_commands()
                continue

            if user_input.startswith("help "):
                command = user_input.split(" ", 1)[1].strip()
                handler.get_command_help(command)
                continue

            parts = user_input.split(maxsplit=2)
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            result = handler.execute(command, *args)
            if result is not None:
                print(f"Result: {result}")

        except KeyboardInterrupt:
            handler.save_library()
            print("\nInterrupted. Exiting gracefully...")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
