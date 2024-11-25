Gogadget is a toolkit for producing immersion and priming materials for language learning.

- It tries to solve the problem that many of the most powerful tools available are hard to install, difficult to use or require lots of effort to configure for optimal results.
- It is capable of downloading audio and video files, automatically transcribing subtitles from videos and podcasts, and automatically producing filtered Anki decks with sentence audio / translations / screenshots / definitions.

!!! note "Useful links"

    - [Installation instructions](getting_started/installation.md)
    - [Example commands](getting_started/example_commands.md)
    - [Detailed command reference](reference/command_reference.md)
    - [Video tutorial](getting_started/video_tutorial.md)

## Video Tutorial

Coming in a few days...

## Key Features

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
- One click installer for Windows and simple installation steps for macOS and Linux.
- Ability to save defaults so that commands can be kept as short and memorable as possible.
- It supports 19 languages fully with partial support for many more.
- Once you have installed the resources for your language, all modules apart from `gogadget download` are fully offline. This makes it useful for travelling or processing personal conversations as there is no server involved.

## Acknowledgements

[gogadget](https://github.com/jonathanfox5/gogadget) © 2024 Jonathan Fox. It is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1). All materials in this repository are covered by CC BY-NC-SA 4.0, unless specifically noted below:

- [gogadget/ytdlp_cli_to_api.py](https://github.com/jonathanfox5/gogadget/blob/main/gogadget/ytdlp_cli_to_api.py) has been directly reproduced from [yt-dlp's github page](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py) ([license](https://raw.githubusercontent.com/yt-dlp/yt-dlp/refs/heads/master/LICENSE)) without modification.
- The Windows installer bundles the binaries for both [FFMPEG](https://ffmpeg.org) ([license](https://ffmpeg.org/legal.html)) and [uv](https://github.com/astral-sh/uv) ([license](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT)).
