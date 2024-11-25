from pathlib import Path

import pandas as pd
import pysubs2
from lemon_tizer import LemonTizer
from rich.progress import track

from .cli_utils import CliUtils
from .config import SUPPORTED_SUB_EXTS, ConfigFile
from .lemmatiser import language_supported
from .utils import (
    dataframe_to_excel,
    generate_output_path,
    import_first_column_from_sheets,
    list_files_with_extension,
    remove_punctuation,
)


def frequency_analyser(
    input_path: Path,
    output_directory: Path,
    language: str,
    lemmatise_words: bool,
    filter_stop_words: bool,
    exclude_spreadsheet_path: Path | None = None,
) -> pd.DataFrame:
    """Main entry point for the frequency analyser function"""

    # Sort out paths
    sub_sheet_save_path = generate_output_path(input_path, output_directory, "subs", "xlsx")
    frequency_analysis_save_path = generate_output_path(
        input_path, output_directory, "frequency_analysis", "xlsx"
    )

    # Arrange the subs in a dataframe
    df_subs = subs_to_dataframe(input_path, sub_sheet_save_path)
    if df_subs is None:
        return None

    # Disable lemmatisation if spacy doesn't support it
    if lemmatise_words and (not language_supported(language)):
        lemmatise_words = False

        CliUtils.print_warning(
            f"Language {language} is not currently supported by the lemmatiser so lemmatisation has been disabled. However, the script will still function. Without lemmatisation, it is highly recommended to set --excluded-words to a spreadsheet of common words for {language} for functions that support it. Type gogadget [command_name_here] --help for more information for each individual command"
        )

    # Get the list of words to filter
    df_exclude = None
    if exclude_spreadsheet_path is not None:
        if (not exclude_spreadsheet_path.is_file()) or (not exclude_spreadsheet_path.exists()):
            CliUtils.print_warning(
                f"{exclude_spreadsheet_path} is not an existing spreadsheet file. Tool will proceed but words will not be filtered."
            )
        else:
            df_exclude = import_first_column_from_sheets(exclude_spreadsheet_path)

    # Do the frequency analysis
    df_freq = generate_frequency_analysis(
        df_input=df_subs,
        language=language,
        lemmatise_words=lemmatise_words,
        df_exclude=df_exclude,
        frequency_analysis_save_path=frequency_analysis_save_path,
        filter_stop_words=filter_stop_words,
    )

    return df_freq


def filter_frequency_analysis(
    df_main: pd.DataFrame,
    df_exclude: pd.DataFrame,
    field_main: str = "word",
    field_exclude: str = "word",
) -> pd.DataFrame:
    """Remove excluded words from the analysis output"""
    df_main = df_main[~df_main[field_main].isin(df_exclude[field_exclude])]

    return df_main


def generate_frequency_analysis(
    df_input: pd.DataFrame,
    language: str,
    lemmatise_words: bool,
    filter_stop_words: bool,
    df_exclude: pd.DataFrame | None = None,
    frequency_analysis_save_path: Path | None = None,
) -> pd.DataFrame:
    """Main helper function to do the frequency analysis"""

    CliUtils.print_status("Frequency analysis: loading language model")

    CONFIG = ConfigFile()
    CONFIG.read_defaults()

    filter_punctuation = CONFIG.lemmatiser.filter_out_non_alpha
    if lemmatise_words:
        lt = LemonTizer(language=language, model_size="lg")
        lt.set_lemma_settings(
            filter_out_non_alpha=filter_punctuation,
            filter_out_common=filter_stop_words,
            convert_input_to_lower=CONFIG.lemmatiser.convert_input_to_lower,
            convert_output_to_lower=CONFIG.lemmatiser.convert_output_to_lower,
            return_just_first_word_of_lemma=CONFIG.lemmatiser.return_just_first_word_of_lemma,
        )

    CliUtils.print_status("Frequency analysis: counting words")
    df_freq_table = pd.DataFrame(
        columns=["word", "example", "example_source", "example_start", "example_end", "frequency"]
    )

    for index, row in track(
        df_input.iterrows(),
        description="Frequency analysis: counting words...",
        total=len(df_input),
    ):
        line = row["text"]
        example_source = row["filename"]
        sentence_start = row["start"]
        sentence_end = row["end"]

        if lemmatise_words:
            word_list = lt.lemmatize_sentence(input_str=line)
        else:
            word_list = split_sentence(input_str=line, filter_punctuation=filter_punctuation)

        for word_dict in word_list:
            for word, word_lemma in word_dict.items():
                word_key = word_lemma

                if word_key in df_freq_table["word"].values:
                    df_freq_table.loc[df_freq_table["word"] == word_key, "frequency"] += 1
                else:
                    new_row = pd.DataFrame(
                        [
                            {
                                "word": word_key,
                                "example": line,
                                "example_source": example_source,
                                "example_start": sentence_start,
                                "example_end": sentence_end,
                                "frequency": 1,
                            }
                        ]
                    )
                    df_freq_table = pd.concat([df_freq_table, new_row], ignore_index=True)

    CliUtils.print_status("Frequency analysis: post-processing")

    # Filter out
    if df_exclude is not None:
        df_freq_table = filter_frequency_analysis(df_freq_table, df_exclude)

    # Sort and export
    df_freq_table = df_freq_table.sort_values(by=["frequency"], ascending=False)

    if frequency_analysis_save_path is not None:
        dataframe_to_excel(df_freq_table, frequency_analysis_save_path)

    return df_freq_table


def split_sentence(input_str: str, filter_punctuation: bool) -> list[dict[str, str]]:
    """Split sentence into words. Used if lemmatiser isn't being used.
    Objective of this is to mirror the output of the lemmatiser for languages that aren't supported
    """

    if filter_punctuation:
        input_str = remove_punctuation(input_str)

    input_str = input_str.lower()
    input_list = input_str.split(" ")

    result: list[dict[str, str]] = []
    for word in input_list:
        processed_word = word.strip()
        result.append({processed_word: processed_word})
    return result


def subs_to_dataframe(
    input_path: Path,
    spreadsheet_output_path: Path | None = None,
) -> pd.DataFrame:
    """Pull subtitle data from files into a dataframe"""

    # Get list of .gg and "standard" subtitle files
    sub_file_list: list[Path] = list_files_with_extension(
        input_path,
        valid_suffixes=SUPPORTED_SUB_EXTS,
        file_description_text="subtitle",
        print_errors=False,
    )
    gg_file_list: list[Path] = list_files_with_extension(
        input_path,
        valid_suffixes=[".gg"],
        file_description_text="subtitle",
        print_errors=False,
    )

    if (len(sub_file_list) + len(gg_file_list)) == 0:
        CliUtils.print_error("No supported subtitle files in directory")
        return None

    # If a gg file is found, remove any vtt or srt with the same from the list to avoid duplication
    reference_names: list[Path] = []
    for path in gg_file_list:
        reference_names.append(path.with_suffix(""))

    combined_file_list: list[Path] = gg_file_list
    for path in sub_file_list:
        if path not in reference_names:
            combined_file_list.append(path)

    df_subs = _extract_subs(combined_file_list)

    if spreadsheet_output_path is not None:
        dataframe_to_excel(df_subs, spreadsheet_output_path)

    return df_subs


def _extract_subs(path_list: list[Path]) -> pd.DataFrame:
    """Helper function for subs_to_dataframe"""

    df = pd.DataFrame(columns=["filename", "start", "end", "text"])
    for path in path_list:
        filename = str(path)

        # Get the type of file from the extension
        try:
            filetype = path.suffix
            if filetype == ".gg":
                filetype = path.with_suffix("").suffix

            filetype = filetype[1:]
        except Exception:
            # We haven't been able to work out the file type, see if pysubs2 can instead
            filetype = None

        subs = pysubs2.load(path.resolve(), format_=filetype)
        for sub in subs:
            add_row = pd.DataFrame(
                [{"filename": filename, "start": sub.start, "end": sub.end, "text": sub.text}]
            )
            df = pd.concat([df, add_row], ignore_index=True)

    return df
