# Building

## Required packages

[Poetry](https://python-poetry.org) is used to build the packages, the installers use [uv](https://docs.astral.sh/uv/) to run the tool in its own virtual environment and the only non-Python dependency is [ffmpeg](https://ffmpeg.org). [Innosetup](https://jrsoftware.org/isinfo.php) is used to build the Windows installer.

## Settings things up

Assumes building on Windows. If you are building on mac / linux, just skip the innosetup related steps.

1. Set version number in [pyproject.toml](pyproject.toml)
2. Set version number in [install/gogadget_windows.iss](install/gogadget_windows.iss)
3. Make sure `poetry` and `innosetup` are installed and in path. (innosetup isn't by default, need to add the root innosetup directory in program files)
4. Download latest windows builds of ffmpeg and uv and put the binaries directly in [install/bin/](install/bin/)

## Build commands

(these are in bash, convert them to whatever shell you are using)

```sh
# Clear out any wheels and existing installers that we have
rm dist/*
rm install/bin/*.whl

# Build new wheel and copy to bin folder
poetry build
cp dist/*.whl install/bin/

# Build windows installer and move to dist folder
iscc install/gogadget_windows.iss
mv install/output/*.exe dist/

# Step just for people called "Jonathan Fox" ;) Updates pypi index.
poetry publish
```

## Targets for testing for each release

- Windows 11 with CUDA
- Windows 11 without CUDA
- Windows 11 without any tools in path or python installed
- macOS (latest available release)
- Ubuntu Server 24.04.1 LTS (primarily because I don't have a linux desktop machine and a large proportion of desktop linux is Ubuntu)

ARM based Windows is not officially supported and the installer only targets 64 bit x86. However, Windows ARM users can follow the custom installation steps if they wish.

# Running from source

First, please note the package requirements at the top of this document.

To download and run the code from source, run the following commands:

```sh
# Download the repo and enter it
git clone https://github.com/jonathanfox5/gogadget
cd gogadget

# Create the virtual environment and install packages
poetry install

# Enter the virtual environment
poetry shell

# Run the tool
gogadget
```

# Requirements for pull requests

Pull requests are welcome. Some basic requirements.

- All python code should be linted / formatted using [ruff](https://docs.astral.sh/ruff/). The `pyproject.toml` file in the repository contains project specific settings that should be automatically picked up by both the command line version and VSCode extension versions of ruff. The main requirements are 100 line length, 4 spaces as intent, import linting and double quotes.
- All code should be type checked by [mypy](https://www.mypy-lang.org). Support for `import-untyped` checking is disabled in `pyproject.toml` to avoid the need to generate stubs for third party libraries.
