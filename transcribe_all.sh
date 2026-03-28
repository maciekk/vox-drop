#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 [--model SIZE] [--language CODE] [--flag-low-confidence] [--confidence-threshold N] file1.mp3 ..." >&2
    exit 1
}

FLAGS=()
FILES=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model|--language|--confidence-threshold)
            FLAGS+=("$1" "$2")
            shift 2
            ;;
        --flag-low-confidence)
            FLAGS+=("$1")
            shift
            ;;
        --*)
            echo "Unknown option: $1" >&2
            usage
            ;;
        *)
            FILES+=("$1")
            shift
            ;;
    esac
done

if [[ ${#FILES[@]} -eq 0 ]]; then
    usage
fi

for file in "${FILES[@]}"; do
    printf '\033[90m%s\033[0m\n' "$(printf '─%.0s' $(seq 1 80))"
    printf '\033[1;36m%s\033[0m\n' "$file"
    python3 "$(dirname "$0")/transcribe.py" "${FLAGS[@]+"${FLAGS[@]}"}" "$file"
done
