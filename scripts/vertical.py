"""Turn a horizontal (16:9) video into a vertical 9:16 Short / Reel / TikTok.

Modes:
  blur  (default) - full video in the middle, blurred copy fills the background
  crop            - zoom in and crop the centre (fills the screen, cuts the sides)

Examples:
  python scripts/vertical.py clip.mp4                 -> clip_vertical.mp4
  python scripts/vertical.py clip.mp4 --mode crop
  python scripts/vertical.py long.mp4 --start 1:20 --end 2:05     (cut a moment and make it vertical)
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import need, run  # noqa: E402

W, H = 1080, 1920


def main():
    p = argparse.ArgumentParser(description="Make a 9:16 vertical video.")
    p.add_argument("video")
    p.add_argument("-o", "--out")
    p.add_argument("--mode", choices=["blur", "crop"], default="blur")
    p.add_argument("--start", help="start time, e.g. 75 or 1:15")
    p.add_argument("--end", help="end time, e.g. 120 or 2:00")
    a = p.parse_args()
    need("ffmpeg")

    src = Path(a.video)
    out = Path(a.out) if a.out else src.with_name(src.stem + "_vertical.mp4")
    if a.mode == "blur":
        vf = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=25:5[bg];"
              f"[0:v]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]")
    else:
        vf = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1[v]"

    cmd = ["ffmpeg", "-y"]
    if a.start:
        cmd += ["-ss", a.start]
    if a.end:
        cmd += ["-to", a.end]
    cmd += ["-i", str(src), "-filter_complex", vf, "-map", "[v]", "-map", "0:a?",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    print("Making vertical video...")
    run(cmd)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
