import argparse
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

from transcribe import WORD_CONFIDENCE_THRESHOLD, load_model, transcribe_file

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".opus", ".aac", ".wma", ".mp4", ".webm"}
DEFAULT_VAULT = Path("~/Documents/Personal/")


def collect_audio_files(directory: Path) -> list[Path]:
    return sorted(
        f for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
    )


def parse_recorded_time(stem: str) -> str | None:
    """Return 'HH:MM' parsed from a YYMMDD_HHMM filename stem, or None if it doesn't match."""
    try:
        dt = datetime.strptime(stem, "%y%m%d_%H%M")
        return dt.strftime("%H:%M")
    except ValueError:
        return None


def classify_entry(text: str) -> tuple[str, str]:
    """Parse voice command prefix. Returns (type, content) where type is 'task'|'note'|'continue'."""
    words = text.split()
    first = words[0].lower().rstrip(".,!?") if words else ""
    rest = " ".join(words[1:]).strip() if len(words) > 1 else ""
    if first in ("task", "note", "continue"):
        return first, rest
    return "note", text


def _get_duration(path: Path) -> float | None:
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe a directory of audio files into an Obsidian inbox note."
    )
    parser.add_argument("directory", type=Path, help="Directory containing audio files")
    parser.add_argument(
        "--vault", type=Path, default=DEFAULT_VAULT,
        help="Obsidian vault root (default: ~/Documents/Personal/)",
    )
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model size (default: small)",
    )
    parser.add_argument("--language", default=None, help="Language code, e.g. 'en'")
    parser.add_argument("--flag-low-confidence", action="store_true",
                        help="Mark uncertain words with [brackets?]")
    parser.add_argument(
        "--confidence-threshold", type=float, default=WORD_CONFIDENCE_THRESHOLD,
        help=f"Word probability below this is flagged (default: {WORD_CONFIDENCE_THRESHOLD})",
    )
    args = parser.parse_args()

    directory = args.directory.expanduser().resolve()
    vault = args.vault.expanduser().resolve()

    if not directory.is_dir():
        sys.exit(f"Not a directory: {directory}")

    audio_files = collect_audio_files(directory)
    if not audio_files:
        sys.exit(f"No audio files found in {directory}")

    inbox = vault / "_inbox"
    if not vault.exists():
        print(f"Warning: vault path does not exist, creating: {vault}", file=sys.stderr)
    if inbox.exists() and not inbox.is_dir():
        sys.exit(f"_inbox exists but is not a directory: {inbox}")
    inbox.mkdir(parents=True, exist_ok=True)

    today = date.today()
    out_path = inbox / f"{today.isoformat()} vox drop.md"
    file_exists = out_path.exists()

    print(f"Loading model '{args.model}'...", file=sys.stderr)
    model = load_model(args.model)

    # Each entry: {'type': 'note'|'task', 'content': str, 'timestamp': str, 'filename': str}
    entries = []
    for audio_file in audio_files:
        print(f"Transcribing: {audio_file.name}", file=sys.stderr)
        recorded = parse_recorded_time(audio_file.stem)
        wall_time = recorded if recorded is not None else f"[{datetime.now().strftime('%H:%M')}]"
        transcript = transcribe_file(
            model, audio_file,
            language=args.language,
            flag_low_confidence=args.flag_low_confidence,
            confidence_threshold=args.confidence_threshold,
        )
        text = transcript.strip()

        if not text:
            size_kb = audio_file.stat().st_size / 1024
            duration = _get_duration(audio_file)
            dur_str = f"{duration:.1f}s" if duration is not None else "unknown"
            body = f"(no voice) — {size_kb:.1f} KB, {dur_str}"
            entries.append({"type": "note", "content": body, "timestamp": wall_time, "filename": audio_file.name})
            continue

        kind, body = classify_entry(text)

        if kind == "task":
            entries.append({"type": "task", "content": body, "timestamp": wall_time, "filename": audio_file.name})
        elif kind == "continue":
            if entries:
                sep = " " if entries[-1]["content"] else ""
                entries[-1]["content"] += sep + body
            else:
                entries.append({"type": "note", "content": body, "timestamp": wall_time, "filename": audio_file.name})
        else:
            entries.append({"type": "note", "content": body, "timestamp": wall_time, "filename": audio_file.name})

    tasks = [e for e in entries if e["type"] == "task"]
    notes = [e for e in entries if e["type"] == "note"]

    output_parts = []
    if tasks:
        section = "## Tasks\n\n"
        section += "".join(f"- [ ] {e['content']}\n" for e in tasks)
        output_parts.append(section)
    if notes:
        section = "## Notes\n"
        for e in notes:
            section += f"\n### {e['timestamp']} — {e['filename']}\n\n{e['content']}\n"
        output_parts.append(section)

    mode = "a" if file_exists else "w"
    with out_path.open(mode, encoding="utf-8") as f:
        if not file_exists:
            f.write(f"---\ntags: [vox-drop, inbox]\ncreated: {today.isoformat()}\n---\n")
        for part in output_parts:
            f.write("\n" + part)

    print(f"Written to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
