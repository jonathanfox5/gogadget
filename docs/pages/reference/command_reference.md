<!-- Copyright: © 2024 Jonathan Fox
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Full source code: https://github.com/jonathanfox5/gogadget -->

# `gogadget`

**Usage**:

```console
$ gogadget [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--version`: Display application version.
- `--help`: Show this message and exit.

**Commands**:

- `anki-deck`: Build an Anki deck using the most common...
- `download`: Download a video or playlist from a...
- `download-audio`: Download a video or playlist from a...
- `download-subtitles`: Download subtitles from an online video...
- `frequency-analysis`: Produce a frequency analysis of the most...
- `transcribe`: Produce subtitle file(s) from audio or...
- `install`: Download models for a given --language and...
- `list-languages`: Display languages supported by the tool.
- `set-defaults`: Configure your default paths so that don&#x27;t...
- `update-downloader`: Update the downloader to use the latest...

## `gogadget anki-deck`

Build an Anki deck using the most common vocabulary in a subtitles file or a folder of subtitles. Optionally include audio and / or screenshots from the source media file(s).

<span style="color: #ffffff; text-decoration-color: #ffffff">If you use this regularly, it&#x27;s highly recommended to set the default paths to your dictionary, excluded words, etc. and preferred processing options to simplify the process.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff">You can set your defaults using the following command: </span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget set-defaults --custom</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Normal usage using standard names where your target language is italian and your native language is English.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget anki-deck --input &quot;folder containing subtitles and media files&quot; --language it --translation-language en</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. As per (1) but uses dictionary, word exclude list and word audio bank. Also uses --exclude-no-definition to filter out proper nouns / non-target language words.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget anki-deck --input &quot;folder containing subtitles and media files&quot; --language it --translation-language en --dictionary &quot;dictionary.json&quot; --word_audio &quot;folder_name&quot; --excluded-words &quot;excel_name.xlsx&quot; --exclude-no-definition</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">3. Equivalent of (2) using short names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget anki-deck -i &quot;folder containing subtitles and media files&quot; -l it -t en -d &quot;dictionary.json&quot; -w &quot;folder_name&quot; -e &quot;excel_name.xlsx&quot; -h</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">4. If you have set all of your defaults as described above, you can just run.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget anki-deck -i &quot;folder containing subtitles and media files&quot;</span>

**Usage**:

```console
$ gogadget anki-deck [OPTIONS]
```

**Options**:

- `-i, --input PATH`: Directory (folder) containing the video file(s) and subtitle files(s) to be turned into an Anki deck. [required]
- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (for English), <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> (for Spanish) or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span> (Italian). Run <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget list-languages</span> for a list of supported languages. [default: it]
- `-t, --translation-language TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Language to use for translations. Translation quality is generally best if either the target language or the translation is set to <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (English). This should be a two letter language code, e.g. <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (for English), <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> (for Spanish) or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span> (Italian). Run <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget list-languages</span> for a list of supported languages. [default: en]
- `-f, --offset INTEGER`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Time, in milliseconds, to offset the subtitles by when extracting audio. Not normally required if subtitles were generated by <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget transcribe</span>. [default: 0]
- `-b, --buffer INTEGER`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Extra time, in milliseconds, to add to the extracted audio to avoid it being cut off. Not normally required if subtitles were generated by <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget transcribe</span>. [default: 50]
- `-x, --max-cards INTEGER`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Maximum number of cards to include in the deck. [default: 100]
- `-w, --word-audio PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Directory of mp3 files of individual words to include in the Anki cards. [default: /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Audio]
- `-d, --dictionary PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Dictionary in json format to retrieve definitions from for the Anki cards. [default: /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Dictionaries/Migaku/Vicon_Ita_to_Eng_Dictionary.json]
- `-e, --excluded-words PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Spreadsheet containing words to exclude from the analysis (e.g. the most common words in a language, words already learned). Words should be in the first column of the spreadsheet but can be split across multiple sub-sheets within the file. [default: /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Frequency_lists/ita_exclude.xlsx]
- `-m, --lemma / -n, --no-lemma`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Enable or disable lemmatisation. If supported for your language, this is generally recommended. [default: lemma]
- `-s, --stop-words / -p, --no-stop-words`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> If lemmatisation is enabled, you can include or exclude stop words. Stop words are short &#x27;function&#x27; words such as &#x27;the&#x27;, &#x27;that&#x27;, &#x27;which&#x27;, etc. [default: no-stop-words]
- `-q, --media / -r, --no-media`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Media to extract sentence audio and screenshots from to display on the Anki card. This can either be a video or audio only source. [default: media]
- `-g, --include-no-definition / -h, --exclude-no-definition`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Include cards where the definition can&#x27;t be found in the dictionary. Setting --exclude-no-definition may improve the quality of the deck as it will likely filter many proper nouns, words not from the target language, etc. [default: exclude-no-definition]
- `--help`: Show this message and exit.

## `gogadget download`

Download a video or playlist from a website URL.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Normal usage using standard names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download --url &quot;https://www.videosite.com/watch?v=videoid&quot;</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. More advanced usage using standard names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download --url &quot;https://www.videosite.com/watch?v=videoid&quot; --output &quot;immersion videos&quot; --subtitle_language en --format &quot;best&quot;</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">3. Equivalent of (2) using short names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download -i &quot;https://www.videosite.com/watch?v=videoid&quot; -o &quot;immersion videos&quot; -l en -f &quot;best&quot;</span>

**Usage**:

```console
$ gogadget download [OPTIONS]
```

**Options**:

- `-i, --url TEXT`: URL of the video or playlist. Supports any website supported by <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md">yt-dlp</a></span>. [required]
- `-o, --output PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from. [default: .]
- `-f, --format TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Specify the format of the video. Accepts <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#format-selection">yt-dlp&#x27;s format options</a></span>.
- `-l, --subtitle-language TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Language of subtitles to download. If you want to download these, you should enter a two letter language code such as <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span>, <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span>. It will try to download manual subtitles first and fallback to automatically generated subtitles if these aren&#x27;t found.
- `-a, --advanced-options TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span><span style="color: #800000; text-decoration-color: #800000">[Advanced]</span> Custom yt-dlp options, should accept any command line arguments on the <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp">github page</a></span>. Please format these as a string, enclosed by quotes.
- `--help`: Show this message and exit.

## `gogadget download-audio`

Download a video or playlist from a website URL and convert it to an audio file.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Normal usage using standard names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download-audio --url &quot;https://www.videosite.com/watch?v=videoid&quot;</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. More advanced usage using standard names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download-audio --url &quot;https://www.videosite.com/watch?v=videoid&quot; --output &quot;immersion videos&quot;</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">3. Equivalent of (2) using short names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download-audio -i &quot;https://www.videosite.com/watch?v=videoid&quot; -o &quot;immersion videos&quot;</span>

**Usage**:

```console
$ gogadget download-audio [OPTIONS]
```

**Options**:

- `-i, --url TEXT`: URL of the video or playlist. Supports any website supported by <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md">yt-dlp</a></span>. [required]
- `-o, --output PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from. [default: .]
- `-a, --advanced-options TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span><span style="color: #800000; text-decoration-color: #800000">[Advanced]</span> Custom yt-dlp options, should accept any command line arguments on the <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp">github page</a></span>. Please format these as a string, enclosed by quotes.
- `--help`: Show this message and exit.

## `gogadget download-subtitles`

Download subtitles from an online video service.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Download english subtitles for a given video.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download-subtitles --url &quot;https://www.videosite.com/watch?v=videoid&quot; --subtitle-language en</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. Equivalent of (1) using short names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget download-subtitles -i &quot;https://www.videosite.com/watch?v=videoid&quot; -l en</span>

**Usage**:

```console
$ gogadget download-subtitles [OPTIONS]
```

**Options**:

- `-i, --url TEXT`: URL of the video or playlist. Supports any website supported by <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md">yt-dlp</a></span>. [required]
- `-l, --subtitle-language TEXT`: Language of subtitles to download. You should enter a two letter language code such as <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span>, <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span>. It will try to download manual subtitles first and fallback to automatically generated subtitles if these aren&#x27;t found.
- `-o, --output PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from. [default: .]
- `-a, --advanced-options TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span><span style="color: #800000; text-decoration-color: #800000">[Advanced]</span> Custom yt-dlp options, should accept any command line arguments on the <span style="color: #000080; text-decoration-color: #000080; text-decoration: underline"><a href="https://github.com/yt-dlp/yt-dlp">github page</a></span>. Please format these as a string, enclosed by quotes.
- `--help`: Show this message and exit.

## `gogadget frequency-analysis`

Produce a frequency analysis of the most common vocabulary in a subtitles file or a folder of subtitles. Useful for priming, also used as a pre-processing stage for some other functions.

<span style="color: #ffffff; text-decoration-color: #ffffff">If you use this regularly, it&#x27;s highly recommended to set the default paths to your excluded words and preferred processing options to simplify the process.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff">You can set your defaults using the following command: </span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget set-defaults --custom</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Normal usage using standard names where your target language is italian.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget frequency-analysis --input &quot;folder containing subtitles&quot; --language it</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. As per (1) but uses word exclude list.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget frequency-analysis --input &quot;folder containing subtitles&quot; --language it --excluded-words &quot;excel_name.xlsx&quot;</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">3. Equivalent of (2) using short names.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget frequency-analysis -i &quot;folder containing subtitles&quot; -l it -e &quot;excel_name.xlsx&quot;</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">4. If you have set all of your defaults as described above, you can just run.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget frequency-analysis -i &quot;folder containing subtitles&quot;</span>

**Usage**:

```console
$ gogadget frequency-analysis [OPTIONS]
```

**Options**:

- `-i, --input PATH`: Directory (folder) containing the subtitle files(s) to be analysed. [required]
- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (for English), <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> (for Spanish) or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span> (Italian). Run <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget list-languages</span> for a list of supported languages. [default: it]
- `-o, --output PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from. [default: .]
- `-e, --excluded-words PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Spreadsheet containing words to exclude from the analysis (e.g. the most common words in a language, words already learned). Words should be in the first column of the spreadsheet but can be split across multiple sub-sheets within the file. [default: /Users/jonathan/Library/Mobile Documents/com~apple~CloudDocs/Italian/Dictionaries/Frequency_lists/ita_exclude.xlsx]
- `-m, --lemma / -n, --no-lemma`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Enable or disable lemmatisation. If supported for your language, this is generally recommended. [default: lemma]
- `-s, --stop-words / -p, --no-stop-words`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> If lemmatisation is enabled, you can include or exclude stop words. Stop words are short &#x27;function&#x27; words such as &#x27;the&#x27;, &#x27;that&#x27;, &#x27;which&#x27;, etc. [default: no-stop-words]
- `--help`: Show this message and exit.

## `gogadget transcribe`

Produce subtitle file(s) from audio or video using whisperX.

<span style="color: #ffffff; text-decoration-color: #ffffff">--input and -i accept both files and directories of files.</span>

<span style="color: #ffffff; text-decoration-color: #ffffff">If you have an NVIDIA GPU that is set up for CUDA, it&#x27;s strongly recommended to pass the --gpu flag as this significantly speeds up the tool.</span>

<span style="color: #ffffff; text-decoration-color: #ffffff">You can also reduce runtime (at the expense of accuracy) by specifying --whisper-model small</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Transcribe a media file or folder of media files that is in English.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget transcribe --input &quot;path to media file or folder containing media files&quot; --language en</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. As per (1) but using the GPU to process the model.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget transcribe --input &quot;path to media file or folder containing media files&quot; --language en --gpu</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">3. Example using short names where the output folder is also specified.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget transcribe -i &quot;path to media file or folder containing media files&quot; -o &quot;folder to save to&quot; -l en -g</span>

**Usage**:

```console
$ gogadget transcribe [OPTIONS]
```

**Options**:

- `-i, --input PATH`: Path to the video or audio file to transcribe. This can be either a specific video / audio file or a folder of files. [required]
- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (for English), <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> (for Spanish) or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span> (Italian). Run <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget list-languages</span> for a list of supported languages. [default: it]
- `-o, --output PATH`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Directory (aka folder) to save the files to. Defaults to the current working directory where the user is running the script from. [default: .]
- `-m, --max-length INTEGER`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> The absolute maximum length that a subtitle can be. [default: 94]
- `-s, --split-length INTEGER`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> The length at which the tool considers splitting a subtitle. [default: 70]
- `-w, --whisper-model TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Specify the whisper model to use for transcription. By default, this is large-v3 turbo but setting this to <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">small</span> can significantly speed the process up at the cost of accuracy. [default: deepdml/faster-whisper-large-v3-turbo-ct2]
- `-a, --align-model TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Specify the model from hugging face to use to align the subtitles with the audio. For the most common languages, the tool will find this for you.
- `-g, --gpu / -c, --cpu`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> You can specify --gpu if you have a CUDA enabled Nvidia graphics card to significantly speed up the processing. [default: cpu]
- `-f, --subtitle-format TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> File format for the subtitles. You can specify vtt, srt, json, txt, tsv or aud. Vtt is the preferred format of the other tools in this suite. [default: vtt]
- `--help`: Show this message and exit.

## `gogadget install`

Download models for a given --language and initialises tools.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Install modules to process Italian and produce English translations.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget install --language it --translation-language en</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. To get a list of language codes to use in the command, run:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget list-languages</span>

**Usage**:

```console
$ gogadget install [OPTIONS]
```

**Options**:

- `-l, --language TEXT`: Language to use for processing. This should be a two letter language code, e.g. <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (for English), <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> (for Spanish) or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span> (Italian). Run <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget list-languages</span> for a list of supported languages. [default: it]
- `-t, --translation-language TEXT`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Language to use for translations. Translation quality is generally best if either the target language or the translation is set to <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (English). This should be a two letter language code, e.g. <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">en</span> (for English), <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">es</span> (for Spanish) or <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">it</span> (Italian). Run <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">gogadget list-languages</span> for a list of supported languages. [default: en]
- `--help`: Show this message and exit.

## `gogadget list-languages`

Display languages supported by the tool.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. List languages supported by all functions of the tool.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget list-languages</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. List languages supported or partially supported by each module.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget list-languages --detailed</span>

**Usage**:

```console
$ gogadget list-languages [OPTIONS]
```

**Options**:

- `-a, --detailed`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> List the languages supported by each module of the tool.
- `--help`: Show this message and exit.

## `gogadget set-defaults`

Configure your default paths so that don&#x27;t need to specify them each time.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Open the settings file on your folder in your default text editor.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget set-defaults --custom</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">2. Reset to factory defaults.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget set-defaults --factory</span>

<span style="color: #800000; text-decoration-color: #800000; font-weight: bold; font-style: italic">~~~~ WARNING ~~~~ It is possible to break the tool by setting incorrect values in the config file.</span>
<span style="color: #800000; text-decoration-color: #800000; font-weight: bold; font-style: italic">Reset to factory defaults if you experience errors or unexpected behaviour.</span>

**Usage**:

```console
$ gogadget set-defaults [OPTIONS]
```

**Options**:

- `-f, --factory`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Load factory default settings. These settings are chosen to be compatible with most systems and languages with minimal tweaking.
- `-c, --custom`: <span style="color: #008080; text-decoration-color: #008080">[Optional]</span> Set custom settings in a text file. Useful for setting default paths to resources.
- `--help`: Show this message and exit.

## `gogadget update-downloader`

Update the downloader to use the latest version of yt-dlp.

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic; text-decoration: underline">Examples:</span>

<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">1. Update downloader.</span>
<span style="color: #ffffff; text-decoration-color: #ffffff; font-style: italic">gogadget update-downloader</span>

**Usage**:

```console
$ gogadget update-downloader [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.
