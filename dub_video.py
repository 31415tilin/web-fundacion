import subprocess
import os
import imageio_ffmpeg
from gtts import gTTS

def dub_video():
    video_in = "sabores-quinsaloma.mp4"
    audio_temp = "temp_audio_en.mp3"
    video_out = "sabores-quinsaloma-en.mp4"
    
    # 1. Text to generate
    text = (
        "Welcome to Sabores de Quinsaloma! This innovative social project in Los Ríos, Ecuador, "
        "empowers rural youth and women through an agro-industrial unit producing artisanal fruit liquors. "
        "By leveraging rich local tropical fruits, we are validating unique recipes, training over five "
        "hundred young leaders, and promoting productive inclusion. Taste the tradition, support local growth!"
    )
    
    print("Generating English audio using gTTS...")
    tts = gTTS(text=text, lang='en', tld='com')
    tts.save(audio_temp)
    print(f"Audio saved to {audio_temp}")
    
    # 2. Get FFmpeg executable
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"FFmpeg executable found at: {ffmpeg_exe}")
    
    # 3. Assemble and run ffmpeg command
    # We want to replace the original audio track completely with the new audio track.
    # -map 0:v:0 picks the video stream from input 0.
    # -map 1:a:0 picks the audio stream from input 1.
    # -c:v copy copies the video without re-encoding (extremely fast and retains 100% quality).
    # -c:a aac encodes the MP3 audio to AAC for better MP4 compatibility.
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", video_in,
        "-i", audio_temp,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        video_out
    ]
    
    print("Executing FFmpeg command...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # 4. Clean up temporary audio file
    if os.path.exists(audio_temp):
        os.remove(audio_temp)
        print(f"Removed temporary audio file {audio_temp}")
        
    if result.returncode == 0:
        print(f"SUCCESS! Video with English audio generated as '{video_out}'")
    else:
        print("ERROR occurred during FFmpeg execution:")
        print(result.stderr)

if __name__ == "__main__":
    dub_video()
