"""Build a complete faceless video from: a script (or voiceover) + a folder of clips/images.

What it does, automatically:
  1. Makes an AI voiceover from your script (free, edge-tts)   - or uses your own audio file
  2. Cuts your stock clips / images to fit the voiceover (images get a slow zoom)
  3. Adds background music quietly under the voice (optional)
  4. Burns bold word-by-word captions (free, offline Whisper)

Free stock footage: pexels.com/videos, pixabay.com/videos, coverr.co (check each licence).
Free music: YouTube Studio -> Audio Library, pixabay.com/music.

Examples:
  python scripts/faceless_short.py --script script.txt --clips clips/ --music music.mp3
  python scripts/faceless_short.py --voice my_voice.mp3 --clips clips/ -o short.mp4
  python scripts/faceless_short.py --script script.txt --clips clips/ --horizontal     (long-form 16:9)
"""
import argparse
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import need, probe, run  # noqa: E402

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
FPS = 30


def make_segment(src, seg, dst, W, H):
    if src.suffix.lower() in IMAGE_EXT:
        frames = max(1, int(seg * FPS))
        vf = (f"scale={W * 2}:{H * 2}:force_original_aspect_ratio=increase,crop={W * 2}:{H * 2},"
              f"zoompan=z='min(zoom+0.0008,1.25)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
              f":s={W}x{H}:fps={FPS},setsar=1,format=yuv420p")
        cmd = ["ffmpeg", "-y", "-i", str(src), "-vf", vf, "-frames:v", str(frames)]
        used = frames / FPS
    else:
        _, _, dur, _ = probe(src)
        used = min(seg, dur) if dur > 0 else seg
        start = random.uniform(0, max(0.0, dur - used - 0.1)) if dur > used + 0.5 else 0
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p"
        cmd = ["ffmpeg", "-y", "-ss", f"{start:.2f}", "-t", f"{used:.2f}", "-i", str(src), "-vf", vf]
    run(cmd + ["-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(dst)])
    _, _, real, _ = probe(dst)
    return real or used


def main():
    p = argparse.ArgumentParser(description="Make a faceless video from a script + clips.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--script", help="text file -> free AI voiceover")
    src.add_argument("--voice", help="your own voiceover audio file")
    p.add_argument("--clips", required=True, help="folder of videos and/or images")
    p.add_argument("--music", help="background music file (optional)")
    p.add_argument("--music-volume", type=float, default=0.12, help="0.05 quiet ... 0.3 loud (default 0.12)")
    p.add_argument("-o", "--out", help="output file (default: final_video.mp4)")
    p.add_argument("--tts-voice", default="en-US-AndrewNeural", help="voice for --script")
    p.add_argument("--rate", default="+5%", help="voice speed for --script")
    p.add_argument("--seconds-per-clip", type=float, default=3.0, help="how long each clip stays on screen")
    p.add_argument("--shuffle", action="store_true", help="random clip order")
    p.add_argument("--horizontal", action="store_true", help="16:9 long-form instead of 9:16 Short")
    p.add_argument("--no-captions", action="store_true")
    p.add_argument("--upper", action="store_true", help="UPPERCASE captions")
    p.add_argument("--model", default="small", help="Whisper model for captions")
    a = p.parse_args()
    need("ffmpeg")
    need("ffprobe")

    W, H = (1920, 1080) if a.horizontal else (1080, 1920)
    out = Path(a.out or "final_video.mp4").resolve()
    clips = sorted(f for f in Path(a.clips).iterdir() if f.suffix.lower() in VIDEO_EXT | IMAGE_EXT)
    if not clips:
        sys.exit(f"No videos or images found in {a.clips}")
    if a.shuffle:
        random.shuffle(clips)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if a.script:
            voice = tmp / "voice.mp3"
            print("1/4 Generating AI voiceover...")
            subprocess.run([sys.executable, str(HERE / "voiceover.py"), a.script, "-o", str(voice),
                            "--voice", a.tts_voice, "--rate", a.rate], check=True)
        else:
            voice = Path(a.voice).resolve()
        _, _, voice_len, _ = probe(voice)
        if voice_len <= 0:
            sys.exit("Could not read the voiceover length.")
        print(f"   voiceover length: {voice_len:.1f}s")

        print("2/4 Cutting clips to fit...")
        parts, total, i = [], 0.0, 0
        while total < voice_len + 0.3:
            seg = min(a.seconds_per_clip, voice_len + 0.5 - total)
            seg = max(seg, 0.5)
            dst = tmp / f"part{i:04}.mp4"
            total += make_segment(clips[i % len(clips)], seg, dst, W, H)
            parts.append(dst)
            i += 1
            print(f"   {min(total, voice_len):5.1f}s / {voice_len:.1f}s", end="\r")
        print()
        (tmp / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-c", "copy", "visuals.mp4"], cwd=tmp)

        print("3/4 Mixing voice and music...")
        mixed = out if a.no_captions else out.with_name(out.stem + "_nocaptions.mp4")
        cmd = ["ffmpeg", "-y", "-i", str(tmp / "visuals.mp4"), "-i", str(voice)]
        if a.music:
            cmd += ["-stream_loop", "-1", "-i", str(Path(a.music).resolve()), "-filter_complex",
                    f"[2:a]volume={a.music_volume}[m];[1:a][m]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]"]
        else:
            cmd += ["-map", "0:v", "-map", "1:a"]
        cmd += ["-t", f"{voice_len + 0.3:.2f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", str(mixed)]
        run(cmd)

    if a.no_captions:
        print(f"Done: {out}")
        return
    print("4/4 Adding captions...")
    from captions import make_captions
    make_captions(mixed, out, model=a.model, uppercase=a.upper)
    srt = mixed.with_suffix(".srt")
    if srt.exists():
        srt.replace(out.with_suffix(".srt"))
    mixed.unlink(missing_ok=True)
    mixed.with_name(mixed.stem + "_captions.ass").unlink(missing_ok=True)
    print(f"Done: {out}  (+ {out.with_suffix('.srt').name} for uploading as subtitles)")


if __name__ == "__main__":
    main()
