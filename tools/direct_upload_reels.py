"""
Direct Resumable Upload of Instagram Reels from Local MP4 file via Meta Graph API.
Uses requests library with streaming binary upload.
"""
import os
import sys
import time
import json
import requests

CREDS_FILE = r"c:\Users\CauMo\source\repos\EvilShtrib-Highlights\tools\instagram_credentials.json"

def get_creds():
    with open(CREDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def upload_local_reels(video_path, caption):
    if not os.path.exists(video_path):
        print(f"ERROR: Video file not found: {video_path}", flush=True)
        return False
        
    creds = get_creds()
    token = creds["long_lived_user_token"]
    ig_id = creds["ig_account_id"]
    file_size = os.path.getsize(video_path)
    
    print("=" * 60, flush=True)
    print(f"UPLOADING REELS TO INSTAGRAM (@evilshtrib)", flush=True)
    print(f"File: {os.path.basename(video_path)} ({file_size / (1024*1024):.2f} MB)", flush=True)
    print("=" * 60, flush=True)
    
    # 1. Initialize Resumable Upload Session
    print("\n[Step 1/4] Initializing Resumable Upload Container...", flush=True)
    init_url = f"https://graph.facebook.com/v21.0/{ig_id}/media"
    init_payload = {
        "media_type": "REELS",
        "upload_type": "resumable",
        "caption": caption,
        "share_to_feed": "true",
        "access_token": token
    }
    
    resp = requests.post(init_url, data=init_payload, timeout=30)
    init_res = resp.json()
    if "error" in init_res:
        print(f"FAILED to initialize container: {init_res['error']}", flush=True)
        return False
        
    container_id = init_res.get("id")
    upload_uri = init_res.get("uri")
    print(f"Container created! ID: {container_id}", flush=True)
    print(f"Upload URI: {upload_uri}", flush=True)
    
    # 2. Upload Binary Video Bytes
    print(f"\n[Step 2/4] Uploading video binary stream ({file_size} bytes)...", flush=True)
    upload_headers = {
        "Authorization": f"OAuth {token}",
        "offset": "0",
        "file_size": str(file_size),
        "Content-Type": "application/octet-stream"
    }
    
    t0 = time.time()
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    up_resp = requests.post(upload_uri, headers=upload_headers, data=video_bytes, timeout=300)
        
    print(f"Upload finished in {time.time()-t0:.1f}s. HTTP {up_resp.status_code}", flush=True)
    try:
        up_data = up_resp.json()
        print(f"Response: {up_data}", flush=True)
    except:
        print(f"Response text: {up_resp.text[:200]}", flush=True)
        
    if up_resp.status_code not in (200, 201):
        print(f"Upload failed with HTTP {up_resp.status_code}", flush=True)
        return False
        
    # 3. Wait for Meta to process video
    print("\n[Step 3/4] Waiting for Meta to transcode and finalize video...", flush=True)
    status_url = f"https://graph.facebook.com/v21.0/{container_id}"
    params = {
        "fields": "status_code,status",
        "access_token": token
    }
    
    max_retries = 40
    for attempt in range(1, max_retries + 1):
        time.sleep(5)
        st_resp = requests.get(status_url, params=params, timeout=30)
        st = st_resp.json()
        code = st.get("status_code", "UNKNOWN")
        print(f"  Check #{attempt}: Status = {code}", flush=True)
        
        if code == "FINISHED":
            print("Video transcode finished!", flush=True)
            break
        elif code in ["ERROR", "EXPIRED"]:
            print(f"Processing failed: {st}", flush=True)
            return False
    else:
        print("Timeout waiting for Meta processing.", flush=True)
        return False
        
    # 4. Publish Reels
    print("\n[Step 4/4] Publishing Reels to Instagram...", flush=True)
    publish_url = f"https://graph.facebook.com/v21.0/{ig_id}/media_publish"
    pub_payload = {
        "creation_id": container_id,
        "access_token": token
    }
    pub_resp = requests.post(publish_url, data=pub_payload, timeout=30)
    pub_res = pub_resp.json()
    if "error" in pub_res:
        print(f"FAILED to publish: {pub_res['error']}", flush=True)
        return False
        
    media_id = pub_res.get("id")
    print("\n" + "=" * 60, flush=True)
    print(f"🎉 REELS PUBLISHED SUCCESSFULLY!", flush=True)
    print(f"Instagram Media ID: {media_id}", flush=True)
    
    permalink = None
    try:
        p_resp = requests.get(
            f"https://graph.facebook.com/v21.0/{media_id}?fields=permalink,shortcode&access_token={token}",
            timeout=15
        )
        p_data = p_resp.json()
        permalink = p_data.get("permalink")
        if permalink:
            print(f"Instagram URL: {permalink}", flush=True)
    except Exception as pe:
        print(f"Warning fetching permalink: {pe}", flush=True)
        
    print("=" * 60, flush=True)
    
    res_path = os.path.join(os.path.dirname(__file__), "publish_result.json")
    try:
        with open(res_path, "w", encoding="utf-8") as f:
            json.dump({
                "status": "success",
                "media_id": media_id,
                "permalink": permalink,
                "video_file": os.path.basename(video_path),
                "published_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2, ensure_ascii=False)
    except Exception as fe:
        pass
        
    return media_id

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/direct_upload_reels.py <path_to_mp4> [caption]", flush=True)
        sys.exit(1)
        
    vpath = sys.argv[1]
    cap = sys.argv[2] if len(sys.argv) > 2 else "EvilShtrib CS 1.6 Highlights #cs16 #counterstrike"
    upload_local_reels(vpath, cap)
