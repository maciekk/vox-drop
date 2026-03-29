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

```bash
vox-drop samples/sample.mp3
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

### Output

Transcription is written to stdout, so you can pipe or redirect it:

```bash
vox-drop recording.mp3 > transcript.txt
vox-drop recording.mp3 | grep "keyword"
```

### Obsidian inbox

Use `vox-drop-inbox` to transcribe a whole directory of audio files into a single Obsidian note. The note is written to `_inbox/YYYY-MM-DD vox drop.md` inside your vault. Running it again on the same day appends to the existing note.

```bash
vox-drop-inbox ~/recordings/ --vault ~/Documents/Personal/
```

Each audio file becomes a `## HH:MM — filename` section. All `vox-drop` options are supported:

```bash
vox-drop-inbox ~/recordings/ --model base --language en
vox-drop-inbox ~/recordings/ --flag-low-confidence
```

The `--vault` flag defaults to `~/Documents/Personal/`. The `_inbox` folder is created automatically if it doesn't exist.

### Batch transcription (stdout)

Use `transcribe_all.sh` to process multiple files in one go, printing to stdout. Each file is separated by a header line:

```bash
./transcribe_all.sh file1.mp3 file2.wav file3.mp3
./transcribe_all.sh --model base --language en *.mp3
```

All `vox-drop` options are supported and applied to every file.

### Low confidence flagging

Use `--flag-low-confidence` to enable word-level confidence scoring. Words below the threshold (default 50%) are marked inline with `[brackets?]`, and a summary is printed at the end:

```
this is a [mumbled?] sentence about [something?]

--- Low confidence words ---
  1:23  'mumbled'             confidence: 31%
  1:24  'something'           confidence: 42%
```

## Credits
File samples (OSR_*.wav) are from Open Speech Repository:<br>
  https://www.voiptroubleshooter.com/open_speech/american.html
