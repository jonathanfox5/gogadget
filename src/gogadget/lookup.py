import shutil
from pathlib import Path

import pandas as pd
from rich.progress import track

from .config import SUPPORTED_WORD_AUDIO_EXTS
from .utils import list_files_with_extension, load_json


def lookup_all_words(
    df: pd.DataFrame, dictionary_path: Path, source_column: str = "word"
) -> pd.DataFrame:
    """Loops through a dataframe and fetches the definitions for all words"""

    # Get dictionary entries
    entries = load_dictionary(dictionary_path)
    assert isinstance(entries, list)

    # Add the definitions for each of the words
    for index, row in track(df.iterrows(), description="Looking up definitions...", total=len(df)):
        word = str(row[source_column]).lower()

        definition = find_definition(entries=entries, search_term=word)

        df.at[index, "definition"] = definition

    return df


def copy_all_word_audio(
    df: pd.DataFrame, library_path: Path, output_directory: Path, source_column: str = "word"
) -> pd.DataFrame:
    """Loops through a dataframe, searches for audio that matches the word and, if found, copy it to a specific directory.
    Path of copied file is written to the dataframe"""

    # Get list of files
    library = get_sound_library(library_path=library_path)

    # Copy the files to the working directory and add a link
    for index, row in track(df.iterrows(), description="Getting word audio...", total=len(df)):
        word = str(row[source_column])
        word_path = copy_sound(
            sound_library=library, lookup_value=word, output_directory=output_directory
        )

        if word_path:
            df.at[index, "word_audio_path"] = str(word_path.resolve())

    return df


def load_dictionary(dictionary_path: Path) -> list | dict:
    """Load a json dictionary from a specified path"""
    entries = load_json(dictionary_path)

    return entries


def get_sound_library(
    library_path: Path,
    file_extensions: list = SUPPORTED_WORD_AUDIO_EXTS,
    file_decription="word sound files",
) -> dict[str, Path]:
    """Find sound files in a directory and save a dictionary in the format {lower case version of the file stem: full path}"""
    sounds = list_files_with_extension(
        input_path=library_path,
        valid_suffixes=file_extensions,
        file_description_text=file_decription,
        search_subdirectories=True,
    )

    sound_library: dict[str, Path] = {}
    for sound in sounds:
        word = sound.stem.lower().strip().rstrip(".").strip()
        if word not in sound_library:
            sound_library[word] = sound

    return sound_library


def copy_sound(
    sound_library: dict[str, Path], lookup_value: str, output_directory: Path
) -> Path | None:
    """If a sound is found within the library, copy it to a specific directory. If successful, return the path of the copied file."""
    lookup_value = lookup_value.lower()

    if lookup_value not in sound_library:
        return None

    src = sound_library[lookup_value]
    filename = src.name
    dst = output_directory / filename

    shutil.copy(src, dst)

    return dst


def find_definition(entries: list, search_term: str) -> str:
    """Lookup the definition of a word within a json dictionary that has been loaded into memory"""

    if search_term:
        search_term = search_term.lower()

        left = 0
        right = len(entries) - 1

        while left <= right:
            mid = (left + right) // 2
            mid_term = entries[mid]["term"]

            if mid_term == search_term:
                return entries[mid]["definition"]
            elif mid_term < search_term:
                left = mid + 1
            else:
                right = mid - 1

        return ""

    return ""
