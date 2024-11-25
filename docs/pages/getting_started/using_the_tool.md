## Understanding Commands

The intended behaviour is that the tool itself will guide the user on how to use it. If you type `gogadget` in a command prompt or terminal window, you will get:

![Main menu](https://github.com/jonathanfox5/gogadget/raw/main/examples/readme_images/main_menu.png)

All commands are listed in the `Primary Functions` box and have their own documentation. Each command has parameters associated with it. These can be listed by just typing `gogadget` then the name of the command that you are interested in. For example, `gogadget download` produces:

![Download Help Text](https://github.com/jonathanfox5/gogadget/raw/main/examples/readme_images/download_help.png)

You will see from the output of that command that you can just run the following to download a video:

```sh
gogadget download --url "https://www.videosite.com/watch?v=videoid"
```

Several commands use a standardised two letter code to identify languages (e.g. English is `en`, Italian is `it`, Japanese is `ja`, etc.) To get a list of supported languages and the associated two letter codes, run this command:

```sh
gogadget list-languages
```

Alternatively, a list is available by clicking [here](supported_languages.md).

## Configuration

It's recommended, but not required, that you fully install the models for the languages that you are interested in. e.g. To install Italian (target language) with English (native language) translations, run:

```sh
gogadget install --language it --translation-language en
```

You can also configure defaults so that you don't need to specify as many parameters each time you run your commands:

```sh
gogadget set-defaults --custom
```

An example for setting defaults can be found [here](example_use_case.md).

## Short Names

All parameters in all commands have both a "standard" form and a "short" form. You can use whatever works best for you! The following two lines are equivalent.

```sh
gogadget download --url "https://www.videosite.com/watch?v=videoid" --output "immersion videos" --subtitle-language en
gogadget download -i "https://www.videosite.com/watch?v=videoid" -o "immersion videos" -l en
```

Note: Regardless of the "standard" name, all commands follow the same logic for their "short" names. The item that is being used as input is `-i`, the output is `-o` and the language is `-l`. Normally you don't need any more than this!
