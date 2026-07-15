#!/usr/bin/env bash
# Example FFmpeg watermark overlay
# Usage:
#   bash scripts/watermark_ffmpeg.sh input.mp4 output_watermarked.mp4 assets/logo.png

INPUT="$1"
OUTPUT="$2"
LOGO_PATH="$3"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ] || [ -z "$LOGO_PATH" ]; then
  echo "Usage: $0 input.mp4 output.mp4 logo.png"
  exit 1
fi

# Place logo in bottom-right with 10px margin and 50% opacity
ffmpeg -i "$INPUT" -i "$LOGO_PATH" -filter_complex \
  "[1]format=rgba,colorchannelmixer=aa=0.5[logo];[0][logo]overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
  -c:a copy -y "$OUTPUT"

echo "Wrote $OUTPUT"
