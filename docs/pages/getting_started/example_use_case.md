## Preparing Priming Materials

The following example is my personal use case for producing priming materials prior to immersing in them. My target language is Italian (`it`) and my native language is English(`en`). I have downloaded a json dictionary, word audio and an exclude list as described in [Getting dictionary, word audio and exclude lists](../getting_started/getting_resources.md).

## Setting Defaults

As a "one off" task, I set up my default settings by running `gogadget set-defaults --custom`. I changed the following settings from the defaults. [the defaults are set for the widest compatibility, not for a specific workflow]

```toml
[general]
# Changed language to target language (mine is Italian)
language = "it"
language_for_translations = "en"
output_directory = "."

[external_resources]
# Set the paths of the resources on my hard drive
# Since this is the configuration for my windows pc, I need to replace backslashes with double backslashes
# The tool *should* fix it if I only typed single backslashes but it's best to get it correct to begin with!
word_exclude_spreadsheet = "C:\\languages\\it\\ita_exclude.xlsx"
dictionary_file = "C:\\languages\\it\\it_to_en.json"
word_audio_directory = "C:\\languages\\it\\word_audio"

[anki]
# Changed the `include_words_with_no_definition` to False. By filtering out words not in the dictionary, this has the effect of filtering out proper nouns and non-target language words
# The reason why this is not default behaviour is that it would cause Anki decks to have no cards if the user hasn't set a dictionary
extract_media = "True"
include_words_with_no_definition = "False"
subs_offset_ms = "0"
subs_buffer_ms = "50"
max_cards_in_deck = "100"

[lemmatiser]
# Keep the settings in here as default but might be useful to tweak them for other languages
lemmatise = "True"
filter_out_non_alpha = "True"
filter_out_stop_words = "True"
convert_input_to_lower = "True"
convert_output_to_lower = "True"
return_just_first_word_of_lemma = "True"

[downloader]
# I keep subtitle_language blank as I prefer to generate my own using `gogadget transcribe`
advanced_options = ""
format = ""
subtitle_language = ""

[transcriber]
# I have changed `whisper_use_gpu` to "True" on my windows PC which has an Nvidia GPU. This massively speeds up transcription but it does require a GPU that can run CUDA
whisper_model = "deepdml/faster-whisper-large-v3-turbo-ct2"
alignment_model = ""
subtitle_format = "vtt"
max_subtitle_length = "94"
subtitle_split_threshold = "70"
whisper_use_gpu = "True"
```

Now that these parameters are set, they no longer need to be specified in the commands.

## Running Commands

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
