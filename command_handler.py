import sys

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def add_command(self, command, function, description="No description provided"):
        """Adds a new command with an optional description."""
        self.commands[command] = {"function": function, "description": description}

    def execute(self, command, *args):
        """Executes a command if it exists."""
        if command in self.commands:
            try:
                self.commands[command]["function"](*args)
            except Exception as e:
                print(f"Error executing {command}: {e}")
        else:
            print(f"Command '{command}' not found.")

    def list_commands(self):
        """Lists all available commands with descriptions."""
        if not self.commands:
            print("No commands available.")
        else:
            print("Available commands:")
            for cmd, details in self.commands.items():
                print(f"- {cmd}: {details['description']}")

    def get_command_help(self, command):
        """Provides help for a specific command."""
        if command in self.commands:
            print(f"Help for '{command}': {self.commands[command]['description']}")
        else:
            print(f"No help found for '{command}'.")

# Example usage
def greet(name):
    print(f"Hello, {name}!")

def add_numbers(a, b):
    try:
        print(f"Sum: {int(a) + int(b)}")
    except ValueError:
        print("Error: Both inputs must be numbers.")

def subtract_numbers(a, b):
    try:
        print(f"Difference: {int(a) - int(b)}")
    except ValueError:
        print("Error: Both inputs must be numbers.")

if __name__ == "__main__":
    handler = CommandHandler()
    handler.add_command("greet", greet, "Greets the user by name.")
    handler.add_command("add", add_numbers, "Adds two numbers.")
    handler.add_command("subtract", subtract_numbers, "Subtracts the second number from the first.")

    while True:
        user_input = input("Enter command (or 'help' for available commands): ").strip()
        if user_input == "exit":
            print("Exiting the program.")
            sys.exit()

        if user_input == "help":
            handler.list_commands()
            continue

        if user_input.startswith("help "):
            command = user_input.split(" ")[1]
            handler.get_command_help(command)
            continue

        parts = user_input.split()
        command = parts[0]
        args = parts[1:]
        handler.execute(command, *args)
