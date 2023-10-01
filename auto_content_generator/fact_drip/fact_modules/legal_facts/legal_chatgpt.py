import openai
import re
import json
from auto_content_generator.fact_drip.databases.facts_db_manager import check_fact_duplicate, insert_fact

def start_legal_chatgpt(config, log_manager, app_logs, MAX_LOG_ENTRIES):
    log_message = "Starting ChatGPT for Legal Facts..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    openai.api_key = config['openai']['api_key']
    system_msg = config['chatgpt']['legal_prompt_categories']
    user_msg = ""

    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=[{"role": "system", "content": system_msg},
                                                          {"role": "user", "content": user_msg}])
        response_content = response["choices"][0]["message"]["content"]
        print(response_content)
        response_content = remove_control_characters(response_content)
        if not response_content.endswith("}"):
            response_content += "}"

        try:
            categories_dict = json.loads(response_content)
            break
        except json.JSONDecodeError:
            attempts += 1
            if attempts < max_attempts:
                print(f"Error decoding response. Retrying ({attempts}/{max_attempts})...")
            else:
                print("Max attempts reached. Could not decode the response.")
                return

    for category in categories_dict["law_categories"]:
        facts_attempt = 0
        while facts_attempt < max_attempts:
            system_msg_for_facts = f"Create me 50 sets of interesting and engaging legal facts with the law category \"{category}\". " + config['chatgpt']['legal_prompt_facts']
            facts_response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                        messages=[{"role": "system", "content": system_msg_for_facts}])
            facts_content = facts_response["choices"][0]["message"]["content"]
            facts_content = remove_control_characters(facts_content)
            try:
                facts_dict = json.loads(facts_content)
                break
            except json.JSONDecodeError:
                facts_attempt += 1
                if facts_attempt == max_attempts:
                    print(f"Error decoding facts for category: {category}. Max attempts reached.")
                    continue

        for fact_key, fact_values in facts_dict.items():
            fact_category = fact_values.get("Category", "")
            fact_pt1 = fact_values.get("Part 1", "")
            fact_pt2 = fact_values.get("Part 2", "")

            if not check_fact_duplicate(fact_category, fact_pt1, fact_pt2):
                insert_fact("legal", fact_category, fact_pt1, fact_pt2)

                print(f"Added Fact to Database!\nCategory: {fact_category}\nFact Part 1: {fact_pt1}\nFact Part 2: {fact_pt2}")
                log_message = f"Added Fact to Database!\nCategory: {fact_category}\nFact Part 1: {fact_pt1}\nFact Part 2: {fact_pt2}"
                if len(app_logs) >= MAX_LOG_ENTRIES:
                    app_logs.pop(0)
                log_manager.append_log(log_message)


def remove_control_characters(s):
    print("Removing control characters from response")
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', s)
