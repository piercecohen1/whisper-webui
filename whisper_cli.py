import argparse
import os
import time
from pydub import AudioSegment
from openai import OpenAI
from groq import Groq
import pyperclip

def get_audio_info(input_file):
    print(f"Loading audio file: {input_file}")
    audio = AudioSegment.from_file(input_file)
    duration = len(audio) / 1000  # Duration in seconds
    print(f"Audio duration: {duration:.2f} seconds")
    return duration

def calculate_bitrate(input_file, target_size):
    duration = get_audio_info(input_file)
    bitrate = (target_size * 8) / (1.048576 * duration)
    print(f"Calculated bitrate: {bitrate:.2f} kbps")
    return int(bitrate)

def compress_audio(input_file, output_file, bitrate):
    print(f"Compressing audio file: {input_file}")
    start_time = time.time()
    audio = AudioSegment.from_file(input_file)
    print(f"Exporting compressed audio to: {output_file}")
    audio.export(output_file, format='mp3', bitrate=f'{bitrate}k')
    end_time = time.time()
    compression_time = end_time - start_time
    print(f"Audio compression completed in {compression_time:.2f} seconds.")

def is_valid_audio_format(input_file):
    valid_formats = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    _, extension = os.path.splitext(input_file)
    return extension.lower() in valid_formats

def transcribe_audio_openai(input_file, output_file, copy_to_clipboard):
    print(f"Transcribing audio file using OpenAI: {input_file}")
    client = OpenAI()
    with open(input_file, "rb") as audio_file:
        start_time = time.time()
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        end_time = time.time()
        transcription_time = end_time - start_time
        print(f"Audio transcription completed in {transcription_time:.2f} seconds.")
    
    save_transcript(transcript, output_file, copy_to_clipboard)

def transcribe_audio_groq(input_file, output_file, copy_to_clipboard):
    print(f"Transcribing audio file using Groq: {input_file}")
    client = Groq()
    with open(input_file, "rb") as file:
        start_time = time.time()
        transcription = client.audio.transcriptions.create(
            file=(input_file, file.read()),
            model="whisper-large-v3",
        )
        end_time = time.time()
        transcription_time = end_time - start_time
        print(f"Audio transcription completed in {transcription_time:.2f} seconds.")
    
    save_transcript(transcription.text, output_file, copy_to_clipboard)

def save_transcript(transcript, output_file, copy_to_clipboard):
    with open(output_file, "w") as transcript_file:
        transcript_file.write(transcript)
    print(f"Transcript saved to: {output_file}")

    if copy_to_clipboard:
        pyperclip.copy(transcript)
        print("Transcription text copied to clipboard.")

def main():
    parser = argparse.ArgumentParser(description='Compress audio file and transcribe using OpenAI or Groq Whisper API')
    parser.add_argument('-i', '--input', required=True, help='Input audio file')
    parser.add_argument('-o', '--output', help='Output filename for the transcript')
    parser.add_argument('--compress-only', action='store_true', help='Compress the audio file only (no transcription)')
    parser.add_argument('-c', '--clipboard', action='store_true', help='Copy the transcription text to the system clipboard')
    parser.add_argument('--api', choices=['openai', 'groq'], default='openai', help='Choose API for transcription (default: openai)')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    copy_to_clipboard = args.clipboard
    api_choice = args.api

    print(f"Input file: {input_file}")

    if not is_valid_audio_format(input_file):
        print('Invalid audio format. Supported formats: mp3, mp4, mpeg, mpga, m4a, wav, webm')
        return

    file_size = os.path.getsize(input_file) / (1024 * 1024)  # File size in MB
    print(f"Input file size: {file_size:.2f} MB")

    if file_size > 25:
        target_size = 24.9 * 1024  # Target size in kilobytes (just under 25MB)
        print(f"Target size: {target_size} KB")

        bitrate = calculate_bitrate(input_file, target_size)

        compressed_file = f'{os.path.splitext(input_file)[0]}_compressed.mp3'
        compress_audio(input_file, compressed_file, bitrate)
        input_file = compressed_file
    else:
        print("Input file size is within the allowed limit. No compression needed.")

    if not args.compress_only:
        if output_file is None:
            transcript_file = f'{os.path.splitext(input_file)[0]}_transcript.txt'
        else:
            transcript_file = output_file
        
        if api_choice == 'openai':
            transcribe_audio_openai(input_file, transcript_file, copy_to_clipboard)
        else:
            transcribe_audio_groq(input_file, transcript_file, copy_to_clipboard)

if __name__ == '__main__':
    main()