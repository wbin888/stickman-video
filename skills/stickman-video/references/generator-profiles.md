# Generator Profiles

Shot length drives the shot count: `N = round(duration / shot_length)`. Tool capabilities change often; treat these as defaults and follow the user's stated limits.

| Profile | Default shot | Prompt language | Audio | Notes |
|---------|-------------|-----------------|-------|-------|
| `generic` | 8 s | English | describe, may be ignored | safe default |
| `veo` (Google Veo) | 8 s | English | native dialogue + SFX | quote spoken lines exactly; include voice block |
| `sora` (OpenAI Sora) | 10 s | English | native audio on newer versions | strong with camera language |
| `kling` (可灵) | 5 s or 10 s | English or Chinese | limited | prefer 10 s; keep 1–2 actions per 5 s |
| `hailuo` (海螺/MiniMax) | 6 s | English or Chinese | none | add narration in post |
| `jimeng` (即梦/Seedance) | 5 s or 10 s | Chinese preferred | limited | write prompt in Chinese, keep anchors identical across shots |
| `runway` | 5 s or 10 s | English | none | concise prompts (< 1000 chars) |
| `image+i2v` | per tool | English | none | first generate a keyframe image per shot, then animate it; best character consistency |

## Profile rules

- **No native audio**: still write the narration and voice block in the storyboard, but in prompts replace the audio section with `Silent video, no music, no voice` and move audio to the post kit.
- **Short shots (5–6 s)**: two beats per shot (`[0–3s]`, `[3–end]`) instead of three.
- **Character drift**: recommend the `image+i2v` route — generate one reference sheet of the hero first, then use it as the image reference for every shot.
- **Length limits**: if the tool truncates long prompts, keep the anchors complete and shorten the beat descriptions.
