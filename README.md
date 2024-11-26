<a href = "https://jonathanfox5.github.io/gogadget/" alt="gogadget"><img src = "https://jonathanfox5.github.io/gogadget/img/header_black.svg" align="center"></a>

<div align = "center">
  <a href = "https://github.com/jonathanfox5/gogadget/releases" alt = "Download"><img src = "https://img.shields.io/github/v/tag/jonathanfox5/gogadget?label=download&color=blue"></a>
  <a href = "https://jonathanfox5.github.io/gogadget" alt = "Documentation"><img src = "https://img.shields.io/badge/view-documentation-brightgreen"></a>
  <a href = "https://pypi.org/project/gogadget/" alt = "PyPI"><img src = "https://img.shields.io/pypi/v/gogadget?color=%23BA55D3"></a>
</div>

## Overview

`gogadget` is a toolkit for producing immersion and priming materials for language learning.

- It tries to solve the problem that many of the most powerful tools available are hard to install, difficult to use or require lots of effort to configure for optimal results.
- It is capable of downloading audio and video files, automatically transcribing subtitles from videos and podcasts, and automatically producing filtered Anki decks with sentence audio / translations / screenshots / definitions.

## Quick start

Full documentation is available in the [manual](https://jonathanfox5.github.io/gogadget/). If you want to dive straight in, you may find the following useful:

- **[Installation instructions](https://jonathanfox5.github.io/gogadget/getting_started/installation/)**: An installer is available for Windows and simple terminal commands are available for macOS
- **[Example commands](https://jonathanfox5.github.io/gogadget/getting_started/example_commands/)**: Simple examples of the most common commands.
- **[Detailed command reference](https://jonathanfox5.github.io/gogadget/reference/command_reference/)**: Every command listed with all possible parameters and examples. Warning - could be overwhelming!
- **[Video tutorial](https://jonathanfox5.github.io/gogadget/getting_started/video_tutorial/)**: A video tutorial covering the installation of the tool and an overview of its functions.

## Video tutorial

Coming in a few days...

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
- [One click installer](https://github.com/jonathanfox5/gogadget/releases/) for Windows and [simple installation steps](https://jonathanfox5.github.io/gogadget/getting_started/installation/) for macOS and Linux.
- Ability to save defaults so that commands can be kept as short and memorable as possible.
- It supports 19 [languages](https://jonathanfox5.github.io/gogadget/getting_started/supported_languages/) fully with partial support for many more.
- Once you have installed the resources for your language, all modules apart from `gogadget download` are fully offline. This makes it useful for travelling or for processing personal conversations as there is no server involved.

## Example commands

You may prefer to watch the [Youtube Tutorial](https://jonathanfox5.github.io/gogadget/getting_started/video_tutorial/) for demonstrations of the features, including configuration for more advanced users.

### Download media

Download video from a website.

```sh
gogadget download --url "https://www.videosite.com/watch?v=videoid"
```

Note: The commands `gogadget download-audio` and `gogadget download-subtitles` are also available.

### Generate subtitles

Automatically generate subtitles for a video / folder of videos that are in English (`en`):

```sh
gogadget transcribe --input "your folder or filename" --language en
```

Note: If you have followed the steps in [the installation instructions](https://jonathanfox5.github.io/gogadget/getting_started/installation/) to enable GPU transcription, add `--gpu` to the end of the command to significantly speed up the transcription.

### Create Anki deck

Generate Anki cards from a full season of an Italian (`it`) program. Include images / audio on the cards, translate the sentences to the default language (English) and exclude the 1000 most common Italian words:

```sh
gogadget anki-deck --input "folder name" --language it --excluded-words "ita_top_1000_words.xlsx"
```

See [the manual](https://jonathanfox5.github.io/gogadget/getting_started/getting_resources/) for details on how to obtain dictionaries, exclude word spreadsheets and word audio to use with this command.

Note: You can set default parameters using `gogadget set-defaults --custom`. Once you have set up your defaults, this would allow you use this shortened version of the command:

```sh
gogadget anki-deck --input "folder name"
```

An example for setting defaults can be found [in the manual](https://jonathanfox5.github.io/gogadget/getting_started/example_use_case/).

## Installation

### Windows

Installation instructions for Windows:

1. Download the latest version of the gogadget installer from [this page](https://github.com/jonathanfox5/gogadget/releases).

2. Run the installer. It's highly recommended that you accept all of the default settings unless you know what you are doing!

3. You can run gogadget from the desktop shortcut, from the start menu or by right clicking inside a folder and selecting "Open gogadget here".

4. _[Optional]_ You can install all of the models required for your chosen language. Type the following to get the instructions:

```sh
gogadget install
```

Note: If you want to enable GPU transcription of subtitles, please tick the "CUDA" checkbox in the installer. For more information, please see [here](https://jonathanfox5.github.io/gogadget/getting_started/installation/#enabling-gpu-powered-transcription).

### macOS

Installation instructions for macOS:

1. Install homebrew if you haven't already got it installed by pasting the following line into the Terminal app and hitting enter.

   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install the required support packages, using Terminal:

   ```sh
   brew install ffmpeg uv
   ```

3. Install gogadget, using Terminal:

   ```sh
   uv tool install gogadget --python 3.12 --upgrade
   ```

4. You can then run the tool by typing the following command into Terminal:

   ```sh
   gogadget
   ```

5. _[Optional]_ You can install all of the models required for your chosen language. Type the following into Terminal to get the instructions:

   ```sh
   gogadget install
   ```

### Linux

Installation instructions for Linux:

1. Install uv using the following terminal command. uv is a python package manager that is used to keep gogadget packages separate so that they don't interfere with your existing python installation.

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install required packages (if you don't already have them) using your package manager. This will depend on your distribution. For example:

   - Ubuntu based distributions: `sudo apt install ffmpeg build-essential python3-dev`
   - Fedora based distributions: `sudo dnf install ffmpeg @development-tools python3-devel`
   - Arch based distributions: `sudo pacman -S ffmpeg base-devel`

3. Configure your paths if they aren't already set up:

   ```sh
   source $HOME/.local/bin/env
   ```

4. Install gogadget using uv. Note that we are using Python 3.10 instead of Python 3.12 that the other platforms are using. This is to ensure that all dependencies build correctly on ARM CPUs.

   ```sh
   uv tool install gogadget --python 3.10 --upgrade
   ```

5. You can then run the tool by typing the following command into your terminal:

   ```sh
   gogadget
   ```

6. _[Optional]_ You can install all of the models required for your chosen language. Type the following to get the instructions:

   ```sh
   gogadget install
   ```

7. _[Optional]_ If you wish to use your GPU instead of your CPU and your system is configured for CUDA. **AFTER** you run:

   ```sh
   uv tool install gogadget --python 3.10 --upgrade
   ```

You can **THEN** run:

```sh
uv tool install gogadget --python 3.10 --with 'torch==2.5.1+cu124' --with 'torchaudio==2.5.1+cu124' --index 'https://download.pytorch.org/whl/cu124'
```

Note that **BOTH** commands are required, in this order!

For more information on using your GPU, please see [here](https://jonathanfox5.github.io/gogadget/getting_started/installation/#enabling-gpu-powered-transcription).

### Enabling GPU powered transcription

#### Requirements

To enable GPU powered transcription of subtitles, you will need:

- A CUDA enabled NVIDIA gpu with a decent amount of VRAM (>=8 GB)
- Windows or Linux
- Up to date GPU drivers installed

These requirements are the same for most Whisper based transcription tools. Therefore, there will be plenty of guides to help you if you get stuck!

If you are using **Windows**, you will need to make sure that you tick "CUDA" in the installer.

If you are running **Linux** or are **manually** configuring it on Windows, you will need to follow the final step of the [Linux](#linux) installation instructions.

#### Running with GPU enabled

You will need to specify `--gpu` when running any transcription tasks e.g.:

```sh
gogadget transcribe -i "input file or folder" -l "code for your language" --gpu
```

Alternatively, you can change the value of `whisper_use_gpu` in the settings file to `"True"`. You can access the settings by running:

```sh
gogadget set-defaults --custom
```

## More information

Full documentation is available in the [manual](https://jonathanfox5.github.io/gogadget/).

## Acknowledgements

[gogadget](https://github.com/jonathanfox5/gogadget) is Copyright © 2024 Jonathan Fox.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details. You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

All materials in this repository are covered by the aforementioned license, unless specifically noted below:

- [gogadget/ytdlp_cli_to_api.py](https://github.com/jonathanfox5/gogadget/blob/main/gogadget/ytdlp_cli_to_api.py) has been directly reproduced from [yt-dlp's github page](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py) ([license](https://raw.githubusercontent.com/yt-dlp/yt-dlp/refs/heads/master/LICENSE)) without modification.
- The Windows installer bundles the binaries for both [FFMPEG](https://ffmpeg.org) ([license](https://ffmpeg.org/legal.html)) and [uv](https://github.com/astral-sh/uv) ([license](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT)).
