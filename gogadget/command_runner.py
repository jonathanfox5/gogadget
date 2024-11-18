import shlex
import subprocess
from shutil import which

from .cli_utils import CliUtils


def program_exists(tool_name: str) -> bool:
    """Check if a program can be accessed from the command line"""
    result = which(tool_name) is not None
    return result


def install_package(package_name: str | list[str], app_name: str) -> None:
    # Convert to string if we have a list
    if isinstance(package_name, list):
        package_name = " ".join(package_name)

    update_command: str | None = None
    if program_exists("uv"):
        result = get_command_output("uv tool list")
        # Double check that we have installed it with uv
        if app_name in result:
            update_command = f"uv tool install {app_name} --with {package_name}"

    if update_command:
        run_command(update_command, True)
    else:
        CliUtils.print_warning(f"Not installing {package_name}, manual installation detected.")


def update_package(package_name: str, app_name: str) -> None:
    """Update a python package within the uv tool package"""

    update_command: str | None = None
    if program_exists("uv"):
        result = get_command_output("uv tool list")
        # Double check that we have installed it with uv
        if app_name in result:
            update_command = f"uv tool upgrade {app_name} --upgrade-package {package_name}"

    if update_command:
        run_command(update_command, True)
    else:
        CliUtils.print_warning(f"Not updating {package_name}, manual installation detected.")


def run_command(command: str | list[str], print_command: bool = False) -> None:
    """Run a command line program"""

    if isinstance(command, str):
        command = arg_string_to_list(command)

    if print_command:
        command_string = " ".join(command)
        CliUtils.print_status(f"Running command: {command_string}")

    process = subprocess.Popen(command, shell=True)
    process.wait()


def arg_string_to_list(argument_string: str) -> list[str]:
    """Converts a string of arguments into a list"""

    arg_list = shlex.split(argument_string)
    return arg_list


def get_command_output(command: str | list[str]) -> str:
    if isinstance(command, str):
        command = arg_string_to_list(command)

    try:
        runner = subprocess.run(command, capture_output=True, text=True, shell=True)
        result = runner.stdout

        return str(result)
    except Exception:
        return ""
