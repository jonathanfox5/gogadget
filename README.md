# Overview

gogadget is a toolkit for producing immersion and priming materials for language learning.

- It tries to solve the problem that many of the most powerful tools available are hard to install, difficult to use or are paywalled.
- It is capable of downloading audio and video files, automatically transcribing subtitles from videos and podcasts, and automatically producing filtered Anki decks with sentence audio / translations / screenshots / definitions.

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

## General Examples

Please see the [Youtube Tutorial](#youtube-tutorial) for demonstrations of the features, including configuration for more advanced users.

1. Download a video:

   ```sh
   gogadget download --url "https://www.videosite.com/watch?v=videoid"
   ```

2. Automatically create subtitles for a video / folder of videos that are in English (`en`):

   ```sh
   gogadget transcribe --input-path "your folder or filename" --language en
   ```

3. Generate Anki cards from a full season of an Italian (`it`) program. Include images / audio on the cards, translate the sentences to the default language (English) and exclude the 1000 most common Italian words:

   ```sh
   gogadget anki-deck --input-directory "folder name" --language it --excluded-words "ita_top_1000_words.xlsx"
   ```

4. You can set default parameters using `gogadget set-defaults --custom`. Once you have set up your defaults, this would allow you to type the following for example (3):

   ```sh
   gogadget anki-deck --input-directory "folder name"
   ```

5. Commands have both a "standard" form and a "short" form. You can use whatever works best for you! The following two lines are equivalent:

   ```sh
   gogadget download --url "https://www.videosite.com/watch?v=videoid" --output-directory "immersion videos" --subtitle_language en
   gogadget download -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos" -l en
   ```

All commands will produce help text by default, eliminating the need to remember syntax. For example:

![Example Help Text](https://github.com/jonathanfox5/gogadget/raw/main/examples/readme_images/help_text.png?raw=true)

## Worked Example

Go to [Example use case](#example-use-case) which shows an example use case that includes downloading a playlist, transcribing subtitles and creating a fully featured Anki deck. It also shows how setting defaults can reduce the process to three simple commands.

## Youtube Tutorial

Coming in a few days...

# Table of Contents

- [Overview](#overview)
  - [Key Features](#key-features)
  - [General Examples](#general-examples)
  - [Worked Example](#worked-example)
  - [Youtube Tutorial](#youtube-tutorial)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Quick Start](#quick-start)
  - [Understanding Commands](#understanding-commands)
  - [_\[Advanced\]_ Short Names](#advanced-short-names)
  - [Configuration](#configuration)
  - [Getting dictionary, word audio and exclude lists](#getting-dictionary-word-audio-and-exclude-lists)
  - [Example use case](#example-use-case)
- [Supported Languages](#supported-languages)
- [Command reference](#command-reference)
  - [`gogadget`](#gogadget)
  - [`gogadget anki-deck`](#gogadget-anki-deck)
  - [`gogadget download`](#gogadget-download)
  - [`gogadget download-audio`](#gogadget-download-audio)
  - [`gogadget download-subtitles`](#gogadget-download-subtitles)
  - [`gogadget frequency-analysis`](#gogadget-frequency-analysis)
  - [`gogadget transcribe`](#gogadget-transcribe)
  - [`gogadget install`](#gogadget-install)
  - [`gogadget list-languages`](#gogadget-list-languages)
  - [`gogadget set-defaults`](#gogadget-set-defaults)
  - [`gogadget update-downloader`](#gogadget-update-downloader)
- [Default Parameters](#default-parameters)
- [Developer](#developer)
  - [Running from source](#running-from-source)
  - [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

# Installation

## Windows

Installation instructions for Windows:

1. Download the latest version of gogadget by clicking [here](https://github.com/jonathanfox5/gogadget/archive/refs/tags/gogadget_windows_v0.1.0.zip).
2. Extract the zip folder to wherever is convenient to you. Inside the folder, you will find `windows_installer.ps1`. Double click it, wait for it to complete and you are done!

3. You can then run the tool by typing the following command into command prompt or powershell:

```sh
gogadget
```

4. _[Optional]_ You can install all of the models required for your chosen language. Type the following to get the instructions:

```sh
gogadget install
```

## macOS

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
uv tool install gogadget --python3.12
```

4. You can then run the tool by typing the following command into Terminal:

```sh
gogadget
```

5. _[Optional]_ You can install all of the models required for your chosen language. Type the following into Terminal to get the instructions:

```sh
gogadget install
```

## Linux

Installation instructions for Linux:

1. Install uv using the following terminal command. uv is a python package manager that is used to keep gogadget packages separate so that they don't interfere with your existing python installation.

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install ffmpeg using your package manager. This will depend on your distribution. For example:

- Ubuntu based distributions: `apt install ffmpeg`
- Fedora based distributions: `dnf install ffmpeg`
- Arch based distributions: `pacman -S ffmpeg`

3. Install gogadget using uv:

```sh
uv tool install gogadget --python3.12
```

4. You can then run the tool by typing the following command into your terminal:

```sh
gogadget
```

5. _[Optional]_ You can install all of the models required for your chosen language. Type the following to get the instructions:

```sh
gogadget install
```

# Quick Start

This is a written overview on how to use the tool. If this isn't your thing, you might find the following useful instead:

- **If you prefer to watch a tutorial rather than follow written instructions, it is available here: [Youtube Tutorial](#youtube-tutorial)**
- Examples of some of the functions are given here: [General Examples](#general-examples)
- Full written documentation of every function in the tool is available here: [Command reference](#command-reference)
- An explanation of the settings file is here: [Default Parameters](#default-parameters)

## Understanding Commands

The intended behaviour is that the tool itself will guide the user on how to use it. If you type `gogadget` in a command prompt or terminal window, you will get:

![Main menu](https://github.com/jonathanfox5/gogadget/raw/main/examples/readme_images/main_menu.png?raw=true)

All commands are listed in the `Primary Functions` box and have their own documentation. Each command has parameters associated with it. These can be listed by just typing `gogadget` then the name of the command that you are interested in. For example, `gogadget download` produces:

![Download Help Text](https://github.com/jonathanfox5/gogadget/raw/main/examples/readme_images/download_help.png?raw=true)

You will see from the output of that command that you can just run the following to download a video:

```sh
gogadget download --url "https://www.videosite.com/watch?v=videoid"
```

Several commands use a standardised two letter code to identify languages (e.g. English is `en`, Italian is `it`, Japanese is `ja`, etc.) To get a list of supported languages and the associated two letter codes, run this command:

```sh
gogadget list-languages
```

## _[Advanced]_ Short Names

All parameters in all commands have both a "standard" form and a "short" form. You can use whatever works best for you! The following two lines are equivalent.

```sh
gogadget download --url "https://www.videosite.com/watch?v=videoid" --output-directory "immersion videos" --subtitle_language en
gogadget download -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos" -l en
```

Note: Regardless of the "standard" name, all commands follow the same logic for their "short" names. The item that is being used as input is `-i`, the output is `-o` and the language is `-l`. Normally you don't need any more than this!

## Configuration

It's recommended, but not required, that you fully install the models for the languages that you are interested in. e.g. To install Italian (target language) with English (native language) translations, run:

```sh
gogadget install --language it --translation-language en
```

You can also configure defaults so that you don't need to specify as many parameters each time you run your commands:

```sh
gogadget set-defaults --custom
```

## Getting dictionary, word audio and exclude lists

`gogadget anki-deck` accepts the following arguments:

- `--dictionary` This should be a dictionary in json format. [Vocabsieve's documentation](https://docs.freelanguagetools.org/resources.html) is an excellent resource for finding one in your target language. I personally use the Migaku `Vicon_Ita_to_Eng_Dictionary.json` that is linked in the Vocabsieve docs and the Wiktionary ones are also very good.
- `--word-audio` This is should be a directory of `mp3` files with native pronunciations of individual words. [Vocabsieve's documentation](https://docs.freelanguagetools.org/resources.html) is, again, an excellent resource for these. I use both the Forvo and Lingua Libre ones that are linked in the Vocabsieve docs. The use of `mp3` (rather than any other audio format) is enforced by the tool due to compatibility issues with certain versions of Anki. If you are on macOS or Linux then you can use FFMPEG to batch convert from `ogg` to `mp3`.

  ```sh
   for i in *.ogg; do ffmpeg -i "$i" "${i%.*}.mp3"; done
   rm *.ogg
  ```

- `--excluded-words` is a spreadsheet with words that you don't want included in your deck. This is useful to make sure that you aren't wasting time reviewing words that you already know. [Wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists) is a good source for frequency lists but you could also export your known words from Anki to get a more personalised experience. The only requirement is that the words that you want to filter out should be in column `A` of the spreadsheet though you can use multiple sub-sheets in the file if you wish to organise them.

## Example use case

The following example is my personal use case for producing priming materials prior to immersing in them. My target language is Italian (`it`) and my native language is English(`en`). I have set up a json dictionary, word audio and an exclude list as described in [Getting dictionary, word audio and exclude lists](#getting-dictionary-word-audio-and-exclude-lists).

As a "one off" task, I set up my default settings by running `gogadget set-defaults --custom`. I changed the following settings from the defaults. [the defaults are set for the widest compatibility, not for a specific workflow]

```ini
[general]
# Change language to target language (mine is Italian)
language = it
language_for_translations = en
output_directory = .

[external_resources]
# Set the paths of the resources on my hard drive
dictionary_file = /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Dictionaries/Migaku/Vicon_Ita_to_Eng_Dictionary.json
word_audio_directory = /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Audio
word_exclude_spreadsheet = /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Frequency_lists/ita_exclude.xlsx

[anki]
# Change the `include_words_with_no_definition` to False. By filtering out words not in the dictionary, this has the effect of filtering out proper nouns and non-target language words
extract_media = True
include_words_with_no_definition = False
subs_offset_ms = 0
subs_buffer_ms = 50
max_cards_in_deck = 100

[lemmatiser]
# Keep the settings in here as default but might be useful to tweak them for other languages
lemmatise = True
filter_out_non_alpha = True
filter_out_stop_words = True
convert_input_to_lower = True
convert_output_to_lower = True
return_just_first_word_of_lemma = True

[downloader]
# I keep subtitle_language blank as I prefer to generate my own using `gogadget transcribe`
advanced_options =
format =
subtitle_language =

[transcriber]
# Change `whisper_use_gpu` to True on my windows PC which has an Nvidia GPU. This massively speeds up transcription but isn't compatible unless you have a GPU that can run CUDA
whisper_model = deepdml/faster-whisper-large-v3-turbo-ct2
alignment_model =
subtitle_format = vtt
whisper_use_gpu = True
```

Now that these parameters are set, they no longer need to be specified in the commands.

For this example, let's assume that I'm downloading a playlist of videos for a specific series that I want to learn the key vocabulary for. The URL of this hypothetical playlist is `https://www.videosite.com/playlist_name` and I'm storing everything in a folder called `immersion`.

I would take the following steps. You can type the command without the extra parameters into your terminal (e.g. `gogadget download`) if you want to understand the specific options that I'm choosing.

1. Download the videos that are in the playlist:

   ```sh
   gogadget download -i "https://www.videosite.com/playlist_name" -o "immersion"
   ```

2. Transcribe the Italian subtitles for all of the videos in the folder. I could have just downloaded them in the previous step by specifying a `--subtitle-language` in the command or in the defaults but I prefer the accuracy of transcribing them myself.

   ```sh
   gogadget transcribe -i "immersion" -o "immersion"
   ```

3. Create the Anki deck:

   ```sh
   gogadget anki-deck -i "immersion"
   ```

An Anki deck will be written to `immersion/media/`. I can then just double click on the `.apkg` file in there and it will automatically be loaded.

# Supported Languages

| Language              | Code | All Modules | Lemmatiser | Transcriber | Translator |
| --------------------- | ---- | ----------- | ---------- | ----------- | ---------- |
| Albanian              | sq   |             |            |             | ✅         |
| Arabic                | ar   |             |            | ✅          | ✅         |
| Azerbaijani           | az   |             |            |             | ✅         |
| Basque                | eu   |             |            |             | ✅         |
| Bengali               | bn   |             |            |             | ✅         |
| Bulgarian             | bg   |             |            |             | ✅         |
| Catalan               | ca   | ✅          | ✅         | ✅          | ✅         |
| Chinese               | zh   | ✅          | ✅         | ✅          | ✅         |
| Chinese (traditional) | zt   |             |            |             | ✅         |
| Croatian              | hr   |             | ✅         | ✅          |            |
| Czech                 | cs   |             |            | ✅          | ✅         |
| Danish                | da   | ✅          | ✅         | ✅          | ✅         |
| Dutch                 | nl   | ✅          | ✅         | ✅          | ✅         |
| English               | en   | ✅          | ✅         | ✅          | ✅         |
| Esperanto             | eo   |             |            |             | ✅         |
| Estonian              | et   |             |            |             | ✅         |
| Finnish               | fi   | ✅          | ✅         | ✅          | ✅         |
| French                | fr   | ✅          | ✅         | ✅          | ✅         |
| Galician              | gl   |             |            |             | ✅         |
| German                | de   | ✅          | ✅         | ✅          | ✅         |
| Greek                 | el   | ✅          | ✅         | ✅          | ✅         |
| Hebrew                | he   |             |            | ✅          | ✅         |
| Hindi                 | hi   |             |            | ✅          | ✅         |
| Hungarian             | hu   |             |            | ✅          | ✅         |
| Indonesian            | id   |             |            |             | ✅         |
| Irish                 | ga   |             |            |             | ✅         |
| Italian               | it   | ✅          | ✅         | ✅          | ✅         |
| Japanese              | ja   | ✅          | ✅         | ✅          | ✅         |
| Korean                | ko   | ✅          | ✅         | ✅          | ✅         |
| Latvian               | lv   |             |            |             | ✅         |
| Lithuanian            | lt   |             | ✅         |             | ✅         |
| Macedonian            | mk   |             | ✅         |             |            |
| Malay                 | ms   |             |            |             | ✅         |
| Malayalam             | ml   |             |            | ✅          |            |
| Norwegian             | no   |             |            | ✅          |            |
| Norwegian Bokmål      | nb   |             | ✅         |             | ✅         |
| Norwegian Nynorsk     | nn   |             |            | ✅          |            |
| Persian               | fa   |             |            | ✅          | ✅         |
| Polish                | pl   | ✅          | ✅         | ✅          | ✅         |
| Portuguese            | pt   | ✅          | ✅         | ✅          | ✅         |
| Romanian              | ro   |             | ✅         |             | ✅         |
| Russian               | ru   | ✅          | ✅         | ✅          | ✅         |
| Slovak                | sk   |             |            | ✅          | ✅         |
| Slovenian             | sl   | ✅          | ✅         | ✅          | ✅         |
| Spanish               | es   | ✅          | ✅         | ✅          | ✅         |
| Swedish               | sv   |             | ✅         |             | ✅         |
| Tagalog               | tl   |             |            |             | ✅         |
| Telugu                | te   |             |            | ✅          |            |
| Thai                  | th   |             |            |             | ✅         |
| Turkish               | tr   |             |            | ✅          | ✅         |
| Ukrainian             | uk   | ✅          | ✅         | ✅          | ✅         |
| Urdu                  | ur   |             |            | ✅          | ✅         |
| Vietnamese            | vi   |             |            | ✅          |            |

# Command reference

## `gogadget`

Lists each of the available commands.

**Usage**:

```console
$ gogadget [OPTIONS] COMMAND
```

**Options**:

- `--version`: Display application version.
- `--help`: Show this message and exit.

**Commands**:

- `anki-deck`: Build an Anki deck using the most common vocabulary in a subtitles file or a folder of subtitles. Optionally include audio and / or screenshots from the source media file(s).
- `download`: Download a video or playlist from a website URL.
- `download-audio`: Download a video or playlist from a website URL and convert it to an audio file.
- `download-subtitles`: Download subtitles from an online video service.
- `frequency-analysis`: Produce a frequency analysis of the most common vocabulary in a subtitles file or a folder of subtitles. Useful for priming, also used as a pre-processing stage for some other functions.
- `transcribe`: Produce subtitle file(s) from audio or video using whisperX.
- `install`: Download models for a given `--language` and initialises tools.
- `list-languages`: Display languages supported by the tool.
- `set-defaults`: Configure your default paths so that don't need to specify them each time.
- `update-downloader`: Update the downloader to use the latest version of yt-dlp.

## `gogadget anki-deck`

Build an Anki deck using the most common vocabulary in a subtitles file or a folder of subtitles. Optionally include audio and / or screenshots from the source media file(s).

If you use this regularly, it's highly recommended to set the default paths to your dictionary, excluded words, etc. and preferred processing options to simplify the process.
You can set your defaults using the following command:

```sh
gogadget set-defaults --custom
```

**Examples**:

1. Normal usage using standard names where your target language is italian and your native language is English.

   ```sh
   gogadget anki-deck --input-directory "folder containing subtitles and media files" --language it --translation-language en
   ```

2. As per (1) but uses dictionary, word exclude list and word audio bank. Also uses --exclude-no-definition to filter out proper nouns / non-target language words.

   ```sh
   gogadget anki-deck --input-directory "folder containing subtitles and media files" --language it --translation-language en --dictionary "dictionary.json" --word_audio "folder_name" --excluded-words "excel_name.xlsx" --exclude-no-definition
   ```

3. Equivalent of (2) using short names.

   ```sh
   gogadget anki-deck -i "folder containing subtitles and media files" -l it -t en -d "dictionary.json" -w "folder_name" -e "excel_name.xlsx" -h
   ```

4. If you have set all of your defaults as described above, you can just run.

   ```sh
   gogadget anki-deck -i "folder containing subtitles and media files"
   ```

**Usage**:

```console
$ gogadget anki-deck [OPTIONS]
```

**Options**:

- `-i, --input-directory PATH`: Directory (folder) containing the video file(s) and subtitle files(s) to be turned into an Anki deck.
- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. `en` (for English), `es` (for Spanish) or `it` (Italian). Run `gogadget list-languages` for a list of supported languages.
- `-t, --translation-language TEXT`: [Optional] Language to use for translations. Translation quality is generally best if either the target language or the translation is set to `en` (English). This should be a two letter language code, e.g. `en` (for English), `es` (for Spanish) or `it` (Italian). Run `gogadget list-languages` for a list of supported languages.
- `-f, --offset INTEGER`: [Optional] Time, in milliseconds, to offset the subtitles by when extracting audio. Not normally required if subtitles were generated by gogadget transcribe.
- `-b, --buffer INTEGER`: [Optional] Extra time, in milliseconds, to add to the extracted audio to avoid it being cut off. Not normally required if subtitles were generated by gogadget transcribe.
- `-x, --max-cards INTEGER`: [Optional] Maximum number of cards to include in the deck.
- `-w, --word-audio PATH`: [Optional] Directory of mp3 files of individual words to include in the Anki cards.
- `-d, --dictionary PATH`: [Optional] Dictionary in json format to retrieve definitions from for the Anki cards.
- `-e, --excluded-words PATH`: [Optional] Spreadsheet containing words to exclude from the analysis (e.g. the most common words in a language, words already learned). Words should be in the first column of the spreadsheet but can be split across multiple sub-sheets within the file.
- `-m, --lemma / -n, --no-lemma`: [Optional] Enable or disable lemmatisation. If supported for your language, this is generally recommended.
- `-s, --stop-words / -p, --no-stop-words`: [Optional] If lemmatisation is enabled, you can include or exclude stop words. Stop words are short 'function' words such as 'the', 'that', 'which', etc.
- `-q, --media / -r, --no-media`: [Optional] Media to extract sentence audio and screenshots from to display on the Anki card. This can either be a video or audio only source.
- `-g, --include-no-definition / -h, --exclude-no-definition`: [Optional] Include cards where the definition can't be found in the dictionary. Setting `--exclude-no-definition` may improve the quality of the deck as it will likely filter many proper nouns, words not from the target language, etc.
- `--help`: Show this message and exit.

## `gogadget download`

Download a video or playlist from a website URL.

**Examples**:

1. Normal usage using standard names.

   ```sh
   gogadget download --url "https://www.videosite.com/watch?v=videoid"
   ```

2. More advanced usage using standard names.

   ```sh
   gogadget download --url "https://www.videosite.com/watch?v=videoid" --output-directory "immersion videos" --subtitle_language en --format "best"
   ```

3. Equivalent of (2) using short names.

   ```sh
   gogadget download -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos" -l en -f "best"
   ```

**Usage**:

```console
$ gogadget download [OPTIONS]
```

**Options**:

- `-i, --url TEXT`: URL of the video or playlist. Supports any website supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).
- `-o, --output-directory PATH`: [Optional] Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from.
- `-f, --format TEXT`: [Optional] Specify the format of the video. Accepts [yt-dlp's](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection) format options.
- `-l, --subtitle-language TEXT`: [Optional] Language of subtitles to download. If you want to download these, you should enter a two letter language code such as `en`, `es` or `it`. It will try to download manual subtitles first and fallback to automatically generated subtitles if these aren't found.
- `-a, --advanced-options TEXT`: [Optional][Advanced] Custom yt-dlp options, should accept any command line arguments on the [github page](https://github.com/yt-dlp/yt-dlp). Please format these as a string, enclosed by quotes.
- `--help`: Show this message and exit.

## `gogadget download-audio`

Download a video or playlist from a website URL and convert it to an audio file.

**Examples**:

1. Normal usage using standard names.

   ```sh
   gogadget download-audio --url "https://www.videosite.com/watch?v=videoid"
   ```

2. More advanced usage using standard names.

   ```sh
   gogadget download-audio --url "https://www.videosite.com/watch?v=videoid" --output-directory "immersion videos"
   ```

3. Equivalent of (2) using short names.

   ```sh
   gogadget download-audio -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos"
   ```

**Usage**:

```console
$ gogadget download-audio [OPTIONS]
```

**Options**:

- `-i, --url TEXT`: URL of the video or playlist. Supports any website supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).
- `-o, --output-directory PATH`: [Optional] Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from.
- `-a, --advanced-options TEXT`: [Optional][Advanced] Custom yt-dlp options, should accept any command line arguments on the [github page](https://github.com/yt-dlp/yt-dlp). Please format these as a string, enclosed by quotes.
- `--help`: Show this message and exit.

## `gogadget download-subtitles`

Download subtitles from an online video service.

**Examples**:

1. Download english subtitles for a given video.

   ```sh
   gogadget download-subtitles --url "https://www.videosite.com/watch?v=videoid" --subtitle-language en
   ```

2. Equivalent of (1) using short names.

   ```sh
   gogadget download-subtitles -i "https://www.videosite.com/watch?v=videoid" -l en
   ```

**Usage**:

```console
$ gogadget download-subtitles [OPTIONS]
```

**Options**:

- `-i, --url TEXT`: URL of the video or playlist. Supports any website supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).
- `-l, --subtitle-language TEXT`: Language of subtitles to download. If you want to download these, you should enter a two letter language code such as `en`, `es` or `it`. It will try to download manual subtitles first and fallback to automatically generated subtitles if these aren't found.
- `-o, --output-directory PATH`: [Optional] Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from.
- `-a, --advanced-options TEXT`: [Optional][Advanced] Custom yt-dlp options, should accept any command line arguments on the [github page](https://github.com/yt-dlp/yt-dlp). Please format these as a string, enclosed by quotes.
- `--help`: Show this message and exit.

## `gogadget frequency-analysis`

Produce a frequency analysis of the most common vocabulary in a subtitles file or a folder of subtitles. Useful for priming, also used as a pre-processing stage for some other functions.

If you use this regularly, it's highly recommended to set the default paths to your excluded words and preferred processing options to simplify the process.
You can set your defaults using the following command:

```sh
gogadget set-defaults --custom
```

**Examples**:

1. Normal usage using standard names where your target language is italian.

   ```sh
   gogadget frequency-analysis --input-directory "folder containing subtitles and media files" --language it
   ```

2. As per (1) but uses word exclude list.

   ```sh
   gogadget frequency-analysis --input-directory "folder containing subtitles and media files" --language it --excluded-words "excel_name.xlsx"
   ```

3. Equivalent of (2) using short names.

   ```sh
   gogadget frequency-analysis -i "folder containing subtitles and media files" -l it -e "excel_name.xlsx"
   ```

4. If you have set all of your defaults as described above, you can just run.

   ```sh
   gogadget frequency-analysis -i "folder containing subtitles and media files"
   ```

**Usage**:

```console
$ gogadget frequency-analysis [OPTIONS]
```

**Options**:

- `-i, --input-path PATH`: Path to the video or audio file to transcribe. This can be either a specific video / audio file or a folder of files.
- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. `en` (for English), `es` (for Spanish) or `it` (Italian). Run `gogadget list-languages` for a list of supported languages.
- `-o, --output-directory PATH`: [Optional] Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from.
- `-e, --excluded-words PATH`: [Optional] Spreadsheet containing words to exclude from the analysis (e.g. the most common words in a language, words already learned). Words should be in the first column of the spreadsheet but can be split across multiple sub-sheets within the file.
- `-m, --lemma / -n, --no-lemma`: [Optional] Enable or disable lemmatisation. If supported for your language, this is generally recommended.
- `-s, --stop-words / -p, --no-stop-words`: [Optional] If lemmatisation is enabled, you can include or exclude stop words. Stop words are short 'function' words such as 'the', 'that', 'which', etc.
- `--help`: Show this message and exit.

## `gogadget transcribe`

Produce subtitle file(s) from audio or video using whisperX.

`--input_path` and `-i` accept both files and directories of files.

If you have an NVIDIA GPU that is set up for CUDA, it's strongly recommended to pass the `--gpu` flag as this significantly speeds up the tool.

You can also reduce runtime (at the expense of accuracy) by specifying `--whisper-model small`

**Examples**:

1. Transcribe a media file or folder of media files that is in English.

   ```sh
   gogadget transcribe --input-path "path to media file or folder containing media files" --language en
   ```

2. As per (1) but using the GPU to process the model.

   ```sh
   gogadget transcribe --input-path "path to media file or folder containing media files" --language en --gpu
   ```

3. Example using short names where the output folder is also specified.

   ```sh
   gogadget transcribe -i "path to media file or folder containing media files" -o "folder to save to" -l en -g
   ```

**Usage**:

```console
$ gogadget transcribe [OPTIONS]
```

**Options**:

- `-i, --input-path PATH`: Path to the video or audio file to transcribe. This can be either a specific video / audio file or a folder of files.
- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. `en` (for English), `es` (for Spanish) or `it` (Italian). Run `gogadget list-languages` for a list of supported languages.
- `-o, --output-directory PATH`: [Optional] Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from.
- `-w, --whisper-model TEXT`: [Optional] Specify the whisper model to use for transcription. By default, this is large-v3 turbo but setting this to `small` can significantly speed the process up at the cost of accuracy.
- `-a, --align-model TEXT`: [Optional] Specify the model from hugging face to use to align the subtitles with the audio. For the most common languages, the tool will find this for you. Run `gogadget list-languages` to see supported languages.
- `-g, --gpu / -c, --cpu`: [Optional] You can specify `--gpu` if you have a CUDA enabled Nvidia graphics card to significantly speed up the processing.
- `-f, --subtitle-format TEXT`: [Optional] File format for the subtitles. You can specify `vtt`, `srt`, `json`, `txt`, `tsv` or `aud`. `vtt` is the preferred format of the other tools in this suite.
- `--help`: Show this message and exit.

## `gogadget install`

Download models for a given `--language` and initialises tools.

**Examples**:

1. Install modules to process Italian and produce English translations.

   ```sh
   gogadget install --language it --translation-language en
   ```

2. To get a list of language codes to use in the command, run:

   ```sh
   gogadget list-languages
   ```

**Usage**:

```console
$ gogadget install [OPTIONS]
```

**Options**:

- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. en (for English), es (for Spanish) or it (Italian). Run gogadget list-languages for a list of supported languages.
- `-t, --translation-language TEXT`: [Optional] Language to use for translations. Translation quality is generally best if either the target language or the translation is set to en (English). This should be a two letter language code, e.g. `en` (for English), `es` (for Spanish) or `it` (Italian). Run `gogadget list-languages` for a list of supported languages.
- `--help`: Show this message and exit.

## `gogadget list-languages`

Display languages supported by the tool.

**Examples**:

1. List languages supported by all functions of the tool.

   ```sh
   gogadget list-languages
   ```

2. List languages supported or partially supported by each module.

   ```sh
   gogadget list-languages --detailed
   ```

**Usage**:

```console
$ gogadget list-languages [OPTIONS]
```

**Options**:

- `-a, --detailed`: [Optional] List the languages supported by each module of the tool.
- `--help`: Show this message and exit.

## `gogadget set-defaults`

Configure your default paths so that don't need to specify them each time.

**Examples**:

1. Open the settings file on your folder in your default text editor.

   ```sh
   gogadget set-defaults --custom
   ```

2. Reset to factory defaults.

   ```sh
   gogadget set-defaults --factory
   ```

**~~WARNING~~** It is possible to break the tool by setting incorrect values in the config file.
Reset to factory defaults if you experience errors or unexpected behaviour.

**Usage**:

```console
$ gogadget set-defaults [OPTIONS]
```

**Options**:

- `-f, --factory`: [Optional] Load factory default settings. These settings are chosen to be compatible with most systems and languages with minimal tweaking.
- `-c, --custom`: [Optional] Set custom settings in a text file. Useful for setting default paths to resources.
- `--help`: Show this message and exit.

## `gogadget update-downloader`

Update the downloader to use the latest version of yt-dlp.

**Examples**:

1. Update downloader.

   ```sh
   gogadget update-downloader
   ```

**Usage**:

```console
$ gogadget update-downloader [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

# Default Parameters

```ini
[instructions]
# Main instruction:
# - Set your default values in this file
#
# Some tips:
# - Everything in here is treated as a string.
#   Therefore, do ~~~NOT~~~ include 'quote marks' around any of your entries, it will just break things!
# - You can type True or False for settings that are on/off (e.g. lemmatise, extract_media, etc.)
# - The script will attempt to fall back to sensible defaults if it can't read your values.
#   If your setting appears to not be read by the tool, this is probably the reason!
# - When specifying values in [external_resources], you can type None to show that the functionality is being used.
#   This does not work in any other section.
#   (Reasoning: This behaviour simplifies the user interface for less experienced users.
#   If you are reading this, you are being treated as an 'advanced user'!)
#
# ~~~~ WARNING ~~~~ It is possible to break the tool by setting incorrect values in here
#   Run `gogadget set-defaults --factory` (without quotes) to reset this file if you run into errors or unexplained behaviour

[general]
# language and language_for_translations should be a valid two letter language code
#   they can be left blank if desired
#   for a list of supported languages, run `gogadget list-languages` (without quotes)
#
# output_directory needs to be a valid folder on your system
#   do ~~~not~~~ include quote marks around the path
#   default is a period / dot. this represents the user's current working directory
language =
language_for_translations = en
output_directory = .

[external_resources]
# these parameters can be set to `none` (without quotes) if you don't want to use them
# setting parameters to `none` only works in this section, see instructions at top for explanation
# if you specify a path for these parameters, do ~~~not~~~ include quote marks around the path
dictionary_file = None
word_audio_directory = None
word_exclude_spreadsheet = None

[anki]
extract_media = True
include_words_with_no_definition = True
subs_offset_ms = 0
subs_buffer_ms = 50
max_cards_in_deck = 100

[lemmatiser]
lemmatise = True
filter_out_non_alpha = True
filter_out_stop_words = True
convert_input_to_lower = True
convert_output_to_lower = True
return_just_first_word_of_lemma = True

[downloader]
advanced_options =
format =
subtitle_language =

[transcriber]
whisper_model = deepdml/faster-whisper-large-v3-turbo-ct2
alignment_model =
subtitle_format = vtt
whisper_use_gpu = False
```

# Developer

## Running from source

[Poetry](https://python-poetry.org) is used to build the packages, the installers use [uv](https://docs.astral.sh/uv/) to run the tool in its own virtual environment and the only non-Python dependency is [ffmpeg](https://ffmpeg.org).

To download and run the code from source, run the following commands:

```sh
# Download the repo and enter it
git clone https://github.com/jonathanfox5/gogadget
cd gogadget

# Create the virtual environment and install packages
poetry install

# Enter the virtual environment
poetry shell

# Run the tool
gogadget
```

## Contributing

Pull requests are welcome. Some basic requirements:

- All code should be linted / formatted using [ruff](https://docs.astral.sh/ruff/). The `pyproject.toml` file in the repository contains project specific settings that should be automatically picked up by both the command line version and VSCode extension versions of ruff. The main ones are 100 line length, 4 spaces as intent and double quotes.
- All code should be type checked by [mypy](https://www.mypy-lang.org).

# Acknowledgements

[gogadget](https://https://github.com/jonathanfox5/gogadget) by Jonathan Fox is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1). All materials in this repository are covered by CC BY-NC-SA 4.0, unless specifically noted below:

- [gogadget/ytdlp_cli_to_api.py](gogadget/ytdlp_cli_to_api.py) has been directly reproduced from [yt-dlp's github page](https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/cli_to_api.py) ([license](https://raw.githubusercontent.com/yt-dlp/yt-dlp/refs/heads/master/LICENSE)) without modification.
- The Windows installer bundles the binaries for both [FFMPEG](https://ffmpeg.org) ([license](https://ffmpeg.org/legal.html)) and [uv](https://github.com/astral-sh/uv) ([license](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT)).
