"""
Instagram Reels Auto-Publisher for EvilShtrib Highlights via Meta Graph API.
Usage:
    python tools/upload_to_reels.py --token <TOKEN> --account-id <IG_ACCOUNT_ID> [--proxy http://127.0.0.1:PORT]
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error

DEFAULT_CAPTION = (
    "☣ EVILSHTRIB > CLASSIC BIOHAZARD [CS 1.6] ☣\n"
    "🔥 36 Kills in 60s! Real Match HLTV Multi-Kill Highlights!\n"
    "🎮 IP: 185.225.201.113:27015\n"
    "⚡️ Connect in console: connect 185.225.201.113:27015\n\n"
    "#cs16 #counterstrike #biohazard #cs16zombie #evilshtrib #gaming #esports #highlights #reels #gamingreels #nostalgia"
)

DEFAULT_VIDEO_URL = "https://github.com/CauMoH/EvilShtrib-Highlights/raw/main/EvilShtrib_Reels_9x16.mp4"

def make_request(url, data=None, proxy=None):
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()
        
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode('utf-8') if data else None,
        headers={'User-Agent': 'EvilShtrib-Uploader/1.0'}
    )
    
    try:
        with opener.open(req, timeout=30.0) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            return json.loads(err_body)
        except:
            return {"error": {"message": err_body, "code": e.code}}
    except Exception as e:
        return {"error": {"message": str(e)}}

def upload_reels(token, account_id, video_url=DEFAULT_VIDEO_URL, caption=DEFAULT_CAPTION, proxy=None):
    print(f"=== Starting Instagram Reels Upload ===")
    print(f"Account ID: {account_id}")
    print(f"Video URL:  {video_url}")
    if proxy:
        print(f"Proxy:      {proxy}")
        
    # Step 1: Create Reel Container
    print("\n[Step 1/3] Creating Media Container...")
    create_url = f"https://graph.facebook.com/v21.0/{account_id}/media"
    create_payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": token
    }
    
    res = make_request(create_url, create_payload, proxy=proxy)
    if "error" in res:
        print(f"FAILED to create container: {res['error']}")
        return False
        
    container_id = res.get("id")
    print(f"Container created successfully! ID: {container_id}")
    
    # Step 2: Poll Container Status until FINISHED
    print("\n[Step 2/3] Waiting for Meta to download and process video...")
    status_url = f"https://graph.facebook.com/v21.0/{container_id}?fields=status_code,status&access_token={token}"
    
    max_retries = 30
    for attempt in range(1, max_retries + 1):
        time.sleep(5)
        st = make_request(status_url, proxy=proxy)
        code = st.get("status_code", "UNKNOWN")
        print(f"  Attempt {attempt}/{max_retries}: Status = {code}")
        
        if code == "FINISHED":
            print("Video processing finished successfully!")
            break
        elif code in ["ERROR", "EXPIRED"]:
            print(f"Processing failed: {st}")
            return False
    else:
        print("Timeout waiting for video processing.")
        return False
        
    # Step 3: Publish Media
    print("\n[Step 3/3] Publishing Reels to Instagram...")
    publish_url = f"https://graph.facebook.com/v21.0/{account_id}/media_publish"
    pub_payload = {
        "creation_id": container_id,
        "access_token": token
    }
    
    pub_res = make_request(publish_url, pub_payload, proxy=proxy)
    if "error" in pub_res:
        print(f"FAILED to publish: {pub_res['error']}")
        return False
        
    media_id = pub_res.get("id")
    print(f"\n🎉 REELS PUBLISHED SUCCESSFULLY!")
    print(f"Instagram Media ID: {media_id}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Reels to Instagram via Graph API")
    parser.add_argument("--token", required=True, help="Meta Graph API Access Token")
    parser.add_argument("--account-id", required=True, help="Instagram Business Account ID")
    parser.add_argument("--video-url", default=DEFAULT_VIDEO_URL, help="Public URL of the MP4 video")
    parser.add_argument("--caption", default=DEFAULT_CAPTION, help="Reels Caption text")
    parser.add_argument("--proxy", default=None, help="HTTP/HTTPS Proxy (e.g. http://127.0.0.1:10808)")
    
    args = parser.parse_args()
    upload_reels(args.token, args.account_id, args.video_url, args.caption, args.proxy)
