import openai
import json
import re
from auto_content_generator.mock_times.databases.mt_database_manager import delete_article_by_url


def start_chatgpt_main(article, config, app_logs, MAX_LOG_ENTRIES, log_manager):
    openai.api_key = config['openai']['api_key']
    system_msg = config['chatgpt']['main_prompt']

    title = article[0]
    image_url = article[1]
    article_url = article[2]
    user_msg = article[3]

    print(title)
    print(image_url)
    print(article_url)
    print(user_msg)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                             {"role": "user", "content": user_msg}])

    response_content = response["choices"][0]["message"]["content"]
    print(response_content)
    updated_article = process_response(response_content, article, app_logs, MAX_LOG_ENTRIES, log_manager)

    if updated_article != None:
        log_message = "Main ChatGPT Processing Completed!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    return updated_article


def process_response(response_content, article, app_logs, MAX_LOG_ENTRIES, log_manager):
    cleaned_response = remove_control_characters(response_content)
    if not cleaned_response.endswith("}"):
        cleaned_response += "}"

    try:
        response_data = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        log_message = "Error Decoding JSON: " + str(e)
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

        log_message = "Deleting Article: " + article[2]
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        delete_article_by_url(article[2])
        return None

    image_url, article_url, instagram_contents, twitter_contents, facebook_contents = article[1], article[2], article[
        5], article[6], article[7]

    category = response_data.get("Category", "Unknown")
    title = response_data.get("Title", "Unknown")
    contents = response_data.get("Article", "Unknown")

    updated_article = (
        title,
        image_url,
        article_url,
        contents,
        category,
        instagram_contents,
        twitter_contents,
        facebook_contents,
        "main_processed"
    )

    print(updated_article)
    print("Random article details:")
    print(f"Title: {updated_article[0]}")
    print(f"Image URL: {updated_article[1]}")
    print(f"Article URL: {updated_article[2]}")
    print(f"Contents: {updated_article[3]}")
    print(f"Category: {updated_article[4]}")
    print(f"Instagram Contents: {updated_article[5]}")
    print(f"Twitter Contents: {updated_article[6]}")
    print(f"Facebook Contents: {updated_article[7]}")
    print(f"Development Status: {updated_article[8]}")

    log_message = "Category: " + updated_article[4]
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Title: " + updated_article[0]
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Contents: " + updated_article[3]
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    return updated_article


def remove_control_characters(s):
    print("Removing control characters from response")
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)