## Github actions

On every commit:

- There is a github action that rebuilds the documentation website on each commit.

On tag commits:

- The python wheel will be
  - Built
  - Uploaded to PyPi & TestPyPi
  - Signed and added to a new Github release

## Manual build

### Required packages

[`uv`](https://docs.astral.sh/uv/) is used to build the packages and [`Innosetup`](https://jrsoftware.org/isinfo.php) is used to build the Windows installer.

The installers use [`uv`](https://docs.astral.sh/uv/) to run the tool in its own virtual environment and the only non-Python runtime dependency is [`ffmpeg`](https://ffmpeg.org).

### Settings things up

The following assumes building on Windows so that the Windows installer can be created in addition to the multi-platform wheel. If you are building on mac / linux, just skip the innosetup related steps.

1. Set version number in [pyproject.toml](https://github.com/jonathanfox5/gogadget/blob/main/pyproject.toml)
2. Set version number in [install/gogadget_windows.iss](https://github.com/jonathanfox5/gogadget/blob/main/install/gogadget_windows.iss)
3. Make sure `uv` and `innosetup` are installed and in path. (innosetup isn't by default, you will need to add the root innosetup directory that is located in program files)
4. Download latest windows builds of `ffmpeg` and `uv` and put the binaries directly in [install/bin/](https://github.com/jonathanfox5/gogadget/tree/main/install/bin/)

### Build commands (Windows)

These commands are for Bash on Windows, you will need to convert them to whatever shell / platform you are using.

```sh title="install/windows_build.sh"
--8<-- "install/windows_build.sh"
```

### Documentation

The documentation uses mkdocs-material. You can install it with uv:

```sh
uv tool install mkdocs --with mkdocs-glightbox --with mkdocs-material --with mdx-truly-sane-lists --with mkdocs-minify-plugin
```

The command reference page can automatically be regenerated with:

```sh
uv sync
uv run typer gogadget.main utils docs --name gogadget --output docs/pages/reference/command_reference.md
```

From the newly generated `docs/pages/reference/command_reference.md`, I then delete the first bit of help text that is shown in the command line version when typing `gogadget`. This is for aesthetic purposes only!

A test server can be run with:

```sh
mkdocs serve -f docs/mkdocs.yml
```

## Running from source

### Generic

Firstly, please note the package requirements at the top of this document. You can then run:

```sh title="install/run_from_source_example.sh"
--8<-- "install/run_from_source_example.sh"
```

### On clean install of Ubuntu Server 24.04 LTS

```sh title="install/linux_test_install.sh"
--8<-- "install/linux_test_install.sh"
```
