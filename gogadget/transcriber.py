import gc
from pathlib import Path

import whisperx_numpy2_compatibility as whisperx
from torch.cuda import empty_cache as empty_cuda_cache
from torch.cuda import is_available as is_cuda_available
from whisperx_numpy2_compatibility.SubtitlesProcessor import SubtitlesProcessor
from whisperx_numpy2_compatibility.utils import get_writer as get_whisperx_writer

from .cli_utils import CliUtils
from .config import SUPPORTED_AUDIO_EXTS, SUPPORTED_VIDEO_EXTS
from .utils import get_cpu_cores, list_files_with_extension


def transcriber(
    input_path: Path,
    output_directory: Path,
    language: str,
    use_gpu: bool,
    whisper_model: str,
    alignment_model: str,
    sub_format: str,
    max_line_length: int,
    sub_split_threshold: int,
) -> list:
    """Main entry point for the media file transcriber"""
    # TODO: Supress warning messages
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

    # Create output directory if it doesn't already exist
    output_directory.mkdir(parents=True, exist_ok=True)

    # Whisper settings that we aren't exposing to the user
    batch_size = 8
    verbose = True

    # Configure other settings based upon user input
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

    # Do the main transcription step
    stage_1_results = stage1_transcription(
        input_paths=path_list,
        language=language,
        device=device,
        compute_type=compute_type,
        whisper_model_name=whisper_model,
        batch_size=batch_size,
        cpu_cores=get_cpu_cores(minus_one=False),
        verbose=verbose,
    )

    # If we are using CUDA, we need to clear the model from memory before running the next one
    reclaim_memory_transcriber()

    # Check we have something, otherwise error
    if not stage_1_results:
        CliUtils.print_error("Could not transcribe files, failed stage 1")
        return []

    # Do the alignment step
    stage_2_results = stage2_transcription(
        stage1_results=stage_1_results,
        language=language,
        device=device,
        alignment_model_name=alignment_model,
        verbose=verbose,
    )

    # If we are using CUDA, we need to clear the model from memory before running the next one
    reclaim_memory_transcriber()

    # Check we have something, otherwise error
    if not stage_2_results:
        CliUtils.print_error("Could not transcribe files, failed stage 2")
        return []

    # Write subs to file, one for Anki use, one for normal use
    CliUtils.print_status("Transcriber: Processing, stage 3 of 3")
    write_subtitles_anki(
        stage2_results=stage_2_results,
        output_directory=output_directory,
        subtitle_format=sub_format,
    )
    sub_paths = write_subtitles_split(
        stage2_results=stage_2_results,
        output_directory=output_directory,
        subtitle_format=sub_format,
        max_line_length=max_line_length,
        sub_split_threshold=sub_split_threshold,
    )

    return sub_paths


def stage1_transcription(
    input_paths: list[Path],
    language: str,
    device: str,
    compute_type: str,
    whisper_model_name: str,
    batch_size: int,
    cpu_cores: int,
    verbose: bool,
) -> list[dict]:
    # Load transcription model
    CliUtils.print_status("Transcriber: Loading stage 1 model")
    model = whisperx.load_model(
        whisper_arch=whisper_model_name,
        device=device,
        compute_type=compute_type,
        language=language,
        threads=cpu_cores,
    )

    results: list[dict] = []
    for file_path in input_paths:
        CliUtils.print_status(
            f"Transcriber: Processing {file_path}, stage 1 of 3, this may take a while depending on file length and your computer hardware"
        )
        audio = whisperx.load_audio(str(file_path.resolve()))
        result = model.transcribe(
            audio=audio, batch_size=batch_size, language=language, print_progress=verbose
        )
        result["language"] = language

        result_dict = {
            "path": file_path,
            "audio_object": audio,
            "stage1_output": result,
            "language": language,
        }

        results.append(result_dict)

    # Reclaim memory before running the next model
    del model

    return results


def stage2_transcription(
    stage1_results: list[dict],
    language: str,
    device: str,
    alignment_model_name: str | None,
    verbose: bool,
) -> list[dict]:
    # Process arguments. Whisperx needs a model to be None to activate its own chooser
    if isinstance(alignment_model_name, str):
        if alignment_model_name.strip() == "":
            alignment_model_name = None

    model, metadata = whisperx.load_align_model(
        language_code=language, device=device, model_name=alignment_model_name
    )

    results: list[dict] = []
    for result_dict in stage1_results:
        CliUtils.print_status(f"Transcriber: Processing {result_dict['path']}, stage 2 of 3")
        stage2_result = whisperx.align(
            transcript=result_dict["stage1_output"]["segments"],
            model=model,
            align_model_metadata=metadata,
            audio=result_dict["audio_object"],
            device=device,
            return_char_alignments=False,
            print_progress=verbose,
        )
        stage2_result["language"] = language

        result_dict["stage2_output"] = stage2_result

        results.append(result_dict)

    # Reclaim memory before running the next model
    del model

    return results


def write_subtitles_split(
    stage2_results: list[dict],
    output_directory: Path,
    subtitle_format: str,
    max_line_length: int,
    sub_split_threshold: int,
) -> list:
    is_vtt = False
    if subtitle_format.lower() == "vtt":
        is_vtt = True

    output_paths: list[Path] = []
    for result_dict in stage2_results:
        media_path: Path = result_dict["path"]
        output_path = output_directory / f"{media_path.stem}.{subtitle_format}"

        if output_path.exists():
            output_path.unlink(missing_ok=True)

        CliUtils.print_plain(f"Writing split (normal) subtitles: {output_path}")

        subtitles_proccessor = SubtitlesProcessor(
            result_dict["stage2_output"]["segments"],
            result_dict["language"],
            max_line_length=max_line_length,
            min_char_length_splitter=sub_split_threshold,
            is_vtt=is_vtt,
        )

        subtitles_proccessor.save(output_path, advanced_splitting=True)

        output_paths.append(output_path)

    return output_paths


def write_subtitles_anki(
    stage2_results: list[dict], output_directory: Path, subtitle_format: str
) -> list:
    # We don't care about these but the function forces us to include them
    writer_args = {"highlight_words": False, "max_line_count": None, "max_line_width": None}

    writer = get_whisperx_writer(
        output_format=subtitle_format, output_dir=str(output_directory.resolve())
    )

    for result_dict in stage2_results:
        media_path: Path = result_dict["path"]
        intermediate_path = Path(
            output_directory / f"{media_path.stem}.{subtitle_format}.{subtitle_format}"
        )
        final_path = intermediate_path.with_suffix(".gg")

        if intermediate_path.exists():
            intermediate_path.unlink(missing_ok=True)

        if final_path.exists():
            final_path.unlink(missing_ok=True)

        CliUtils.print_plain(f"Writing long form subtitles (for Anki use): {final_path}")

        # Write subtitles
        writer(result_dict["stage2_output"], str(intermediate_path.resolve()), writer_args)

        # Rename the subtitles so that mpv, etc. don't automatically pick them up
        if intermediate_path.exists():
            print("exists")
            intermediate_path.rename(final_path)

    return []


def reclaim_memory_transcriber():
    gc.collect()
    if cuda_available():
        empty_cuda_cache()


def cuda_available() -> bool:
    return is_cuda_available()
