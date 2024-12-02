<!-- Copyright: © 2024 Jonathan Fox
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Full source code: https://github.com/jonathanfox5/gogadget -->

<h1 align="center">
  <a href="https://gogadget.jfox.io"><img src="img/header.svg" alt="gogadget" style="max-width: 1000px; width: 90%; height: auto" /></a>
  <br>
  Language Learning Toolkit
  <br>
  <a href="https://github.com/jonathanfox5/gogadget/releases"><img src="https://img.shields.io/github/v/tag/jonathanfox5/gogadget?label=download&color=blue" alt="Download" /></a>
  <a href="https://gogadget.jfox.io"><img src="https://img.shields.io/badge/view-documentation-brightgreen" alt="Documentation" /></a>
  <a href="https://pypi.org/project/gogadget/"><img src="https://img.shields.io/pypi/v/gogadget?color=%23BA55D3" alt="PyPI" /></a>
</h1>

## Overview

`gogadget` is a toolkit for producing immersion and priming materials for language learning.

- It tries to solve the problem that many of the most powerful tools available are hard to install, difficult to use or require lots of effort to configure for optimal results.
- It is capable of downloading audio and video files, automatically transcribing subtitles from videos and podcasts, and automatically producing filtered Anki decks with sentence audio / translations / screenshots / definitions.

## Video tutorial

--8<-- "docs/pages/getting_started/video_tutorial.md"

## Useful links

- [Installation instructions](getting_started/installation.md)
- [Example commands](getting_started/example_commands.md)
- [Detailed command reference](reference/command_reference.md)
- [Video tutorial](getting_started/video_tutorial.md)
- [Getting help with problems](misc/getting_help.md)

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
- [One click installer](https://github.com/jonathanfox5/gogadget/releases/) for Windows and [simple installation steps](getting_started/installation.md) for macOS and Linux.
- Ability to save defaults so that commands can be kept as short and memorable as possible.
- It supports 19 [languages](getting_started/supported_languages.md) fully with partial support for many more.
- Once you have installed the resources for your language, all modules apart from `gogadget download` are fully offline. This makes it useful for travelling or for processing personal conversations as there is no server involved.

## Why is `gogadget` free?

`gogadget` is [free software](https://www.gnu.org/philosophy/free-sw.html), both in terms of "free beer" and "freedom".

You can therefore run the program as you wish, for any purpose, provided that you comply with the terms of the license ([AGPLv3-or-later](https://github.com/jonathanfox5/gogadget/blob/main/LICENSE)). This means that, theoretically, you could even modify it and distribute your own version (even though I would personally _**much**_ rather that you submit a [pull request](https://github.com/jonathanfox5/gogadget/pulls) to improve this version!) The main practical restriction of AGPLv3 is that you need to license your version under these same terms, including making your source code available to your users so that everyone can benefit from it.

Why free:

1. I have greatly benefited from other pieces of free software such as the incredible [Anki](https://apps.ankiweb.net). It therefore only feels right to give back in the same manner.
2. There are far too many pieces of software that try to lock you in, force subscriptions on you, steal your data, etc. I didn't want to create another one!
3. I don't run any servers for the application so the only real cost is my time. Therefore, I don't need to charge.
4. I hope that this can be a platform that others can build upon and therefore continue the cycle of creating high quality tools that anyone can use and tweak.

## Acknowledgements

--8<-- "docs/pages/license_info/acknowledgements.md"

`LICENSE` files for each of the python dependencies will be included with the installation. For convenience, you can view an auto-generated table of each of the licenses and authors [here](license_info/full_license_info.md).
