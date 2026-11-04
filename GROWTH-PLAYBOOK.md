# Growth Playbook: YouTube + Instagram from 0

Nobody can promise a video will go viral. What you *can* do is make every video give the algorithm
and the viewer a reason to push it further. This playbook is that system.

---

## 0. The big idea: one channel that does two jobs

You make **faceless AI content** and do **client edits**. Don't keep these separate.
Your edits *are* your content:

| Content type | Grows followers? | Gets you clients? |
|---|---|---|
| Faceless niche Shorts (facts, stories, motivation…) | ✅✅ | ❌ |
| **Before/after edits** ("raw clip → edited") | ✅✅ | ✅✅ |
| **Editing tips / "how I made this"** | ✅ | ✅✅ |
| Client work you have permission to post | ✅ | ✅✅ |

**Recommended setup:**
- **Channel/Page A: faceless niche** (pick ONE niche). This is for views, reach and future ad money.
- **Channel/Page B: you as an editor**, faceless too (screen recordings, before/after). This is for clients.
  Put "DM for edits" in the bio and the link to your portfolio.

If you only have energy for one, do **B**. Before/after edit videos are one of the most-shared formats,
and every view is also an ad for your service.

### Picking the niche for channel A
Pick a niche that:
1. **People search for and share**: facts, history mysteries, space, psychology, money, motivation, scary stories, "things you didn't know about…"
2. **Is easy to illustrate with free stock footage or AI images**
3. **You can make 100 videos about without running out**

Test: run `python scripts\ideas.py ideas "your niche"`. If 15 of the 20 ideas make *you* curious, it's a good niche.

---

## 1. Why people share and follow (build every video around one of these)

People share a video when it makes **them** look good, feel something, or helps a friend:

| Trigger | What the viewer thinks | Example |
|---|---|---|
| **"Whoa" / curiosity** | "My friend has to see this" | "This ocean is 3× deeper than Everest is tall" |
| **Useful** | "Saving this for later" (saves = huge signal) | "5 CapCut tricks that look expensive" |
| **Identity / relatable** | "This is SO me" → tags a friend | "Editors at 3am when the client says 'small change'" |
| **Emotion** | Inspired, shocked, nostalgic | Comeback stories, short motivational stories |
| **Debate** | Has to comment | "Most people get this wrong…" |
| **Satisfying transformation** | Watches twice | Before → after edit, glow-ups, restorations |

**People follow when they expect MORE of the same.** So:
- Same niche, same style, same caption font and colours every time. Make it recognisable in 1 second.
- Make series: "Part 1/2/3", "Day 12 of editing every day", "Facts you didn't know #47".
- End with a reason to follow: *"Part 2 tomorrow"* beats *"please subscribe"*.

---

## 2. The script formula (for 20–45 second Shorts and Reels)

```
HOOK (0–2s)      One line that creates a question in their head. No intro, no "hey guys".
SETUP (2–8s)     Quick context: why this matters.
3 BEATS (8–35s)  Each beat = new info / twist / escalation. Cut visuals every 1.5–3s.
PAYOFF (35–40s)  The answer, the reveal, the "whoa".
LOOP / CTA       Last line flows back into the first line (rewatch) OR "Part 2 tomorrow".
```

### 12 hook formulas (copy these)
1. "You've been lied to about ___."
2. "This is why ___ (surprising fact)."
3. "Nobody talks about ___."
4. "Stop scrolling if you ___."
5. "In 30 seconds you'll know more about ___ than 99% of people."
6. "This ___ looks normal… until you notice ___."
7. "Here's what happens if ___."
8. "I edited this in 10 minutes. Here's how." *(editor channel)*
9. "Raw footage vs. after my edit." *(editor channel)*
10. "The ___ trick that pro editors don't share."
11. "Scientists can't explain ___."
12. "Number 3 is the reason ___."

### Example script (faceless, about 35 seconds)
> The Moon is running away from us, and we can measure it.
> Every year it drifts about four centimetres further from Earth.
> That sounds tiny. But billions of years ago, the Moon was so close it looked huge in the sky,
> and a full day on Earth lasted only about six hours.
> The cause? Tides. The oceans act like a brake on Earth's spin, and that energy pushes the Moon outward.
> So the days are slowly getting longer. And one day, far in the future, total solar eclipses will stop forever,
> because the Moon will be too small to cover the Sun.
> Enjoy them while you can.

### Example script (editor channel, about 25 seconds)
> *(raw clip, boring)* This is what my client sent me.
> *(fast cut)* Here's what I did with it.
> *(edited version plays)*
> Three things made the difference: I cut every pause, I added zooms on the punchlines,
> and I synced the cuts to the beat. Want your videos edited like this? Link in bio.

Generate your own: `python scripts\ideas.py script "topic" --seconds 35 -o script.txt`
and `python scripts\ideas.py hooks "topic"`.

---

## 3. The editing checklist (retention = reach)

The algorithm mostly measures **how much of the video people watch** and **whether they rewatch, share or save**.

- [ ] **First frame is already interesting.** No logo, no black screen, no slow fade.
- [ ] **Hook text on screen in the first second** (big, 3–6 words), plus the voice saying it.
- [ ] **A visual change every 1.5–3 seconds**: new clip, zoom, text pop, angle change.
- [ ] **Captions on every word** (`captions.py`). Most people watch muted.
- [ ] **Remove every pause** (`auto-editor`). Silence = swipe.
- [ ] **Sound design**: whoosh on transitions, a "ding" or pop on key words, music at about 10–15% under the voice.
- [ ] **Zoom in 10–20% on punchlines.**
- [ ] **No dead ending.** Cut the moment the payoff lands, or loop it back to the start.
- [ ] **Vertical 1080×1920**, important stuff in the middle (the top and bottom get covered by app buttons).
- [ ] **Watch it once on your phone with sound off** before posting. Is it still clear? Still interesting?

---

## 4. Posting: YouTube

- **Shorts:** one per day if you can, at least 4 per week. Consistency beats perfection.
- **Title** (it shows on Shorts too): curiosity + keyword, under 60 characters.
- **Description:** first line = the keyword sentence. Add 3 hashtags.
- **Long-form (later, once Shorts get traction):** 6–12 minute versions of your best-performing Short topics.
  Long-form earns much more per view and builds loyal subscribers.
- **Thumbnail (long-form):** one subject, 3–5 big words max, high contrast. Upscale images with Upscayl.
- **Pin a comment** with a question to start discussion.
- **Monetisation (YPP):** 1,000 subs plus 4,000 watch hours (long-form) or 10M Shorts views in 90 days.
  Faceless is allowed, but **reused or low-effort mass content gets rejected**, so add your own script and angle.

## 5. Posting: Instagram

- **Reels are your growth engine.** Post the same video you made for Shorts (clean file, no TikTok/YouTube watermark).
- **Cover image:** set a clean cover with the title text so your grid looks organised.
  People check your grid before following.
- **Caption:** first line = hook (it's all people see). Then 1–2 lines and a question.
  3–5 relevant hashtags is enough.
- **Saves and sends (shares to DMs) matter most on Instagram.** "Useful" and "relatable" content wins here.
- **Carousels** (5–10 slides) are great for "editing tips" and get re-shown to people who didn't swipe.
- **Stories every day:** behind the scenes, polls ("which edit is better, A or B?"). This builds the followers you already have.
- **Collab posts:** team up with a creator in your niche. The video appears on both pages.
- **Bio:** what you post + who it's for + call to action.
  *e.g. "Daily space facts 🚀 | New Reel every day"* or *"Video editor ✂️ Reels & YouTube edits | DM 'EDIT' for rates"*

---

## 6. Your first 30 days

| Week | Do this |
|---|---|
| **1** | Pick the niche. Set up profile pic, bio, banner, and the same name on YT + IG. Make **7 videos** before posting anything, so you have a buffer. Post 1/day. |
| **2** | Keep posting daily. Reply to **every** comment within the first hour (signals engagement). Spend 15 min/day leaving genuine comments on bigger accounts in your niche. |
| **3** | Check analytics: which 2 videos had the best **average % viewed**? Make 3 more videos in that exact style or topic. Start one "series". |
| **4** | Double down on the winning format. Try 1 collab or 1 long-form video. Write down what worked. |

**Weekly 15-minute review** (YouTube Studio / IG Insights):
- **Swipe-away / skip rate high?** Your hook is weak. Test new hook formulas.
- **People drop off in the middle?** The video is too slow. More cuts, cut a beat.
- **Lots of views but no follows?** The content isn't a recognisable series yet, or the profile doesn't explain what you post.
- **Lots of saves/shares?** That's your winner. Make 5 more like it.

Most channels need **30–100 videos** before one breaks out. The ones that grow are the ones that didn't stop at video 20.

---

## 7. Turning followers into editing clients

- Every editor-channel video ends with **"DM 'EDIT' for rates"** or **"link in bio"**.
- Make a simple portfolio: a pinned Reel or Highlight called **"My Work"** with 3–5 before/afters.
- Reach out daily to 5 small creators (1k–50k followers) who post unedited or poorly edited videos:
  *"Hey! Loved your video on ___. I re-edited the first 15 seconds as a free sample. Want me to send it?"*
  Free samples convert far better than "do you need an editor?"
- Get a short testimonial from every happy client and post it.
- Use `python scripts\ideas.py client "what they asked for"` to plan each job quickly.

---

## 8. Never do this (it kills accounts)

- ❌ Buying followers, likes or views, or using "growth booster" bots: shadowban or deletion.
- ❌ Reuploading other people's videos or movie/TV clips without changes: copyright strikes.
- ❌ Deleting videos that "flopped". Sometimes they take off weeks later.
- ❌ Changing niche every week. The algorithm can't learn who your audience is.
- ❌ Clickbait that doesn't pay off. People swipe away, retention drops, and reach dies.
