<!-- Copyright: © 2024 Jonathan Fox
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Full source code: https://github.com/jonathanfox5/gogadget -->

## Accessing settings

The settings can be accessed with the following command. It will open the settings file in your default GUI text editor on macOS / Linux or in notepad / VSCode on Windows.

```sh
gogadget set-defaults --custom
```

If required, the settings file can be reset with the following command.

```sh
gogadget set-defaults --factory
```

## Settings file location

`gogadget set-defaults --custom` will open the settings file for you. Should you wish to access the file directly, it should be stored at:

- **Windows**: `%APPDATA%\gogadget\gogadget.toml` (you can paste this directly in like a normal path, Windows will convert `%APPDATA` to the correct folder within your user directory)
- **macOS**: `~/Library/Application Support/gogadget/gogadget.toml`
- **Linux**: `~/.config/gogadget/gogadget.toml`

Alternate paths could include `~/.gogadget/gogadget.toml` and `%LOCALAPPDATA%\gogadget\gogadget.toml` if you have system settings that override the default directory behaviour.

Note that the settings file is generated on the first run of the tool so won't be available until you have run it (any command works) at least once.

## Default Settings

```toml title="default_gogadget.toml"
--8<-- "examples/configs/default_gogadget.toml"
```
