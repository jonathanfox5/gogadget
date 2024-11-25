## Requirements for pull requests

Pull requests are welcome. Some basic requirements.

- All python code should be linted / formatted using [ruff](https://docs.astral.sh/ruff/). The [pyproject.toml](https://github.com/jonathanfox5/gogadget/blob/main/pyproject.toml) file in the repository contains project specific settings that should be automatically picked up by both the command line version and VSCode extension versions of ruff. The main requirements are 100 line length, 4 spaces as intent, import linting and double quotes.
- All code should be type checked by [mypy](https://www.mypy-lang.org). Support for `import-untyped` checking is disabled in [pyproject.toml](https://github.com/jonathanfox5/gogadget/blob/main/pyproject.toml) to avoid the need to generate stubs for third party libraries.

## Targets for testing for each release

- Windows 11 with CUDA
- Windows 11 without CUDA
- Windows 11 without any tools in path or python installed
- macOS: latest available release
- Linux: Ubuntu Server 24.04.1 LTS ARM (Oracle Cloud)

ARM based Windows is not officially supported and the installer only targets 64 bit x86. However, Windows ARM users can follow the custom installation steps if they wish.