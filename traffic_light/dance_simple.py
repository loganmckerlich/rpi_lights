import sounddevice as sd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import time
from scipy.signal import lfilter
import librosa
from scipy.signal import find_peaks
from scipy.ndimage import uniform_filter1d

# Parameters for FFT analysis
rate = 44100  # Sample rate for audio
chunk_size = 1024  # Number of frames per buffer
BASS_RANGE = (20, 250)  # Bass: 20-250 Hz
TENOR_RANGE = (250, 2000)  # Tenor: 250-2000 Hz
TREBLE_RANGE = (2000, 20000)  # Treble: 2000-20000 Hz
TIME_INTERVAL = 0.0005
MOVING_AVG_WINDOW = 10  # Number of samples for moving average



class LiveAudioVisualizer():
    def __init__(self):
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=rate, blocksize=chunk_size)
        self.audio_data = np.zeros(chunk_size)
        self.BPM_EST = None
        self.REDUCTION_VAL = 0
        self.TRIM = 500
        self.BEAT_THRESHOLD = 5
        self.NORMALIZE = False
        # base filler
        self.fig = go.Figure()
        empty_trace = go.Scatter(x=[], y=[], mode='lines', name='Empty')
        self.fig.add_trace(empty_trace)
        self.recent_audio = np.zeros(chunk_size * 10)  # Buffer for BPM analysis

        if 'aud_is_running' not in st.session_state:
            st.session_state.aud_is_running = False
        if 'aud_x' not in st.session_state:
            st.session_state.aud_x = []
        if 'aud_bass' not in st.session_state:
            st.session_state.aud_bass = []
        if 'aud_treble' not in st.session_state:
            st.session_state.aud_treble = []
        if 'aud_tenor' not in st.session_state:
            st.session_state.aud_tenor = []
        if 'aud_beat' not in st.session_state:
            st.session_state.aud_beat = []

    def toggle(self):
        if not st.session_state.aud_is_running:
            st.session_state.aud_x = []
            st.session_state.aud_bass = []
            st.session_state.aud_treble = []
            st.session_state.aud_tenor = []
            st.session_state.aud_beat = []

        st.session_state.aud_is_running = not st.session_state.aud_is_running

    def min_max_scale(self,array):
        min_val = np.min(array)
        max_val = np.max(array)
        # Avoid division by zero if all elements are identical
        if max_val - min_val == 0:
            return np.zeros_like(array)
        return (array - min_val) / (max_val - min_val)
    
    def noise_reduce(self, y):
        """Apply moving average filter to reduce noise"""
        # n = self.REDUCTION_VAL  # the larger n is, the smoother curve will be
        # if n==0:
        #     return y
        # b = [1.0 / n] * n
        # a = 1
        # yy = lfilter(b, a, y)
        yy = np.array([np.mean(y[max(0, i - self.REDUCTION_VAL + 1):i + 1]) for i in range(len(y))])
        return yy
    
    def get_type(self, fft_result, fft_freq, range_):
        """Filter and return bass frequencies' amplitudes"""
        mask = (fft_freq >= range_[0]) & (fft_freq <= range_[1])
        amp = np.mean(fft_result[mask])
        return amp
    
    def audio_callback(self, indata, frames, time, status):
        """Called when new audio data is available"""
        if status:
            print(status)
        self.audio_data = indata[:, 0]  # Capture single-channel audio
        self.recent_audio[:-frames] = self.recent_audio[frames:]
        self.recent_audio[-frames:] = self.audio_data

    
    def detect_and_predict_beat(self, fft_freq, fft_result):
        """Using FFT to predict the next beat based on signal periodicity"""
        # Predict the presence of beats by detecting the dominant frequency in the range of 60-200 BPM
        predicted_beat = None
        for i, freq in enumerate(fft_freq):
            if 60 <= freq <= 200:  # Considering BPM range for detection
                if fft_result[i] > self.BEAT_THRESHOLD:  # Arbitrary threshold for beat detection
                    predicted_beat = 0  # If there's a beat in the frequency range
                    break
        
        return predicted_beat

    def detect_bpm(self):
        """
        Estimate BPM based on periodicity in the buffered audio signal.
        """
        audio = self.recent_audio
        audio = audio - np.mean(audio)
        audio = audio / np.max(np.abs(audio))
        correlation = np.correlate(audio, audio, mode='full')[len(audio) // 2:]
        correlation = uniform_filter1d(correlation, size=100)
        peaks, _ = find_peaks(correlation, height=0.5)  # Adjust threshold as needed
        if len(peaks) < 2:
            return None
        peak_lags = np.diff(peaks)
        bpm_estimates = 60 / (peak_lags / rate)
        bpm_estimates = bpm_estimates[(bpm_estimates >= 40) & (bpm_estimates <= 200)]
        self.BPM_EST = np.median(bpm_estimates) if len(bpm_estimates) > 0 else None

    def analyze_audio(self, audio_chunk):
        """Analyze the audio chunk and return FFT results"""
        fft_result = np.fft.fft(audio_chunk)
        fft_freq = np.fft.fftfreq(len(fft_result), 1 / rate)

        # Keep only positive frequencies
        fft_freq = fft_freq[:len(fft_freq) // 2]
        fft_result = np.abs(fft_result[:len(fft_result) // 2])
        
        bass = self.get_type(fft_result, fft_freq, BASS_RANGE)
        treble = self.get_type(fft_result, fft_freq, TREBLE_RANGE)
        tenor = self.get_type(fft_result, fft_freq, TENOR_RANGE)
        beat = self.detect_and_predict_beat(fft_freq,fft_result)
        
        return bass, treble, tenor, beat
    
    @st.fragment
    def main(self, placeholder):
        self.stream.start()

        x = st.session_state.aud_x
        bass = st.session_state.aud_bass
        treble = st.session_state.aud_treble
        tenor = st.session_state.aud_tenor
        beat = st.session_state.aud_beat
        
        if not st.session_state.aud_is_running:
            placeholder.plotly_chart(self.fig, use_container_width=True)
            self.stream.stop()
            return  # Exit here if it's stopped
        
        while True:
            if not st.session_state.aud_is_running:
                self.stream.stop()
                break
            
            audio_chunk = self.audio_data
            bass_val, treble_val, tenor_val, beat_val = self.analyze_audio(audio_chunk)
            self.detect_bpm()

            if len(x) > 0:
                x.append(x[-1] + TIME_INTERVAL)
            else:
                x.append(0)

            bass = np.append(bass, bass_val)
            treble = np.append(treble, treble_val)
            tenor = np.append(tenor, tenor_val)
            beat = np.append(beat, beat_val)

            if len(x)>self.TRIM:
                x = x[-1*(self.TRIM):]
                bass = bass[-1*(self.TRIM):]
                treble = treble[-1*(self.TRIM):]
                tenor = tenor[-1*(self.TRIM):]
                beat = beat[-1*(self.TRIM):]
            
            bass2 = bass.copy()
            treble2 = treble.copy()
            tenor2 = tenor.copy()
            beat2 = beat.copy()
            if self.REDUCTION_VAL>0:
                if len(bass) > MOVING_AVG_WINDOW:
                    bass2 = self.noise_reduce(bass)
                    treble2 = self.noise_reduce(treble)
                    tenor2 = self.noise_reduce(tenor)

            if self.NORMALIZE:
                bass2 = self.min_max_scale(bass2)
                treble2 = self.min_max_scale(treble2)
                tenor2 = self.min_max_scale(tenor2)

            # Create a new plot each iteration
            fig = go.Figure()

            # Bass trace
            bass_trace = go.Scatter(x=x, y=bass2, mode='lines', name='Bass')
            fig.add_trace(bass_trace)

            # Treble trace (corrected y data)
            treble_trace = go.Scatter(x=x, y=treble2, mode='lines', name='Treble')
            fig.add_trace(treble_trace)

            # Tenor trace
            tenor_trace = go.Scatter(x=x, y=tenor2, mode='lines', name='Tenor')
            fig.add_trace(tenor_trace)

            beat_trace = go.Scatter(x=x, y=beat2, mode='markers', name='Beat')
            fig.add_trace(beat_trace)

            fig.update_layout(
                title="Live Audio",
                xaxis_title="Time",
                yaxis_title="Amplitude"
            )

            # Plot the updated chart
            placeholder.plotly_chart(fig, use_container_width=True)

            self.fig = fig
            time.sleep(TIME_INTERVAL)  # Control the update rate
