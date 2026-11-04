# Creator Toolkit 🎬

A free toolkit for **faceless AI content** and **client video edits** that runs on your own computer.
It needs no subscription, has no usage limits, and doesn't depend on Claude or ChatGPT.

Every tool here is free, open-source and widely used, with thousands of GitHub stars.
The installer only uses official installers (winget on Windows, Homebrew on Mac).

| What you get | Tool | ⭐ on GitHub |
|---|---|---|
| Instant trimming/cutting with no quality loss | [LosslessCut](https://github.com/mifi/lossless-cut) | 46k |
| Auto-removes silences and dead air, can export to a Premiere/Resolve/FCP timeline | [auto-editor](https://github.com/WyattBlue/auto-editor) | 6k |
| Offline AI captions, word-by-word highlight | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) + `scripts/captions.py` | 26k |
| Free AI voiceover in 400+ voices and many languages | [edge-tts](https://github.com/rany2/edge-tts) + `scripts/voiceover.py` | 12k |
| AI writer on your PC for ideas, scripts, titles and tags (no limits) | [Ollama](https://github.com/ollama/ollama) + `scripts/ideas.py` | 186k |
| AI upscaler for sharp thumbnails | [Upscayl](https://github.com/upscayl/upscayl) | 52k |
| Screen and voice recording | [OBS Studio](https://github.com/obsproject/obs-studio) | 79k |
| Video downloader (for your own or client files) | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 205k |
| The engine behind everything | FFmpeg | — |

🧰 **The short list of extra tools worth installing (motion graphics, voice, sound): [BEST-TOOLS.md](BEST-TOOLS.md)**

📈 **New to growing a channel? Read [GROWTH-PLAYBOOK.md](GROWTH-PLAYBOOK.md) first.** It covers niche, hooks,
script formula, editing for retention, posting, a 30-day plan, and turning followers into editing clients.

---

## 1. Install (one time)

**Windows 10/11**
1. Click the green **Code** button on this GitHub page, then **Download ZIP**, and unzip it (to Documents, for example).
2. Double-click **`install-windows.bat`**. It takes 10–20 minutes and downloads about 4 GB.
3. When it finishes, double-click **`start.bat`**. A window opens with all the commands listed.

**Mac**
```bash
bash install-mac.sh
```
After that, open Terminal in the folder and run `source .venv/bin/activate` each time before using the scripts.

> Tip: in the toolkit window, you can **drag a file onto it** to paste the file's path.

---

## 2. Faceless video workflow (about 5 minutes per Short)

```bat
:: 1) Get ideas for your niche
python scripts\ideas.py ideas "space facts"

:: 2) Write a script (saved to script.txt)
python scripts\ideas.py script "Why the Moon is drifting away" --seconds 45 -o script.txt

:: 3) Put 8-15 stock clips or images in a folder called "clips"
::    free footage: pexels.com/videos, pixabay.com/videos   music: YouTube Studio > Audio Library

:: 4) Build the whole video: voiceover + clips + music + captions
python scripts\faceless_short.py --script script.txt --clips clips --music music.mp3 -o short1.mp4

:: 5) Get the title, description, tags and hashtags
python scripts\ideas.py seo "Why the Moon is drifting away"
```
Useful options: `--horizontal` for 16:9 long-form, `--tts-voice en-US-GuyNeural`, `--rate +10%`,
`--seconds-per-clip 2` for faster cuts, `--shuffle`, `--upper` for UPPERCASE captions, and `--voice my_voice.mp3` to use your own recording.

## 3. Client edit workflow

| Job | Command / tool |
|---|---|
| Remove silences from raw talking footage | `auto-editor raw.mp4` |
| Same, but send a timeline to your editor | `auto-editor raw.mp4 --export premiere` (or `resolve`, `final-cut-pro`) |
| Captions (.srt for any editor + burned-in version) | `python scripts\captions.py video.mp4` |
| Only the subtitle file | `python scripts\captions.py video.mp4 --no-burn` |
| Hindi / Spanish / any language | `python scripts\captions.py video.mp4 --language hi` |
| Better accuracy (slower) | `python scripts\captions.py video.mp4 --model medium` |
| Long video → vertical Short | `python scripts\vertical.py podcast.mp4 --start 12:30 --end 13:20` |
| Quick trims and splits | **LosslessCut** app |
| Edit plan from a client brief | `python scripts\ideas.py client "turn a 20 min podcast into 3 reels"` |
| Upscale thumbnails / low-res images | **Upscayl** app |

If you edit in **DaVinci Resolve**, also look at [AutoSubs](https://github.com/tmoroney/auto-subs) (4.5k ⭐), which adds free AI subtitles inside Resolve.

## 4. Growing a channel from zero subscribers

- **Pick one narrow niche per channel** and post consistently, ideally one Short a day. The algorithm needs data to figure out who to show you to.
- **The first 2 seconds decide everything.** Use `ideas.py hooks` and put the most curious line first.
- **Keep Shorts 20–45 seconds** with fast cuts (`--seconds-per-clip 2`). Retention matters more than length.
- **Post the same video to YouTube Shorts and Instagram Reels.** Upload the clean file and don't reuse one with another app's watermark.
- **Check YouTube Studio → Analytics after 48 hours.** Make more of whatever kept people watching.
- **Don't use follower/like/view "booster" bots or tools.** They break YouTube and Instagram rules, get channels banned, and many are malware.
- **Copyright:** only use footage and music you have rights to (Pexels, Pixabay, YouTube Audio Library, your client's files).
- **YouTube monetisation:** "faceless" is fine, but low-effort, mass-produced repetitive content can be demonetised. Add a real angle and a script with value.

## Troubleshooting

| Problem | Fix |
|---|---|
| `'ffmpeg' was not found` | Close the window and open `start.bat` again. If it still fails, restart the PC. |
| `Ollama is not running` | Open the Ollama app from the Start menu. |
| `model not found` (ideas.py) | Run `ollama pull llama3.2` once. |
| Voiceover failed | It needs internet. Check the voice name with `python scripts\voiceover.py --list en`. |
| First captions run is slow | It downloads the Whisper model once (~500 MB). Later runs are faster. |
