from pathlib import Path

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
        CliUtils.print_rich("Supported formats:")
        CliUtils.print_rich(supported_formats)
        return []

    # Configure settings
    output_dir_str = str(output_directory.resolve())
    compute_type = "int8"
    device = "cpu"
    if use_gpu:
        if cuda_available():
            device = "cuda"
            compute_type = "float16"
        else:
            CliUtils.print_warning(
                """You have requested --gpu but CUDA is not configured.
Troubleshooting:
    - If you are on windows, did you check the CUDA option in the installer?
    - Please see readme for more information"""
            )
            CliUtils.print_warning("Falling back to --cpu")

    # Run for each file
    for file_path in path_list:
        file_str = str(file_path.resolve())

        command = [
            "whispergg",
            file_str,
            "--compute_type",
            compute_type,
            "--device",
            device,
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


def cuda_available() -> bool:
    from torch.cuda import is_available

    return is_available()


# def configure_cuda() -> None:
#     if not cuda_available():
#         install_package(
#             package_name="torch==2.5.1+cu124",
#             package_index="https://download.pytorch.org/whl/cu124",
#             app_name=APP_NAME,
#         )
#         install_package(
#             package_name="torchaudio==2.5.1+cu124",
#             package_index="https://download.pytorch.org/whl/cu124",
#             app_name=APP_NAME,
#         )
