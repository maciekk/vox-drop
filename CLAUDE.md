# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
uv sync
```

Requires ffmpeg installed on the system.

## Usage

```bash
transcribe recording.mp3
transcribe recording.mp3 --model base --language en
```

## Architecture

Two CLI tools:
- `transcribe.py` — transcribes a single audio file to stdout. Entry point `main()`, registered as the `transcribe` console script.
- `process_drop.py` — transcribes a directory of audio files and writes them into an Obsidian vault note. Entry point `main()`, registered as the `vox-to-vault` console script.

Both registered in `pyproject.toml`. No tests, no linting configured.
