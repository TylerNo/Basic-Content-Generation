from auto_content_generator.fact_drip.databases.facts_db_manager import get_random_fact, update_fact_status
from auto_content_generator.fact_drip.fact_modules.psychology_facts.psychology_chatgpt import start_psychology_chatgpt
from auto_content_generator.fact_drip.fact_modules.psychology_facts.psychology_background import get_random_background_video, get_random_background_audio
from auto_content_generator.fact_drip.fact_modules.psychology_facts.psychology_video_compiler import start_video_compiler
from auto_content_generator.fact_drip.fact_modules.psychology_facts.psychology_video_uploader import start_video_uploader


def start_psychology_facts_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    log_message = "Starting Fact Drip / Psychology Facts Manager..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    psychology_fact = get_random_fact("psychology", config, log_manager, app_logs, MAX_LOG_ENTRIES)

    if psychology_fact == None:
        start_psychology_chatgpt(config, log_manager, app_logs, MAX_LOG_ENTRIES)
        psychology_fact = get_random_fact("psychology", config, log_manager, app_logs, MAX_LOG_ENTRIES)

    if psychology_fact != None:
        background_video = get_random_background_video(config, log_manager, app_logs, MAX_LOG_ENTRIES)
        background_audio = get_random_background_audio(config, log_manager, app_logs, MAX_LOG_ENTRIES)

    if background_video and background_audio != None:
        video = start_video_compiler(psychology_fact, background_video, background_audio, config, log_manager, app_logs, MAX_LOG_ENTRIES)
        print(video)

    if video != None:
        upload_status = start_video_uploader(config, log_manager, app_logs, MAX_LOG_ENTRIES, psychology_fact)

    if upload_status != None:
        update_fact_status(psychology_fact, log_manager, app_logs, MAX_LOG_ENTRIES)


