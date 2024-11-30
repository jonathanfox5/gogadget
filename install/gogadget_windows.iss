; Copyright: © 2024 Jonathan Fox
; License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
; Full source code: https://github.com/jonathanfox5/gogadget

#define MyAppName "gogadget"
#define MyAppVersion "0.3.1"
#define MyAppPublisher "Jonathan Fox"
#define MyAppURL "https://github.com/jonathanfox5/gogadget"
#define BaseLaunchBat "gogadget_launcher.bat"
#define ContextLaunchBat "gogadget_context.bat"
#define WheelName "gogadget-0.3.1-py3-none-any.whl"

[Setup]
AppId={{04CF6C0E-59E0-4038-BB70-311BBABA4483}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName="{localappdata}\{#MyAppName}"
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
OutputBaseFilename={#MyAppName}_windows_installer_v{#MyAppVersion}
WizardStyle=modern
DisableDirPage=yes
ChangesEnvironment=true
Compression=zip
SolidCompression=yes
SetupIconFile="{#MyAppName}.ico"
UninstallDisplayIcon="{app}\{#MyAppName}.ico"
WizardSmallImageFile="WizardSmallImageFile.bmp"

[Dirs]
Name: "{%USERPROFILE}\.local\bin"; Flags: uninsneveruninstall

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full installation (HIGHLY Recommended)"
Name: "compact"; Description: "I already have FFMPEG and uv on my path"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "program"; Description: "{#MyAppName}"; Types: full compact custom; Flags: fixed
Name: "ffmpeg"; Description: "FFMPEG (Required)"; Types: full
Name: "uv"; Description: "uv (Required)"; Types: full
Name: "cuda"; Description: "CUDA: Add gpu processing to compatible systems (Optional, see readme)"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "addcontextmenu"; Description: "Add {#MyAppName} to right-click context menu"; GroupDescription: "{cm:AdditionalIcons}";

[Files]
Source: "bin\*.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: program
Source: "bin\*.whl"; DestDir: "{app}"; Flags: ignoreversion; Components: program
Source: "{#MyAppName}.ico"; DestDir: "{app}"; Flags: ignoreversion; Components: program
Source: "bin\ffmpeg.exe"; DestDir: "{%USERPROFILE}\.local\bin"; Flags: uninsneveruninstall; Components: ffmpeg
Source: "bin\uv*.exe"; DestDir: "{%USERPROFILE}\.local\bin"; Flags: uninsneveruninstall; Components: uv

[Run]
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool install {app}\{#WheelName} --python 3.12";
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool update-shell"; Flags: runhidden
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool install {app}\{#WheelName} --python 3.12 --with torch==2.5.1+cu124 --with torchaudio==2.5.1+cu124 --index https://download.pytorch.org/whl/cu124"; Components: cuda

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#BaseLaunchBat}"; IconFilename: "{app}\{#MyAppName}.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#BaseLaunchBat}"; Tasks: desktopicon; IconFilename: "{app}\{#MyAppName}.ico"

[Run]
Filename: "{app}\{#BaseLaunchBat}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[Registry]
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}"; Flags: uninsdeletekeyifempty
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}\Command"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}";  ValueType: string; ValueName: ""; ValueData: "Open {#MyAppName} here"; Flags: createvalueifdoesntexist uninsdeletevalue; Tasks: addcontextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}\Command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#ContextLaunchBat}"""; Flags: createvalueifdoesntexist uninsdeletevalue; Tasks: addcontextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\{#MyAppName}.ico"""; Flags: createvalueifdoesntexist uninsdeletevalue; Tasks: addcontextmenu

[UninstallRun]
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool uninstall gogadget"; RunOnceId: "UninstallTool"; Flags: runhidden
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "cache clean"; RunOnceId: "ClearUvCache"; Components: uv
