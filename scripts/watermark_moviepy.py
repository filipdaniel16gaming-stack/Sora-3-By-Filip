#!/usr/bin/env python3
"""
Overlay a logo onto a video using MoviePy.
Usage:
  python3 scripts/watermark_moviepy.py input.mp4 output_watermarked.mp4 assets/logo.png

"""
import sys
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

if len(sys.argv) < 4:
    print("Usage: watermark_moviepy.py input.mp4 output.mp4 logo.png")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]
logo_path = sys.argv[3]

video = VideoFileClip(input_path)
logo = (ImageClip(logo_path)
        .set_duration(video.duration)
        .resize(width=int(video.w * 0.18))  # scale logo relative to video width
        .set_pos(("right", "bottom"))
        .margin(right=10, bottom=10, opacity=0)
        .set_opacity(0.6))

final = CompositeVideoClip([video, logo])
final.write_videofile(output_path, codec="libx264", audio_codec="aac")
