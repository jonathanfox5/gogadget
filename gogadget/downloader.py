from pathlib import Path

import yt_dlp

from .cli_utils import CliUtils
from .command_runner import arg_string_to_list, update_package
from .config import APP_NAME
from .ytdlp_cli_to_api import cli_to_api


def downloader(
    url: str,
    download_directory: Path = Path(""),
    format: str = "",
    subtitle_language: str = "",
    extract_audio: bool = False,
    other_options: str = "",
    subs_only: bool = False,
) -> list[Path]:
    """Main entry point for downloading videos / audio using yt-dlp"""

    # Check if subtitles are available
    subs_available = False
    if subtitle_language != "":
        subs_available = check_subs_available(url, subtitle_language)

    if (not subs_available) and subs_only:
        if subtitle_language.strip() == "":
            CliUtils.print_error(
                "Exiting, no subtitles available for download as value of `--subtitle-language` was blank. You can use [cyan bold]gogadget transcribe[/] to generate your own subtitles."
            )
        else:
            CliUtils.print_error(
                f"Exiting, no subtitles available for download for chosen language `{subtitle_language}`. You can use [cyan bold]gogadget transcribe[/] to generate your own subtitles."
            )
        return []

    # Work out the command line arguments that we want to use
    option_args = []

    if download_directory.name != "":
        option_args += ["-P", download_directory.name]
    if format != "":
        option_args += ["-f", format]
    if extract_audio:
        option_args += ["-x", "--audio-format", "mp3"]
    if subtitle_language != "" and subs_available:
        option_args += ["--write-subs", "--sub-lang", subtitle_language, "--write-auto-subs"]
    if subs_only:
        option_args += ["--skip-download"]
    if other_options != "":
        option_args += arg_string_to_list(other_options)

    # Convert the options to api style
    ydl_opts = cli_to_api(option_args, cli_defaults=True)

    # Get list of videos to download (e.g. if it's a playlist)
    CliUtils.print_status("Downloader: getting list of videos to download")
    url_list = url_to_list(url=url, ydl_opts=ydl_opts)

    # Extract the video(s)
    CliUtils.print_status("Downloader: downloading files")
    file_list = download_videos(urls=url_list, ydl_opts=ydl_opts)

    return file_list


def download_videos(urls: list[str], ydl_opts: dict) -> list[Path]:
    """Loop through urls and download each of them"""
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            file_list = []
            for url in urls:
                info_dict = ydl.sanitize_info(ydl.extract_info(url, download=True))
                file_path = Path(ydl.prepare_filename(info_dict))
                file_list.append(file_path)

            return file_list

    except Exception as e:
        CliUtils.print_error("Could not download videos", e)
        return []


def url_to_list(url: str, ydl_opts: dict) -> list[str]:
    """Unwrap playlists so that they are treated as individual items in the list"""

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.sanitize_info(ydl.extract_info(url, download=False))
            link_type = info_dict.get("_type", "video")

            urls = []
            if link_type == "video":
                urls.append(url)
            elif link_type == "playlist":
                urls = []
                if "entries" in info_dict:
                    for entry in info_dict["entries"]:
                        urls.append(entry["url"])
            else:
                CliUtils.print_warning(
                    f"Downloader does not currently support url of type {link_type}. May not function correctly."
                )

            return urls
    except Exception as e:
        CliUtils.print_error("Could not parse download urls", e)
        return []


def check_subs_available(url: str, language: str) -> bool:
    """Determine if subtitles are available on the website for a specified language code.
    Note that some websites don't use codes fully compliant with ISO (e.g. the might do en_to_it rather than just it)
    """

    try:
        option_args = ["--write-subs", "--sub-lang", language, "--write-auto-subs"]
        ydl_opts = cli_to_api(option_args, cli_defaults=False)
        ydl_opts["skip_downloads"] = True

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.sanitize_info(ydl.extract_info(url, download=False))

            captions_list: list[str] = []
            if "automatic_captions" in info_dict:
                captions_list = captions_list + list(info_dict["automatic_captions"].keys())

            if "subtitles" in info_dict:
                captions_list = captions_list + list(info_dict["subtitles"].keys())

            if len(captions_list) == 0:
                CliUtils.print_warning("No captions available for download for this video")
                return False
            elif language not in captions_list:
                CliUtils.print_warning(
                    f"No captions available in language {language} for this video"
                )
                return False

        return True
    except Exception:
        CliUtils.print_warning("Could not extract captions information for this video")
        return False


def downloader_dummy() -> None:
    """Dummy object to initialise yt-dlp on the very first run of the tool"""
    yt_dlp.YoutubeDL

    return


def downloader_update() -> None:
    """Update the yt-dlp python package"""
    update_package("yt-dlp", APP_NAME)
