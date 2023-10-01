from auto_content_generator.mock_times.utilities.image_processor import delete_specific_res_images, start_image_processor
from auto_content_generator.mock_times.databases.mt_database_manager import validate_and_delete_incomplete_articles, load_random_preprocessed_article, update_development_status_to_uploaded
from auto_content_generator.mock_times.utilities.main_chatgpt import start_chatgpt_main
from auto_content_generator.mock_times.utilities.socials_chatgpt import start_chatgpt_socials
from auto_content_generator.mock_times.utilities.validation import start_validation
from auto_content_generator.mock_times.utilities.image_upload import start_image_upload
from auto_content_generator.mock_times.uploading.webflow_upload import start_webflow_upload
from auto_content_generator.mock_times.uploading.instagram_upload import start_instagram_upload
from auto_content_generator.mock_times.uploading.twitter_upload import start_twitter_upload
from auto_content_generator.mock_times.uploading.facebook_upload import start_facebook_upload

folder_path = "auto_content_generator/mock_times/assets/pictures"

def start_mock_times_manager(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    print("Mock Times Manager Started...")

    log_message = "Mock Times Manager Starting..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    article = None
    updated_article = None
    updated_article2 = None
    updated_article3 = None
    uploaded_image_main = None
    uploaded_image_thumbnail = None

    log_message = "Starting Image Processor..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    delete_specific_res_images(folder_path, 700, 350)

    log_message = "Images Successfully Processed!"
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Starting Article Validation..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)
    validate_and_delete_incomplete_articles(log_manager, app_logs, MAX_LOG_ENTRIES)

    log_message = "Article Validation Complete!"
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Loading Random Article..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)
    random_article = load_random_preprocessed_article()

    print(random_article)
    image_url = random_article[1]
    article_url = random_article[2]
    log_message = f"Loaded Article from {article_url}"
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    if random_article != None:
        log_message = "Starting Image Processor..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        article = start_image_processor(random_article, app_logs, MAX_LOG_ENTRIES, log_manager)

    if article != None:
        log_message = "Starting Main ChatGPT Processor..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        updated_article = start_chatgpt_main(article, config, app_logs, MAX_LOG_ENTRIES, log_manager)


    if updated_article != None:
        log_message = "Starting Socials ChatGPT Processor..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        updated_article2 = start_chatgpt_socials(updated_article, config, app_logs, MAX_LOG_ENTRIES, log_manager)

    if updated_article2 != None:
        log_message = "Starting Article Validation 2..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        updated_article3 = start_validation(updated_article2)
        if updated_article3 != None:
            log_message = "Article Validation Successful!"
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

    if updated_article3 != None:
        log_message = "Starting Image Upload..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        uploaded_image_main = start_image_upload(image_url)
        if uploaded_image_main:
            print(f"Image uploaded successfully. URL: {uploaded_image_main}")
            log_message = "Main Image Successfully Uploaded! " + uploaded_image_main
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

        image_url = image_url.replace("pictures", "thumbnails")

        uploaded_image_thumbnail = start_image_upload(image_url)
        if uploaded_image_thumbnail:
            print(f"Image uploaded successfully. URL: {uploaded_image_thumbnail}")
            log_message = "Thumbnail Image Successfully Uploaded! " + uploaded_image_thumbnail
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

    if uploaded_image_main and uploaded_image_thumbnail != None:
        log_message = "Starting Upload to Mock Times Website..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        start_webflow_upload(updated_article3, uploaded_image_main, uploaded_image_thumbnail, app_logs, MAX_LOG_ENTRIES, log_manager)

        log_message = "Starting Upload to Mock Times Instagram..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        instagram_contents = updated_article3[5]
        start_instagram_upload(uploaded_image_thumbnail, instagram_contents, app_logs, MAX_LOG_ENTRIES, log_manager)

        log_message = "Starting Upload to Mock Times Twitter..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        twitter_contents = updated_article3[6]
        start_twitter_upload(uploaded_image_thumbnail, twitter_contents, app_logs, MAX_LOG_ENTRIES, log_manager)

        log_message = "Starting Upload to Mock Times Facebook..."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        facebook_contents = updated_article3[7]
        start_facebook_upload(uploaded_image_thumbnail, facebook_contents, app_logs, MAX_LOG_ENTRIES, log_manager)

        log_message = "Updated Development Status to Uploaded!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        article_url = updated_article3[2]
        update_development_status_to_uploaded(article_url)
