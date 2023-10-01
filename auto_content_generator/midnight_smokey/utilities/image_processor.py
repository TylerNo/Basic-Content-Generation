import os
import random
from PIL import Image

def start_image_process():
    directory = 'auto_content_generator/midnight_smokey/assets/thumbnails'
    folder_path = directory
    remove_duplicates(folder_path)
    convert_to_jpeg_with_dimensions(folder_path)


    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None

    image_name = random.choice(files)
    return image_name

def dhash(image, hash_size=8):

    resized = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(resized.getdata())

    diff = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            diff.append(pixel_left > pixel_right)

    return sum([2 ** i for (i, v) in enumerate(diff) if v])


def remove_duplicates(folder_path):
    print("Removing image duplicates")
    seen_hashes = set()
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            with Image.open(file_path) as img:
                h = dhash(img)
                if h in seen_hashes:
                    os.remove(file_path)
                else:
                    seen_hashes.add(h)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def resize_image_to_fill(img, target_width, target_height):
    print("Resizing image")
    width, height = img.size
    aspect_ratio = width / height

    if aspect_ratio < target_width / target_height:
        new_width = target_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = target_height
        new_width = int(new_height * aspect_ratio)

    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (resized_img.width - target_width) / 2
    top = (resized_img.height - target_height) / 2
    right = (resized_img.width + target_width) / 2
    bottom = (resized_img.height + target_height) / 2

    return resized_img.crop((left, top, right, bottom))

def convert_to_jpeg_with_dimensions(folder_path, target_width=1920, target_height=1080):

    print("Converting image")
    extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp', '.ico']
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not any(filename.lower().endswith(ext) for ext in extensions):
            os.remove(file_path)
            print("Removing " + filename)
            continue

        with Image.open(file_path) as img:
            if img.size == (1920, 1080):
                continue
            resized_img = resize_image_to_fill(img, target_width, target_height)
            canvas = Image.new("RGB", (target_width, target_height), (255, 255, 255))
            canvas.paste(resized_img, (0, 0))

            output_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".jpeg")
            canvas.save(output_path, "JPEG")

            os.remove(file_path)
            print("Converting " + filename + " to jpeg")
