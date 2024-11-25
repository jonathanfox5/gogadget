from .command_runner import program_exists


def ffmpeg_warning() -> str:
    """Print a warning if FFMPEG is not found in path"""
    if not program_exists("ffmpeg"):
        return "[bold red]~~~WARNING~~~ FFMPEG is not found in the system path. Many functions will not work without it."
    return ""


class HelpText:
    """Contains the description of commands and parameters for each of the user facing functions
    Error text is handled within individual functions"""

    # General info
    license = "[blue bold link=https://https://github.com/jonathanfox5/gogadget]gogadget[/] © 2024 Jonathan Fox is licensed under [blue bold link=https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1]CC BY-NC-SA 4.0[/]."

    # Commands
    main = """
    gogadget is a toolkit for producing immersion and priming tools for language learning. It is capable of downloading audio and video files, automatically transcribing subtitles from videos and podcasts, and automatically producing filtered Anki decks with sentence audio / translations / screenshots / definitions.

    [bright_white i][u]Basics[/u]
    All commands are listed in the "Primary Functions" box below and have their own documentation. Each command has parameters associated with it. These can be listed by just typing [b magenta]gogadget[/] then the name of the command that you are interested in. For example:
    [b magenta]gogadget download[/]

    You will see from the output of that command that you can just run the following to download a video:
    [b magenta]gogadget download --url "https://www.videosite.com/watch?v=videoid"[/]

    [u]Advanced[/u]
    Commands have both a "standard" form and a "short" form. You can use whatever works best for you! The following two lines are equivalent.
    [b magenta]gogadget download --url "https://www.videosite.com/watch?v=videoid" --output "immersion videos" --subtitle_language en
    gogadget download -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos" -l en[/]
    
    Note: Regardless of the "standard" name, all commands follow the same logic for their "short" names. The item that is being used as input is -i, the output is -o and the language is -l. Normally you don't need any more than this!

    To get a list of supported languages and the associated two letter codes, run this command:
    [b magenta]gogadget list-languages[/]

    [u]Configuration[/u]
    It's recommended, but not required, that you fully install the models for the languages that you are interested in. e.g. To install Italian (target language) with English (native language) translations, run:
    [b magenta]gogadget install --language it --translation-language en[/]

    You can also configure defaults so that you don't need to specify as many parameters each time you run your commands:
    [b magenta]gogadget set-defaults --custom[/][/]
    """
    install = """Download models for a given --language and initialises tools.

    [bright_white i][u]Examples:[/u]
    1. Install modules to process Italian and produce English translations.
    gogadget install --language it --translation-language en

    2. To get a list of language codes to use in the command, run:
    gogadget list-languages
    """
    set_defaults = """
    Configure your default paths so that don't need to specify them each time.
    
    [bright_white i][u]Examples:[/u]

    1. Open the settings file on your folder in your default text editor.
    gogadget set-defaults --custom

    2. Reset to factory defaults.
    gogadget set-defaults --factory

    [red b]~~~~ WARNING ~~~~ It is possible to break the tool by setting incorrect values in the config file.
    Reset to factory defaults if you experience errors or unexpected behaviour.
    """
    update_downloader = """
    Update the downloader to use the latest version of yt-dlp.

    [bright_white i][u]Examples:[/u]

    1. Update downloader.
    gogadget update-downloader
    """
    list_languages = """
    Display languages supported by the tool.

    [bright_white i][u]Examples:[/u]
    1. List languages supported by all functions of the tool.
    gogadget list-languages

    2. List languages supported or partially supported by each module.
    gogadget list-languages --detailed
    """
    download = """
    Download a video or playlist from a website URL. 
    
    [bright_white i][u]Examples:[/u]

    1. Normal usage using standard names.
    gogadget download --url "https://www.videosite.com/watch?v=videoid"
    
    2. More advanced usage using standard names.
    gogadget download --url "https://www.videosite.com/watch?v=videoid" --output "immersion videos" --subtitle_language en --format "best"

    3. Equivalent of (2) using short names.
    gogadget download -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos" -l en -f "best"
    """
    download_audio = """
    Download a video or playlist from a website URL and convert it to an audio file.
    
    [bright_white i][u]Examples:[/u]

    1. Normal usage using standard names.
    gogadget download-audio --url "https://www.videosite.com/watch?v=videoid"
    
    2. More advanced usage using standard names.
    gogadget download-audio  --url "https://www.videosite.com/watch?v=videoid" --output "immersion videos"

    3. Equivalent of (2) using short names.
    gogadget download-audio  -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos"
    """
    download_subtitles = """
    Download subtitles from an online video service.

    [bright_white i][u]Examples:[/u]
    1. Download english subtitles for a given video.
    gogadget download-subtitles --url "https://www.videosite.com/watch?v=videoid" --subtitle-language en

    2. Equivalent of (1) using short names.
    gogadget download-subtitles -i "https://www.videosite.com/watch?v=videoid" -l en
    """
    transcribe = """
    Produce subtitle file(s) from audio or video using whisperX.

    [bright_white]--input and -i accept both files and directories of files.

    If you have an NVIDIA GPU that is set up for CUDA, it's strongly recommended to pass the --gpu flag as this significantly speeds up the tool.

    You can also reduce runtime (at the expense of accuracy) by specifying --whisper-model small

    [i][u]Examples:[/u]
    1. Transcribe a media file or folder of media files that is in English.
    gogadget transcribe --input "path to media file or folder containing media files" --language en

    2. As per (1) but using the GPU to process the model.
    gogadget transcribe --input "path to media file or folder containing media files" --language en --gpu

    3. Example using short names where the output folder is also specified.
    gogadget transcribe -i "path to media file or folder containing media files" -o "folder to save to" -l en -g
    """
    create_anki_deck = """
    Build an Anki deck using the most common vocabulary in a subtitles file or a folder of subtitles. Optionally include audio and / or screenshots from the source media file(s).
    
    [bright_white]If you use this regularly, it's highly recommended to set the default paths to your dictionary, excluded words, etc. and preferred processing options to simplify the process.
    You can set your defaults using the following command: 
    [i]gogadget set-defaults --custom

    [u]Examples:[/u]
    1. Normal usage using standard names where your target language is italian and your native language is English.
    gogadget anki-deck --input "folder containing subtitles and media files" --language it --translation-language en

    2. As per (1) but uses dictionary, word exclude list and word audio bank. Also uses --exclude-no-definition to filter out proper nouns / non-target language words.
    gogadget anki-deck --input "folder containing subtitles and media files" --language it --translation-language en --dictionary "dictionary.json" --word_audio "folder_name" --excluded-words "excel_name.xlsx" --exclude-no-definition
    
    3. Equivalent of (2) using short names.
    gogadget anki-deck -i "folder containing subtitles and media files" -l it -t en -d "dictionary.json" -w "folder_name" -e "excel_name.xlsx" -h
    
    4. If you have set all of your defaults as described above, you can just run.
    gogadget anki-deck -i "folder containing subtitles and media files"
    """
    frequency_analysis = """
    Produce a frequency analysis of the most common vocabulary in a subtitles file or a folder of subtitles. Useful for priming, also used as a pre-processing stage for some other functions.
    
    [bright_white]If you use this regularly, it's highly recommended to set the default paths to your excluded words and preferred processing options to simplify the process.
    You can set your defaults using the following command: 
    [i]gogadget set-defaults --custom

    [u]Examples:[/u]
    1. Normal usage using standard names where your target language is italian.
    gogadget frequency-analysis --input "folder containing subtitles and media files" --language it

    2. As per (1) but uses word exclude list.
    gogadget frequency-analysis --input "folder containing subtitles and media files" --language it --excluded-words "excel_name.xlsx"
    
    3. Equivalent of (2) using short names.
    gogadget frequency-analysis -i "folder containing subtitles and media files" -l it -e "excel_name.xlsx"

    4. If you have set all of your defaults as described above, you can just run.
    gogadget frequency-analysis -i "folder containing subtitles and media files"
    """
    interactive_transcript = "Create an interactive transcript from a video or audio source."

    # Parameters
    video_url = "URL of the video or playlist. Supports any website supported by [blue underline link=https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md]yt-dlp[/]."
    language_code = "Language to use for processing. This should be a two letter language code, e.g. [cyan b]en[/] (for English), [cyan b]es[/] (for Spanish) or [cyan b]it[/] (Italian). Run [cyan bold]gogadget list-languages[/] for a list of supported languages."
    filter_sheet_path = "[cyan][Optional][/] Path to spreadsheet which has list of words to filter. Words need to be in column 'A' but can be entered across multiple sheets."
    application_version = "Display application version."
    video_format = "[cyan][Optional][/] Specify the format of the video. Accepts [blue underline link=https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection]yt-dlp's format options[/]."
    output_directory = "[cyan][Optional][/] Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from."
    ytdlp_options = "[cyan][Optional][/][red][Advanced][/] Custom yt-dlp options, should accept any command line arguments on the [blue underline link=https://github.com/yt-dlp/yt-dlp]github page[/]. Please format these as a string, enclosed by quotes."
    ytdlp_subtitles = "[cyan][Optional][/] Language of subtitles to download. If you want to download these, you should enter a two letter language code such as [cyan b]en[/], [cyan b]es[/] or [cyan b]it[/]. It will try to download manual subtitles first and fallback to automatically generated subtitles if these aren't found."
    ytdlp_subtitles_required = "Language of subtitles to download. You should enter a two letter language code such as [cyan b]en[/], [cyan b]es[/] or [cyan b]it[/]. It will try to download manual subtitles first and fallback to automatically generated subtitles if these aren't found."
    dictionary_file = "[cyan][Optional][/] Dictionary in json format to retrieve definitions from for the Anki cards."
    word_examples = "[cyan][Optional][/] Directory of mp3 files of individual words to include in the Anki cards."
    transcribe_path = "Path to the video or audio file to transcribe. This can be either a specific video / audio file or a folder of files."
    whisper_model = "[cyan][Optional][/] Specify the whisper model to use for transcription. By default, this is large-v3 turbo but setting this to [cyan b]small[/] can significantly speed the process up at the cost of accuracy."
    alignment_model = "[cyan][Optional][/] Specify the model from hugging face to use to align the subtitles with the audio. For the most common languages, the tool will find this for you."
    use_cuda = "[cyan][Optional][/] You can specify --gpu if you have a CUDA enabled Nvidia graphics card to significantly speed up the processing."
    subtitle_format = "[cyan][Optional][/] File format for the subtitles. You can specify vtt, srt, json, txt, tsv or aud. Vtt is the preferred format of the other tools in this suite."
    lemmatise = "[cyan][Optional][/] Enable or disable lemmatisation. If supported for your language, this is generally recommended."
    exclude_sheet = "[cyan][Optional][/] Spreadsheet containing words to exclude from the analysis (e.g. the most common words in a language, words already learned). Words should be in the first column of the spreadsheet but can be split across multiple sub-sheets within the file."
    input_directory_anki = "Directory (folder) containing the video file(s) and subtitle files(s) to be turned into an Anki deck."
    subtitle_offset = "[cyan][Optional][/] Time, in milliseconds, to offset the subtitles by when extracting audio. Not normally required if subtitles were generated by [cyan bold]gogadget transcribe[/]."
    subtitle_buffer = "[cyan][Optional][/] Extra time, in milliseconds, to add to the extracted audio to avoid it being cut off. Not normally required if subtitles were generated by [cyan bold]gogadget transcribe[/]."
    max_cards = "[cyan][Optional][/] Maximum number of cards to include in the deck."
    anki_media = "[cyan][Optional][/] Media to extract sentence audio and screenshots from to display on the Anki card. This can either be a video or audio only source."
    include_no_definition = "[cyan][Optional][/] Include cards where the definition can't be found in the dictionary. Setting --exclude-no-definition may improve the quality of the deck as it will likely filter many proper nouns, words not from the target language, etc."
    stop_words = "[cyan][Optional][/] If lemmatisation is enabled, you can include or exclude stop words. Stop words are short 'function' words such as 'the', 'that', 'which', etc."
    language_code_translation = "[cyan][Optional][/] Language to use for translations. Translation quality is generally best if either the target language or the translation is set to [cyan b]en[/] (English). This should be a two letter language code, e.g. [cyan b]en[/] (for English), [cyan b]es[/] (for Spanish) or [cyan b]it[/] (Italian). Run [cyan bold]gogadget list-languages[/] for a list of supported languages."
    defaults_factory = "[cyan][Optional][/] Load factory default settings. These settings are chosen to be compatible with most systems and languages with minimal tweaking."
    defaults_optimised = "[cyan][Optional][/][red][Advanced][/] Load 'optimised' settings. Results are generally higher quality and tool execution time is reduced. However, some tweaking may be required to get this to run with some systems and language. Generally used in combination with [cyan bold]gogadget set-defaults --custom[/]."
    defaults_custom = "[cyan][Optional][/] Set custom settings in a text file. Useful for setting default paths to resources."
    list_languages_detailed = (
        "[cyan][Optional][/] List the languages supported by each module of the tool."
    )
    install_gpu = "[cyan][Optional][/][red][Advanced][/] Install CUDA for an NVIDIA gpu to speed up transcription."
    max_subtitle_length = "[cyan][Optional][/] The absolute maximum length that a subtitle can be."
    subtitle_split_threshold = (
        "[cyan][Optional][/] The length at which the tool considers splitting a subtitle."
    )

    # .toml file
    toml_instructions = """IMPORTANT INFORMATION
# =====================
# - All values are text and should be therefore be wrapped in double quotes. Valid examples:
#       language = "en"
#       lemmatise = "True"
#       lemmatise = "False"
#       subs_offset_ms = "0"
#       subs_offset_ms = "50"
# - If you don't want to a specify a value, just type two double quotes beside each other e.g.:
#       language = ""
#       word_exclude_spreadsheet = ""
# - If you are on Windows, any paths will need to have any backslashes replaces with a double backslash e.g.:
#       word_exclude_spreadsheet = "C:\\\\data\\\\exclude.xlsx"
#   Since this is easy to forget about, the tool will try to fix it for you. However, it's always best if it is correct to begin with!
#
# WARNING
# =======
# It is possible to break the tool by setting incorrect values in here.
# However, the script will attempt to fall back to sensible defaults if it can't read your values.
# If your setting appears to not be read by the tool, this is probably the reason!
# Run `gogadget set-defaults --factory` (without quotes) to reset this file if you run into errors or unexplained behaviour"""
    toml_general = """language and language_for_translations either be a valid two letter language code or be set to "". 
# Valid examples:
#       language = "en"
#       language = ""
# For a list of supported languages, please see the readme or run `gogadget list-languages` (without quotes)
#
# output_directory needs to be a valid folder on your system.
# You can use a dot "." if you want to use the current directory that you are running commands from.
# Windows paths need to have backslashes replaced with double backslashes, see [instructions] at the top of this file.
# The tool will try to fix it if you forget but it's best to get it correct to begin with!
# Valid examples:
#       output_directory = ""                         # No default, you will have to specify when running the command
#       output_directory = "."                        # The outputs of the command will be written to the current folder
#       output_directory = "immersion_videos"         # Outputs will be written to a sub folder called "immersion_videos"
#       output_directory = "C:\\\\immersion_videos\\\\"   # Outputs will be written to a specific folder on the C:\\ drive
"""
    toml_external = """These can be set to "" if you don't want to use them or want to specify them every time.
# Windows paths need to have backslashes replaced with double backslashes, see [instructions] at the top of this file.
# The tool will try to fix it if you forget but it's best to get it correct to begin with!
# Valid examples:
#       word_exclude_spreadsheet = "C:\\\\data\\\\exclude.xlsx"     # This will load a specific spreadsheet
#       word_exclude_spreadsheet = ""                           # Don't use an exclude spreadsheet or only use when specified in the command
"""
    toml_anki = """extract_media and include_words_with_no_definition should either be set to "True" or "False" and MUST be wrapped in quotes. 
# Valid examples:
#       extract_media = "True"
#       include_words_with_no_definition = "False"
#
# subs_offset_ms, subs_buffer_ms and max_cards_in_deck should be a number wrapped in quotes. 
# Valid examples:
#       subs_offset_ms = "0"
#       subs_buffer_ms = "50"
"""
    toml_lemmatiser = """All values should be set to "True" or "False" and MUST be wrapped in quotes.
# Valid examples:
#       lemmatise = "True"
#       lemmatise = "False"
"""
    toml_downloader = """These should either wrapped in quotes or set to double quotes to leave it blank. 
# Valid examples:
#       format = "best[ext=mp4]"
#       format = ""
"""
    toml_transcriber = """whisper_use_gpu should either be set to "True" or "False" and MUST be wrapped in quotes. 
# Valid examples:
#       whisper_use_gpu = "False"
#       whisper_use_gpu = "True"
#
# max_subtitle_length and subtitle_split_threshold should be a number wrapped in quotes. 
# Valid examples:
#       max_subtitle_length = "100"
#
# The other settings should be text wrapped in quotes or be set to "" if you want to specify them each time.
# These settings are best left alone unless you know what you are doing! Valid examples:
#       whisper_model = "small"
#       alignment_model = ""
"""


class SupportedLanguages:
    """Contains dictionaries of the supported languages for each function plus some explanation text"""

    common_explanation = "All features of the tool are available for the following languages. [b]If your language isn't listed[/], you can run [cyan bold]gogadget list-languages --detailed[/] to get a list of features that are supported by each language."
    whisper_explanation = "The transcriber (whisperX) supports the following languages fully. Languages not listed might work or might work with some manual configuration. However, basic functionality is available for over 100 languages! The transcriber is not required if you provide your own subtitle files."
    spacy_explanation = "The lemmatiser (spacy) supports the following languages. The tool will still work if your language is not available. However, the tool will not be able to lemmatise words or remove 'stop' words."
    argos_explanation = "The translator (argos) supports the following languages. The tool will still work if your language is not available. However, the tool will not be able to translate sentences."
    whisper_languages = {
        "ar": "Arabic",
        "ca": "Catalan",
        "zh": "Chinese",
        "hr": "Croatian",
        "cs": "Czech",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "fi": "Finnish",
        "fr": "French",
        "de": "German",
        "he": "Hebrew",
        "hi": "Hindi",
        "hu": "Hungarian",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "ml": "Malayalam",
        "el": "Greek",
        "no": "Norwegian",
        "nn": "Norwegian Nynorsk",
        "fa": "Persian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ru": "Russian",
        "sk": "Slovak",
        "sl": "Slovenian",
        "es": "Spanish",
        "te": "Telugu",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "vi": "Vietnamese",
    }

    spacy_languages = {
        "ca": "Catalan",
        "zh": "Chinese",
        "hr": "Croatian",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "fi": "Finnish",
        "fr": "French",
        "de": "German",
        "el": "Greek",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "lt": "Lithuanian",
        "mk": "Macedonian",
        "nb": "Norwegian Bokmål",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "sl": "Slovenian",
        "es": "Spanish",
        "sv": "Swedish",
        "uk": "Ukrainian",
    }

    argos_languages = {
        "sq": "Albanian",
        "ar": "Arabic",
        "az": "Azerbaijani",
        "eu": "Basque",
        "bn": "Bengali",
        "bg": "Bulgarian",
        "ca": "Catalan",
        "zh": "Chinese",
        "zt": "Chinese (traditional)",
        "cs": "Czech",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "eo": "Esperanto",
        "et": "Estonian",
        "fi": "Finnish",
        "fr": "French",
        "gl": "Galician",
        "de": "German",
        "el": "Greek",
        "he": "Hebrew",
        "hi": "Hindi",
        "hu": "Hungarian",
        "id": "Indonesian",
        "ga": "Irish",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "lv": "Latvian",
        "lt": "Lithuanian",
        "ms": "Malay",
        "nb": "Norwegian",
        "fa": "Persian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "sk": "Slovak",
        "sl": "Slovenian",
        "es": "Spanish",
        "sv": "Swedish",
        "tl": "Tagalog",
        "th": "Thai",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
    }

    @staticmethod
    def get_common_languages():
        """Works out the languages that are supported by all functions by combining dictionaries"""

        a = SupportedLanguages.spacy_languages
        b = SupportedLanguages.whisper_languages
        c = SupportedLanguages.argos_languages

        output_dict = {}

        for key, value in a.items():
            if (key in b) and (key in c):
                output_dict[key] = value

        return output_dict
