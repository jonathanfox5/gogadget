#define MyAppName "gogadget"
#define MyAppVersion "0.1.2"
#define MyAppPublisher "Jonathan Fox"
#define MyAppURL "https://github.com/jonathanfox5/gogadget"
#define BaseLaunchBat "gogadget_launcher.bat"
#define ContextLaunchBat "gogadget_context.bat"

[Setup]
AppId={{04CF6C0E-59E0-4038-BB70-311BBABA4483}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName="{localappdata}\{#MyAppName}"
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
OutputBaseFilename={#MyAppName}_windows_installer_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableDirPage=yes
ChangesEnvironment=true

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

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "addcontextmenu"; Description: "Add {#MyAppName} to right-click context menu"; GroupDescription: "{cm:AdditionalIcons}";

[Files]
Source: "bin\*.bat"; DestDir: "{app}"; Flags: ignoreversion; Components: program
Source: "bin\ffmpeg.exe"; DestDir: "{%USERPROFILE}\.local\bin"; Components: ffmpeg
Source: "bin\uv*.exe"; DestDir: "{%USERPROFILE}\.local\bin"; Components: uv

[Run]
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool install gogadget>={#MyAppVersion} --python 3.12 --upgrade";
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool update-shell"; Flags: runhidden

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#BaseLaunchBat}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#BaseLaunchBat}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#BaseLaunchBat}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[Registry]
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}";  ValueType: string; ValueName: ""; ValueData: "Open {#MyAppName} here"; Flags: createvalueifdoesntexist uninsdeletevalue; Tasks: addcontextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#ContextLaunchBat}"""; Flags: createvalueifdoesntexist uninsdeletevalue; Tasks: addcontextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\Background\shell\{#MyAppName}";  ValueType: string; ValueName: ""; ValueData: "Open {#MyAppName} here"; Flags: createvalueifdoesntexist uninsdeletevalue; Tasks: addcontextmenu

[UninstallRun]
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "cache clean"; RunOnceId: "ClearUvCache"; Components: uv
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool uninstall gogadget"; RunOnceId: "UninstallTool"; Flags: runhidden
