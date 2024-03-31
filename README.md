# Whisper-API
A client to transcribe audio using the OpenAI Whisper API.

## Overview

This utility compresses audio files to under 25MB and transcribes them using OpenAI's Whisper API. It supports various audio formats including MP3, MP4, MPEG, MPGA, M4A, WAV, and WEBM.

## Installation

1. Ensure you have Python 3.6+ installed.
2. Clone this repository or download the script.
3. Install dependencies with `pip install -r requirements.txt`.
4. Install `ffmpeg` on your system as `pydub`, a library used by this utility, requires it for audio processing. Visit [FFmpeg's official site](https://ffmpeg.org/download.html) for installation instructions.

## Usage

```bash
python whisper_transcribe.py -i <input_audio_file> [--transcribe]
```

- `-i`, `--input` (required): Specify the input audio file path.
- `--transcribe` (optional): Enable transcription using OpenAI Whisper API.

Example:
```bash
python whisper_transcribe.py -i path/to/audio.mp3 --transcribe
```

## Features

- **Compression**: Automatically compresses audio files larger than 25MB.
- **Transcription**: Converts speech to text with the OpenAI Whisper API.
- **Support for Multiple Formats**: Works with a variety of audio formats, including MP3, MP4, MPEG, MPGA, M4A, WAV, and WEBM.

## Requirements

- `ffmpeg`: Required by `pydub` for audio processing.
- `pydub` and `openai`
- Transcription feature requires an OpenAI API key set in your environment variables.

## Disclaimer

Please note that while this utility facilitates audio transcription using the OpenAI Whisper API, the user is solely responsible for any and all charges incurred from the use of the OpenAI API. Ensure you have reviewed OpenAI's current pricing policies and are aware of the potential costs associated with your usage.

Furthermore, the developer of this utility cannot be held liable for any bugs, issues, or unintended behaviors in the code that may result in additional API costs to the user. Users are encouraged to thoroughly test the utility with their workflow and monitor their API usage to prevent unexpected charges.

By using this utility, you acknowledge and agree to assume full responsibility for all charges incurred and to exercise caution and due diligence in its operation.
