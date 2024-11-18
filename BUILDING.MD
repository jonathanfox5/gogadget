# To build:

## Settings things up

Assumes building on Windows. If you are building on mac / linux, just skip the innosetup related steps.

1. Set version number in [pyproject.toml](pyproject.toml)
2. Set version number in [install/gogadget_windows.iss](install/gogadget_windows.iss)
3. Make sure `poetry` and `innosetup` are installed and in path. (innosetup isn't by default, need to add the root innosetup directory in program files)
4. Download latest windows builds of ffmpeg and uv and put the binaries directly in [install/bin/](install/bin/)

## Commands

(these are in bash, convert them to whatever shell you are using)

```sh
# Clear out any wheels and existing installers that we have
rm dist/*
rm install/bin/*.whl
rm install/output/*.exe

# Build new wheel and copy to bin folder
poetry build
cp dist/*.whl install/bin/

# Build windows installer and move to dist folder
iscc install/gogadget_windows.iss
mv install/output/*.exe dist/

# Step just for people called "Jonathan Fox" ;) Updates pypi index.
poetry publish
```

# Targets for testing for each release

- Windows 11 with CUDA
- Windows 11 without CUDA
- Windows 11 without any tools in path or python installed
- macOS (latest available release)
- Ubuntu Server 24.04.1 LTS (primarily because I don't have a linux desktop machine and a large proportion of desktop linux is Ubuntu)
