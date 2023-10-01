import os
import subprocess

BASE_DIR = "auto_content_generator/fact_drip/assets"
VIDEO_DIR = os.path.join(BASE_DIR, "backgrounds", "legal")
OUTPUT_DIR = os.path.join(BASE_DIR, "temp")
ffmpeg = "auto_content_generator/core/assets/ffmpeg.exe"
ffprobe = "auto_content_generator/core/assets/ffprobe.exe"
FONT_PATH = "auto_content_generator/fact_drip/assets/fonts/Gilgan.otf"


def format_text_for_drawtext(text, default_font_size=85, max_lines=4, max_chars_per_line=20):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= max_chars_per_line:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    while len(lines) > max_lines:
        default_font_size -= 8
        max_chars_per_line += 1
        lines, _ = format_text_for_drawtext(text, default_font_size, max_lines, max_chars_per_line)
        print("Adjusted Fact Text")
        print(default_font_size)
        print(max_chars_per_line)

    return lines, default_font_size

def format_category_for_drawtext(category, default_font_size=90, max_chars_per_line=20):
    words = category.split()
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= max_chars_per_line:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    if len(lines) > 1:
        default_font_size -= 7
        max_chars_per_line += 1
        return format_category_for_drawtext(category, default_font_size, max_chars_per_line)
    print(lines)
    print(lines[0])
    print(default_font_size)
    return lines[0], default_font_size

def sanitize_text(text):
    return text.replace("'", "")

def get_video_dimensions(video_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode != 0:
        print(f"Error occurred while executing command: {' '.join(cmd)}")
        print(result.stderr.decode('utf-8'))
    dimensions = result.stdout.decode('utf-8').strip()
    return dimensions

def resize_videos():
    for filename in os.listdir(VIDEO_DIR):
        if filename.endswith('.mp4'):

            input_path = os.path.join(VIDEO_DIR, filename)
            print(f"Input Path: {input_path}")

            temp_output_path = os.path.join(VIDEO_DIR, "temp_" + filename)
            print(f"Temp Output Path: {temp_output_path}")

            dimensions = get_video_dimensions(input_path)
            print(f"Dimensions: {dimensions}")

            if dimensions != "1080x1920":
                cmd = [
                    'ffmpeg',
                    '-i', input_path,
                    '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
                    '-an',
                    '-y',
                    temp_output_path
                ]
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    print(f"Error occurred while executing command: {' '.join(cmd)}")
                    print(result.stderr.decode('utf-8'))

                os.remove(input_path)
                os.rename(temp_output_path, input_path)


def compile_video(background_video, background_audio, category, fact_pt1, fact_pt2):
    video_duration = 9

    overlay_cmd = "[0:v]eq=brightness=-0.35[video_with_overlay]"

    fact_pt1_lines, fact_pt1_font_size = format_text_for_drawtext(fact_pt1)
    fact_pt2_lines, fact_pt2_font_size = format_text_for_drawtext(fact_pt2)

    category = sanitize_text(category)
    fact_pt1_lines = [sanitize_text(line) for line in fact_pt1_lines]
    fact_pt2_lines = [sanitize_text(line) for line in fact_pt2_lines]

    fact_pt1_drawtext_cmds = [
        f"drawtext=text='{line}':fontsize={fact_pt1_font_size}:fontfile='{FONT_PATH}':"
        f"x=(w-text_w)/2:y=h*(3/6)+{index*fact_pt1_font_size}:"
        f"fontcolor=white:shadowcolor=black:shadowx=5:shadowy=5:enable='between(t,1.5,5)':"
        f"alpha='if(between(t,1.5,2),(t-1.5)/0.5,if(between(t,4.5,5),1-(t-4.5)/0.5,1))'"
        for index, line in enumerate(fact_pt1_lines)
    ]

    fact_pt2_drawtext_cmds = [
        f"drawtext=text='{line}':fontsize={fact_pt2_font_size}:fontfile='{FONT_PATH}':"
        f"x=(w-text_w)/2:y=h*(3/6)+{index*fact_pt2_font_size}:"
        f"fontcolor=white:shadowcolor=black:shadowx=5:shadowy=5:enable='between(t,5,8.5)':"
        f"alpha='if(between(t,5,5.5),(t-5)/0.5,if(between(t,8,8.5),1-(t-8)/0.5,1))'"
        for index, line in enumerate(fact_pt2_lines)
    ]

    formatted_category, category_font_size = format_category_for_drawtext(category)

    text_cmd = (
            f"[video_with_overlay]drawtext=text='{formatted_category}':fontsize={category_font_size}:"
            f"fontfile='{FONT_PATH}':x=(w-text_w)/2:y=h*(2/7):fontcolor=black:enable='between(t,0,8.5)':"
            f"alpha='if(lt(t,0.5),t/0.5,if(lt(t,8),1,if(lt(t,8.5),1-(t-8)/0.5,0)))':"
            f"box=1:boxcolor=white:boxborderw=30,"
            + ','.join(fact_pt1_drawtext_cmds) + ","
            + ','.join(fact_pt2_drawtext_cmds)
    )

    cmd = [
        'ffmpeg',
        '-i', background_video,
        '-i', background_audio,
        '-filter_complex', overlay_cmd + ";" + text_cmd,
        '-shortest',
        '-t', str(video_duration),
        '-y',
        os.path.join(OUTPUT_DIR, 'legal_output_video.mp4')
    ]
    print(cmd)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Error occurred while executing command: {' '.join(cmd)}")
        print(result.stderr.decode('utf-8'))



def start_video_compiler(legal_fact, background_video, background_audio, config, log_manager, app_logs, MAX_LOG_ENTRIES):
    log_message = "Starting video compiler..."
    if len(app_logs) >= MAX_LOG_ENTRIES:
        app_logs.pop(0)
    log_manager.append_log(log_message)

    category = legal_fact[2]
    if not (category.endswith('fact') or category.endswith('Fact')):
        category += ' Fact'

    fact_pt1 = legal_fact[3] + "..."
    fact_pt2 = legal_fact[4]

    resize_videos()
    compile_video(background_video, background_audio, category, fact_pt1, fact_pt2)

    return True
