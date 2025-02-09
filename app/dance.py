# import sounddevice as sd
# import numpy as np
# import librosa
# import matplotlib.pyplot as plt
# from scipy.signal import butter, lfilter

# # Constants
# CHUNK = 2048  # Frame size
# RATE = 44100  # Sampling rate
# BUFFER_DURATION = 3.0  # Sliding window (seconds)
# buffer = np.zeros(int(RATE * BUFFER_DURATION))

# # Sensitivity Parameters
# HPF_CUTOFF = 50.0  # High-pass filter cutoff frequency in Hz
# ONSET_THRESHOLD = 0.1  # Fraction of max onset strength to consider significant (0 to 1)
# PEAK_DELTA = 30  # Minimum prominence for a peak
# PEAK_WAIT = 10  # Minimum frames between peaks

# # High-Pass Filter Function
# def highpass_filter(data, cutoff=HPF_CUTOFF, fs=RATE, order=5):
#     nyquist = 0.5 * fs
#     normal_cutoff = cutoff / nyquist
#     b, a = butter(order, normal_cutoff, btype='high', analog=False)
#     return lfilter(b, a, data)

# # Beat Detection with Adjustable Sensitivity
# def detect_beats_with_tuning(audio_buffer):
#     # Preprocess audio
#     filtered_audio = highpass_filter(audio_buffer)
#     filtered_audio /= np.max(np.abs(filtered_audio))  # Normalize
    
#     # Onset strength
#     onset_env = librosa.onset.onset_strength(y=filtered_audio, sr=RATE)
    
#     # Filter weak onsets
#     threshold = ONSET_THRESHOLD * np.max(onset_env)
#     onset_env[onset_env < threshold] = 0

#     # Detect peaks in onset envelope
#     peaks = librosa.util.peak_pick(onset_env, pre_max=5, post_max=5, pre_avg=5, post_avg=5, delta=PEAK_DELTA, wait=PEAK_WAIT)
    
#     return peaks, onset_env

# # Real-Time Audio Callback
# def audio_callback(indata, frames, time, status):
#     global buffer

#     # Handle microphone input
#     audio_data = indata[:, 0]
#     buffer = np.roll(buffer, -frames)
#     buffer[-frames:] = audio_data

#     # Detect beats periodically
#     peaks, onset_env = detect_beats_with_tuning(buffer)
#     current_time = time.inputBufferAdcTime

#     # Trigger light logic on detected peaks
#     for peak in peaks:
#         peak_time = peak / RATE  # Convert buffer index to seconds
#         print(f"Light triggered at {current_time:.2f}s (buffer peak position: {peak})")

#         # Optional: Visualize Onset Strength for Debugging
#         plt.plot(onset_env, label="Onset Strength Envelope")
#         plt.scatter(peak, onset_env[peak], color='red', label='Beat Detected')
#         plt.title("Audio Analysis - Onset Strength")
#         plt.legend()
#         plt.show()

# # Setup SoundDevice Stream
# print("Listening for beats...")
# stream = sd.InputStream(channels=1, samplerate=RATE, callback=audio_callback, blocksize=CHUNK)

# # Start Stream and Run
# with stream:
#     try:
#         input("Press Enter to stop...\n")
#     except KeyboardInterrupt:
#         print("Stopped.")
