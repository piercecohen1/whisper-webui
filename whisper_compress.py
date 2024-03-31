import argparse
import os
from pydub import AudioSegment

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
    audio = AudioSegment.from_file(input_file)
    print(f"Exporting compressed audio to: {output_file}")
    audio.export(output_file, format='mp3', bitrate=f'{bitrate}k')
    print("Audio compression completed.")

def is_valid_audio_format(input_file):
    valid_formats = ['.mp3', '.wav', '.aac', '.flac', '.ogg']
    _, extension = os.path.splitext(input_file)
    return extension.lower() in valid_formats

def main():
    parser = argparse.ArgumentParser(description='Compress audio file to just under 25MB')
    parser.add_argument('-i', '--input', required=True, help='Input audio file')
    args = parser.parse_args()

    input_file = args.input

    print(f"Input file: {input_file}")

    if not is_valid_audio_format(input_file):
        print('Invalid audio format. Supported formats: mp3, wav, aac, flac, ogg')
        return

    target_size = 24.9 * 1024  # Target size in kilobytes (just under 25MB)
    print(f"Target size: {target_size} KB")

    bitrate = calculate_bitrate(input_file, target_size)

    output_file = f'{os.path.splitext(input_file)[0]}_compressed.mp3'

    compress_audio(input_file, output_file, bitrate)
    print(f'Audio file compressed successfully: {output_file}')

if __name__ == '__main__':
    main()
