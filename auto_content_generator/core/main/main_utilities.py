import json
import subprocess
from auto_content_generator.core.main.acg_main import acg_main
import os
from auto_content_generator.core.config.config_init import create_default_config
import sys
import time

def update_code_from_git():
    try:
        subprocess.run(["git", "pull"], check=True)
        subprocess.run(["pip3", "install", "-r", "requirements"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return False

    os.execve(sys.executable, [sys.executable, 'main.py'], os.environ)


def start_generator(log_manager):
    log_message = "Starting..."
    print(log_message)

    log_manager.append_log(log_message)

    config = load_config()
    if config is None:
        print("Failed to load configuration. Stopping generator.")
        return

    while not log_manager.stop_signal:
        acg_main(log_manager.app_logs, log_manager.MAX_LOG_ENTRIES, config, log_manager)

    log_message = "Process Completed!"
    log_manager.append_log(log_message)





def load_config():
    config_path = "auto_content_generator/core/config/config.json"

    # Check if the file exists
    if not os.path.exists(config_path):
        create_default_config()

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config: {e}")
        return None

def save_config(config):
    with open("auto_content_generator/core/config/config.json", "w") as f:
        json.dump(config, f, indent=4)
