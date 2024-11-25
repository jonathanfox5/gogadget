## Requirements for pull requests

Pull requests are welcome. Some basic requirements.

- All python code should be linted / formatted using [ruff](https://docs.astral.sh/ruff/). The [pyproject.toml](https://github.com/jonathanfox5/gogadget/blob/main/pyproject.toml) file in the repository contains project specific settings that should be automatically picked up by both the command line version and VSCode extension versions of ruff. The main requirements are 100 line length, 4 spaces as intent, import linting and double quotes.
- All code should be type checked by [mypy](https://www.mypy-lang.org). Support for `import-untyped` checking is disabled in [pyproject.toml](https://github.com/jonathanfox5/gogadget/blob/main/pyproject.toml) to avoid the need to generate stubs for third party libraries.

## Documentation

The documentation uses mkdocs-material. You can install it with uv:

```sh
uv tool install mkdocs --with mkdocs-glightbox --with mkdocs-material --with mdx-truly-sane-lists --with mkdocs-minify-plugin
```

If you are in the root of the git repository, you can then run the following to run a test server:

```sh
mkdocs serve -f docs/mkdocs.yml
```

There is a github action that rebuilds the documentation on each commit.

## Targets for testing for each release

- Windows 11 with CUDA
- Windows 11 without CUDA
- Windows 11 without any tools in path or python installed
- macOS: latest available release
- Linux: Ubuntu Server 24.04.1 LTS ARM (Oracle Cloud)

ARM based Windows is not officially supported and the installer only targets 64 bit x86. However, Windows ARM users can follow the custom installation steps if they wish.
