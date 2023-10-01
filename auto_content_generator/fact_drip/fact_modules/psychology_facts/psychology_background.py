import os
import random


def get_random_background_video(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    print("Getting random background video...")

    directory_path = "auto_content_generator/fact_drip/assets/backgrounds/psychology"

    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    chosen_file = random.choice(files)

    log_message = "Retrieved random background video: " + chosen_file
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    return os.path.join(directory_path, chosen_file)

def get_random_background_audio(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    print("Getting random background audio...")

    directory_path = "auto_content_generator/fact_drip/assets/audio"

    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    chosen_file = random.choice(files)

    log_message = "Retrieved random background audio: " + chosen_file
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    return os.path.join(directory_path, chosen_file)