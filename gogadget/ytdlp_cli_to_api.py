"""
Taken from: https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py
Public domain licence: https://raw.githubusercontent.com/yt-dlp/yt-dlp/refs/heads/master/LICENSE

File not been modified from source, aside from this comment and removal of if __name__ == "__main__" block.

Used to convert yt-dlp command line arguments into a dictionary that can be read by the python api.
"""

# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yt_dlp
import yt_dlp.options

create_parser = yt_dlp.options.create_parser


def parse_patched_options(opts):
    patched_parser = create_parser()
    patched_parser.defaults.update(
        {
            "ignoreerrors": False,
            "retries": 0,
            "fragment_retries": 0,
            "extract_flat": False,
            "concat_playlist": "never",
        }
    )
    yt_dlp.options.create_parser = lambda: patched_parser
    try:
        return yt_dlp.parse_options(opts)
    finally:
        yt_dlp.options.create_parser = create_parser


default_opts = parse_patched_options([]).ydl_opts


def cli_to_api(opts, cli_defaults=False):
    opts = (yt_dlp.parse_options if cli_defaults else parse_patched_options)(opts).ydl_opts

    diff = {k: v for k, v in opts.items() if default_opts[k] != v}
    if "postprocessors" in diff:
        diff["postprocessors"] = [
            pp for pp in diff["postprocessors"] if pp not in default_opts["postprocessors"]
        ]
    return diff
