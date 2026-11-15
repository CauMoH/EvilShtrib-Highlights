import os, subprocess, imageio_ffmpeg

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
FINAL_DIR = os.path.join(BASE_DIR, "final_videos")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def convert_vol4():
    src_mp4 = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol4.mp4")
    dst_mp4 = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol4_9x16.mp4")
    
    print(f"\nConverting {src_mp4} -> {dst_mp4} (1080x1920 9:16 Reels)...")
    filter_str = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];"
        "[0:v]scale=1080:-1[fg];"
        "[bg][fg]overlay=0:(H-h)/2"
    )
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", src_mp4,
        "-filter_complex", filter_str,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "160k",
        "-movflags", "+faststart",
        dst_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Done! Size: {os.path.getsize(dst_mp4)/(1024*1024):.2f} MB")

if __name__ == "__main__":
    convert_vol4()
