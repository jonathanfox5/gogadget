@echo off

echo Copyright: © 2024 Jonathan Fox
echo License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
echo Full source code: https://github.com/jonathanfox5/gogadget
echo.
echo ~~~ To list all commands, type gogadget then press enter ~~~
echo ~~~ Some useful commands ~~~
echo 1. Get list of two letter language codes to use in the commands
echo      gogadget list-languages
echo 2. Install the required files for your language and the language that you want to translate to (your native language)
echo      gogadget install --language "two letter code" --translation-language "two letter code"
echo 3. Download a video / download just the audio / download just the subtitles
echo      gogadget download --url "url of the video or playlist"
echo      gogadget download-audio --url "url of the video or playlist"
echo      gogadget download-subtitles --url "url of the video or playlist" --subtitle-language "two letter code"
echo 4. Generate subtitles for a video or audio file
echo      gogadget transcribe --input "file or folder with your file(s)" --language "two letter code"
echo 5. Generate a simple Anki deck (more complex options listed by running gogadget anki-deck)
echo      gogadget anki-deck --input "file or folder with your file(s)" --language "two letter code"
echo 6. Set your default file names, folders and command settings so that you don't need to run them every time
echo      gogadget set-defaults --custom
echo.
echo ~~~ You can view additional options and examples for every command by running it without any inputs ~~~
echo Examples:
echo      gogadget
echo      gogadget anki-deck
echo      gogadget download
echo      gogadget transcribe
echo      gogadget install
echo      gogadget set-defaults
echo      etc.
echo.

powershell.exe -noexit -nologo
