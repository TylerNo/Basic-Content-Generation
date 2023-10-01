import os
from PIL import Image, ImageEnhance

def delete_specific_res_images(folder_path, width, height):

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            with Image.open(file_path) as img:
                if img.size == (width, height):
                    img.close()
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")



def enhance_image(image_path, app_logs, MAX_LOG_ENTRIES, log_manager):
    try:
        with Image.open(image_path) as im:
            enhancer = ImageEnhance.Contrast(im)
            im = enhancer.enhance(1.1)

            thumbnail_path = os.path.join("auto_content_generator/mock_times/assets/thumbnails", os.path.basename(image_path)).replace("\\", "/")

            print(f"Saving thumbnail to: {thumbnail_path}")
            log_message = f"Saving Thumbnail to {thumbnail_path}"
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            im_thumbnail = resize_and_crop(im, (900, 690))
            im_thumbnail.save(thumbnail_path)

            im_resized = resize_and_crop(im, (1296, 630))
            im_resized.save(image_path)

            print(f"Saving main image to: {image_path}")
            log_message = f"Saving Main Image to: {image_path}"
            if len(app_logs) >= MAX_LOG_ENTRIES:
                app_logs.pop(0)
            log_manager.append_log(log_message)

            return True

    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        log_message = f"Couldn't find image: {image_path}"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return False

def resize_and_crop(image, target_size):
    image_aspect = image.width / image.height
    target_aspect = target_size[0] / target_size[1]

    if image_aspect > target_aspect:
        if image.height < target_size[1]:
            new_width = round(target_size[1] * image_aspect)
            new_height = target_size[1]
        else:
            new_width = image.width
            new_height = image.height
    else:
        if image.width < target_size[0]:
            new_width = target_size[0]
            new_height = round(target_size[0] / image_aspect)
        else:
            new_width = image.width
            new_height = image.height

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    left = (resized_image.width - target_size[0]) / 2
    top = (resized_image.height - target_size[1]) / 2
    right = (resized_image.width + target_size[0]) / 2
    bottom = (resized_image.height + target_size[1]) / 2

    cropped_image = resized_image.crop((left, top, right, bottom))

    return cropped_image

def start_image_processor(random_article, app_logs, MAX_LOG_ENTRIES, log_manager):

    print("Image processor started...")

    article = random_article

    if not article:
        print("No article to process.")
        log_message = "No Articles to Process."
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return None

    title, image_url, article_url, contents, category, instagram_contents, twitter_contents, facebook_contents, development_status = article


    # Process the image
    success = enhance_image(image_url, app_logs, MAX_LOG_ENTRIES, log_manager)

    if success:
        log_message = "Image Successfully Processed!"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return article
    else:
        print(f"Updated development_stage to 'failed' for article: {title}")
        log_message = f"Updated Development Stage to 'Failed' for article: {title}"
        if len(app_logs) >= MAX_LOG_ENTRIES:
            app_logs.pop(0)
        log_manager.append_log(log_message)
        return None
