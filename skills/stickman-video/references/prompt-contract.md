# Prompt Contract (Phase B)

Use only after the user approved the current storyboard.

## Package order

1. **Global continuity block** – ratio, duration, `N`, style ID, character cards, palette roles, voice block, music arc. (Review summary only; each prompt still repeats the anchors.)
2. **Shot prompts 1…N** – standalone, in the order below.
3. **Stitching guide** – a table: shot `k` last frame → shot `k+1` first frame, cut type.
4. **Audio note** – BGM continuity from shot 1, SFX list per shot, mix priority voice > SFX > music, TTS fallback if needed.

## Standalone prompt order

Each shot prompt is a single block containing, in order:

1. **Spec**: `≈{shot_length}-second clip, {ratio}, 24 fps, 720p or higher.`
2. **Style anchor** – verbatim from the style catalog.
3. **Character anchor(s)** – verbatim, for every visible role.
4. **Palette roles** – plain color words.
5. **Layout** – per ratio (`16:9` left→center→right staging; `9:16` vertical stacking, keep top 10 % and bottom 20 % clear).
6. **First frame** – inherited state from the previous shot (position, facing, props held).
7. **Beats** – `[0–3s]`, `[3–6s]`, `[6–end]` (two beats for 5–6 s shots), each a concrete action tied to the spoken idea.
8. **Camera** – one move per beat at most (static, slow push, pan, whip, zoom).
9. **Spoken line** – `Audio-only narration, exactly: "…"` (narration language, unchanged). Omit if the generator has no audio.
10. **Voice block** – verbatim from `voice-profile.md`.
11. **Music & SFX** – shot 1 defines the BGM; later shots say `continue the same BGM seamlessly`.
12. **Last frame** – the state handed to the next shot.
13. **Negatives** – common + style-specific.

## Common negatives

`No visible text, letters, numbers, subtitles or logos. No speech bubbles. No extra limbs or fingers on the stick figure; exactly two arms and two legs. No character redesign between shots. No photorealistic humans. No watermark.`

## Example shot (S7 Ink Wash, 16:9, veo, 8 s)

```
≈8-second clip, 16:9, 24 fps, 720p.
Traditional Chinese ink wash painting style 2D animation on warm rice paper with large empty negative space, soft black ink bleeding into the paper, misty mountains and water rendered in light grey washes, occasional single red seal-stamp accent shapes with no characters.
Character: A stick figure painted with a single confident calligraphy brush stroke per limb, round head as an ink circle with a light grey wash fill, two arms and two legs, a flowing light grey scholar's robe suggested by two loose brush strokes.
Palette: ink black and greys dominant; vermilion red marks the turning point; pale indigo for water.
Layout: figure starts on the left third, river flows to the right third, empty sky above.
First frame: the figure stands at the riverbank holding a small boat paddle, facing right.
[0–3s] Ink spreads from the left to reveal a calm river; the figure steps into a small boat.
[3–6s] He paddles; the boat glides right as the camera pans slowly with him.
[6–8s] He leans over the side and the sword slips into the water; a vermilion ripple spreads.
Audio-only narration, exactly: "他的剑掉进了江里，他却在船边刻了个记号。"
Narrator voice: adult male in his 40s speaking standard Mandarin Chinese, steady warm low timbre, measured storyteller delivery, medium-slow pace with clear pauses, close-mic dry studio recording with no reverb.
Music: soft guzheng and xiao flute begin; SFX: brush swish, water drip, gentle splash.
Last frame: close on the boat side, the figure's hand lifting a small knife toward the wood.
No visible text, letters, numbers, subtitles or logos. No speech bubbles. Exactly two arms and two legs. No character redesign. No photorealistic humans. No watermark. No readable Chinese characters or seal text, no anime faces, no saturated modern colors, no 3D.
```

## Final checklist (prompts)

- [ ] Storyboard approved in its current form.
- [ ] `N` prompts, each standalone with style, character and voice anchors verbatim.
- [ ] Spoken lines match the approved narration exactly.
- [ ] Each last frame matches the next first frame (or a planned cut).
- [ ] No text in footage, no color codes, negatives appended.
- [ ] Stitching guide and audio note included.
