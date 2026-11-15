import os, subprocess, imageio_ffmpeg

BASE_DIR = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights"
FINAL_DIR = os.path.join(BASE_DIR, "final_videos")
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def convert_to_9x16(src_mp4, dst_mp4):
    print(f"\nConverting {src_mp4} -> {dst_mp4} (1080x1920 9:16)...")
    filter_str = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
        "[0:v]scale=1080:-1[fg];"
        "[bg][fg]overlay=0:(H-h)/2"
    )
    cmd = [
        FFMPEG_EXE, "-y",
        "-i", src_mp4,
        "-filter_complex", filter_str,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        dst_mp4
    ]
    subprocess.run(cmd, check=True)
    print(f"Done! Size: {os.path.getsize(dst_mp4)/(1024*1024):.2f} MB")

if __name__ == "__main__":
    v2_in = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol2.mp4")
    v2_out = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol2_9x16.mp4")
    if os.path.exists(v2_in) and (not os.path.exists(v2_out) or os.path.getsize(v2_out) < 1000):
        convert_to_9x16(v2_in, v2_out)
        
    v3_in = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol3.mp4")
    v3_out = os.path.join(FINAL_DIR, "EvilShtrib_60s_Vol3_9x16.mp4")
    if os.path.exists(v3_in) and (not os.path.exists(v3_out) or os.path.getsize(v3_out) < 1000):
        convert_to_9x16(v3_in, v3_out)
