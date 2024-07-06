import streamlit as st
import os
import time
from pydub import AudioSegment
from groq import Groq
from openai import OpenAI
import tempfile
import pyperclip
import requests
import json

def get_audio_info(input_file):
    audio = AudioSegment.from_file(input_file)
    duration = len(audio) / 1000  # Duration in seconds
    return duration

def calculate_bitrate(duration, target_size):
    bitrate = (target_size * 8) / (1.048576 * duration)
    return int(bitrate)

def compress_audio(input_file, bitrate):
    audio = AudioSegment.from_file(input_file)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio.export(temp_file.name, format='mp3', bitrate=f'{bitrate}k')
    return temp_file.name

def is_valid_audio_format(filename):
    valid_formats = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    _, extension = os.path.splitext(filename)
    return extension.lower() in valid_formats

def upload_to_tmpfiles(file_path):
    url = 'https://tmpfiles.org/api/v1/upload'
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        response_data = json.loads(response.text)
        # The API returns a data URL, we need to modify it to get the direct file URL
        data_url = response_data['data']['url']
        file_url = data_url.replace('https://tmpfiles.org/', 'https://tmpfiles.org/dl/')
        return file_url
    else:
        raise Exception(f"File upload failed with status code {response.status_code}")

def transcribe_audio_groq(input_file):
    client = Groq()
    with open(input_file, "rb") as file:
        start_time = time.time()
        transcription = client.audio.transcriptions.create(
            file=(input_file, file.read()),
            model="whisper-large-v3",
        )
        end_time = time.time()
    return transcription.text, end_time - start_time

def transcribe_audio_openai(input_file):
    client = OpenAI()
    with open(input_file, "rb") as audio_file:
        start_time = time.time()
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        end_time = time.time()
    return transcript, end_time - start_time

def transcribe_audio_fal(input_file):
    url = "https://fal.run/fal-ai/wizper"
    headers = {
        "Authorization": f"Key {os.environ.get('FAL_KEY')}",
        "Content-Type": "application/json"
    }
    
    # Upload the file and get the URL
    audio_url = upload_to_tmpfiles(input_file)
    
    data = {
        "audio_url": audio_url,
        "task": "transcribe",
        "language": "en",
        "chunk_level": "segment",
        "version": "3"
    }
    
    start_time = time.time()
    response = requests.post(url, headers=headers, json=data)
    end_time = time.time()
    
    if response.status_code == 200:
        result = response.json()
        return result["text"], end_time - start_time
    else:
        raise Exception(f"Fal API request failed with status code {response.status_code}")

def save_transcript_to_file(transcript, filename):
    try:
        with open(filename, "w") as f:
            f.write(transcript)
        return True
    except Exception as e:
        st.error(f"Failed to save transcript: {str(e)}")
        return False

def main():
    st.title("Whisper Web UI")

    # Use session state to store the transcript and user confirmation
    if 'transcript' not in st.session_state:
        st.session_state.transcript = ""
    if 'transcription_time' not in st.session_state:
        st.session_state.transcription_time = 0
    if 'fal_disclaimer_accepted' not in st.session_state:
        st.session_state.fal_disclaimer_accepted = False

    # API selection
    api_choice = st.radio("Select API for transcription:", ("OpenAI", "Groq", "Fal"))

    # Fal API disclaimer
    if api_choice == "Fal" and not st.session_state.fal_disclaimer_accepted:
        with st.expander("⚠️ Important Disclaimer for Fal API Usage", expanded=True):
            st.warning(
                "By using the Fal API option, you agree to the following:\n\n"
                "1. Your audio file will be uploaded to tmpfiles.org.\n"
                "2. The uploaded file will be publicly accessible for 60 minutes.\n"
                "3. After 60 minutes, the file will be automatically deleted from tmpfiles.org.\n\n"
                "This is necessary because the Fal API requires a URL\n\n"
                "Please ensure that you have the necessary rights to upload and make your audio file temporarily public."
            )
            st.session_state.fal_disclaimer_accepted = st.checkbox("I understand and agree to proceed")

    if api_choice != "Fal" or st.session_state.fal_disclaimer_accepted:
        uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"])

        if uploaded_file is not None:
            st.audio(uploaded_file, format="audio/mp3")

            if st.button("Process Audio"):
                with st.spinner("Processing audio..."):
                    # Save uploaded file temporarily
                    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1])
                    temp_input.write(uploaded_file.getvalue())
                    temp_input.close()

                    file_size = os.path.getsize(temp_input.name) / (1024 * 1024)  # File size in MB
                    st.write(f"Input file size: {file_size:.2f} MB")

                    if file_size > 25:
                        st.write("File size exceeds 25MB. Compressing...")
                        target_size = 24.9 * 1024  # Target size in kilobytes (just under 25MB)
                        duration = get_audio_info(temp_input.name)
                        bitrate = calculate_bitrate(duration, target_size)
                        compressed_file = compress_audio(temp_input.name, bitrate)
                        input_file = compressed_file
                        st.write("Compression complete.")
                    else:
                        st.write("File size is within the allowed limit. No compression needed.")
                        input_file = temp_input.name

                    st.write(f"Transcribing audio using {api_choice} API...")
                    try:
                        if api_choice == "OpenAI":
                            st.session_state.transcript, st.session_state.transcription_time = transcribe_audio_openai(input_file)
                        elif api_choice == "Groq":
                            st.session_state.transcript, st.session_state.transcription_time = transcribe_audio_groq(input_file)
                        else:  # Fal
                            st.session_state.transcript, st.session_state.transcription_time = transcribe_audio_fal(input_file)
                        st.write(f"Transcription complete! Time taken: {st.session_state.transcription_time:.2f} seconds")
                    except Exception as e:
                        st.error(f"Transcription failed: {str(e)}")

                    # Cleanup temporary files
                    os.unlink(temp_input.name)
                    if file_size > 25:
                        os.unlink(compressed_file)

        # Always display the transcript if it exists
        if st.session_state.transcript:
            st.subheader("Transcript:")
            st.text_area("", value=st.session_state.transcript, height=300)

            # Copy to clipboard button
            if st.button("Copy to Clipboard"):
                try:
                    pyperclip.copy(st.session_state.transcript)
                    st.success("Transcript copied to clipboard!")
                except Exception as e:
                    st.error(f"Failed to copy to clipboard: {str(e)}")

            # Save to file section
            st.subheader("Save Transcript to File")
            output_filename = st.text_input("Enter output filename for transcript:")
            if st.button("Save Transcript"):
                if output_filename:
                    if save_transcript_to_file(st.session_state.transcript, output_filename):
                        st.success(f"Transcript saved to {output_filename}")
                else:
                    st.warning("Please enter a filename to save the transcript.")

if __name__ == '__main__':
    main()

