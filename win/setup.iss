#define MyAppName "scrobbler"
;#define MyAppVersion "x.y.z"
#define MyAppPublisher "hauzer"
#define MyAppURL "https://bitbucket.org/hauzer/scrobbler/"
#define MyAppExeName "scrobbler.exe"

[Setup]
AppId={{0759D401-D3D1-4953-9135-6D25C271A0DE}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile={#ProjectDir}\LICENSE
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#SourceFilesDir}\scrobbler.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\_sqlite3.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\cacert.pem"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\python33.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\sqlite3.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#SourceFilesDir}\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
