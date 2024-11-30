<!-- Copyright: © 2024 Jonathan Fox
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Full source code: https://github.com/jonathanfox5/gogadget -->

# Getting dictionary, word audio and exclude lists

`gogadget anki-deck` accepts the following arguments:

- `--dictionary` This should be a dictionary in json format. [Vocabsieve's documentation](https://docs.freelanguagetools.org/resources.html) is an excellent resource for finding one in your target language. I personally use the Migaku `Vicon_Ita_to_Eng_Dictionary.json` that is linked in the Vocabsieve docs. The Wiktionary ones are also very good.
- `--word-audio` This is should be a directory of `mp3` files with native pronunciations of individual words. [Vocabsieve's documentation](https://docs.freelanguagetools.org/resources.html) is, again, an excellent resource for these. I use both the Forvo and Lingua Libre ones that are linked in the Vocabsieve docs. The use of `mp3` (rather than any other audio format) is enforced by the tool due to compatibility issues with certain versions of Anki. If you are on macOS or Linux then you can use FFMPEG to batch convert from `ogg` to `mp3`.

  ```sh
   find . -type f -name "*.ogg" -exec sh -c 'ffmpeg -i "$1" "${1%.*}.mp3" && rm "$1"' _ {} \;
  ```

- `--excluded-words` is a spreadsheet with words that you don't want included in your deck. This is useful to make sure that you aren't wasting time reviewing words that you already know. [Wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists) is a good source for frequency lists but you could also export your known words from Anki to get a more personalised experience. The only requirement is that the words that you want to filter out should be in column `A` of the spreadsheet though you can use multiple sub-sheets in the file if you wish to organise them. I've uploaded example exclude lists [here](https://github.com/jonathanfox5/gogadget/tree/main/examples/exclude_lists/).
