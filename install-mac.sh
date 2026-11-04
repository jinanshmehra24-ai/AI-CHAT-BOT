#!/usr/bin/env bash
# Creator Toolkit installer for macOS (uses Homebrew, the standard Mac package manager).
# Run in Terminal:  bash install-mac.sh
set -e
cd "$(dirname "$0")"

if ! command -v brew >/dev/null 2>&1; then
  echo "Installing Homebrew (official installer from brew.sh)..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
fi

brew install python@3.12 ffmpeg
for app in losslesscut kdenlive upscayl obs ollama; do
  brew install --cask "$app" || echo "Skipped $app (already installed?)"
done

"$(brew --prefix)/bin/python3.12" -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt

echo "Open the Ollama app once, then run:  ollama pull llama3.2"
echo
echo "All done! Each time you use the toolkit, open Terminal in this folder and run:"
echo "  source .venv/bin/activate"
