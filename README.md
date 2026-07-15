# Sora 2 video generation skeleton + watermarking tools

This repository contains example scripts to create a Sora 2 (text-to-video) job, download the resulting MP4, and overlay a Sora-style watermark (logo) onto the video using either FFmpeg or MoviePy.

Files added by this commit:
- scripts/generate_sora2_video.py — skeleton script to create and poll a Sora 2 job (edit endpoints/parameters for your provider)
- scripts/watermark_ffmpeg.sh — example FFmpeg command to overlay assets/logo.svg (or logo.png)
- scripts/watermark_moviepy.py — MoviePy-based overlay script
- assets/logo.svg — placeholder Sora-style logo (replace with your provided PNG if you prefer)
- README.md — usage instructions
- requirements.txt — Python dependencies for MoviePy overlay

Notes:
- Do not modify Sora.txt; it will continue to return the single word "Sora".
- You must supply a valid API key and may need organization-level access to use Sora 2 API.
- Replace assets/logo.svg with your original PNG (named logo.png) if you want the exact raster watermark.

