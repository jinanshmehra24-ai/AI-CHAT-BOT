# Creator Toolkit installer for Windows 10/11.
# Installs only free, open-source, well-known tools via winget (Microsoft's official app installer).
# Run by double-clicking install-windows.bat

$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "winget not found. Install 'App Installer' from the Microsoft Store, then run this again." -ForegroundColor Red
    Read-Host "Press Enter to close"; exit 1
}

$apps = @(
    @{ id = "Python.Python.3.12";      name = "Python 3.12 (runs the toolkit scripts)" },
    @{ id = "Gyan.FFmpeg";             name = "FFmpeg (video engine used by everything)" },
    @{ id = "mifi.losslesscut";        name = "LosslessCut (instant trimming, no quality loss)" },
    @{ id = "KDE.Kdenlive";            name = "Kdenlive (full free video editor)" },
    @{ id = "Upscayl.Upscayl";         name = "Upscayl (AI image upscaler for thumbnails)" },
    @{ id = "OBSProject.OBSStudio";    name = "OBS Studio (screen / voice recording)" },
    @{ id = "Ollama.Ollama";           name = "Ollama (free AI writer that runs on your PC)" }
)

foreach ($app in $apps) {
    Write-Host "`n=== Installing $($app.name)" -ForegroundColor Cyan
    winget install -e --id $app.id --accept-source-agreements --accept-package-agreements --silent
}

# refresh PATH so the new tools are visible in this window
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

Write-Host "`n=== Setting up the Python tools (captions, voiceover, auto-editor, yt-dlp)" -ForegroundColor Cyan
$py = "py"
if (-not (Get-Command py -ErrorAction SilentlyContinue)) { $py = "python" }
& $py -3.12 -m venv .venv 2>$null
if (-not (Test-Path ".venv\Scripts\python.exe")) { & $py -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "`n=== Downloading the free local AI writing model (about 2 GB, one time)" -ForegroundColor Cyan
if (Get-Command ollama -ErrorAction SilentlyContinue) { ollama pull llama3.2 }
else { Write-Host "Open the Ollama app once, then run:  ollama pull llama3.2" -ForegroundColor Yellow }

Write-Host "`nAll done! Double-click start.bat to open the toolkit." -ForegroundColor Green
Read-Host "Press Enter to close"
