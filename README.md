# vox-drop

Transcribe speech from audio files to text using [Whisper](https://github.com/openai/whisper), running locally on your machine.

## Prerequisites

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`)

## Install

```bash
uv sync
```

The first run will download the Whisper model (~500 MB for `small`).

## Usage

Two commands are available:

| Command | Input | Output |
|---|---|---|
| `vox-drop` | single audio file | stdout |
| `vox-drop-inbox` | directory of audio files | Obsidian vault note |

## vox-drop

Transcribe a single audio file to stdout:

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
vox-drop meeting.mp3 --model base               # faster, lower accuracy
vox-drop interview.wav --language en            # skip auto-detection
vox-drop recording.mp3 > transcript.txt         # save to file
vox-drop recording.mp3 | grep "keyword"         # pipe output
```

### Low confidence flagging

Use `--flag-low-confidence` to enable word-level confidence scoring. Words below the threshold (default 50%) are marked inline with `[brackets?]`, and a summary is printed at the end:

```bash
vox-drop recording.mp3 --flag-low-confidence
vox-drop recording.mp3 --flag-low-confidence --confidence-threshold 0.7  # stricter
```

```
this is a [mumbled?] sentence about [something?]

--- Low confidence words ---
  1:23  'mumbled'             confidence: 31%
  1:24  'something'           confidence: 42%
```

## vox-drop-inbox

Transcribe a directory of audio files into a single Obsidian note. The note is written to `_inbox/YYYY-MM-DD vox drop.md` inside your vault. Running it again on the same day appends to the existing note.

```bash
vox-drop-inbox ~/recordings/ --vault ~/Documents/Personal/
```

Each audio file becomes a `## HH:MM — filename` section. The `--vault` flag defaults to `~/Documents/Personal/`. The `_inbox` folder is created automatically if it doesn't exist.

### Options

All `vox-drop` options are supported, plus:

```
--vault PATH   Obsidian vault root (default: ~/Documents/Personal/)
```

### Examples

```bash
vox-drop-inbox ~/recordings/
vox-drop-inbox ~/recordings/ --vault ~/Notes/
vox-drop-inbox ~/recordings/ --model base --language en
vox-drop-inbox ~/recordings/ --flag-low-confidence
```

## Batch transcription to stdout

Use `transcribe_all.sh` to process multiple files in one go, printing to stdout. Each file is separated by a header line:

```bash
./transcribe_all.sh file1.mp3 file2.wav file3.mp3
./transcribe_all.sh --model base --language en *.mp3
```

## Credits
File samples (OSR_*.wav) are from Open Speech Repository:<br>
  https://www.voiptroubleshooter.com/open_speech/american.html
