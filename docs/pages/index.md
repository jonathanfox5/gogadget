<h1 align="center">
  <a href="https://gogadget.jfox.io"><img src="img/header.svg" alt="gogadget" style="max-width: 1000px; width: 90%; height: auto" /></a>
  <br>
  Language Learning Toolkit
  <br>
  <a href="https://github.com/jonathanfox5/gogadget/releases"><img src="https://img.shields.io/github/v/tag/jonathanfox5/gogadget?label=download&color=blue" alt="Download" /></a>
  <a href="https://gogadget.jfox.io"><img src="https://img.shields.io/badge/view-documentation-brightgreen" alt="Documentation" /></a>
  <a href="https://pypi.org/project/gogadget/"><img src="https://img.shields.io/pypi/v/gogadget?color=%23BA55D3" alt="PyPI" /></a>
</h1>

## Overview

`gogadget` is a toolkit for producing immersion and priming materials for language learning.

- It tries to solve the problem that many of the most powerful tools available are hard to install, difficult to use or require lots of effort to configure for optimal results.
- It is capable of downloading audio and video files, automatically transcribing subtitles from videos and podcasts, and automatically producing filtered Anki decks with sentence audio / translations / screenshots / definitions.

## Video tutorial

Coming in a few days...

## Useful links

- [Installation instructions](getting_started/installation.md)
- [Example commands](getting_started/example_commands.md)
- [Detailed command reference](reference/command_reference.md)
- [Video tutorial](getting_started/video_tutorial.md)

## Key features

- Simple, well documented interface that is consistent across each of its tools.
- Download video, audio and subtitle files.
- Automatic generation of subtitles from video and audio files.
- Produce filtered Anki decks from subtitles that:
  - Contain images and sentence audio from the source video / audio files.
  - Automatically filter out common and known words to reduce Anki review load.
  - Prioritises words that are the most frequent in the source media.
  - Include automatic translations of sentences and definitions of words.
  - Can be built for an individual episode or a whole season.
- Create word frequency analyses for priming purposes.
- [One click installer](https://github.com/jonathanfox5/gogadget/releases/) for Windows and [simple installation steps](getting_started/installation.md) for macOS and Linux.
- Ability to save defaults so that commands can be kept as short and memorable as possible.
- It supports 19 [languages](getting_started/supported_languages.md) fully with partial support for many more.
- Once you have installed the resources for your language, all modules apart from `gogadget download` are fully offline. This makes it useful for travelling or for processing personal conversations as there is no server involved.

## Acknowledgements

[gogadget](https://github.com/jonathanfox5/gogadget) is Copyright © 2024 Jonathan Fox.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details. You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

All materials in this repository are covered by the aforementioned license, unless specifically noted below:

- [gogadget/ytdlp_cli_to_api.py](https://github.com/jonathanfox5/gogadget/blob/main/gogadget/ytdlp_cli_to_api.py) has been directly reproduced from [yt-dlp's github page](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py) ([license](https://raw.githubusercontent.com/yt-dlp/yt-dlp/refs/heads/master/LICENSE)) without modification.
- The Windows installer bundles the binaries for both [FFMPEG](https://ffmpeg.org) ([license](https://ffmpeg.org/legal.html)) and [uv](https://github.com/astral-sh/uv) ([license](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT)).
