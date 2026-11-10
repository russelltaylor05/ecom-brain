# Local setup and test boundaries

Source: https://github.com/maddexritter-rgb/vibe-editing

Pinned revision: `a342d7173d49b6be43e477a0041aad6014fbf377` (MIT licensed).
The complete source and its license are downloaded into `tmp/vibe-editing/upstream` by setup.
The wrapper verifies the revision and refuses to overwrite an unrelated checkout.

## Adapted onboarding

The upstream interview covers brands, tooling, AssemblyAI, Gemini, optional Groq, delivery,
brand assets, and a user-supplied test clip. Local setup preserves the tool check and sample
render, defers the brand interview until real footage is supplied, and records all service
connections as skipped. It writes local progress into `tmp/vibe-editing/status.json`.
It never changes company setup state or writes `~/.config/vibe-editing`.

Required: Git, Python 3.10+, and FFprobe. Setup installs Pillow 12.0.0 and imageio-ffmpeg 0.6.0
into its virtual environment. The latter supplies a private FFmpeg with libass, libx264, and AAC;
the wrapper prepends its runtime `bin/` only for its process and children. The machine's existing
FFmpeg is unchanged. If FFprobe is absent, install it with the platform package manager (on macOS:
`brew install ffmpeg`) and rerun doctor. The doctor verifies the actual filters and encoders:
some system FFmpeg builds lack libass even when FFmpeg itself is installed.
The upstream source and dependency downloads need internet access; rendering uses no
media service. No Node, Premiere, Filmcraft bridge, Tesseract, rclone, yt-dlp, Whisper model,
OpenCV, SciPy, or provider SDK is required for this mode.

The full upstream requirements also include NumPy, OpenCV, SciPy, librosa, soundfile, matplotlib,
requests, httpx, num2words, wordfreq, pyspellchecker, yt-dlp, and faster-whisper. Do not install
that stack for a local render smoke test. The upstream doctor requires AssemblyAI and imports
credential loading, so use the adapter's doctor for local mode.

## What actually runs

The adapter runs the upstream manifest engine, upstream cut and mix stages, caption formatter,
and spice caption generator. It substitutes libx264 for the macOS hardware encoder in cut and
mix and uses the generator's software encoding fallback. It adds a simple center crop to
1080 × 1920 and a pinned-word caption stage. These adapters are versioned by source hashes for
cache invalidation. Face tracking, service calls, upstream caption transcription, automatic
layout, and live editorial access are never invoked. The agent makes editorial decisions.

Local project manifest:

```json
{
  "title": "my-clip",
  "pipeline": "eb-local",
  "output": {"name": "my-clip.mp4"},
  "stages": {
    "cut": {
      "source_video": "00_SOURCE/input.mp4",
      "source_audio": "00_SOURCE/input.mp4",
      "spec": "10_WORK/cuts.json",
      "snap_silence": false
    },
    "reframe": {},
    "captions": {"words": "10_WORK/words.json", "director": "10_WORK/style.json"},
    "mix": {"music": null, "voice_lufs": -16, "limiter": 0.45}
  }
}
```

Cuts: `{"segments":[{"in":0,"out":4},{"in":6,"out":10}]}`.
Words: `{"words":[{"word":"Hello","start":0.2,"end":0.6}]}`.
Word times refer to the assembled cut, not the original source. Style:
`{"words":{"0":{"w":"strong","c":"speaker"}},"voice_spans":[]}`.
The formatter can merge tokens, so style indices refer to normalized words; inspect the generated
`10_WORK/normalized.json` when authoring a style stream. The local mode keeps the original
upstream spice preset and scales it to the output frame. It avoids the missing upstream
`caption-clips/presets/spice_1080.json` reference by passing `spice.json` explicitly.

## Smoke result

Smoke generates an eight-second synthetic landscape source with a test tone, cuts two sections,
center-crops, burns supplied captions, levels audio, and renders through the actual upstream
engine. It checks H.264/AAC, dimensions, duration, complete decoding, a visible caption difference,
and cache reuse on a second render. It saves logs, a sample frame, contract, and `report.json`.
Run it in a fresh project directory; it refuses to overwrite earlier test evidence.

Synthetic timed words are a rendering fixture, not a transcription of the tone. This test does
not establish speech accuracy, editorial selection quality, moving-face framing, real brand
approval, URL ingest, music rights, cloud audits, or delivery. A real onboarding pass still needs
a user-supplied clip and visual/audio review.
