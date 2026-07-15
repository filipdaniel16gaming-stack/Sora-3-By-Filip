#!/usr/bin/env python3
"""
Skeleton: create a Sora 2 video generation job, poll for completion, and download the result.

This script is a template. Replace endpoint paths and parameters to match your provider's current API.

Usage:
  export OPENAI_API_KEY="sk-..."
  python3 scripts/generate_sora2_video.py --prompt "A calm blue cloud mascot waving" --duration 8 --resolution 720p

"""
import os
import time
import argparse
import requests
from tqdm import tqdm

API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("SORA_API_KEY")
# Base URL: adjust to your provider (OpenAI example)
BASE_URL = "https://api.openai.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def create_job(prompt, duration=8, resolution="720p", model="sora-2"):
    payload = {
        "model": model,
        "prompt": prompt,
        "resolution": resolution,
        "duration": duration,
    }
    url = f"{BASE_URL}/videos/create"
    resp = requests.post(url, json=payload, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def get_status(job_id):
    url = f"{BASE_URL}/videos/{job_id}/status"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def download_file(url, dest_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest_path, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc=dest_path) as pbar:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--duration", type=int, default=8)
    parser.add_argument("--resolution", default="720p")
    parser.add_argument("--model", default="sora-2")
    args = parser.parse_args()

    if not API_KEY:
        print("ERROR: Set OPENAI_API_KEY or SORA_API_KEY environment variable with your API key.")
        return

    print("Creating job...")
    job = create_job(args.prompt, args.duration, args.resolution, args.model)
    job_id = job.get("id") or job.get("job_id")
    print("Job created:", job)

    print("Polling for status. This may take a while...")
    while True:
        status = get_status(job_id)
        state = status.get("status") or status.get("state")
        print("Status:", state)
        if state in ("succeeded", "completed", "done"):
            # provider may return a URL or array of outputs
            video_url = status.get("url") or status.get("video_url") or (status.get("outputs") or [{}])[0].get("url")
            if video_url:
                out_path = f"output_{job_id}.mp4"
                print("Downloading:", video_url)
                download_file(video_url, out_path)
                print("Saved to", out_path)
            else:
                print("Job completed but no video URL found in status response:", status)
            break
        elif state in ("failed", "error"):
            print("Job failed:", status)
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
