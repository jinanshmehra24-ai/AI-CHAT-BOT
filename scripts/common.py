"""Small helpers shared by the toolkit scripts (FFmpeg / FFprobe wrappers)."""
import json
import shutil
import subprocess
import sys


def need(tool):
    if shutil.which(tool) is None:
        sys.exit(f"'{tool}' was not found. Run the installer for your computer first (see README).")


def run(cmd, cwd=None):
    """Run a command, stop with a readable error if it fails."""
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        sys.exit(f"Command failed:\n  {' '.join(map(str, cmd))}\n\n{result.stderr[-2000:]}")
    return result.stdout


def probe(path):
    """Return (width, height, duration_seconds, has_audio) for a media file."""
    need("ffprobe")
    out = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", str(path)])
    info = json.loads(out)
    width = height = None
    has_audio = False
    for s in info.get("streams", []):
        if s.get("codec_type") == "video" and width is None:
            width, height = s.get("width"), s.get("height")
        if s.get("codec_type") == "audio":
            has_audio = True
    duration = float(info.get("format", {}).get("duration") or 0)
    return width, height, duration, has_audio
