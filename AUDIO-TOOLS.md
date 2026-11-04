# Free AI Voice & Sound Effects Tools (from GitHub)

Star counts were checked in Nov 2026.
💻 = runs fine on a normal PC (CPU). 🎮 = needs an NVIDIA GPU (roughly 6 GB+ VRAM) to be practical.
**Commercial use** matters because monetised YouTube and client work count as commercial:
✅ = licence allows commercial use. ⚠️ = non-commercial or special licence, so read it before using it for paid or monetised work.

---

## 1. AI voiceover (text to speech)

| Tool | ⭐ | Runs on | Commercial | Why use it |
|---|---|---|---|---|
| [edge-tts](https://github.com/rany2/edge-tts) ✅ *(in your toolkit)* | 12k | 💻 (needs internet) | ⚠️ unofficial use of Microsoft's free voices | 400+ natural voices, zero setup. Could stop working any time |
| [Kokoro](https://github.com/hexgrad/kokoro) | 10k | 💻 | ✅ Apache-2.0 | **Best offline voice for normal PCs.** Very natural, fast, fully local |
| [Chatterbox](https://github.com/resemble-ai/chatterbox) | 28k | 🎮 | ✅ MIT | **Emotion control** (calm → dramatic) and cloning **your own** voice. Great for storytelling |
| [Chatterbox TTS Server](https://github.com/devnen/Chatterbox-TTS-Server) | 1.5k | 🎮 | ✅ MIT | Easy web interface for Chatterbox |
| [CosyVoice](https://github.com/QwenAudio/CosyVoice) | 24k | 🎮 | ✅ Apache-2.0 | Many languages, voice cloning |
| [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS) | 6.4k | 🎮 | ✅ Apache-2.0 | Very human-sounding, can laugh and sigh |
| [Piper](https://github.com/OHF-Voice/piper1-gpl) | 6k | 💻 | ✅ (check each voice) | Super fast, runs even on weak laptops. Less natural |
| [IndexTTS](https://github.com/index-tts/index-tts) | 25k | 🎮 | ⚠️ own licence | Precise timing control, good for dubbing to exact lengths |
| [F5-TTS](https://github.com/SWivid/F5-TTS) | 16k | 🎮 | ⚠️ model is non-commercial | High-quality cloning. Personal projects only |
| [Fish Speech](https://github.com/fishaudio/fish-speech) | 34k | 🎮 | ⚠️ non-commercial licence | Top quality. Check the licence before monetising |
| [VibeVoice](https://github.com/microsoft/VibeVoice) | 55k | 🎮 | ⚠️ Microsoft says research use | Long multi-speaker conversations (podcast style) |

### Voice cloning / changing your voice
| Tool | ⭐ | Runs on | Commercial | Why use it |
|---|---|---|---|---|
| [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | 65k | 🎮 | ✅ MIT | Train a voice from **1 minute of audio** |
| [OpenVoice](https://github.com/myshell-ai/OpenVoice) | 38k | 🎮 | ✅ MIT | Instant cloning plus style control |
| [Applio](https://github.com/IAHispano/Applio) | 4k | 🎮 | ✅ MIT (the app) | Turn your recorded voice into another voice (RVC) |

### All-in-one apps (several engines in one window)
| Tool | ⭐ | What's inside |
|---|---|---|
| [Voice-Pro](https://github.com/abus-aikorea/voice-pro) | 13k | Edge-TTS, Kokoro, F5, CosyVoice, voice changer, vocal remover, subtitles, translation |
| [TTS-WebUI](https://github.com/rsxdalv/TTS-WebUI) | 3.3k | One interface for many TTS and music models |

> ⚠️ **Voice cloning rules:** only clone **your own voice** or a voice you have **written permission** for.
> Cloning celebrities or other creators can get your channel removed and can be illegal.
> YouTube requires you to tick **"Altered or synthetic content"** when a realistic AI voice could be mistaken for a real person.

---

## 2. Sound effects (SFX) for motion graphics

### AI sound effect generators
| Tool | ⭐ | Runs on | Commercial | What it does |
|---|---|---|---|---|
| [stable-audio-tools](https://github.com/Stability-AI/stable-audio-tools) (Stable Audio Open model) | 3.9k | 🎮 | ✅ free for creators under $1M/yr revenue (Stability Community Licence) | **Text → sound effect**: "deep cinematic whoosh", "glitch riser", "UI click". Best all-round SFX generator |
| [MMAudio](https://github.com/hkchengrex/MMAudio) | 2.3k | 🎮 | ⚠️ check model licence | **Video → matching sound.** Feed it your animation and it creates synced audio |
| [HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley) | 1.1k | 🎮 (big GPU) | ⚠️ Tencent licence (not for EU/UK/S. Korea) | High-quality Foley that matches the video |
| [AudioCraft (AudioGen)](https://github.com/facebookresearch/audiocraft) | 24k | 🎮 | ⚠️ models are non-commercial | Text → sound effects and music. Fine for practice and personal use |
| [AudioLDM](https://github.com/haoheliu/AudioLDM) | 2.9k | 🎮 | ⚠️ check | Text → sound effects |

### Design your own SFX (no AI, 100% yours, ✅ commercial)
Motion designers make whooshes, risers, impacts and glitches this way:

| Tool | ⭐ | Use it for |
|---|---|---|
| [Vital](https://github.com/mtytel/vital) | 2.2k | Free wavetable synth: **whooshes, risers, swells, sci-fi UI sounds** |
| [Surge XT](https://github.com/surge-synthesizer/surge) | 4.1k | Free synth with huge presets: impacts, drones, glitches |
| [LMMS](https://github.com/LMMS/lmms) | 11k | Free music/beat software that hosts the synths above and lets you layer sounds |
| [Audacity](https://github.com/audacity/audacity) | 19k | Layer, pitch-shift, reverse and reverb sounds into custom SFX |
| [jsfxr](https://github.com/grumdrig/jsfxr) / [bfxr](https://github.com/increpare/bfxr) | 283 / 1k | One-click **retro / game / UI** sounds (pops, coins, blips) |

**Classic recipe for a motion-graphics whoosh:** white noise in Vital, filter sweep low → high, add reverb,
reverse a copy for a "riser", then end on a low impact (sine drop + distortion).

### Background music (AI)
| Tool | ⭐ | Runs on | Commercial | What it does |
|---|---|---|---|---|
| [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) | 14k | 🎮 | ✅ check repo licence | Free local **Suno-style** song and instrumental generator |
| [ACE-Step UI](https://github.com/fspecii/ace-step-ui) | 5k | 🎮 | — | Easy interface for ACE-Step |

### Free SFX libraries (no generating needed)
- **Freesound.org**: filter by licence **"Creative Commons 0"** to use sounds anywhere without credit.
- **Pixabay → Sound Effects**: free for commercial use.
- **YouTube Studio → Audio Library → Sound effects**: safe for YouTube.
- **Sonniss "GDC Game Audio Bundle"**: tens of GB of pro SFX, free, royalty-free (released yearly).

---

## Recommended setup

| Your PC | AI voice | Sound effects |
|---|---|---|
| **Normal laptop / no NVIDIA GPU** | edge-tts (toolkit) → Kokoro for offline | Vital + Audacity + Freesound/Pixabay libraries |
| **NVIDIA GPU (8 GB+)** | Chatterbox (emotion + your own voice clone) | Stable Audio Open for text→SFX, MMAudio for video→SFX |

**Easiest single install:** Voice-Pro, which bundles several voice engines in one app.
