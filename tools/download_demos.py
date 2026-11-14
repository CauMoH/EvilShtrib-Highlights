"""
Download Demos Tool for EvilShtrib-Highlights.
Fetches recent demo recordings from EvilShtrib VDS (/opt/evilshtrib_demos/) via SFTP.
"""

import os
import zipfile
import paramiko

VDS_HOST = '185.225.201.113'
VDS_USER = 'root'
VDS_PASS = 'u5f_-d+2XB'
REMOTE_DEMOS_DIR = '/opt/evilshtrib_demos'

TARGET_DEMOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demos')

def download_recent_demos(count=6):
    os.makedirs(TARGET_DEMOS_DIR, exist_ok=True)
    print(f"Connecting to VDS {VDS_HOST} via SFTP...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VDS_HOST, username=VDS_USER, password=VDS_PASS, timeout=15)
    sftp = ssh.open_sftp()
    
    files = sftp.listdir_attr(REMOTE_DEMOS_DIR)
    zip_files = [f for f in files if f.filename.endswith('.zip') and f.st_size > 5 * 1024 * 1024]
    # Sort by mtime descending (most recent first)
    zip_files.sort(key=lambda x: -x.st_mtime)
    
    selected = zip_files[:count]
    print(f"Found {len(zip_files)} eligible demo archives. Downloading latest {len(selected)}:")
    
    extracted_demos = []
    
    for idx, item in enumerate(selected):
        r_path = f"{REMOTE_DEMOS_DIR}/{item.filename}"
        local_zip = os.path.join(TARGET_DEMOS_DIR, item.filename)
        size_mb = item.st_size / (1024 * 1024)
        print(f"[{idx+1}/{len(selected)}] Downloading {item.filename} ({size_mb:.2f} MB)...")
        sftp.get(r_path, local_zip)
        
        # Extract .dem file
        with zipfile.ZipFile(local_zip, 'r') as z:
            for dem_name in z.namelist():
                if dem_name.endswith('.dem'):
                    z.extract(dem_name, TARGET_DEMOS_DIR)
                    extracted_path = os.path.join(TARGET_DEMOS_DIR, dem_name)
                    extracted_demos.append(extracted_path)
                    print(f"    Extracted: {dem_name} ({os.path.getsize(extracted_path)/(1024*1024):.1f} MB)")
        
        # Remove zip archive to save space
        try:
            os.remove(local_zip)
        except OSError:
            pass
            
    sftp.close()
    ssh.close()
    print(f"\nSuccessfully downloaded and extracted {len(extracted_demos)} demos into {TARGET_DEMOS_DIR}!")
    return extracted_demos

if __name__ == '__main__':
    download_recent_demos(6)
