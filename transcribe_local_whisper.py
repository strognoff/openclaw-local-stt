#!/usr/bin/env python3
"""Local speech-to-text transcription using faster-whisper.

This is a tiny CLI helper intended to be called by OpenClaw (or manually) to
transcribe an audio file (e.g. Telegram voice note .ogg).

It prints JSON to stdout.

Usage:
  ./transcribe_local_whisper.py /path/to/audio.ogg

Env:
  WHISPER_MODEL=tiny|base|small|medium|large-v3 (default: tiny)

Output JSON:
  {"success": true, "model": "tiny", "language": "en", "duration": 3.2, "text": "..."}
"""

import json
import os
import sys

from faster_whisper import WhisperModel


def main() -> int:
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No file path provided"}))
        return 1

    audio_path = sys.argv[1]

    model_size = os.environ.get("WHISPER_MODEL", "tiny")

    # Safe defaults for CPU-only hosts.
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_path, beam_size=5)
    text = "".join(seg.text for seg in segments).strip()

    print(
        json.dumps(
            {
                "success": True,
                "model": model_size,
                "language": getattr(info, "language", None),
                "duration": getattr(info, "duration", None),
                "text": text,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
