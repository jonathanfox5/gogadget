from pathlib import Path

import ffmpeg
import pandas as pd
from rich.progress import track

from .cli_utils import CliUtils
from .config import SUPPORTED_AUDIO_EXTS, SUPPORTED_SUB_EXTS, SUPPORTED_VIDEO_EXTS
from .utils import generate_output_path, list_files_with_extension


def extract_sentence_media(
    audio_dir: Path,
    screenshot_dir: Path,
    df: pd.DataFrame,
    subs_to_media: dict[Path, Path],
    subs_offset: int,
    subs_buffer: int,
) -> pd.DataFrame:
    """Extract screenshots and audio clips from media as specified by each row in a dataframe.
    Minimum required fields in df: example_source [str], example_start [int in ms], example_end [int in ms].
    DF should ideally also has blank fields for screenshot_path [str] and sentence_audio_path [str]
    """

    # Loop through and extract the media
    extract_log: list[str] = []
    for index, row in track(df.iterrows(), description="Extracting media...", total=len(df)):
        sub_path = Path(str(row["example_source"]))
        media_path = subs_to_media[sub_path]

        start_time = int(row["example_start"])
        end_time = int(row["example_end"])
        mid_time = int((start_time + end_time) / 2)
        buffered_start = max((start_time + subs_offset - subs_buffer), 1)
        buffered_end = end_time + subs_offset + subs_buffer

        # If the identified file is a video, grab the screenshot half way between the start and end time
        if media_path.suffix in SUPPORTED_VIDEO_EXTS:
            screenshot_path = extract_frame(
                video_path=media_path,
                output_directory=screenshot_dir,
                timestamp_ms=mid_time,
                extract_log=extract_log,
            )
            df.at[index, "screenshot_path"] = str(screenshot_path.resolve())
            extract_log.append(str(screenshot_path))

        # Assuming we aren't going to blow up ffmpeg, extract the the sentence audio
        if (media_path.suffix in SUPPORTED_VIDEO_EXTS) or (
            media_path.suffix in SUPPORTED_AUDIO_EXTS
        ):
            audio_path = extract_audio_segment(
                video_path=media_path,
                output_directory=audio_dir,
                start_time_ms=buffered_start,
                end_time_ms=buffered_end,
                extract_log=extract_log,
            )
            df.at[index, "sentence_audio_path"] = str(audio_path.resolve())
            extract_log.append(str(audio_path))

    return df


def match_subtitles_to_media(input_directory: Path) -> dict[Path, Path]:
    """Based upon file name, try to match subtitles with media files.
    If both video and audio have the same file name, prioritise video"""

    supported_subs = SUPPORTED_SUB_EXTS + [".gg"]

    result: dict[Path, Path] = {}

    all_subs: list[Path] = list_files_with_extension(
        input_path=input_directory,
        valid_suffixes=supported_subs,
        file_description_text="subtitles",
        search_subdirectories=False,
        print_errors=False,
    )
    all_videos: list[Path] = list_files_with_extension(
        input_path=input_directory,
        valid_suffixes=SUPPORTED_VIDEO_EXTS,
        file_description_text="videos",
        search_subdirectories=False,
        print_errors=False,
    )
    all_audio: list[Path] = list_files_with_extension(
        input_path=input_directory,
        valid_suffixes=SUPPORTED_AUDIO_EXTS,
        file_description_text="audio files",
        search_subdirectories=False,
        print_errors=False,
    )

    if len(all_subs) == 0:
        CliUtils.print_warning("No supported subtitles in directory. Supported formats:")
        CliUtils.print_rich(supported_subs)
        return result

    if (len(all_videos) + len(all_audio)) == 0:
        CliUtils.print_warning("No media files in directory. Suppported formats:")
        CliUtils.print_rich(SUPPORTED_VIDEO_EXTS + SUPPORTED_AUDIO_EXTS)
        return result

    # Try to match a video file first. If we can't find it, move on to looking at audio files
    for subs in all_subs:
        sub_stem = subs.stem.split(".")[0]

        matched = False
        for video in all_videos:
            video_stem = video.stem.split(".")[0]

            if sub_stem == video_stem:
                matched = True
                result[subs] = video
                break

        if matched:
            continue

        for audio in all_audio:
            audio_stem = audio.stem.split(".")[0]

            if sub_stem == audio_stem:
                matched = True
                result[subs] = audio
                break

    if len(result) == 0:
        CliUtils.print_warning("Could not match subtitles to media files.")

    return result


def extract_frame(
    video_path: Path,
    output_directory: Path,
    timestamp_ms: int,
    extract_log: list[str] = [],
    file_format: str = "jpg",
) -> Path:
    """Extract a screenshot from a specific position in a video"""
    # Create output filename
    output_path = generate_output_path(video_path, output_directory, str(timestamp_ms), file_format)

    # For efficiency, don't extract twice if we have already extracted it
    if str(output_path) in extract_log:
        return output_path

    # Convert timestamp from milliseconds to seconds
    timestamp_seconds = timestamp_ms / 1000.0

    # Extract
    (
        ffmpeg.input(str(video_path), ss=timestamp_seconds)
        .output(str(output_path), vframes=1, loglevel="quiet")
        .run(overwrite_output=True)
    )

    return output_path


def extract_audio_segment(
    video_path: Path,
    output_directory: Path,
    start_time_ms: int,
    end_time_ms: int,
    extract_log: list[str] = [],
    file_format: str = "mp3",
):
    """Extract an audio clip from a media file and normalise it for speech."""

    # Create output filename
    output_path = generate_output_path(
        video_path, output_directory, str(start_time_ms), file_format
    )

    # For efficiency, don't extract twice if we have already extracted it
    if str(output_path) in extract_log:
        return output_path

    # Convert start and end times from milliseconds to seconds
    start_time_seconds = start_time_ms / 1000.0
    end_time_seconds = end_time_ms / 1000.0

    # Extract it
    (
        ffmpeg.input(str(video_path.resolve()), ss=start_time_seconds, to=end_time_seconds)
        .filter("speechnorm")
        .output(str(output_path.resolve()), format=file_format, loglevel="quiet")
        .run(overwrite_output=True)
    )

    return output_path
