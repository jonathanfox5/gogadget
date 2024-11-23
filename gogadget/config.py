import importlib.metadata
import re
from pathlib import Path
from typing import Any

import rtoml
import typer

from .cli_utils import CliUtils
from .command_runner import get_platform, program_exists, run_command
from .help_text import HelpText

"""Metadata"""
APP_NAME = "gogadget"

"""Supported file formats"""
SUPPORTED_VIDEO_EXTS = [
    ".mp4",
    ".webm",
    ".mov",
    ".mkv",
    ".mpeg",
    ".mpg",
    ".avi",
    ".ogv",
    ".wmv",
    ".m4v",
    ".3gp",
    ".ts",
]
SUPPORTED_AUDIO_EXTS = [".mp3", ".ogg", ".wav", ".opus", ".m4a", ".aac", ".aiff", ".flac"]
SUPPORTED_SUB_EXTS = [".srt", ".vtt"]
SYNTHETIC_SUB_EXTS = [".gg"]
SUPPORTED_WORD_AUDIO_EXTS = [".mp3"]


def get_version_number() -> str:
    """Gets the version number of the python package"""
    try:
        version = importlib.metadata.version(f"{APP_NAME}")
        return f"{APP_NAME} version: {version}"
    except Exception:
        return "[bold red]Couldn't get version. If you are running this from source, no version number is available."


def main_package_directory() -> Path:
    """Get the path of where the python source files are for the project"""
    # Just return the directory of config.py since it's in the root of the package
    path = Path(__file__).parent.resolve()
    return path


def get_resources_directory() -> Path:
    """Get the path of the project (source) resources file"""
    path = main_package_directory() / "resources"

    return path


class ConfigFile:
    """Class to configure the user config file"""

    # User configuration directory e.g. ~/Library/Application Support/... on macos
    CONFIG_DIRECTORY = Path(typer.get_app_dir(APP_NAME))

    def config_file_exists(self) -> bool:
        """Has the config file been created?"""
        config_file = self.get_config_file_path()
        return config_file.exists()

    def launch_config_file_in_editor(self) -> None:
        """Open in the platform default editor (macos/linux) On Windows, try to open in vscode, fall back to notepad"""
        config_file = self.get_config_file_path()

        if not config_file.exists():
            self.create_config_file()

        config_file_str = str(config_file.resolve())

        if get_platform() == "Windows":
            # Try to open with vscode. If not available, open in notepad
            if program_exists("code"):
                run_command(["code", config_file_str])
            else:
                run_command(["notepad.exe", config_file_str])
        else:
            typer.launch(config_file_str)

    def get_config_file_path(self) -> Path:
        """Get the default path name for the config file"""
        config_file = ConfigFile.CONFIG_DIRECTORY / f"{APP_NAME}.toml"

        return config_file

    def create_config_file(self) -> Path:
        """Create a blank config file if it doesn't already exist"""
        config_file = self.get_config_file_path()

        if config_file.exists():
            return config_file

        config_root = config_file.parent

        if not config_root.exists():
            config_root.mkdir(parents=True, exist_ok=True)

        config_file.touch()

        return config_file

    def factory_reset(self) -> None:
        """Factory reset of app defaults.

        Deletes the config file to avoid accidentally writing old data. It will be regenerated next time the app is launched
        """

        config_file = self.get_config_file_path()

        if config_file.exists() and config_file.is_file():
            config_file.unlink(missing_ok=True)
            CliUtils.print_rich(
                "Config file deleted. Will be re-generated next time the program is launched."
            )

    def write_defaults(self) -> None:
        """Write the factory defaults to the config file in .toml format"""

        # Since this is run on every load but rarely used, only import within the function
        import tomlkit
        from tomlkit.items import Table

        # Helper function to pull together a table (section) of the toml file
        # Write everything as a string to make it easier for novices to edit. We will convert it later.
        def create_table(content: dict[str, Any] | None, comment_str: str | None = None) -> Table:
            result = tomlkit.table()

            if comment_str:
                result.add(tomlkit.comment(comment_str))
            if content:
                for key, value in content.items():
                    if value is None:
                        value = ""

                    # Escape any paths
                    if isinstance(value, Path):
                        value = re.sub(r"\\", r"\\\\", str(value))

                    result.add(key, str(value))

            return result

        # Create config file if it doesn't currently exist
        file_path = self.create_config_file()

        doc = tomlkit.document()
        doc.add("instructions", create_table(None, HelpText.toml_instructions))
        doc.add(
            "general", create_table(self.get_object_values(self.general), HelpText.toml_general)
        )
        doc.add(
            "external_resources",
            create_table(self.get_object_values(self.external_resources), HelpText.toml_external),
        )
        doc.add("anki", create_table(self.get_object_values(self.anki), HelpText.toml_anki))
        doc.add(
            "lemmatiser",
            create_table(self.get_object_values(self.lemmatiser), HelpText.toml_lemmatiser),
        )
        doc.add(
            "downloader",
            create_table(self.get_object_values(self.downloader), HelpText.toml_downloader),
        )
        doc.add(
            "transcriber",
            create_table(self.get_object_values(self.transcriber), HelpText.toml_transcriber),
        )

        with file_path.open("w", encoding="utf-8") as f:
            tomlkit.dump(doc, f)

    def get_object_values(self, defaults_class: object) -> dict[str, Any]:
        """Get the non-built in parameters from an object

        Be careful if the object has both parameters and functions.
        This is designed to work with objects with parameters only.
        """

        output: dict[str, Any] = {}
        for key, value in vars(defaults_class).items():
            if not key.startswith("__"):
                if isinstance(value, Path):
                    value = str(value)
                output[key] = value

        return output

    def read_defaults(self) -> None:
        """Read the defaults values from a toml file"""
        config_file = self.get_config_file_path()

        if not config_file.exists():
            CliUtils.print_error("Could not read configuration file. Defaults have not been loaded")
            return None

        config: dict = {}

        parse_error = False
        try:
            config = rtoml.load(config_file)
        except rtoml.TomlParsingError:
            parse_error = True

        # Attempt to fix it, most likely culprit is escaped paths
        if parse_error:
            try:
                self.fix_toml_paths(config_file)
                config = rtoml.load(config_file)
            except Exception as e:
                CliUtils.print_error(
                    "Could not read user config file. gogadget will use its own default values.\nYou may want to run `gogadget set-defaults --factory` to reset the user configuration.",
                    e,
                )
                return None

        # We don't want this to cause a crash as we need the user to always be able to run gogadget set-defaults --factory
        # This runs every time, including before that command
        # If there is an issue, the tool will revert to the defaults set in the classes
        try:
            general = config["general"]
            self.general.language = self.read_str(general, "language", self.general.language)
            self.general.language_for_translations = self.read_str(
                general, "language_for_translations", self.general.language_for_translations
            )
            self.general.output_directory = self.read_path(
                general, "output_directory", self.general.output_directory, blank_is_none=False
            )  # type: ignore

            external_resources = config["external_resources"]
            self.external_resources.dictionary_file = self.read_path(
                external_resources, "dictionary_file", self.external_resources.dictionary_file
            )
            self.external_resources.word_audio_directory = self.read_path(
                external_resources,
                "word_audio_directory",
                self.external_resources.word_audio_directory,
            )
            self.external_resources.word_exclude_spreadsheet = self.read_path(
                external_resources,
                "word_exclude_spreadsheet",
                self.external_resources.word_exclude_spreadsheet,
            )

            anki = config["anki"]
            self.anki.extract_media = self.read_bool(anki, "extract_media", self.anki.extract_media)
            self.anki.include_words_with_no_definition = self.read_bool(
                anki, "include_words_with_no_definition", self.anki.include_words_with_no_definition
            )
            self.anki.subs_offset_ms = self.read_int(
                anki, "subs_offset_ms", self.anki.subs_offset_ms
            )
            self.anki.subs_buffer_ms = self.read_int(
                anki, "subs_buffer_ms", self.anki.subs_buffer_ms
            )
            self.anki.max_cards_in_deck = self.read_int(
                anki, "max_cards_in_deck", self.anki.max_cards_in_deck
            )

            lemmatiser = config["lemmatiser"]
            self.lemmatiser.lemmatise = self.read_bool(
                lemmatiser, "lemmatise", self.lemmatiser.lemmatise
            )
            self.lemmatiser.filter_out_non_alpha = self.read_bool(
                lemmatiser, "filter_out_non_alpha", self.lemmatiser.filter_out_non_alpha
            )
            self.lemmatiser.filter_out_stop_words = self.read_bool(
                lemmatiser, "filter_out_stop_words", self.lemmatiser.filter_out_stop_words
            )
            self.lemmatiser.convert_input_to_lower = self.read_bool(
                lemmatiser, "convert_input_to_lower", self.lemmatiser.convert_input_to_lower
            )
            self.lemmatiser.convert_output_to_lower = self.read_bool(
                lemmatiser, "convert_output_to_lower", self.lemmatiser.convert_output_to_lower
            )
            self.lemmatiser.return_just_first_word_of_lemma = self.read_bool(
                lemmatiser,
                "return_just_first_word_of_lemma",
                self.lemmatiser.return_just_first_word_of_lemma,
            )

            downloader = config["downloader"]
            self.downloader.advanced_options = self.read_str(
                downloader, "advanced_options", self.downloader.advanced_options
            )
            self.downloader.format = self.read_str(downloader, "format", self.downloader.format)
            self.downloader.subtitle_language = self.read_str(
                downloader, "subtitle_language", self.downloader.subtitle_language
            )

            transcriber = config["transcriber"]
            self.transcriber.whisper_model = self.read_str(
                transcriber, "whisper_model", self.transcriber.whisper_model
            )
            self.transcriber.alignment_model = self.read_str(
                transcriber, "alignment_model", self.transcriber.alignment_model
            )
            self.transcriber.subtitle_format = self.read_str(
                transcriber, "subtitle_format", self.transcriber.subtitle_format
            )
            self.transcriber.whisper_use_gpu = self.read_bool(
                transcriber, "whisper_use_gpu", self.transcriber.whisper_use_gpu
            )
            self.transcriber.max_subtitle_length = self.read_int(
                transcriber, "max_subtitle_length", self.transcriber.max_subtitle_length
            )
            self.transcriber.subtitle_split_threshold = self.read_int(
                transcriber, "subtitle_split_threshold", self.transcriber.subtitle_split_threshold
            )

        except Exception as e:
            CliUtils.print_error(
                "Could not read configuration parameters.\nPlease fix your user config file and / or consider running `gogadget set-defaults --factory` to reset it.",
                e,
            )

    def fix_toml_paths(self, file_path: Path) -> None:
        """Escapes any windows paths in the toml file"""
        # Read the content of the file
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()

        # Replace single backslashes with double backslashes, ignoring existing double backslashes
        escaped_content = re.sub(r"(?<!\\)\\(?!\\)", r"\\\\", content)

        # Write the modified content back to the file
        with file_path.open("w", encoding="utf-8") as f:
            f.write(escaped_content)

    def read_path(
        self, toml_dict: dict, dict_key: str, default_value: Path | None, blank_is_none: bool = True
    ) -> Path | None:
        value = toml_dict.get(dict_key)
        """Read value from a dictionary and convert it to path. If it's blank, change return type based upon blank_is_none"""

        if value is None:
            # Nothing found in the dictionary, return the default value, regardless of value of blank_is_none
            return default_value

        # Convert whatever we have to a string and remove all whitespace
        value = str(value).strip()

        if value != "":
            # Not blank, convert it to a path and return
            return Path(value)
        elif blank_is_none:
            # It's blank and we have decided that blank should be treated as none
            return None
        else:
            # Otherwise, blank is blank
            # Path("") is actually equivalent to Path(".")
            # Therefore, let's be safe and just return the default value
            return default_value

    def read_bool(self, toml_dict: dict, dict_key: str, default_value: bool) -> bool:
        """Get a value from a dictionary. If it's a bool, return it. If not, try to convert the string into the name of a bool type"""
        value = toml_dict.get(dict_key, default_value)

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            value = value.lower().strip()

            if value == "true":
                return True
            elif value == "false":
                return False

        # Unclear what we have, just return the default
        return default_value

    def read_int(self, toml_dict: dict, dict_key: str, default_value: int) -> int:
        """Get a value from a dictionary and convert to int. If key not present, return default. Return default if we can't convert it to int."""
        try:
            value = int(toml_dict.get(dict_key, default_value))
            return value
        except ValueError:
            return default_value

    def read_str(self, toml_dict: dict, dict_key: str, default_value: str) -> str:
        """Get a value from a dictionary and convert to str and strip whitespace. Return default value if key isn't present in dict."""
        value = str(toml_dict.get(dict_key, default_value)).strip()
        return value

    class general:
        """Object to hold default values. Pre-initialised with factory defaults"""

        language: str = ""
        language_for_translations: str = "en"
        output_directory: Path = Path("")

    class external_resources:
        """Object to hold default values. Pre-initialised with factory defaults"""

        word_exclude_spreadsheet: Path | None = None
        dictionary_file: Path | None = None
        word_audio_directory: Path | None = None

    class anki:
        """Object to hold default values. Pre-initialised with factory defaults"""

        extract_media: bool = True
        include_words_with_no_definition: bool = True
        subs_offset_ms: int = 0
        subs_buffer_ms: int = 50
        max_cards_in_deck: int = 100

    class lemmatiser:
        """Object to hold default values. Pre-initialised with factory defaults"""

        lemmatise: bool = True
        filter_out_non_alpha: bool = True
        filter_out_stop_words: bool = True
        convert_input_to_lower: bool = True
        convert_output_to_lower: bool = True
        return_just_first_word_of_lemma: bool = True

    class downloader:
        """Object to hold default values. Pre-initialised with factory defaults"""

        advanced_options: str = ""
        format: str = ""
        subtitle_language: str = ""

    class transcriber:
        """Object to hold default values. Pre-initialised with factory defaults"""

        whisper_model: str = "deepdml/faster-whisper-large-v3-turbo-ct2"
        alignment_model: str = ""
        subtitle_format: str = "vtt"
        max_subtitle_length: int = 94  # Industry standard of 47, then multiplied by 2
        subtitle_split_threshold: int = 70  # 75% of the above
        whisper_use_gpu: bool = False
