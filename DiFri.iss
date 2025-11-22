; all paths are according to my system , do adjust all those accordingly while generating your installer

[Setup]
AppId={{B5BAF560-08C6-4A70-B7CE-F043325988D1}}
AppName=DiFri
AppVersion=2.0
UninstallDisplayName=DiFri
AppPublisher=Abhijit-71
AppPublisherURL=https://www.github.com/Abhijit-71/DiFri
AppSupportURL=https://www.github.com/Abhijit-71/DiFri
AppUpdatesURL=https://www.github.com/Abhijit-71/DiFri

; Install to Program Files
DefaultDirName={pf}\DiFri

; Needs admin to write associations & Program Files
PrivilegesRequired=admin

UninstallDisplayIcon={app}\DiFri.exe

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DefaultGroupName=DiFri

LicenseFile=LICENSE.txt

OutputBaseFilename=DiFri_setup

; Soft-coded icon, must exist inside overall project
SetupIconFile=dbrowser_logo.ico

SolidCompression=yes
WizardStyle=modern


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce


[Files]
; Main EXE
Source: "C:\Users\Abhijit\Desktop\DiFri\src\dist\DiFri\DiFri.exe"; \
    DestDir: "{app}"; Flags: ignoreversion

; All supporting files
Source: "C:\Users\Abhijit\Desktop\DiFri\src\dist\DiFri\*"; \
    DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Setup icon (soft coded)
Source: "C:\Users\Abhijit\Desktop\DiFri\src\svg\dbrowser_logo.ico"; \
    DestDir: "{app}"


[Icons]
Name: "{group}\DiFri"; Filename: "{app}\DiFri.exe"
Name: "{autodesktop}\DiFri"; Filename: "{app}\DiFri.exe"; Tasks: desktopicon


[Run]
Filename: "{app}\DiFri.exe"; Description: "{cm:LaunchProgram,DiFri}"; \
    Flags: nowait postinstall skipifsilent


; ---------------------------
;     FILE ASSOCIATIONS
; ---------------------------
[Registry]

; ---------- PDF ----------
Root: HKCR; Subkey: ".pdf"; ValueType: string; ValueData: "DiFri.pdf"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "DiFri.pdf"; ValueType: string; ValueData: "PDF File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "DiFri.pdf\DefaultIcon"; ValueType: string; ValueData: "{app}\_internal\svg\pdf.ico"
Root: HKCR; Subkey: "DiFri.pdf\shell\open\command"; \
    ValueType: string; ValueData: """{app}\DiFri.exe"" ""%1"""

    
; ---------- HTML ----------
Root: HKCR; Subkey: ".html"; ValueType: string; ValueData: "DiFri.html"; Flags: uninsdeletevalue
Root: HKCR; Subkey: ".htm";  ValueType: string; ValueData: "DiFri.html"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "DiFri.html"; ValueType: string; ValueData: "HTML File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "DiFri.html\DefaultIcon"; ValueType: string; ValueData: "{app}\_internal\svg\html.ico"
Root: HKCR; Subkey: "DiFri.html\shell\open\command"; \
    ValueType: string; ValueData: """{app}\DiFri.exe"" ""%1"""

; ---------- SVG ----------
Root: HKCR; Subkey: ".svg"; ValueType: string; ValueData: "DiFri.svg"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "DiFri.svg"; ValueType: string; ValueData: "SVG File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "DiFri.svg\DefaultIcon"; ValueType: string; ValueData: "{app}\_internal\svg\svg.ico"
Root: HKCR; Subkey: "DiFri.svg\shell\open\command"; \
    ValueType: string; ValueData: """{app}\DiFri.exe"" ""%1"""