---
name: stickman-video
description: "Stickman_Video: turn a topic, article, script or outline into a stick-figure animated video plan. Produces an approved storyboard, then standalone per-shot prompts for AI video generators (Veo, Kling, Sora, Hailuo, Jimeng/即梦, Runway, etc.), plus narration script, SRT subtitles and an editing guide. Use whenever the user wants a stickman / 火柴人 / stick-figure / faceless explainer or story video, a storyboard (分镜) for one, or video-generation prompts in a stick-figure style, even if they don't say 'skill'."
---

# Stickman_Video

Direct stick-figure videos as a **film director**, not as a renderer: lock the brief, write a storyboard the user approves, then hand over generator-ready prompts and post-production assets.

Talk to the user in their language. Paths below are relative to this skill folder.

## Pipeline at a glance

| Step | Output | Gate |
|------|--------|------|
| 0. Brief | ratio, duration, style, generator, narration language | Ask only for what is missing |
| 1. Storyboard | header + shot table + narration | **Stop and wait for approval** |
| 2. Prompt pack | one standalone prompt per shot | Only after approval of the *current* storyboard |
| 3. Post kit | SRT subtitles, edit guide, title/cover copy | Optional, offer once |

## 0. Brief (setup gate)

Required before planning:

1. **Source** – topic, article, script, outline or link text.
2. **Aspect ratio** – `16:9` (YouTube/B站横屏) or `9:16` (抖音/Shorts/Reels 竖屏).
3. **Visual style** – one entry from [style catalog](references/style-catalog.md): `S1 Ink` (light/dark), `S2 Flat Pop`, `S3 Chalkboard`, `S4 Whiteboard`, `S5 Neon Night`, `S6 Paper Cutout`, `S7 Ink Wash`, `S8 Pixel Arcade`, `S9 Blueprint`, `S10 Comic Halftone`.

Defaults when omitted (state them, don't ask):

- **Duration**: 60 s.
- **Generator**: `generic` (8 s shots). See [generator profiles](references/generator-profiles.md) for shot length and prompt quirks per tool.
- **Narration language**: the user's conversation language. Add an English version only if asked.

Rules:

- If ratio **or** style is missing, ask for all missing items in **one** short message (offer the style list with one-line descriptions) and stop. Never pick them silently.
- Shot count `N = round(duration / shot_length)`; round duration to the nearest whole shot.
- Do not re-ask anything the user already answered. Time pressure does not waive the gate.

## 1. Storyboard (Phase A)

Read [storyboard template](references/storyboard-template.md), [style catalog](references/style-catalog.md) and [voice profile](references/voice-profile.md). Then:

1. Rewrite the source into a spoken narration using the **Hook → Tension → Breakdown → Payoff** arc (details in the template). Keep facts, names and numbers; never invent statistics, quotes or claims.
2. Fit narration length to duration (≈ 4–5 Chinese characters/s or ≈ 2.3–2.7 English words/s).
3. Fill the header, the character card, the voice profile and the shot table.
4. End with a clear approval question and **stop**.

Any change to ratio, duration, style, character, narrator or overall structure produces a new storyboard that needs fresh approval. Approval of an older draft does not carry over.

## 2. Prompt pack (Phase B)

Only after explicit approval, read [prompt contract](references/prompt-contract.md) and the chosen generator section of [generator profiles](references/generator-profiles.md). Deliver:

1. Global continuity block (review summary).
2. `N` standalone prompts, each fully self-contained: it repeats the **character anchor**, **style anchor** and **voice block** verbatim. No "same as before" shortcuts.
3. Stitching guide (how shot `k` ends and shot `k+1` begins).
4. Audio note (BGM continuity, SFX list, mix priority: voice > SFX > music).

Prompts are written in English (generators follow English best) unless the generator profile says otherwise (e.g. Jimeng accepts Chinese). Spoken lines stay in the narration language, quoted exactly.

## 3. Post kit (optional)

After the prompt pack, offer once (never block delivery):

- `subtitles.srt` – write the approved narration to a text file, one shot per line as `<seconds>|<narration>` (format: `examples/narration-sample.txt`), then run `python3 scripts/make_srt.py narration.txt -o subtitles.srt` (use `--max-chars 42` for English).
- Edit guide – cut points, transitions, on-screen text overlays (overlays live here, not inside generation prompts).
- Title, description, hashtags and a cover-frame prompt matching the style.

## Hard rules (all styles)

- One locked character design per role for the whole video; repeat the full anchor every shot.
- Stick figures always have **two arms and two legs**; a moving limb replaces its previous pose.
- Motion is concrete action (run, push, draw, open, fall, point), with a visual change every 2–3 s. No idle standing, no abstract morphing blobs.
- No visible text, letters, numbers or UI copy in generated footage; no speech bubbles. Narration is audio only.
- Colors are named in plain words (“warm orange”), never hex/RGB/Pantone.
- Layout follows the ratio: `16:9` stages action left→center→right; `9:16` stacks action vertically and keeps the lower 20 % and top 10 % clear for platform UI.
- Do not imitate living artists, trademarked characters or real people's likeness.

## Final check

Before every response, run the checklist at the end of the loaded reference and fix any failure first.
