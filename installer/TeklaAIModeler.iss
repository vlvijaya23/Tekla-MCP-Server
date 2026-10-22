[Setup]
AppName=Tekla AI Modeler
AppVersion=1.0.0
DefaultDirName={pf}\Tekla AI Modeler
DefaultGroupName=Tekla AI Modeler
OutputDir=C:\tekla-mcp\installer\output
OutputBaseFilename=TeklaAIModelerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "C:\tekla-mcp\dist\TeklaAIModeler.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Tekla AI Modeler"; Filename: "{app}\TeklaAIModeler.exe"

Name: "{autodesktop}\Tekla AI Modeler"; Filename: "{app}\TeklaAIModeler.exe"

[Run]
Filename: "{app}\TeklaAIModeler.exe"; Description: "Launch Tekla AI Modeler"; Flags: nowait postinstall skipifsilent