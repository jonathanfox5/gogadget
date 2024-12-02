<!-- Copyright: © 2024 Jonathan Fox
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Full source code: https://github.com/jonathanfox5/gogadget -->

## Why can't you include them for me?

Before we jump into where to get the resources, it's worth covering off why these resources aren't included by default.

Dictionaries, example word audio and exclude lists are not included by default with `gogadget` as I do not have the bandwidth to collect, test, maintain and distribute them for hundreds of different word pairings (I am one person working on this in their spare time). Since `gogadget` is purposefully designed to be [free software](../index.md/#why-is-gogadget-free) that is "offline only" where possible, you will need to bring your own rather than relying on an online service.

Although this is more tricky for you (as the user) to set up, I believe that the positives outweigh the negatives in this specific instance:

- This makes it highly customisable, allowing you to use your favourite resources.
- You can bring your own lists of known words, etc. that are personalised to you.
- Once you have the resources, they can't be taken away from you. There is no server to be shut down, company that will suddenly start charging for a previously "free" service, etc.
- I can't include copyrighted materials with `gogadget` unless their license explictly allows it (even if they are freely available). However, as a user of the tool, you can use any resources that you have permission to use.

## Specifying resources directly within the `gogadget anki-deck` command.

These files are used by `gogadget anki-deck` and they are specified the following arguments:

- `--dictionary` This should be a dictionary in `json` format. [Vocabsieve's documentation](https://docs.freelanguagetools.org/resources.html) is an excellent resource for finding one in your target language. The Migaku and Wiktionary ones are both very good if you want a bilingual dictionary. If the dictionary that you want isn't available in `json` format, [converters are available](https://duckduckgo.com/?q=stardict+to+json+converter).
- `--word-audio` This is should be a directory of `mp3` files with native pronunciations of individual words. [Vocabsieve's documentation](https://docs.freelanguagetools.org/resources.html) is, again, an excellent resource for these. I use both the Forvo and Lingua Libre ones that are linked in the Vocabsieve docs. The use of `mp3` (rather than any other audio format) is enforced by the tool due to compatibility issues with certain versions of Anki.

??? note "Tips for batch converting files"

    If you need to batch convert files to mp3, you can use any freely available converter. If you are on macOS or Linux (or are running bash on Windows), you already have everything that you need in order to do the conversion.

    This is an example bash command for batch converting all files in all subfolders from `ogg` to `mp3`. Just navigate to the folder containing them and paste in the following command into your terminal:

    ```sh
    find . -type f -name "*.ogg" -exec sh -c 'ffmpeg -i "$1" "${1%.*}.mp3" && rm "$1"' _ {} \;
    ```

    This is also theoretically possible using PowerShell on Windows. If anyone wants to write a **tested** PowerShell one-liner (plus usage instructions) that can just be pasted in by a non-tech savvy user on Windows, I'm willing to accept a [pull request](https://github.com/jonathanfox5/gogadget/pulls) for the documentation. Creating a formal command within `gogadget` is on the [feature to-do list](https://github.com/jonathanfox5/gogadget/issues/3) but is not currently my top priority item.

- `--excluded-words` is a spreadsheet with words that you don't want included in your Anki deck. This is useful to make sure that you aren't wasting time reviewing words that you already know. [Wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists) is a good source for frequency lists but you could also export your known words from Anki to get a more personalised experience. The only requirement is that the words that you want to filter out should be in column `A` of the spreadsheet though you can use multiple sub-sheets in the file if you wish to organise them. I've uploaded example exclude lists [here](https://github.com/jonathanfox5/gogadget/tree/main/examples/exclude_lists/).

## Specifying resources in the config files

You can specify resources in the configuration file so that they will be included every time that you run a command. If you need more help on using the configuration file, please see [here](../reference/default_settings.md).

You can access the configuration file by running:

```sh
gogadget set-defaults --custom
```

The lines that you need to change are below.

```toml
[external_resources]
# These can be set to "" if you don't want to use them or want to specify them every time.
# Windows paths need to have backslashes replaced with double backslashes, see [instructions] at the top of this file.
# The tool will try to fix it if you forget but it's best to get it correct to begin with!
# Valid examples:
#       word_exclude_spreadsheet = "C:\\data\\exclude.xlsx"     # This will load a specific spreadsheet
#       word_exclude_spreadsheet = ""                           # Don't use an exclude spreadsheet or only use when specified in the command

word_exclude_spreadsheet = "path here"
dictionary_file = "path here"
word_audio_directory = "path here"
```

**If** you have set a dictionary file I recommend changing the following setting to clean up the Anki deck by filtering out proper names and non-target language words: In the Anki section, change `include_words_with_no_definition` to `"False"`.

```toml
[anki]
include_words_with_no_definition = "False"
```

This isn't the default setting because, if you don't have a dictionary set, **you would end up with zero cards in your Anki deck**!
