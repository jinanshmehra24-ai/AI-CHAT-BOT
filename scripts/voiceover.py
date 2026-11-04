"""Free AI voiceover from a text script (Microsoft Edge neural voices, no API key).

Needs an internet connection, but no account and no paid plan.

Examples:
  python scripts/voiceover.py script.txt                       -> script.mp3
  python scripts/voiceover.py script.txt --voice en-US-GuyNeural --rate +10%
  python scripts/voiceover.py --list en                        -> list English voices
Popular voices: en-US-AndrewNeural, en-US-ChristopherNeural, en-US-GuyNeural (male),
                en-US-AriaNeural, en-US-JennyNeural, en-GB-SoniaNeural (female),
                hi-IN-MadhurNeural, hi-IN-SwaraNeural (Hindi)
"""
import argparse
import asyncio
import os
import sys
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit("edge-tts is not installed. Run the installer first (see README).")

PROXY = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or None


async def list_voices(prefix):
    for v in sorted(await edge_tts.list_voices(proxy=PROXY), key=lambda v: v["ShortName"]):
        if v["ShortName"].lower().startswith(prefix.lower()):
            print(f'{v["ShortName"]:32} {v["Gender"]}')


def main():
    p = argparse.ArgumentParser(description="Free AI voiceover (edge-tts).")
    p.add_argument("script", nargs="?", help="text file with your script")
    p.add_argument("-o", "--out", help="output .mp3 (default: same name as the script)")
    p.add_argument("--voice", default="en-US-AndrewNeural")
    p.add_argument("--rate", default="+0%", help="speed, e.g. +10%%  (slower: --rate=-10%%)")
    p.add_argument("--pitch", default="+0Hz", help="pitch, e.g. -5Hz")
    p.add_argument("--list", metavar="LANG", help="list voices starting with LANG, e.g. en, en-US, hi")
    a = p.parse_args()

    if a.list:
        asyncio.run(list_voices(a.list))
        return
    if not a.script:
        p.error("give a script file, or use --list")
    script = Path(a.script)
    text = script.read_text(encoding="utf-8").strip()
    if not text:
        sys.exit("The script file is empty.")
    out = Path(a.out) if a.out else script.with_suffix(".mp3")
    print(f"Generating voiceover with {a.voice}...")
    try:
        asyncio.run(edge_tts.Communicate(text, a.voice, rate=a.rate, pitch=a.pitch, proxy=PROXY).save(str(out)))
    except Exception as e:  # network problems, wrong voice name, etc.
        out.unlink(missing_ok=True)
        sys.exit(f"Voiceover failed: {e}\nCheck your internet connection and the voice name (--list en).")
    print(f"Saved voiceover: {out}")


if __name__ == "__main__":
    main()
