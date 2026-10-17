import subprocess
import os

def mix_live_audio(live_url, audio_file_path, output_path):
    """
    دالة لدمج البث المباشر مع ملف صوتي باستخدام FFmpeg
    """
    # أمر FFmpeg (نفس الأمر الذي نجح في Termux سابقاً)
    command = [
        "ffmpeg", "-y",
        "-i", live_url,
        "-i", audio_file_path,
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        output_path
    ]
    
    try:
        # تشغيل الأمر
        subprocess.run(command, check=True)
        return True, output_path
    except subprocess.CalledProcessError as e:
        return False, str(e)
