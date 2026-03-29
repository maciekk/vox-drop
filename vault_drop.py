import argparse
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

    sections = []
    for audio_file in audio_files:
        print(f"Transcribing: {audio_file.name}", file=sys.stderr)
        wall_time = datetime.now().strftime("%H:%M")
        transcript = transcribe_file(
            model, audio_file,
            language=args.language,
            flag_low_confidence=args.flag_low_confidence,
            confidence_threshold=args.confidence_threshold,
        )
        sections.append(f"\n## {wall_time} — {audio_file.name}\n\n{transcript.strip()}\n")

    mode = "a" if file_exists else "w"
    with out_path.open(mode, encoding="utf-8") as f:
        if not file_exists:
            f.write(f"---\ntags: [vox-drop, inbox]\ncreated: {today.isoformat()}\n---\n")
        for section in sections:
            f.write(section)

    print(f"Written to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
