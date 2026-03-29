# vox-drop

Zero effort transcribing+ path for "dictated MP3s" -> Obsidian vault.

Transcribes speech from audio files to text using [Whisper](https://github.com/openai/whisper), running locally on your machine, with some special tricks (e.g., first word in recording interpreted as a command).

## Prerequisites

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/)

## Install

```bash
uv sync
```

The first run will download the Whisper model (~500 MB for `small`).

## Usage

Two commands are available:

| Command | Input | Output |
|---|---|---|
| `transcribe` | single audio file | stdout |
| `vox-to-vault` | directory of audio files | Obsidian vault note |

## transcribe

Transcribe a single audio file to stdout:

```bash
transcribe recording.mp3
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
transcribe meeting.mp3 --model base               # faster, lower accuracy
transcribe interview.wav --language en            # skip auto-detection
transcribe recording.mp3 > transcript.txt         # save to file
transcribe recording.mp3 | grep "keyword"         # pipe output
```

### Low confidence flagging

Use `--flag-low-confidence` to enable word-level confidence scoring. Words below the threshold (default 50%) are marked inline with `[brackets?]`, and a summary is printed at the end:

```bash
transcribe recording.mp3 --flag-low-confidence
transcribe recording.mp3 --flag-low-confidence --confidence-threshold 0.7  # stricter
```

```
this is a [mumbled?] sentence about [something?]

--- Low confidence words ---
  1:23  'mumbled'             confidence: 31%
  1:24  'something'           confidence: 42%
```

## vox-to-vault

Transcribe a directory of audio files into a single Obsidian note. The note is written to `_inbox/YYYY-MM-DD vox drop.md` inside your vault. Running it again on the same day appends to the existing note.

```bash
vox-to-vault ~/recordings/ --vault ~/Documents/Personal/
```

Each audio file becomes a `## HH:MM — filename` section. The `--vault` flag defaults to `~/Documents/Personal/`. The `_inbox` folder is created automatically if it doesn't exist.

### Options

All `transcribe` options are supported, plus:

```
--vault PATH   Obsidian vault root (default: ~/Documents/Personal/)
```

### Examples

```bash
vox-to-vault ~/recordings/
vox-to-vault ~/recordings/ --vault ~/Notes/
vox-to-vault ~/recordings/ --model base --language en
vox-to-vault ~/recordings/ --flag-low-confidence
```

## Credits
File samples (OSR_*.wav) are from Open Speech Repository:<br>
  https://www.voiptroubleshooter.com/open_speech/american.html
