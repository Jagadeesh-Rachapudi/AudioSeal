import torch
import torchaudio
import urllib.request
import os
from audioseal import AudioSeal

def download_audio(url, save_path):
    """Download an audio file from a URL and save it locally."""
    print(f"Downloading audio from {url}...")
    urllib.request.urlretrieve(url, save_path)
    print(f"Audio downloaded and saved to {save_path}")

def encode_watermark(input_audio_path, output_watermarked_path, message_bits=16, alpha=0.8):
    """Embed a 16-bit watermark into an audio file and save the watermarked audio."""
    # Load the audio file
    audio, sr = torchaudio.load(input_audio_path)
    audio = audio.unsqueeze(0)  # Add batch dimension if needed

    # Load the generator model
    generator = AudioSeal.load_generator("audioseal_wm_16bits")

    # Generate a random 16-bit message
    secret_message = torch.randint(0, 2, (1, message_bits), dtype=torch.int32)
    print(f"Original 16-bit message: {secret_message}")

    # Encode the message into the audio
    watermark = generator(audio, sample_rate=sr, message=secret_message, alpha=alpha)
    watermarked_audio = audio + watermark

    # Detach the tensor and convert to CPU before saving
    watermarked_audio = watermarked_audio.detach().cpu()

    # Save the watermarked audio
    torchaudio.save(output_watermarked_path, watermarked_audio.squeeze(0), sr)
    print(f"Watermarked audio saved to: {output_watermarked_path}")

    return secret_message

def decode_watermark(watermarked_audio_path):
    """Extract a 16-bit watermark from a watermarked audio file."""
    # Load the watermarked audio
    watermarked_audio, sr = torchaudio.load(watermarked_audio_path)
    watermarked_audio = watermarked_audio.unsqueeze(0)  # Add batch dimension if needed

    # Load the detector model
    detector = AudioSeal.load_detector("audioseal_detector_16bits")

    # Extract the watermark
    result, extracted_message = detector.detect_watermark(watermarked_audio, sample_rate=sr)
    print(f"Extracted 16-bit message: {extracted_message}")

    # Check if the watermark detection was successful
    if result > 0.5:
        print("Watermark successfully detected!")
    else:
        print("Watermark not detected.")

    return extracted_message

if __name__ == "__main__":
    # Download URL and file paths
    example_audio_url = "https://keithito.com/LJ-Speech-Dataset/LJ037-0171.wav"
    input_audio_path = "example_audio.wav"
    output_watermarked_path = "watermarked_audio.wav"

    # Step 1: Download the example audio
    if not os.path.exists(input_audio_path):
        download_audio(example_audio_url, input_audio_path)

    # Step 2: Embed the 16-bit watermark and save the watermarked audio
    original_message = encode_watermark(input_audio_path, output_watermarked_path)

    # Step 3: Decode the watermark from the watermarked audio
    extracted_message = decode_watermark(output_watermarked_path)

    # Compare the original and extracted messages
    matching_bits = torch.count_nonzero(torch.eq(original_message, extracted_message)).item()
    print(f"Matching bits: {matching_bits}/16")
