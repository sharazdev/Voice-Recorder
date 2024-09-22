import pyaudio
import wave
import threading
import time
import datetime

class AudioRecorder:
    """A class for recording audio using PyAudio."""

    def __init__(self):
        """Initialise the AudioRecorder with default settings."""
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.start_time = 0
        self.stream = None

    def start_recording(self, device_index):
        """Start recording audio from the specified device."""
        self.is_recording = True
        self.frames = []
        self.start_time = time.time()

        def record():
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                          channels=1,
                                          rate=44100,
                                          input=True,
                                          input_device_index=device_index,
                                          frames_per_buffer=1024)

            while self.is_recording:
                data = self.stream.read(1024)
                self.frames.append(data)

        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()

    def stop_recording(self):
        """Stop the current recording session."""
        self.is_recording = False
        if self.record_thread.is_alive():
            self.record_thread.join()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def save_recording(self, filename):
        """Save the recorded audio to a WAV file."""
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def get_available_devices(self):
        """Get a list of available input devices."""
        devices = []
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices.append((i, device_info['name']))
        return devices

    def get_recording_time(self):
        """Get the current recording time."""
        if self.is_recording:
            return time.time() - self.start_time
        return 0
    
    def get_timestamp(self):
        """Get a timestamp string for the current time."""
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")