from importlib import import_module
from pathlib import Path

import typer
from typing_extensions import Annotated

from .cli_utils import CliUtils
from .config import (
    APP_NAME,
    ConfigFile,
    get_resources_directory,
    get_version_number,
)
from .help_text import HelpText, SupportedLanguages, ffmpeg_warning

"""
Define settings for the cli framework (Typer) and load defaults from config file
"""
app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
    pretty_exceptions_enable=False,
)

CONFIG = ConfigFile()

# Write the config if it doesn't already exist
if not CONFIG.config_file_exists():
    CONFIG.write_defaults()

CONFIG.read_defaults()


"""
Primary commands
"""


@app.command(
    no_args_is_help=True,
    help=HelpText.create_anki_deck,
    rich_help_panel="Primary Functions",
    epilog=ffmpeg_warning(),
)
def anki_deck(
    input_directory: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            callback=CliUtils.validate_directory,
            help=HelpText.input_directory_anki,
            show_default=False,
            rich_help_panel="Required",
        ),
    ],
    language: Annotated[
        str,
        typer.Option(
            "--language",
            "-l",
            help=HelpText.language_code,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Required",
        ),
    ] = CONFIG.general.language,
    translation_language: Annotated[
        str,
        typer.Option(
            "--translation-language",
            "-t",
            help=HelpText.language_code_translation,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.language_for_translations,
    offset: Annotated[
        int,
        typer.Option("--offset", "-f", help=HelpText.subtitle_offset, rich_help_panel="Optional"),
    ] = CONFIG.anki.subs_offset_ms,
    buffer: Annotated[
        int,
        typer.Option("--buffer", "-b", help=HelpText.subtitle_buffer, rich_help_panel="Optional"),
    ] = CONFIG.anki.subs_buffer_ms,
    max_cards: Annotated[
        int,
        typer.Option("--max-cards", "-x", help=HelpText.max_cards, rich_help_panel="Optional"),
    ] = CONFIG.anki.max_cards_in_deck,
    word_audio: Annotated[
        Path | None,
        typer.Option(
            "--word-audio",
            "-w",
            callback=CliUtils.validate_optional_directory,
            help=HelpText.word_examples,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.external_resources.word_audio_directory,
    dictionary: Annotated[
        Path | None,
        typer.Option(
            "--dictionary",
            "-d",
            callback=CliUtils.validate_optional_file,
            help=HelpText.dictionary_file,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.external_resources.dictionary_file,
    excluded_words: Annotated[
        Path | None,
        typer.Option(
            "--excluded-words",
            "-e",
            callback=CliUtils.validate_optional_file,
            help=HelpText.exclude_sheet,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.external_resources.word_exclude_spreadsheet,
    lemma: Annotated[
        bool,
        typer.Option(
            "--lemma/--no-lemma", "-m/-n", help=HelpText.lemmatise, rich_help_panel="Optional Flags"
        ),
    ] = CONFIG.lemmatiser.lemmatise,
    stop_words: Annotated[
        bool,
        typer.Option(
            "--stop-words/--no-stop-words",
            "-s/-p",
            help=HelpText.stop_words,
            rich_help_panel="Optional Flags",
        ),
    ] = (not CONFIG.lemmatiser.filter_out_stop_words),
    media: Annotated[
        bool,
        typer.Option(
            "--media/--no-media",
            "-q/-r",
            help=HelpText.anki_media,
            rich_help_panel="Optional Flags",
        ),
    ] = CONFIG.anki.extract_media,
    include_no_definition: Annotated[
        bool,
        typer.Option(
            "--include-no-definition/--exclude-no-definition",
            "-g/-h",
            help=HelpText.include_no_definition,
            rich_help_panel="Optional Flags",
        ),
    ] = CONFIG.anki.include_words_with_no_definition,
):
    CliUtils.print_status("Anki builder: starting")

    # Build deck
    anki = import_module(".create_anki", APP_NAME)
    anki.create_anki(
        input_directory=input_directory,
        language=language,
        native_language=translation_language,
        subs_offset=offset,
        subs_buffer=buffer,
        max_cards=max_cards,
        lemma=lemma,
        filter_stop_words=not (stop_words),
        include_no_definition=include_no_definition,
        extract_media=media,
        word_audio_path=word_audio,
        dictionary_path=dictionary,
        excluded_words=excluded_words,
    )


@app.command(
    no_args_is_help=True,
    rich_help_panel="Primary Functions",
    help=HelpText.download,
    epilog=ffmpeg_warning(),
)
def download(
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-i",
            help=HelpText.video_url,
            show_default=False,
            callback=CliUtils.validate_url,
            rich_help_panel="Required",
        ),
    ],
    output_directory: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            callback=CliUtils.validate_directory,
            help=HelpText.output_directory,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.output_directory,
    format: Annotated[
        str,
        typer.Option(
            "--format",
            "-f",
            callback=CliUtils.clean_string,
            help=HelpText.video_format,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.downloader.format,
    subtitle_language: Annotated[
        str,
        typer.Option(
            "--subtitle-language",
            "-l",
            callback=CliUtils.clean_string,
            help=HelpText.ytdlp_subtitles,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.downloader.subtitle_language,
    advanced_options: Annotated[
        str,
        typer.Option(
            "--advanced-options",
            "-a",
            callback=CliUtils.clean_string,
            help=HelpText.ytdlp_options,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.downloader.advanced_options,
):
    CliUtils.print_status("Downloader: starting")
    downloader = import_module(".downloader", APP_NAME)

    if subtitle_language:
        subtitle_language = subtitle_language.lower().strip()

    downloader.downloader(
        url=url,
        download_directory=output_directory,
        format=format,
        subtitle_language=subtitle_language,
        other_options=advanced_options,
    )


@app.command(
    no_args_is_help=True,
    rich_help_panel="Primary Functions",
    help=HelpText.download_audio,
    epilog=ffmpeg_warning(),
)
def download_audio(
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-i",
            help=HelpText.video_url,
            show_default=False,
            callback=CliUtils.validate_url,
            rich_help_panel="Required",
        ),
    ],
    output_directory: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            callback=CliUtils.validate_directory,
            help=HelpText.output_directory,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.output_directory,
    advanced_options: Annotated[
        str,
        typer.Option(
            "--advanced-options",
            "-a",
            callback=CliUtils.clean_string,
            help=HelpText.ytdlp_options,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.downloader.advanced_options,
):
    CliUtils.print_status("Downloader: starting")
    downloader = import_module(".downloader", APP_NAME)
    downloader.downloader(
        url=url,
        download_directory=output_directory,
        extract_audio=True,
        other_options=advanced_options,
    )


@app.command(
    no_args_is_help=True,
    rich_help_panel="Primary Functions",
    help=HelpText.download_subtitles,
    epilog=ffmpeg_warning(),
)
def download_subtitles(
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-i",
            help=HelpText.video_url,
            show_default=False,
            callback=CliUtils.validate_url,
            rich_help_panel="Required",
        ),
    ],
    subtitle_language: Annotated[
        str,
        typer.Option(
            "--subtitle-language",
            "-l",
            callback=CliUtils.clean_string,
            help=HelpText.ytdlp_subtitles_required,
            rich_help_panel="Required",
        ),
    ] = CONFIG.downloader.subtitle_language,
    output_directory: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            callback=CliUtils.validate_directory,
            help=HelpText.output_directory,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.output_directory,
    advanced_options: Annotated[
        str,
        typer.Option(
            "--advanced-options",
            "-a",
            callback=CliUtils.clean_string,
            help=HelpText.ytdlp_options,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.downloader.advanced_options,
):
    CliUtils.print_status("Downloader: starting")

    downloader = import_module(".downloader", APP_NAME)

    if subtitle_language:
        subtitle_language = subtitle_language.lower().strip()

    downloader.downloader(
        url=url,
        download_directory=output_directory,
        subs_only=True,
        other_options=advanced_options,
        subtitle_language=subtitle_language,
    )

    return


@app.command(
    no_args_is_help=True, help=HelpText.frequency_analysis, rich_help_panel="Primary Functions"
)
def frequency_analysis(
    input_path: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help=HelpText.transcribe_path,
            show_default=False,
            callback=CliUtils.validate_path_exists,
            rich_help_panel="Required",
        ),
    ],
    language: Annotated[
        str,
        typer.Option(
            "--language",
            "-l",
            help=HelpText.language_code,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Required",
        ),
    ] = CONFIG.general.language,
    output_directory: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            callback=CliUtils.validate_directory,
            help=HelpText.output_directory,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.output_directory,
    excluded_words: Annotated[
        Path | None,
        typer.Option(
            "--excluded-words",
            "-e",
            callback=CliUtils.validate_optional_file,
            help=HelpText.exclude_sheet,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.external_resources.word_exclude_spreadsheet,
    lemma: Annotated[
        bool,
        typer.Option(
            "--lemma/--no-lemma", "-m/-n", help=HelpText.lemmatise, rich_help_panel="Optional Flags"
        ),
    ] = CONFIG.lemmatiser.lemmatise,
    stop_words: Annotated[
        bool,
        typer.Option(
            "--stop-words/--no-stop-words",
            "-s/-p",
            help=HelpText.stop_words,
            rich_help_panel="Optional Flags",
        ),
    ] = (not CONFIG.lemmatiser.filter_out_stop_words),
):
    CliUtils.print_status("Frequency analysis: starting")

    frequency_analyser = import_module(".frequency_analyser", APP_NAME)
    frequency_analyser.frequency_analyser(
        input_path=input_path,
        output_directory=output_directory,
        language=language,
        lemmatise_words=lemma,
        exclude_spreadsheet_path=excluded_words,
        filter_stop_words=(not stop_words),
    )


# @app.command(
#     no_args_is_help=True,
#     help=HelpText.interactive_transcript,
#     rich_help_panel="Primary Functions",
#     epilog=ffmpeg_warning(),
# )
# def interactive_transcript():
#     return


@app.command(
    no_args_is_help=True,
    rich_help_panel="Primary Functions",
    help=HelpText.transcribe,
    epilog=ffmpeg_warning(),
)
def transcribe(
    input_path: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help=HelpText.transcribe_path,
            show_default=False,
            callback=CliUtils.validate_path_exists,
            rich_help_panel="Required",
        ),
    ],
    language: Annotated[
        str,
        typer.Option(
            "--language",
            "-l",
            help=HelpText.language_code,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Required",
        ),
    ] = CONFIG.general.language,
    output_directory: Annotated[
        Path,
        typer.Option(
            "--output",
            "-o",
            callback=CliUtils.validate_directory,
            help=HelpText.output_directory,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.output_directory,
    max_length: Annotated[
        int,
        typer.Option(
            "--max-length",
            "-m",
            callback=CliUtils.validate_greater_than_zero,
            help=HelpText.max_subtitle_length,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.transcriber.max_subtitle_length,
    split_length: Annotated[
        int,
        typer.Option(
            "--split-length",
            "-s",
            callback=CliUtils.validate_greater_than_zero,
            help=HelpText.subtitle_split_threshold,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.transcriber.subtitle_split_threshold,
    whisper_model: Annotated[
        str,
        typer.Option(
            "--whisper-model",
            "-w",
            callback=CliUtils.clean_string,
            help=HelpText.whisper_model,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.transcriber.whisper_model,
    align_model: Annotated[
        str,
        typer.Option(
            "--align-model",
            "-a",
            callback=CliUtils.clean_string,
            help=HelpText.alignment_model,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.transcriber.alignment_model,
    gpu: Annotated[
        bool,
        typer.Option(
            "--gpu/--cpu", "-g/-c", help=HelpText.use_cuda, rich_help_panel="Optional Flags"
        ),
    ] = CONFIG.transcriber.whisper_use_gpu,
    subtitle_format: Annotated[
        str,
        typer.Option(
            "--subtitle-format", "-f", help=HelpText.subtitle_format, rich_help_panel="Optional"
        ),
    ] = CONFIG.transcriber.subtitle_format,
):
    CliUtils.print_status("Transcriber: starting")
    CliUtils.print_warning(
        "Some transcriber functions may appear to freeze for a few minutes if you haven't run them before!"
    )
    transcriber = import_module(".transcriber", APP_NAME)
    transcriber.transcriber(
        input_path=input_path,
        output_directory=output_directory,
        language=language,
        use_gpu=gpu,
        whisper_model=whisper_model,
        alignment_model=align_model,
        sub_format=subtitle_format,
        max_line_length=max_length,
        sub_split_threshold=split_length,
    )


"""
Configuration commands
"""


@app.command(
    no_args_is_help=True,
    rich_help_panel="Configuration",
    help=HelpText.install,
    epilog=ffmpeg_warning(),
)
def install(
    language: Annotated[
        str,
        typer.Option(
            "--language",
            "-l",
            help=HelpText.language_code,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Required",
        ),
    ] = CONFIG.general.language,
    translation_language: Annotated[
        str,
        typer.Option(
            "--translation-language",
            "-t",
            help=HelpText.language_code_translation,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Optional",
        ),
    ] = CONFIG.general.language_for_translations,
):
    CliUtils.print_status("Updating downloader (yt-dlp)")
    downloader = import_module(".downloader", APP_NAME)
    downloader.downloader_update()

    CliUtils.print_status("Initialiser downloader")
    downloader.downloader_dummy()

    CliUtils.print_status("Initialising transcriber")
    CliUtils.print_warning(
        "Some transcriber functions may appear to freeze for a few minutes if you haven't run them before!"
    )
    CliUtils.print_status("Transcriber: Checking CUDA status")
    transcriber = import_module(".transcriber", APP_NAME)

    cuda = transcriber.cuda_available()
    if cuda:
        CliUtils.print_rich("CUDA enabled, can use GPU processing")
    else:
        CliUtils.print_rich("CUDA disabled, using CPU processing")

    CliUtils.print_status("Transcriber: Initialising models")
    dummy_transcribe_file = get_resources_directory() / "a.mp3"
    transcriber.transcriber(
        input_path=dummy_transcribe_file,
        output_directory=get_resources_directory(),
        language=language,
        use_gpu=CONFIG.transcriber.whisper_use_gpu,
        whisper_model=CONFIG.transcriber.whisper_model,
        alignment_model=CONFIG.transcriber.alignment_model,
        sub_format=CONFIG.transcriber.subtitle_format,
        max_line_length=CONFIG.transcriber.max_subtitle_length,
        sub_split_threshold=CONFIG.transcriber.subtitle_split_threshold,
    )

    CliUtils.print_status("Initialising lemmatiser")
    lemmatiser = import_module(".lemmatiser", APP_NAME)
    if lemmatiser.language_supported(language=language):
        lemmatiser.lemma_dummy(language)
        print(f"Supported {language}")
    else:
        CliUtils.print_warning(f"Lemmatisation is not currently supported for language {language}")

    CliUtils.print_status("Initialising translator")
    translator = import_module(".translator", APP_NAME)
    translator.install(language, translation_language)


@app.command(rich_help_panel="Configuration", help=HelpText.list_languages)
def list_languages(
    detailed: Annotated[
        bool,
        typer.Option(
            "--detailed",
            "-a",
            help=HelpText.list_languages_detailed,
            rich_help_panel="Optional Flags",
        ),
    ] = False,
):
    CliUtils.print_rich(SupportedLanguages.common_explanation)
    CliUtils.print_rich(SupportedLanguages.get_common_languages())

    if detailed:
        CliUtils.print_rich("\n")
        CliUtils.print_rich(SupportedLanguages.whisper_explanation)
        CliUtils.print_rich(SupportedLanguages.whisper_languages)
        CliUtils.print_rich("\n")
        CliUtils.print_rich(SupportedLanguages.spacy_explanation)
        CliUtils.print_rich(SupportedLanguages.spacy_languages)
        CliUtils.print_rich("\n")
        CliUtils.print_rich(SupportedLanguages.argos_explanation)
        CliUtils.print_rich(SupportedLanguages.argos_languages)


@app.command(no_args_is_help=True, rich_help_panel="Configuration", help=HelpText.set_defaults)
def set_defaults(
    factory: Annotated[
        bool | None,
        typer.Option(
            "--factory", "-f", help=HelpText.defaults_factory, rich_help_panel="Optional Flags"
        ),
    ] = None,
    custom: Annotated[
        bool | None,
        typer.Option(
            "--custom", "-c", help=HelpText.defaults_custom, rich_help_panel="Optional Flags"
        ),
    ] = None,
):
    if factory:
        CONFIG.factory_reset()
    elif custom:
        CONFIG.launch_config_file_in_editor()


@app.command(rich_help_panel="Configuration", help=HelpText.update_downloader)
def update_downloader():
    CliUtils.print_status("Downloader update: starting")
    downloader = import_module(".downloader", APP_NAME)
    downloader.downloader_update()


"""
Define callbacks and subcommands.
"""


def version_callback(value: bool):
    """Return version number"""
    if value:
        CliUtils.print_rich(get_version_number())

        CliUtils.print_rich(f"\n{HelpText.license}")

        raise typer.Exit()


@app.callback(help=HelpText.main)
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, help=HelpText.application_version),
    ] = None,
):
    return


if __name__ == "__main__":
    app()
