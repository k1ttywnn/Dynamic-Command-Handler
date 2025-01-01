# Dynamic Command Handler

## Overview

The **Dynamic Command Handler** is a versatile Python tool designed for managing and executing customizable commands in real-time. It supports dynamic command execution, provides comprehensive error handling, and includes an intuitive built-in help system. Ideal for developers creating command-line interfaces (CLI) or automating workflows, this utility enables flexible and adaptive command handling.

## Key Features

- **Real-time Command Execution**: Easily add, execute, and manage commands with user-defined arguments.
- **Error Handling**: Built-in error detection and handling to manage faulty commands gracefully.
- **Command Help System**: Interactive help to list available commands and show detailed descriptions.
- **Customizable**: Easily extend the tool with new commands and behaviors tailored to your use case.

## Installation

Clone or download the repository to your local machine:

```bash
git clone https://github.com/k1ttywnn/Dynamic-Command-Handler.git
```

Then, run the Python script:

```bash
python command_handler.py
```

## Usage

### Adding Commands

You can add new commands by calling the `add_command()` function, passing the command name, function, and an optional description.

### Running Commands

Once running, type a command followed by any required arguments. For example:

- `greet John` will greet the user "John".
- `add 2 3` will sum the numbers 2 and 3.
- `subtract 10 5` will subtract 5 from 10.

### Help System

To view available commands, type `help`.

For help with a specific command, type:

- `help greet` – Shows details about the greet command.

### Exiting

To exit the program, type `exit`.

## Example:

```bash
Enter command: greet John
Hello, John!

Enter command: add 3 5
Sum: 8
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.

## Contribution

Feel free to open issues or submit pull requests if you would like to improve this tool. Contributions are welcome!

```

This version of the README is more polished and includes detailed information about the functionality and usage of your project, making it clear for users to understand how to install, use, and contribute. You can also customize it further based on specific details about your project.
