
def start_validation(updated_article2):

    title, image_url, article_url, contents, category, instagram_contents, twitter_contents, facebook_contents, development_status = updated_article2[0], updated_article2[1], updated_article2[2], updated_article2[3], updated_article2[4], updated_article2[5], updated_article2[6], updated_article2[7], updated_article2[8]




    words_to_check = ["Yahoo", "yahoo"]
    max_char_count = 250
    print(title)
    if not title:
        print("No title, skipping this article")
        return None

    for word in words_to_check:
        title = title.replace(word, '')



    words_to_check = ["Yahoo", "yahoo"]
    print(contents)
    if not contents:
        print("No contents, skipping this article")
        return None

    for word in words_to_check:
        contents = contents.replace(word, '')

    print(category)
    if not category:
        print("No category, skipping this article")
        return None

    valid_categories = ["US", "World", "Science", "Health", "Finance", "Entertainment", "Politics", "Sports"]
    if category not in valid_categories:
        category = "Miscellaneous"

    # #INSTAGRAM CHECK
    # max_char_count = 2000
    # print(Instagram)
    # if not Instagram:
    #     print("No Instagram, skipping this article")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # if len(Instagram) >= max_char_count:
    #     print("Character count too large for Instagram, skipping article...")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # for word in words_to_check:
    #     Instagram = Instagram.replace(word, '')


    max_char_count = 278
    print(twitter_contents)
    if not twitter_contents:
        print("No Twitter, skipping this article")
        return None

    if len(twitter_contents) >= max_char_count:
        twitter_contents = twitter_contents[:278]

    for word in words_to_check:
        twitter_contents = twitter_contents.replace(word, '')


    # #THREADS CHECK
    # max_char_count = 400
    # print(Threads)
    # if not Threads:
    #     print("No Threads, skipping this article")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # if len(Threads) >= max_char_count:
    #     print("Character count too large for Threads, skipping article...")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # for word in words_to_check:
    #     Threads = Threads.replace(word, '')
    #
    #
    # #FACEBOOK CHECK
    # max_char_count = 600
    # print(Facebook)
    # if not Facebook:
    #     print("No Facebook, skipping this article")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # if len(Facebook) >= max_char_count:
    #     print("Character count too large for Threads, skipping article...")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # for word in words_to_check:
    #     Facebook = Facebook.replace(word, '')
    #
    #
    # #REDDIT CHECK
    # max_char_count = 1000
    # print(Reddit)
    # if not Reddit:
    #     print("No Facebook, skipping this article")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # if len(Reddit) >= max_char_count:
    #     print("Character count too large for Threads, skipping article...")
    #     start_uploading(no_upload_flag, stop_flag_container)
    #
    # for word in words_to_check:
    #     Reddit = Reddit.replace(word, '')
    development_status = "upload_ready"

    updated_article3 = (
        title,
        image_url,
        article_url,
        contents,
        category,
        instagram_contents,
        twitter_contents,
        facebook_contents,
        development_status
    )

    return updated_article3
