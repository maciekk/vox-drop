# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

Requires ffmpeg installed on the system.

## Usage

```bash
vox-drop recording.mp3
vox-drop recording.mp3 --model base --language en
```

## Architecture

Single-file CLI tool (`transcribe.py`) that uses `faster-whisper` to transcribe audio files to text locally via Whisper models. Entry point is `main()`, registered as the `vox-drop` console script in `pyproject.toml`. No tests, no linting configured.
