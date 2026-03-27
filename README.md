# vox-drop

Transcribe speech from audio files to text using [Whisper](https://github.com/openai/whisper), running locally on your machine.

## Prerequisites

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`)

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The first run will download the Whisper model (~500 MB for `small`).

## Usage

```bash
vox-drop recording.mp3
```

### Options

```
--model {tiny,base,small,medium,large-v3}   Model size (default: small)
--language CODE                              Language code, e.g. 'en' (auto-detected if omitted)
--flag-low-confidence                        Mark uncertain words and print a summary
--confidence-threshold N                     Word probability threshold (default: 0.5)
```

### Examples

```bash
vox-drop meeting.mp3 --model base        # faster, lower accuracy
vox-drop interview.wav --language en      # skip auto-detection
vox-drop recording.mp3 --flag-low-confidence  # highlight uncertain words
vox-drop recording.mp3 --flag-low-confidence --confidence-threshold 0.7  # stricter
```

### Low confidence flagging

Use `--flag-low-confidence` to enable word-level confidence scoring. Words below the threshold (default 50%) are marked inline with `[brackets?]`, and a summary is printed at the end:

```
this is a [mumbled?] sentence about [something?]

--- Low confidence words ---
  1:23  'mumbled'             confidence: 31%
  1:24  'something'           confidence: 42%
```
