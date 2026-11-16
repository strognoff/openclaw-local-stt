# openclaw-local-stt

Local speech-to-text (STT) helper for OpenClaw, using **faster-whisper**.

This repo provides a tiny CLI script that transcribes an audio file (e.g. Telegram voice notes saved as `.ogg`) and prints JSON.

## Why

- **Runs locally** (no cloud STT API keys)
- **Fast** on CPU for short voice notes
- Simple interface that’s easy for OpenClaw agents/tools to call

## Requirements

- Python **3.10+** (3.12 recommended)
- PyAV is constrained below 17 because faster-whisper currently passes `metadata_errors` to its decoder, an argument removed in PyAV 17
- `ffmpeg` may be needed depending on audio formats and your environment

## Install

```bash
git clone https://github.com/strognoff/openclaw-local-stt
cd openclaw-local-stt

python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Usage

```bash
# Optional: choose model size (default: tiny)
export WHISPER_MODEL=tiny

python transcribe_local_whisper.py /path/to/voice_note.ogg
```

Example output:

```json
{"success": true, "model": "tiny", "language": "en", "duration": 3.2, "text": "hello"}
```

## Using with OpenClaw

This is designed to be called via OpenClaw’s `exec` tool from an agent, for example:

- When OpenClaw receives a Telegram voice note it saves the file under something like:
  - `~/.openclaw/media/inbound/<file>.ogg`

Then the agent can run:

```bash
python /path/to/openclaw-local-stt/transcribe_local_whisper.py ~/.openclaw/media/inbound/<file>.ogg
```

…and parse the JSON to get the transcript.

### Notes

- Model downloads happen on first run. If you pick larger models they will be slower on CPU.
- If you get audio decode errors, install `ffmpeg`:

```bash
sudo apt-get update && sudo apt-get install -y ffmpeg
```

## Security

- The script does **not** upload audio anywhere.
- Treat transcripts as potentially sensitive; avoid logging them publicly.
