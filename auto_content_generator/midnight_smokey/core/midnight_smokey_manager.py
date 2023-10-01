from auto_content_generator.midnight_smokey.databases.ms_database_manager import get_random_scraped_song
from auto_content_generator.midnight_smokey.utilities.youtube_download import start_youtube_download
from auto_content_generator.midnight_smokey.utilities.audio_processor import start_audio_processor
from auto_content_generator.midnight_smokey.utilities.image_processor import start_image_process
from auto_content_generator.midnight_smokey.utilities.video_compiler import start_video_compiler
from auto_content_generator.midnight_smokey.utilities.google_drive_uploader import upload_file
from auto_content_generator.midnight_smokey.utilities.youtube_upload import start_youtube_upload
from auto_content_generator.midnight_smokey.databases.ms_database_manager import update_development_status_to_uploaded
from auto_content_generator.midnight_smokey.utilities.check_temp_files import start_temp_check

def start_midnight_smokey_manager(log_manager, app_logs, MAX_LOG_ENTRIES):
    for i in range(1):
        log_message = "Starting Midnight Smokey Manager..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        log_message = "Choosing Random Song..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        start_temp_check()

        random_song = get_random_scraped_song()

        song_choice = random_song[0]

        log_message = "Random Song: " + song_choice
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        song_id = random_song[3]

        log_message = "Starting Download from YouTube"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        dl_flag_success = start_youtube_download(random_song)

        if dl_flag_success == False:
            log_message = "YouTube Download Failed for " + song_choice
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)
            return

        if dl_flag_success == True:
            log_message = "Starting Audio Processor..."
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            audio_status = start_audio_processor()

            if audio_status == None:
                return

            log_message = "Audio Successfully Processed!"
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

        log_message = "Starting Image Processor..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        image_name = start_image_process()
        print(image_name)

        log_message = "Image Successfully Processed!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        if image_name == None:
            log_message = "Image Processing Failed!"
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)
            return
        else:
            log_message = "Starting Video Compiler..."
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)
            start_video_compiler(image_name)

        log_message = "Video Successfully Compiled!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        log_message = "Uploading Video to Google Drive..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        uploaded_file = upload_file('output_video.mp4',
                                    'auto_content_generator/midnight_smokey/assets/temp/output_video.mp4',
                                    'video/mp4')

        log_message = "Video Successfully Uploaded!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        log_message = "Starting YouTube Upload via Publer..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        status = start_youtube_upload(uploaded_file, random_song)

        if status == None:
            return

        log_message = "Video Scheduled For 5 Hours From Now!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        update_development_status_to_uploaded(song_id, app_logs, MAX_LOG_ENTRIES, log_manager)

        log_message = "Development Status Updated to 'Uploaded'!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        return


