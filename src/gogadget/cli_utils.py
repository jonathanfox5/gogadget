import re
from pathlib import Path
from typing import Any

import typer
from rich import print as printr
from rich.text import Text


class CliUtils:
    """Utilities to make life easier with a typer cli application"""

    @staticmethod
    def clean_string(input_str: str) -> str:
        """Callback that strips whitespace from string"""
        cleaned = input_str.strip()

        return cleaned

    @staticmethod
    def print_plain(item: Any) -> None:
        """Print an object using the standard library function"""
        print(item)

    @staticmethod
    def print_rich(item: Any) -> None:
        """Print an object using rich's formatting"""
        printr(item)

    @staticmethod
    def print_status(message: str) -> None:
        """Print status message using rich"""
        printr(
            Text(
                f"~~~ {message} ~~~",
                style="bold blue",
            )
        )

    @staticmethod
    def print_warning(message: str) -> None:
        """Print warning message using rich"""
        printr(
            Text(
                f"### {message} ###",
                style="bold red",
            )
        )

    @staticmethod
    def print_error(message: str, e: Exception | None = None) -> None:
        """Print error message using rich. Optionally print exception text"""

        error_text = ""
        if e is not None:
            error_text = f"{str(e)}"

        printr(
            Text(
                f"### {message} ###\n{error_text}",
                style="bold red",
            )
        )

    @staticmethod
    def validate_language_code(lang: str) -> str:
        """Forces language code to lower case without trailing whitespace,"""
        lang = lang.strip().lower()

        if len(lang) != 2:
            raise typer.BadParameter(
                f"Language must be a two letter code. Run `gogoprimer --list-langages` for a list of supported languages. User provided language: `{lang}`."
            )

        return lang

    @staticmethod
    def validate_greater_than_zero(number: int) -> int:
        """Forces language code to lower case without trailing whitespace,"""

        if number <= 0:
            raise typer.BadParameter(f"Must be a positive integer, user input was `{number}`.")

        return number

    @staticmethod
    def validate_optional_directory(path: Path | None) -> Path | None:
        """Checks that a directory path is theoretically valid, if specified"""
        if path is None:
            return None
        else:
            return CliUtils.validate_directory(path)

    @staticmethod
    def validate_optional_file(path: Path | None) -> Path | None:
        """Checks that a file path is theoretically valid, if specified"""
        if path is None:
            return None
        else:
            return CliUtils.validate_file(path)

    @staticmethod
    def validate_directory(path: Path) -> Path:
        """Checks that a directory path is theoretically valid"""
        return CliUtils._validate_path(path, must_be_directory=True)

    @staticmethod
    def validate_file(path: Path) -> Path:
        """Checks that a file path is theoretically valid"""
        return CliUtils._validate_path(path, must_be_file=True)

    @staticmethod
    def validate_path_exists(path: Path) -> Path:
        """Checks that a path exists on the user's system"""
        return CliUtils._validate_path(path, must_exist=True)

    @staticmethod
    def _validate_path(
        path: Path,
        allow_blank: bool = False,
        must_be_file: bool = False,
        must_be_directory: bool = False,
        must_exist: bool = False,
    ) -> Path:
        """Helper method to enable various checks"""
        if (not allow_blank) and (path is None):
            raise typer.BadParameter("Cannot be blank!")
        if (must_be_file) and (not path.is_file()):
            raise typer.BadParameter(f"Must be a file path. User provided path: `{path}`.")
        if (must_be_directory) and (not path.is_dir()):
            raise typer.BadParameter(
                f"Must be a valid directory (aka folder). User provided path: `{path}`."
            )
        if (must_exist) and (not path.exists()):
            raise typer.BadParameter(f"Path does not exist. User provided path: `{path}`.")

        return path

    @staticmethod
    def validate_url(url: str) -> str:
        """Validate that a url is theoretically possible"""
        regex = re.compile(
            r"(\w+://)?"  # protocol                      (optional)
            r"(\w+\.)?"  # host                          (optional)
            r"(([\w-]+)\.(\w+))"  # domain
            r"(\.\w+)*"  # top-level domain              (optional, can have > 1)
            r"([\w\-\._\~/]*)*(?<!\.)"  # path, params, anchors, etc.   (optional)
        )

        url = url.strip()

        if url == "":
            raise typer.BadParameter("URL cannot be blank!")
        if not regex.match(url):
            raise typer.BadParameter(f"Invalid url. User provided url: `{url}`.")

        return url
