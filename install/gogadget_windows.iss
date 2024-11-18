#define MyAppName "gogadget"
#define MyAppVersion "0.2.0"
#define MyAppPublisher "Jonathan Fox"
#define MyAppURL "https://github.com/jonathanfox5/gogadget"

[Setup]
AppId={{04CF6C0E-59E0-4038-BB70-311BBABA4483}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName="{%USERPROFILE}\.local\bin"
DefaultGroupName={#MyAppName}
PrivilegesRequired=lowest
OutputBaseFilename={#MyAppName}_windows_installer_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

ChangesEnvironment=true

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Types]
Name: "full"; Description: "Full installation (HIGHLY Recommended)"
Name: "compact"; Description: "I already have FFMPEG and uv on my path"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "program"; Description: "gogadget"; Types: full compact custom; Flags: fixed
Name: "ffmpeg"; Description: "FFMPEG (Required)"; Types: full
Name: "uv"; Description: "uv (Required)"; Types: full

[Files]
Source: "bin\ffmpeg.exe"; DestDir: "{%USERPROFILE}\.local\bin"; Flags: ignoreversion; Components: ffmpeg
Source: "bin\uv*.exe"; DestDir: "{%USERPROFILE}\.local\bin"; Flags: ignoreversion; Components: uv

[Run]
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool install gogadget --python 3.12 --upgrade";
Filename: "{%USERPROFILE}\.local\bin\uv.exe"; Parameters: "tool update-shell"; Flags: runhidden
