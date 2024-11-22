import html
import json
import multiprocessing
import re
from pathlib import Path

import pandas as pd

from .cli_utils import CliUtils


def get_cpu_cores(minus_one: bool = False):
    """Get the number of logical cores in the system. minus_one can be set to leave a core unused to improve system responsiveness"""

    cores = multiprocessing.cpu_count()

    if minus_one:
        cores -= 1

        # Deal with situations where we only have a single cpu core
        cores = cores or 1

    return cores


def generate_output_path(
    source_material_path: Path, output_directory: Path, file_description: str, file_format: str
) -> Path:
    """Create a standardised file path based upon a source media file or directory"""

    # Remove punctuation before and after sanitise string to minimise garbage
    file_stem = sanitise_string_html(remove_punctuation(source_material_path.stem).strip())
    file_stem = remove_punctuation(file_stem).strip()
    file_stem = file_stem[0:30]

    if file_stem == "":
        file_stem = "_"

    video_suffix = source_material_path.suffix.replace(".", "")
    output_path = output_directory / f"{file_stem}_{video_suffix}_{file_description}.{file_format}"

    return output_path


def remove_punctuation(input_string: str) -> str:
    """Remove punctuation from a string."""

    pattern = r"[^\w\s'-]"

    output_string = re.sub(pattern, "", input_string)

    return output_string


def write_to_json(data: dict | list, file_path: Path) -> None:
    """Write a dict or list to json"""
    try:
        with open(file_path.resolve(), "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        CliUtils.print_error(f"Could not write {str(file_path)}", e)


def load_json(file_path: Path, encoding: str = "utf-8") -> list | dict:
    """Load a json into a list or dict, as appropriate"""
    with open(file_path, "r", encoding=encoding) as file:
        data = json.load(file)

    return data


def dataframe_to_excel(df: pd.DataFrame, file_path: Path, include_index: bool = False) -> None:
    """Save a pandas dataframe to an excel format"""

    try:
        df.to_excel(file_path, index=include_index)
    except Exception as e:
        CliUtils.print_error(f"Could not write {str(file_path)}", e)


def read_file_to_string(file_path: Path, encoding: str = "utf-8") -> str:
    """Read a text based file into memory"""
    output = ""

    with file_path.open("r", encoding=encoding) as file:
        output = file.read()

    return output


def import_first_column_from_sheets(file_path: Path) -> pd.DataFrame:
    """Import the contents of the first column of every sheet in a spreadsheet to dataframe. Ignore the header row."""

    excel_file = pd.ExcelFile(file_path)

    df = pd.DataFrame(columns=["word"])

    # Loop through each sheet
    for sheet_name in excel_file.sheet_names:
        # Read the first column of the sheet, ignoring the header
        new_rows = pd.read_excel(file_path, sheet_name=sheet_name, usecols=[0], names=["word"])

        df = pd.concat([df, new_rows], ignore_index=True)

    return df


def list_files_with_extension(
    input_path: Path,
    valid_suffixes: list,
    file_description_text: str = "",
    search_subdirectories: bool = False,
    print_errors: bool = True,
) -> list[Path]:
    """Gets a list of files (filtered by file extension) from an input path which may be a file or directory."""

    if not input_path.exists():
        if print_errors:
            CliUtils.print_error(
                f"Provided input path does not exist! User provided path: {str(input_path)}"
            )

        return []

    if input_path.is_file():
        if input_path.suffix not in valid_suffixes:
            if print_errors:
                CliUtils.print_error(
                    f"File is not a supported {file_description_text} file! User provided path: {str(input_path)}"
                )
                CliUtils.print_rich(f"Supported {file_description_text} file types:")
                CliUtils.print_rich(valid_suffixes)

        return [input_path]

    elif input_path.is_dir():
        search_pattern = "*"
        if search_subdirectories:
            search_pattern = "**/*"

        glob = input_path.glob(search_pattern)

        path_list = []
        for item in glob:
            if item.is_file() and (item.suffix in valid_suffixes):
                path_list.append(item)

        if len(path_list) == 0:
            if print_errors:
                CliUtils.print_error(
                    f"No {file_description_text} supported files found in directory! User provided path: {str(input_path)}."
                )
                CliUtils.print_rich(f"Supported {file_description_text} file types:")
                CliUtils.print_rich(valid_suffixes)

        return path_list
    else:
        if print_errors:
            CliUtils.print_error("Could not get list of files")
        return []


def sanitise_string_html(input_string: str) -> str:
    """Make a string html safe"""

    if isinstance(input_string, str):
        output_string = html.escape(input_string)
        return output_string
    else:
        return ""
