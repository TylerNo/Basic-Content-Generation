import os

def start_temp_check():
    files_to_delete = [
        "auto_content_generator/midnight_smokey/assets/temp/audio.mp3",
        "auto_content_generator/midnight_smokey/assets/temp/audio.part",
        "auto_content_generator/midnight_smokey/assets/temp/output.wav",
        "auto_content_generator/midnight_smokey/assets/temp/output_video.mp4",
        "temp.wav"
    ]

    for file_path in files_to_delete:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Successfully deleted {file_path}")
            except Exception as e:
                print(f"An error occurred while deleting {file_path}: {e}")
        else:
            print(f"{file_path} does not exist")
