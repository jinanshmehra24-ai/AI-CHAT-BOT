"""Free, unlimited AI writer that runs on YOUR computer (Ollama) - no Claude/ChatGPT limits.

One-time setup: install Ollama (the installer does it), then download a model once:
    ollama pull llama3.2          (small, fast, ~2 GB - works on most laptops)
    ollama pull qwen2.5:7b        (better writing, needs ~8 GB RAM)

Examples:
  python scripts/ideas.py ideas  "space facts"                -> 20 video ideas for a niche
  python scripts/ideas.py script "Why the Moon is drifting away" --seconds 45
  python scripts/ideas.py seo    "Why the Moon is drifting away"   -> titles, description, tags, hashtags
  python scripts/ideas.py hooks  "Why the Moon is drifting away"   -> 10 scroll-stopping first lines
  python scripts/ideas.py client "cut a 60s highlight from a 20 min podcast about fitness"  -> edit plan
  python scripts/ideas.py calendar "space facts"                -> 30-day posting plan
  python scripts/ideas.py insta  "Why the Moon is drifting away"   -> Instagram caption + cover text
Add  -o file.txt  to save the answer (e.g. save a script, then feed it to faceless_short.py).
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

PROMPTS = {
    "ideas": ("Give 20 specific video ideas for a brand-new faceless YouTube Shorts / Instagram Reels channel "
              "in this niche: {topic}. Favour ideas that are curiosity-driven, easy to illustrate with stock "
              "footage, and searchable. For each: a punchy title (max 60 characters) and one line on why people "
              "would watch to the end. Number them."),
    "script": ("Write a voiceover script for a faceless short video about: {topic}. Length: about {seconds} "
               "seconds when spoken (~{words} words). Rules: the first sentence is a strong hook that creates "
               "curiosity; short, simple sentences; no headings, no emojis, no stage directions, no 'in this "
               "video'; build to a satisfying payoff; end with a short line that makes people comment or "
               "rewatch. Output ONLY the words to be spoken."),
    "seo": ("I am uploading a video about: {topic}. Write: 5 title options (max 60 characters, curiosity + "
            "keyword), a 3-sentence description with the main keyword in the first sentence, 15 comma-separated "
            "tags, 5 hashtags, and a 6-word text idea for the thumbnail."),
    "hooks": ("Write 10 different opening lines (max 12 words each) for a short video about: {topic}. Each must "
              "stop someone from scrolling in the first 2 seconds. Mix styles: question, shocking fact, "
              "'you've been lied to', countdown, bold claim. Number them."),
    "calendar": ("Make a 30-day posting calendar for a brand-new YouTube Shorts + Instagram Reels channel in this "
                 "niche: {topic}. One video per day. For each day: the video title, the hook (first line), and the "
                 "format (fact, story, list, myth-buster, before/after, series part). Group them into 2-3 recurring "
                 "series so people follow for the next part. Output as a numbered list Day 1 to Day 30."),
    "insta": ("Write an Instagram Reel caption for a video about: {topic}. First line is a hook under 10 words "
              "(it is all people see before 'more'). Then 2 short lines of value, then a question that makes people "
              "comment, then a line asking them to save or send it to a friend, then 4 relevant hashtags. "
              "Also give a 5-word text for the Reel cover image."),
    "client": ("I am a freelance video editor. Client request: {topic}. Give me a clear edit plan: structure with "
               "timestamps to aim for, where to cut, pacing, captions style, b-roll/zoom/sound-effect ideas, "
               "music mood, aspect ratios to export, and a short checklist before delivery."),
}


def ask(model, prompt, host):
    body = json.dumps({"model": model, "prompt": prompt, "stream": True}).encode()
    req = urllib.request.Request(f"{host}/api/generate", data=body, headers={"Content-Type": "application/json"})
    text = []
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            for line in r:
                if not line.strip():
                    continue
                chunk = json.loads(line)
                if chunk.get("error"):
                    sys.exit(f"Ollama error: {chunk['error']}\nTry:  ollama pull {model}")
                piece = chunk.get("response", "")
                print(piece, end="", flush=True)
                text.append(piece)
    except urllib.error.HTTPError as e:
        sys.exit(f"Ollama error: {e.read().decode(errors='ignore')}\nTry:  ollama pull {model}")
    except urllib.error.URLError:
        sys.exit("Ollama is not running. Open the Ollama app (or run 'ollama serve') and try again.")
    print()
    return "".join(text).strip()


def main():
    p = argparse.ArgumentParser(description="Free local AI writer for creators (Ollama).")
    p.add_argument("mode", choices=PROMPTS)
    p.add_argument("topic", help="niche, topic, or client request (in quotes)")
    p.add_argument("--seconds", type=int, default=45, help="script length for 'script' mode")
    p.add_argument("--model", default="llama3.2")
    p.add_argument("--host", default="http://localhost:11434")
    p.add_argument("-o", "--out", help="save the answer to a text file")
    a = p.parse_args()
    prompt = PROMPTS[a.mode].format(topic=a.topic, seconds=a.seconds, words=int(a.seconds * 2.5))
    answer = ask(a.model, prompt, a.host)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(answer + "\n")
        print(f"\nSaved: {a.out}")


if __name__ == "__main__":
    main()
