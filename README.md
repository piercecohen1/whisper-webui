# Whisper Web UI

This project provides both a Streamlit web application (`whisper_webui.py`) and a command-line interface (`whisper_cli.py`) for transcribing audio files using the Whisper Large v3 model via either the OpenAI or Groq API. It offers a user-friendly interface for uploading audio, processing it, and obtaining transcriptions quickly and efficiently.

![Screenshot_003781](https://github.com/piercecohen1/whisper-webui/assets/19575201/b1eedffc-1cdb-4671-bfcb-156d770d68ea)

## Features

- Automatic compression for files larger than 25MB
- Support for multiple audio formats (mp3, mp4, mpeg, mpga, m4a, wav, webm)
- Transcription using Whisper Large v3 model through OpenAI or Groq API
- Display of transcription time and results
- Option to copy transcript to clipboard
- Ability to save transcript to a file
- Both web-based and command-line interfaces

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/audio-transcription-app.git
   cd audio-transcription-app
   ```

2. Install the required dependencies:
   ```
   pip install streamlit groq openai pydub pyperclip
   ```

3. Set up your API keys as environment variables:
   ```
   export OPENAI_API_KEY='your_openai_api_key_here'
   export GROQ_API_KEY='your_groq_api_key_here'
   ```

## Usage

### Streamlit Web Application (`whisper_webui.py`)

1. Run the Streamlit app:
   ```
   streamlit run whisper_webui.py
   ```

2. Open your web browser and navigate to the provided local URL (typically `http://localhost:8501`).

3. Use the interface to upload an audio file, process it, and view the transcription results.

### Command-Line Interface (`whisper_cli.py`)

The CLI version offers more flexibility and options for transcription. Here's how to use it:

```
python whisper_cli.py [-h] -i INPUT [-o OUTPUT] [--compress-only] [-c] [--api {openai,groq}]
```

Options:
- `-i INPUT`, `--input INPUT`: Input audio file (required)
- `-o OUTPUT`, `--output OUTPUT`: Output filename for the transcript
- `--compress-only`: Compress the audio file only (no transcription)
- `-c`, `--clipboard`: Copy the transcription text to the system clipboard
- `--api {openai,groq}`: Choose API for transcription (default: openai)

Examples:

1. Transcribe an audio file using OpenAI API:
   ```
   python whisper_cli.py -i input.mp3 -o transcript.txt
   ```

2. Transcribe using Groq API and copy to clipboard:
   ```
   python whisper_cli.py -i input.wav --api groq -c
   ```

3. Compress an audio file without transcribing:
   ```
   python whisper_cli.py -i large_file.mp3 --compress-only
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is released under the MIT License.
