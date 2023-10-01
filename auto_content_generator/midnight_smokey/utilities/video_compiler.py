import subprocess
from PIL import Image

audio_path = "auto_content_generator/midnight_smokey/assets/temp/output.wav"
output_video = "auto_content_generator/midnight_smokey/assets/temp/output_video.mp4"

def start_video_compiler(image_name):
    print("Starting video compiler")
    image_path = "auto_content_generator/midnight_smokey/assets/thumbnails/" + str(image_name)

    with Image.open(image_path) as img:
        width, height = img.size

    if width == 1024 and height == 1024:
        filter_str = 'scale=1080:1080,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black'
    elif width == 1920 and height == 1080:
        filter_str = None
    else:
        raise ValueError("Unsupported image dimensions")

    cmd = [
        'ffmpeg',
        '-y',
        '-loglevel', 'verbose',
        '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
    ]

    if filter_str:
        cmd.extend(['-vf', filter_str])

    cmd.extend([
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_video
    ])
    subprocess.run(cmd)

    print("Video compiler completed")
