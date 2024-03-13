import audio_record
import audio_transcribe
import datetime
import os
import data

def write_text_to_file(text, max_line_length, filename):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) <= max_line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    lines.append(current_line.strip())
    formatted_text = '\n'.join(lines)

    with open(filename, 'w') as file:
        file.write(formatted_text)

def generate_transcript_file_name():
    # Get the current date as a string (e.g., '2022-03-08')
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Construct the filename with the current date
    file_name = f"./transcriptions/all_hands_transcript_{current_date}.txt"
    return file_name

def delete_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                # print(f"Deleted: {file_path}")
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
                # print(f"Deleted directory: {file_path}")
        except Exception as e:
            # print(f"Error deleting {file_path}: {e}")
            pass

def main():
    print("RECORDING AUDIO")
    audio_record.record_audio(base_filename=data.file_name)

    print("CREATE TRANSCRIPT")
    transcript = audio_transcribe.generate_full_transcript_from_all_files()

    print("DELETING OLD AUDIO")
    delete_files_in_folder(folder_path=data.folder_path)
        
    print("WRITING TRANSCRIPT TO FILE")
    write_text_to_file(text=transcript, max_line_length=100, filename=generate_transcript_file_name())

if __name__ == "__main__":
    main()
