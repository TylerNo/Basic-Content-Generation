import json

def create_default_config():
    default_config = """{
    "auth": {
        "password": "",
        "secret_key": "secret_key_goes_here"
    },
    "chatgpt": {
        "legal_prompt_categories": "Create me a simple JSON formatted list that includes the top 10 categories of legal/law facts that pertain more to the top themes or genres and that regular people would be most interested in. The title for the list should be \"law_categories\" and then the list should only include the categories. These categories need to be interesting, relatable, and categories of law that regular people/citizens are interested in. Each category name needs to be as short as possible. Do not exceed 25 characters for each category name.",
        "legal_prompt_facts": "Each JSON item should have a title of the fact number such as 'Fact 1', 'Fact 2', etc. Each JSON item should then have the values of 'Category', 'Part 1', and 'Part 2'. Each fact should be 1 sentence (no more than 125 total characters!), and that sentence should be split up between 'Part 1' and 'Part 2' in equal sizes. Keep the facts engaging and relatable to everyone. The reading grade level should be under grade 7 ideally with easy to understand language and short sentences. Each fact should be unique, engaging, and simple. Do not reuse any facts. Do not exceed the 125 total character limit for each fact. Here is an example response format for some random categories: {\"Fact 1\": {\"Category\": \"Criminal Law\", \"Part 1\": \"In the US, you are innocent until proven guilty, but\", \"Part 2\": \"you can still be detained for quite some time before a trial.\"}, \"Fact 2\": {\"Category\": \"Prohibition\", \"Part 1\": \"During Prohibition, the government poisoned a\", \"Part 2\": \"large quantity of alcohol, leading to the deaths of many people.\"}, \"Fact 3\": {\"Category\": \"Legal System\", \"Part 1\": \"There's no official language in the US, so laws and\", \"Part 2\": \"official documents are not legally required to be in English.\"}}",
        "main_prompt": "You're a comedy writer who will completely rewrite this text into a unique and naturally funny, sarcastic article. Respond in PERFECT JSON format ONLY with the sections \"Category\", \"Title\", and \"Article\". For the article, be sure to format it with RICH TEXT within the JSON with ONLY paragraph tags. Options for the category are \"US\", \"World\", \"Sports\", \"Entertainment\", \"Politics\", \"Finance\", \"Health\", \"Science\", or \"Miscellaneous\". Make the title a funny and catchy headline for the article but make it as short as possible.",
        "motivation_prompt_categories": "Create me a simple JSON formatted list that includes the top 10 categories of motivation that pertain more to the themes or genres of motivational content such as 'positive thinking' or 'passion & purpose' or 'personal growth'. The title for the list should be \"motivation_categories\" and then the list should only include the categories. These categories need to be interesting, relatable, and categories of motivation that regular people/citizens are interested in. Each category name needs to be as short as possible. Do not exceed 25 characters for each category name.",
        "motivation_prompt_facts": "Each JSON item should have a title of the fact number such as 'Fact 1', 'Fact 2', etc. Each JSON item should then have the values of 'Category', 'Part 1', and 'Part 2'. Each fact should be 1 sentence (no more than 150 total characters!), and that sentence should be split up between 'Part 1' and 'Part 2' in equal sizes. Keep the facts engaging, polarizing, over the top and relatable to everyone or people in particular situations. The reading grade level should be under grade 7 ideally with easy to understand language and short sentences. Each fact should be unique, engaging, and simple. Do not reuse any facts. Do not exceed the 150 total character limit for each fact. Here is an example response format for some random categories: {\"Fact 1\": {\"Category\": \"Resilience\", \"Part 1\": \"Embrace obstacles because they're just...\", \"Part 2\": \"important lessons in disguise.\"}, \"Fact 2\": {\"Category\": \"Positive Thinking\", \"Part 1\": \"A positive mindset is linked to\", \"Part 2\": \"improved learning abilities and academic performance.\"}, \"Fact 3\": {\"Category\": \"Personal Growth\", \"Part 1\": \"Personal growth often occurs at\", \"Part 2\": \"the intersection of challenge and support.\"}}",
        "psychology_prompt_categories": "Create me a simple JSON formatted list that includes the top 10 categories of psychology facts. The title for the list should be \"psychology_categories\" and then the list should only include the categories. These categories need to be interesting, relatable, and categories of psychology that regular people/citizens are interested in. Each category name needs to be as short as possible. Do not exceed 25 characters for each category name.",
        "psychology_prompt_facts": "Each JSON item should have a title of the fact number such as 'Fact 1', 'Fact 2', etc. Each JSON item should then have the values of 'Category', 'Part 1', and 'Part 2'. Each fact should be 1 sentence (no more than 150 total characters!), and that sentence should be split up between 'Part 1' and 'Part 2' in equal sizes. Keep the facts engaging, polarizing, over the top and relatable to everyone or people in particular situations. The reading grade level should be under grade 7 ideally with easy to understand language and short sentences. Each fact should be unique, engaging, and simple. Do not reuse any facts. Do not exceed the 150 total character limit for each fact. Here is an example response format for some random categories: {\"Fact 1\": {\"Category\": \"Personality Types\", \"Part 1\": \"Agreeable individuals tend to be\", \"Part 2\": \"supportive and caring, and place a high value on maintaining positive relationships.\"}, \"Fact 2\": {\"Category\": \"Mental Health\", \"Part 1\": \"People who suffer from an anxiety disorder\", \"Part 2\": \"typically feel like they're on a cliff, with constant fear of falling.\"}, \"Fact 3\": {\"Category\": \"Emotionals\", \"Part 1\": \"Being aware of your own emotions can\", \"Part 2\": \"help you make better decisions.\"}}",
        "social_prompt": "You're a comedy writer who will summarize the text uniquely in a funny and sarcastic way for each social media item listed here. Respond in perfect JSON format and do not exceed the character limit (CL) for each item. (Social Medias: \"Instagram CL=2500\", \"Twitter CL=250\", \"Facebook CL=600\")"
    },
    "fact_drip": {
        "legal_facts": true,
        "motivation_facts": true,
        "psychology_facts": true
    },
    "functions": {
        "fact_drip": true,
        "midnight_smokey": true,
        "mock_times": true
    },
    "main": {
        "max_log_entries": 100
    },
    "openai": {
        "api_key": ""
    },
    "spotify": {
        "client_id": "",
        "client_secret": "",
        "playlists": [
            "PLAYLIST ID",
            "PLAYLIST ID"
        ]
    }
}"""
    try:
        with open("auto_content_generator/core/config/config.json", "w") as f:
            json.dump(default_config, f)
        print("Default config created.")
    except Exception as e:
        print(f"Failed to create default config: {e}")
        return None