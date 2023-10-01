import openai
import re
import json
from auto_content_generator.mock_times.databases.mt_database_manager import delete_article_by_url

def process_response2(response_content, updated_article, app_logs, MAX_LOG_ENTRIES, log_manager):
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

        delete_article_by_url(updated_article[2])
        return None

    title, image_url, article_url, contents, category, instagram_contents, twitter_contents, facebook_contents, development_status = updated_article[0], updated_article[1], updated_article[2], updated_article[3], updated_article[4], updated_article[5], updated_article[6], updated_article[7], updated_article[8]
    instagram_contents = response_data.get("Instagram")
    twitter_contents = response_data.get("Twitter")
    facebook_contents = response_data.get("Facebook")

    if None in [instagram_contents, twitter_contents, facebook_contents]:
        print("Some social media responses are missing. Not updating the database.")
        return None

    updated_article2 = (
        title,
        image_url,
        article_url,
        contents,
        category,
        instagram_contents,
        twitter_contents,
        facebook_contents,
        "socials_processed"
    )
    print(updated_article2)
    print("Random article details:")
    print(f"Title: {updated_article2[0]}")
    print(f"Image URL: {updated_article2[1]}")
    print(f"Article URL: {updated_article2[2]}")
    print(f"Contents: {updated_article2[3]}")
    print(f"Category: {updated_article2[4]}")
    print(f"Instagram Contents: {updated_article2[5]}")
    print(f"Twitter Contents: {updated_article2[6]}")
    print(f"Facebook Contents: {updated_article2[7]}")
    print(f"Development Status: {updated_article2[8]}")

    log_message = "Instagram Contents: " + updated_article2[5]
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Twitter Contents: " + updated_article2[6]
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    log_message = "Facebook Contents: " + updated_article2[7]
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    return updated_article2


def remove_control_characters(s):
    print("Removing control characters from response")
    return re.sub(r'[\x00-\x09\x0b-\x1f\x7f-\x9f]', '', s)


def start_chatgpt_socials(updated_article, config, app_logs, MAX_LOG_ENTRIES, log_manager):
    openai.api_key = config['openai']['api_key']
    system_msg = config['chatgpt']['social_prompt']

    user_msg = updated_article[3]
    print(user_msg)


    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                             {"role": "user", "content": user_msg}])

    response_content = response["choices"][0]["message"]["content"]
    print(response_content)
    updated_article2 = process_response2(response_content, updated_article, app_logs, MAX_LOG_ENTRIES, log_manager)

    if updated_article2 != None:
        log_message = "Socials ChatGPT Processing Complete!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)

    return updated_article2
