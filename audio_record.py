import threading
import wave
import time
import sounddevice as sd
import numpy as np
import data


def record_audio(base_filename):
    # Set the sampling rate and the number of channels
    fs = 44100  # You can adjust this based on your preferences
    channels = 2  # Stereo
    single_len = 5
    iteration = 1

    global_stop = threading.Event()  # Event to stop the global loop

    # Thread to listen for keyboard input
    def keyboard_input_thread():
        nonlocal global_stop
        input("Press Enter to stop: \n")
        global_stop.set()

    # Start the keyboard input thread
    keyboard_thread = threading.Thread(target=keyboard_input_thread)
    keyboard_thread.start()

    while not global_stop.is_set():
        # Open the WAV file for writing
        with wave.open(f"./{data.folder_path}/{base_filename}_{iteration}.wav", 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wf.setframerate(fs)

            # Create a flag for stopping the recording
            stop_recording = threading.Event()

            def recording_thread():
                nonlocal stop_recording
                print(f"Recording {base_filename}_{iteration}.")
                start_time = time.time()

                while not stop_recording.is_set():
                    # Record audio with increased gain
                    recording = sd.rec(int(fs) * single_len, samplerate=fs, channels=channels, dtype=np.int16)
                    sd.wait()

                    # Write frames to the open WAV file
                    wf.writeframes(recording.tobytes())

                    # Check if the specified time interval has passed
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= single_len:
                        break

            # Start the recording thread
            record_thread = threading.Thread(target=recording_thread)
            record_thread.start()

            # Wait for the recording thread to finish
            record_thread.join()

            print(f"Recording {base_filename}_{iteration} stopped.")
            
            # Increment the iteration for the next file
            iteration += 1

    # Wait for the keyboard input thread to finish
    keyboard_thread.join()


if __name__ == "__main__":
    pass
