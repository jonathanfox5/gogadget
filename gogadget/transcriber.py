from pathlib import Path

from rich import print

from .cli_utils import CliUtils
from .command_runner import run_command
from .config import SUPPORTED_AUDIO_EXTS, SUPPORTED_VIDEO_EXTS
from .utils import list_files_with_extension


def transcriber(
    input_path: Path,
    output_directory: Path,
    language: str,
    use_gpu: bool,
    whisper_model: str,
    alignment_model: str,
    sub_format: str,
) -> list:
    """Main entry point for the media file transcriber"""

    # Get media files in path (path could be a file or a directory)
    supported_formats = SUPPORTED_VIDEO_EXTS + SUPPORTED_AUDIO_EXTS
    path_list = list_files_with_extension(
        input_path,
        valid_suffixes=(SUPPORTED_VIDEO_EXTS + SUPPORTED_AUDIO_EXTS),
        file_description_text="media files",
    )

    if len(path_list) == 0:
        CliUtils.print_warning("No supported file formats found")
        print("Supported formats: ", supported_formats)
        return []

    # Configure settings
    output_dir_str = str(output_directory.resolve())
    compute_type = "int8"
    device = "cpu"
    if use_gpu:
        device == "gpu"
        compute_type = "float16"

    # Run for each file
    for file_path in path_list:
        file_str = str(file_path.resolve())

        command = [
            "whispergg",
            file_str,
            "--compute_type",
            compute_type,
            "--language",
            language,
            "--model",
            whisper_model,
            "--print_progress",
            "True",
            "--output_format",
            sub_format,
            "--output_dir",
            output_dir_str,
        ]

        if alignment_model != "":
            command += ["--align_model", alignment_model]

        run_command(command, print_command=True)

    return path_list
