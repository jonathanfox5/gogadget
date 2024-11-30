<!-- Copyright: © 2024 Jonathan Fox
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Full source code: https://github.com/jonathanfox5/gogadget -->

# Installation

## Windows

Installation instructions for Windows:

1. Download the latest version of the gogadget installer from [this page](https://github.com/jonathanfox5/gogadget/releases).

2. Run the installer. It's highly recommended that you accept all of the default settings unless you know what you are doing!

3. You can run gogadget from the desktop shortcut, from the start menu or by right clicking inside a folder and selecting "Open gogadget here".

4. _[Optional]_ You can install all of the models required for your chosen language. Type the following to get the instructions:

   ```sh
   gogadget install
   ```

!!! note "GPU Powered Transcription"

    If you want to enable GPU transcription of subtitles, please tick the "CUDA" checkbox in the installer. For more information, please see [here](#enabling-gpu-powered-transcription).

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
   uv tool install gogadget --python 3.12 --upgrade
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

2. Install required packages (if you don't already have them) using your package manager. This will depend on your distribution. For example:

   - Ubuntu based distributions: `sudo apt install ffmpeg build-essential python3-dev`
   - Fedora based distributions: `sudo dnf install ffmpeg @development-tools python3-devel`
   - Arch based distributions: `sudo pacman -S ffmpeg base-devel`

3. Configure your paths if they aren't already set up:

   ```sh
   source $HOME/.local/bin/env
   ```

4. Install gogadget using uv. Note that we are using Python 3.10 instead of Python 3.12 that the other platforms are using. This is to ensure that all dependencies build correctly on ARM CPUs.

   ```sh
   uv tool install gogadget --python 3.10 --upgrade
   ```

5. You can then run the tool by typing the following command into your terminal:

   ```sh
   gogadget
   ```

6. _[Optional]_ You can install all of the models required for your chosen language. Type the following to get the instructions:

   ```sh
   gogadget install
   ```

!!! note "GPU Powered Transcription"

    _[Optional]_ If you wish to use your GPU instead of your CPU and you have CUDA installed and configured on your system.

    **AFTER** you run:

    ```sh
    uv tool install gogadget --python 3.10 --upgrade
    ```

    You can **THEN** run:

    ```sh
    uv tool install gogadget --python 3.10 --with 'torch==2.5.1+cu124' --with 'torchaudio==2.5.1+cu124' --index 'https://download.pytorch.org/whl/cu124'
    ```

    Note that **BOTH** commands are required, in this order!

    For more information, please see [here](#enabling-gpu-powered-transcription).

## Enabling GPU powered transcription

### Requirements

To enable GPU powered transcription of subtitles, you will need:

- A CUDA enabled NVIDIA gpu with a decent amount of VRAM (>=8 GB)
- Windows or Linux
- Up to date GPU drivers installed

These requirements are the same for most Whisper based transcription tools. Therefore, there will be plenty of guides to help you if you get stuck!

If you are using **Windows**, you will need to make sure that you tick "CUDA" in the installer.

If you are running **Linux** or are **manually** configuring it on Windows, you will need to follow the final step of the [Linux](#linux) installation instructions.

!!! note "Troubleshooting: CUDA Toolkit"

    On most systems, there should be no need to install the CUDA toolkit as it the required runtimes should be provided by your drivers. However, you may wish to try installing the toolkit manually if you run into any problems: <https://developer.nvidia.com/cuda-toolkit>

### Running with GPU enabled

You will need to specify `--gpu` when running any transcription tasks e.g.:

```sh
gogadget transcribe -i "input file or folder" -l "code for your language" --gpu
```

Alternatively, you can change the value of `whisper_use_gpu` in the settings file to `"True"`. You can access the settings by running:

```sh
gogadget set-defaults --custom
```

## Custom installation notes

You should ignore this section if you are using the installation instructions for Windows, macOS or Linux. This is only to help anyone doing their own custom installation.

Notes on Python version:

- The tool is currently compatible with Python `3.10`, `3.11` and `3.12`. On some platforms, some dependencies have issues when you build them on newer python versions so its generally safest to install `3.10`.
- `3.13` is **not** supported as the dependencies `ctranslate2` and `torch` do not currently provide compatible packages.
- If you manually install gogadget and you get errors about either of these packages, a Python version issue is probably the cause.

You may get some ideas for custom installations from my [script](https://github.com/jonathanfox5/gogadget/blob/main/install/linux_test_install.sh) that I use to test on clean installs of linux.

!!! note "Building from source"

    If you are doing a custom installation, you may find the developer documentation on [building the project from source](../developer/building.md) helpful.
