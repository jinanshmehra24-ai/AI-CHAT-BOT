"""Auto-captions for any video or audio, 100% free and offline (Whisper AI).

Makes an .srt file (for YouTube / CapCut / Premiere / client hand-off) and,
for videos, can burn bold "Shorts style" captions with the spoken word
highlighted.

Examples:
  python scripts/captions.py my_video.mp4                 -> my_video.srt + my_video_captioned.mp4
  python scripts/captions.py my_video.mp4 --no-burn       -> only my_video.srt
  python scripts/captions.py talk.mp4 --words 6 --model medium --language en
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import need, probe, run  # noqa: E402

YELLOW = r"{\c&H00FFFF&}"   # ASS colours are BGR
WHITE = r"{\c&HFFFFFF&}"


def transcribe(media, model_name="small", language=None):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is not installed. Run the installer first (see README).")
    print(f"Loading Whisper model '{model_name}' (first run downloads it once)...")
    model = WhisperModel(model_name, device="auto", compute_type="int8")
    segments, info = model.transcribe(str(media), language=language, word_timestamps=True, vad_filter=True)
    words = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                words.append((w.start, w.end, text))
        print(f"  transcribed {seg.end:6.1f}s", end="\r")
    print(f"\nDetected language: {info.language}, {len(words)} words")
    return words


def chunk_words(words, per_line):
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= per_line or w[0] - cur[-1][1] > 0.6):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if w[2][-1:] in ".!?":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return chunks


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def ass_time(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def write_srt(chunks, path):
    lines = []
    for i, c in enumerate(chunks, 1):
        lines += [str(i), f"{srt_time(c[0][0])} --> {srt_time(c[-1][1])}", " ".join(w[2] for w in c), ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_ass(chunks, path, width, height, uppercase):
    vertical = height >= width
    size = int(height * (0.055 if vertical else 0.065))
    align = 5 if vertical else 2           # 5 = middle-centre, 2 = bottom-centre
    margin_v = int(height * (0.0 if vertical else 0.07))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial,{size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{max(2, size // 12)},{max(1, size // 25)},{align},{int(width * 0.08)},{int(width * 0.08)},{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for c in chunks:
        texts = [w[2].replace("{", "(").replace("}", ")") for w in c]
        if uppercase:
            texts = [t.upper() for t in texts]
        for i, w in enumerate(c):
            start = w[0]
            end = c[i + 1][0] if i + 1 < len(c) else c[-1][1]
            line = " ".join(f"{YELLOW}{t}{WHITE}" if j == i else t for j, t in enumerate(texts))
            events.append(f"Dialogue: 0,{ass_time(start)},{ass_time(max(end, start + 0.05))},Cap,,0,0,0,,{line}")
    Path(path).write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def make_captions(media, out_video=None, words_per_line=None, model="small", language=None,
                  burn=True, uppercase=False):
    need("ffmpeg")
    media = Path(media).resolve()
    width, height, _, _ = probe(media)
    is_video = width is not None
    if words_per_line is None:
        words_per_line = 3 if (is_video and height >= width) else 7
    words = transcribe(media, model, language)
    if not words:
        sys.exit("No speech found in this file.")
    chunks = chunk_words(words, words_per_line)
    srt_path = media.with_suffix(".srt")
    write_srt(chunks, srt_path)
    print(f"Saved subtitles: {srt_path}")
    if not (burn and is_video):
        return srt_path
    ass_path = media.with_name(media.stem + "_captions.ass")
    write_ass(chunks, ass_path, width, height, uppercase)
    out_video = Path(out_video).resolve() if out_video else media.with_name(media.stem + "_captioned.mp4")
    print("Burning captions into the video...")
    # run from the .ass folder so Windows drive letters don't break the filter
    run(["ffmpeg", "-y", "-i", str(media), "-vf", f"ass={ass_path.name}", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out_video)],
        cwd=ass_path.parent)
    print(f"Saved captioned video: {out_video}")
    return out_video


def main():
    p = argparse.ArgumentParser(description="Free offline auto-captions (Whisper).")
    p.add_argument("media", help="video or audio file")
    p.add_argument("-o", "--out", help="output video path")
    p.add_argument("--words", type=int, help="words per caption (default 3 vertical, 7 horizontal)")
    p.add_argument("--model", default="small", help="tiny / base / small / medium / large-v3 (bigger = better but slower)")
    p.add_argument("--language", help="force a language code, e.g. en, hi, es (default: auto-detect)")
    p.add_argument("--no-burn", action="store_true", help="only make the .srt file")
    p.add_argument("--upper", action="store_true", help="UPPERCASE captions")
    a = p.parse_args()
    make_captions(a.media, a.out, a.words, a.model, a.language, not a.no_burn, a.upper)


if __name__ == "__main__":
    main()
