import argparse
import sys
from pathlib import Path

from faster_whisper import WhisperModel

WORD_CONFIDENCE_THRESHOLD = 0.5


def format_timestamp(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(description="Transcribe speech in an audio file to text.")
    parser.add_argument("file", type=Path, help="Path to audio file (MP3, WAV, etc.)")
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model size (default: small)",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Language code, e.g. 'en' (auto-detected if omitted)",
    )
    parser.add_argument(
        "--flag-low-confidence",
        action="store_true",
        help="Mark uncertain words with [brackets?] and print a summary",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=WORD_CONFIDENCE_THRESHOLD,
        help=f"Word probability below this is flagged (default: {WORD_CONFIDENCE_THRESHOLD})",
    )
    args = parser.parse_args()

    if not args.file.exists():
        sys.exit(f"File not found: {args.file}")

    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    transcribe_opts = dict(language=args.language)
    if args.flag_low_confidence:
        transcribe_opts["word_timestamps"] = True

    segments, info = model.transcribe(str(args.file), **transcribe_opts)

    flagged_words = []

    for segment in segments:
        if not args.flag_low_confidence:
            print(segment.text.strip())
            continue

        parts = []
        for word in segment.words:
            text = word.word
            if word.probability < args.confidence_threshold:
                text = f"[{text.strip()}?]"
                flagged_words.append((word.start, word.word.strip(), word.probability))
            parts.append(text)
        print("".join(parts).strip())

    if flagged_words:
        print("\n--- Low confidence words ---")
        for start, word, prob in flagged_words:
            ts = format_timestamp(start)
            print(f"  {ts}  {word!r:20s}  confidence: {prob:.0%}")


if __name__ == "__main__":
    main()
