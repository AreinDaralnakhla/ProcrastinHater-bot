import requests
import pyaudio
from google.cloud import speech
import queue
import openai
import os

IFTTT_WEBHOOK_KEY = ""
OPENAI_API_KEY = ""
GOOGLE_APPLICATION_CREDENTIALS = ""


# Initialize Google Speech Client
print("Initializing Google Speech Client...")
speech_client = speech.SpeechClient()

# Queue to store audio data
audio_queue = queue.Queue()

# Callback for audio data
def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

# IFTTT Webhook Trigger Function
def trigger_ifttt(event_name, color):
    try:
        print(f"Sending IFTTT trigger: Event = {event_name}, Color = {color}")
        url = f"https://maker.ifttt.com/trigger/triggerLED/json/with/key/{IFTTT_WEBHOOK_KEY}"
        payload = {"value1": color}
        response = requests.post(url, json=payload)
        print(f"IFTTT Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to send IFTTT trigger: {e}")

# Use OpenAI to classify the transcript
def is_distracting_content(transcript):
    try:
        print(f"Sending transcript to OpenAI: {transcript}")
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that evaluates whether my audio content is distracting and not study related (meaning if I'm procrasticating and watching reels and videos online instead of listening to educational material). Respond with only 'yes' or 'no'."},
                {"role": "user", "content": f"Is the following transcript distracting? {transcript}"}
            ]
        )
        result = response["choices"][0]["message"]["content"].strip().lower()
        print(f"OpenAI Response: {result}")
        return "yes" in result
    except Exception as e:
        print(f"[ERROR] OpenAI API Error: {e}")
        return False

# Transcribe audio and act on distracting content
def process_transcript(transcript):
    print(f"Received Transcript: {transcript}")
    if is_distracting_content(transcript):
        print("⚠️ Distracting content detected!")
         # Trigger red LED
        trigger_ifttt("triggerLED", "red") 
    else:
        print("Content is not distracting.")

# Stream and transcribe audio
def stream_audio():
    try:
        print("Starting audio stream...")
        audio_interface = pyaudio.PyAudio()
        stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
            stream_callback=audio_callback,
        )
        print("Listening for audio...")
        stream.start_stream()

        # Configure recognition
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        streaming_config = speech.StreamingRecognitionConfig(config=config)

        # Audio generator
        def audio_generator():
            while True:
                yield speech.StreamingRecognizeRequest(
                    audio_content=audio_queue.get()
                )

        # Process transcription
        print("Transcribing audio...")
        responses = speech_client.streaming_recognize(streaming_config, audio_generator())
        for response in responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                print(f"Transcription Result: {transcript}")
                process_transcript(transcript)

    except Exception as e:
        print(f"Error during transcription: {e}")

# Run the audio stream
if __name__ == "__main__":
    print("Starting ProcrastinHater...")
    stream_audio()
