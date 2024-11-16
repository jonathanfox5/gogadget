import subprocess
from shutil import which

from .cli_utils import CliUtils


def program_exists(tool_name: str) -> bool:
    """Check if a program can be accessed from the command line"""
    result = which(tool_name) is not None
    return result


def update_package(package_name: str) -> None:
    """Update a python package"""
    command = ["pip", "install", "--upgrade", package_name]
    run_command(command, True)


def run_command(command: list[str], print_command: bool = False) -> None:
    """Run a command line program"""
    if print_command:
        command_string = " ".join(command)
        CliUtils.print_status(f"Running command: {command_string}")

    process = subprocess.Popen(command)
    process.wait()
