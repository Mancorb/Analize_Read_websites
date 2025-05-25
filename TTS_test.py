from TTS.api import TTS

# Load the model (English LJSpeech Tacotron2-DDC)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

text = "This is a test with pitch, speed, and emotion adjustments."

# Coqui TTS supports:
# - `speaker_wav` to mimic speaker voice (not used here)
# - `style_wav` to mimic style or emotion (optional, use None if not available)
# - `speed` float > 0.5 to 2.0 (default 1.0)
# - `pitch` float to shift pitch (1.0 is default)

# Example values for your emotion tags:
emotion_params = {
    "anger": {"speed": 1.5, "pitch": 1.2},
    "fear": {"speed": 1.3, "pitch": 1.1},
    "joy": {"speed": 1.4, "pitch": 1.3},
    "sadness": {"speed": 0.8, "pitch": 0.8},
    "neutral": {"speed": 1.0, "pitch": 1.0},
    "disgust": {"speed": 0.7, "pitch": 0.7},
    "surprise": {"speed": 1.6, "pitch": 1.4}
}

# Pick an emotion to test
emotion = "joy"
params = emotion_params[emotion]

# Synthesize with speed and pitch adjustments
tts.tts_to_file(
    text=text,
    file_path=f"output_{emotion}.wav",
    speed=params["speed"],
    pitch=params["pitch"]
)

print(f"Audio with {emotion} emotion saved as output_{emotion}.wav")
