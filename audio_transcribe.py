import speech_recognition as sr
import os
import data
def get_files_in_folder(folder_path):
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return file_list

def generate_transcript(wav_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)  # Record the entire audio file
        try:
            transcript = recognizer.recognize_google(audio_data, language="en-US")
            return transcript
        except sr.UnknownValueError:
            # print("Speech Recognition could not understand the audio.")
            return None
        except sr.RequestError as e:
            # print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def generate_full_transcript_from_all_files():
    full_transcripts = ""
    files_in_folder = get_files_in_folder(data.folder_path)
    for file in files_in_folder:
        try:
            transcript = generate_transcript(wav_file=f"{data.folder_path}/{file}")

            full_transcripts += transcript  + " "
        except:
            continue
        
    return full_transcripts
if __name__ == "__main__":
    pass
    # https://otter.ai/my-notes