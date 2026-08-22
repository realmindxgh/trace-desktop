#define MyAppName "AsantePDF"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "RealMindX Education Ltd"
#define MyAppExeName "AsantePDF.exe"
#ifndef SourceDir
  #define SourceDir "..\dist\app"
#endif

[Setup]
AppId={{8C75D2B2-CFA8-4DBB-9F43-0B2E46A7C6A4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://realmindxgh.com
AppSupportURL=https://realmindxgh.com
DefaultDirName={autopf}\AsantePDF
DefaultGroupName=AsantePDF
DisableProgramGroupPage=yes
PrivilegesRequired=admin
OutputDir=..\dist\installer
OutputBaseFilename=AsantePDF Setup
SetupIconFile=..\assets\asantepdf.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
WizardSizePercent=110
DisableWelcomePage=no
CloseApplications=yes
RestartApplications=no
RestartIfNeededByRun=no
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.19041
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Complete free PDF toolkit for Windows
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
ChangesAssociations=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked

[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\prereqs\vc_redist.x64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{autoprograms}\AsantePDF"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\AsantePDF"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; PDF integration is deliberately mandatory. There is no opt-out task.
[Registry]
Root: HKCU; Subkey: "Software\Classes\Applications\{#MyAppExeName}"; ValueType: string; ValueName: "FriendlyAppName"; ValueData: "AsantePDF"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".pdf"; ValueData: ""
Root: HKCU; Subkey: "Software\Classes\Applications\{#MyAppExeName}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\OpenWithProgids"; ValueType: none; ValueName: "Applications\{#MyAppExeName}"; Flags: uninsdeletevalue

[Run]
Filename: "{tmp}\vc_redist.x64.exe"; Parameters: "/install /quiet /norestart"; StatusMsg: "Installing required Microsoft runtime..."; Flags: waituntilterminated; Check: NeedVCRedist
Filename: "{app}\{#MyAppExeName}"; Description: "Launch AsantePDF"; Flags: nowait postinstall skipifsilent

[Code]
function NeedVCRedist: Boolean;
var
  Installed: Cardinal;
begin
  Result := True;
  if RegQueryDWordValue(HKLM64, 'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64', 'Installed', Installed) then
    Result := Installed <> 1;
end;

procedure InitializeWizard;
begin
  WizardForm.Color := $00F7F7F7;
  WizardForm.WelcomeLabel1.Caption := 'Install AsantePDF';
  WizardForm.WelcomeLabel2.Caption :=
    'A complete, free PDF toolkit for viewing, organising, converting, OCR, editing, signing, inspecting, repairing and processing PDF files.' + #13#10 + #13#10 +
    'Setup includes the local PDF, OCR and Office conversion engines required by AsantePDF.' + #13#10 +
    'There are no premium features or subscriptions. Your documents stay on this computer during normal operations.';
end;
