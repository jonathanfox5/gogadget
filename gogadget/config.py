import configparser
import importlib.metadata
from importlib import import_module
from pathlib import Path

import typer

from .cli_utils import CliUtils
from .command_runner import program_exists, run_command
from .help_text import HelpText

"""Simple app metadata"""
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

        # TODO: [Release] Check this works on windows. Check both code and notepad
        config_file_str = str(config_file.resolve())

        platform = import_module("platform")
        if platform.system() == "Windows":
            # Try to open with vscode. If not available, open in notepad
            if program_exists("code"):
                run_command(["code", config_file_str])
            else:
                run_command(["notepad.exe", config_file_str])
        else:
            typer.launch(config_file_str)

    def get_config_file_path(self) -> Path:
        """Get the default path name for the config file"""
        config_file = ConfigFile.CONFIG_DIRECTORY / "gogadget.ini"

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
            config_file.unlink()
            print("Config file deleted. Will be re-generated next time the program is launched.")

    def write_defaults(self) -> None:
        """Write the factory defaults to the config file in .ini format"""

        file_path = self.create_config_file()

        config = configparser.ConfigParser(allow_no_value=True)
        config.add_section("instructions")
        config.add_section("general")
        config.set("general", HelpText.ini_instructions, None)

        config["general"] = {HelpText.ini_general: None} | self.get_object_values(self.general)  # type: ignore
        config["external_resources"] = {HelpText.ini_external: None} | self.get_object_values(
            self.external_resources
        )  # type: ignore
        config["anki"] = self.get_object_values(self.anki)
        config["lemmatiser"] = self.get_object_values(self.lemmatiser)
        config["downloader"] = self.get_object_values(self.downloader)
        config["transcriber"] = self.get_object_values(self.transcriber)

        # Case sensitive stuff here
        config.optionxform = str  # type: ignore
        config.set("instructions", HelpText.ini_instructions, None)

        with file_path.open("w") as f:
            config.write(f)

    def get_object_values(self, defaults_class: object) -> dict[str, str]:
        """Get the non-built in parameters from an object

        Be careful if the object has both parameters and functions.
        This is designed to work with objects with parameters only.
        """

        output: dict = {}
        for key, value in vars(defaults_class).items():
            if not key.startswith("__"):
                output[key] = str(value)

        return output

    def read_optional_path(
        self, section: configparser.SectionProxy, param_name: str
    ) -> Path | None:
        """Read path from ini file but return None if ini string = 'None'"""
        value = section.get(param_name, "none")
        value = value.lower()

        if value == "none":
            return None

        return Path(value)

    def read_defaults(self) -> None:
        """Read default values in from the user ini file"""

        config_file = self.get_config_file_path()

        if not config_file.exists():
            CliUtils.print_error("Could not read configuration file. Defaults have not been loaded")
            return None

        try:
            config = configparser.ConfigParser()
            config.read(config_file)

            general = config["general"]
            self.general.language = general.get("language", self.general.language)
            self.general.language_for_translations = general.get(
                "language_for_translations", self.general.language_for_translations
            )
            self.general.output_directory = Path(general.get("output_directory", ""))

            external_resources = config["external_resources"]
            self.external_resources.dictionary_file = self.read_optional_path(
                external_resources, "dictionary_file"
            )
            self.external_resources.word_audio_directory = self.read_optional_path(
                external_resources, "word_audio_directory"
            )
            self.external_resources.word_exclude_spreadsheet = self.read_optional_path(
                external_resources, "word_exclude_spreadsheet"
            )

            anki = config["anki"]
            self.anki.extract_media = anki.getboolean("extract_media", self.anki.extract_media)
            self.anki.include_words_with_no_definition = anki.getboolean(
                "include_words_with_no_definition", self.anki.include_words_with_no_definition
            )
            self.anki.subs_offset_ms = anki.getint("subs_offset_ms", self.anki.subs_offset_ms)
            self.anki.subs_buffer_ms = anki.getint("subs_buffer_ms", self.anki.subs_buffer_ms)
            self.anki.max_cards_in_deck = anki.getint(
                "max_cards_in_deck", self.anki.max_cards_in_deck
            )

            lemmatiser = config["lemmatiser"]
            self.lemmatiser.lemmatise = lemmatiser.getboolean(
                "lemmatise", self.lemmatiser.lemmatise
            )
            self.lemmatiser.filter_out_non_alpha = lemmatiser.getboolean(
                "filter_out_non_alpha", self.lemmatiser.filter_out_non_alpha
            )
            self.lemmatiser.filter_out_stop_words = lemmatiser.getboolean(
                "filter_out_stop_words", self.lemmatiser.filter_out_stop_words
            )
            self.lemmatiser.convert_input_to_lower = lemmatiser.getboolean(
                "convert_input_to_lower", self.lemmatiser.convert_input_to_lower
            )
            self.lemmatiser.convert_output_to_lower = lemmatiser.getboolean(
                "convert_output_to_lower", self.lemmatiser.convert_output_to_lower
            )
            self.lemmatiser.return_just_first_word_of_lemma = lemmatiser.getboolean(
                "return_just_first_word_of_lemma", self.lemmatiser.return_just_first_word_of_lemma
            )

            downloader = config["downloader"]
            self.downloader.advanced_options = downloader.get(
                "advanced_options", self.downloader.advanced_options
            )
            self.downloader.format = downloader.get("format", self.downloader.format)
            self.downloader.subtitle_language = downloader.get(
                "subtitle_language", self.downloader.subtitle_language
            )

            transcriber = config["transcriber"]
            self.transcriber.whisper_model = transcriber.get(
                "whisper_model", self.transcriber.whisper_model
            )
            self.transcriber.alignment_model = transcriber.get(
                "alignment_model", self.transcriber.alignment_model
            )
            self.transcriber.subtitle_format = transcriber.get(
                "subtitle_format", self.transcriber.subtitle_format
            )
            self.transcriber.whisper_use_gpu = transcriber.getboolean(
                "whisper_use_gpu", self.transcriber.whisper_use_gpu
            )

        except Exception as e:
            CliUtils.print_error("Could not read configuration parameters", e)

    class general:
        """Object to hold default values. Pre-initialised with factory defaults"""

        language: str = ""
        language_for_translations: str = "en"
        output_directory: Path = Path("")

    class external_resources:
        """Object to hold default values. Pre-initialised with factory defaults"""

        dictionary_file: Path | None = None
        word_audio_directory: Path | None = None
        word_exclude_spreadsheet: Path | None = None

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
        whisper_use_gpu: bool = False
