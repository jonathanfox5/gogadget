
Please see the [Youtube Tutorial](#youtube-tutorial) for demonstrations of the features, including configuration for more advanced users.

## Download media

Download video from a website.

```sh
gogadget download --url "https://www.videosite.com/watch?v=videoid"
```

!!! note
    The commands `gogadget download-audio` and `gogadget download-subtitles` are also available.

## Generate subtitles

Automatically generate subtitles for a video / folder of videos that are in English (`en`):

```sh
gogadget transcribe --input "your folder or filename" --language en
```

!!! note "GPU Powered Transcription"
    If you have followed the steps in [the installation instructions](installation.md) to enable GPU transcription, add `--gpu` to the end of the command to use it.

## Create Anki Deck

Generate Anki cards from a full season of an Italian (`it`) program. Include images / audio on the cards, translate the sentences to the default language (English) and exclude the 1000 most common Italian words:

```sh
gogadget anki-deck --input "folder name" --language it --excluded-words "ita_top_1000_words.xlsx"
```

See [this section](getting_resources.md) for details on how to obtain dictionaries, exclude word spreadsheets and word audio to use with this command.

!!! note "Setting defaults to make using commands easier"
    You can set default parameters using `gogadget set-defaults --custom`. Once you have set up your defaults, this would allow you use this shortened version of the command:

    ```sh
    gogadget anki-deck --input "folder name"
    ```

    An example for setting defaults can be found [here](example_use_case.md).