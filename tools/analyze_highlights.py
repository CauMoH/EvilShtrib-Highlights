"""
Highlight Analyzer for EvilShtrib CS 1.6 Demos.
Parses GoldSource Protocol 48 HLTV demos to detect and score verified zombie kills.
"""

import os
import glob
import struct
import re
from collections import defaultdict, Counter

DEMOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demos')

CS_WEAPONS = {
    'awp': 50,
    'hegrenade': 45,
    'grenade': 45,
    'deagle': 40,
    'xm1014': 35,
    'm3': 35,
    'scout': 35,
    'ak47': 30,
    'm4a1': 25,
    'elite': 25,
    'p228': 25,
    'fiveseven': 25,
    'usp': 25,
    'glock18': 25,
    'glock': 25,
    'mp5navy': 20,
    'ump45': 20,
    'p90': 20,
    'mac10': 20,
    'tmp': 20,
    'galil': 25,
    'famas': 25,
    'sg550': 25,
    'g3sg1': 25,
    'sg552': 25,
    'aug': 25,
    'm249': 25,
}

def parse_demo_kills(dem_path):
    with open(dem_path, 'rb') as f:
        header = f.read(544)
        map_name = header[16:276].split(b'\0')[0].decode('ascii', errors='ignore')
        dir_offset = struct.unpack('<II', header[536:544])[1]
        
        f.seek(dir_offset)
        num_entries = struct.unpack('<I', f.read(4))[0]
        entries = []
        for _ in range(num_entries):
            e_type, desc, flags, play, track_time, frame_num, offset, flen = struct.unpack('<I64sIIfIII', f.read(92))
            entries.append((e_type, desc.split(b'\0')[0].decode('ascii', errors='ignore'), offset, flen))
            
        playback_offset = entries[1][2]
        playback_len = entries[1][3]
        f.seek(playback_offset)
        data = f.read(playback_len)

    # Extract player names from svc_updateuserinfo (0x0D = 13)
    player_names = {}
    for m in re.finditer(rb'\x0d([\x01-\x20])(....)\\name\\([^\\]+)', data):
        slot = m.group(1)[0]
        name = m.group(3).decode('latin1', 'ignore').strip()
        if name and name != "HLTV":
            player_names[slot] = name

    # Fallback to status strings if any slot missing
    for m in re.finditer(rb'#\s*(\d+)\s+\"([^\"]{2,32})\"', data):
        try:
            raw_name = m.group(2)
            if all(32 <= b <= 126 for b in raw_name):
                pid = int(m.group(1).decode())
                pname = raw_name.decode('ascii').strip()
                if pid not in player_names and 2 <= len(pname) <= 24:
                    player_names[pid] = pname
        except Exception:
            pass

    pos = 0
    kills = []
    
    while pos < len(data) - 9:
        ftype = data[pos]
        time_val, frame_idx = struct.unpack('<fI', data[pos+1:pos+9])
        pos += 9
        
        if ftype in (0, 1):
            if pos + 468 > len(data):
                break
            msg_len = struct.unpack('<I', data[pos+464:pos+468])[0]
            block_start = pos + 468
            block_end = block_start + msg_len
            pos = block_end
            
            # Scan for DeathMsg (ID 83)
            p = block_start
            while p < block_end - 6:
                if data[p] == 83: # DeathMsg
                    mlen = data[p+1]
                    if 4 <= mlen <= 20 and p + 2 + mlen <= block_end:
                        k = data[p+2]
                        v = data[p+3]
                        hs = data[p+4]
                        w_raw = data[p+5:p+2+mlen].split(b'\0')[0]
                        try:
                            w_name = w_raw.decode('ascii').lower()
                            if w_name in CS_WEAPONS and k != 0 and k != v:
                                kname = player_names.get(k, f"Player_{k}")
                                vname = player_names.get(v, f"Zombie_{v}")
                                kills.append({
                                    'time': time_val,
                                    'frame': frame_idx,
                                    'killer': k,
                                    'killer_name': kname,
                                    'victim': v,
                                    'victim_name': vname,
                                    'weapon': w_name,
                                    'headshot': bool(hs),
                                    'map': map_name,
                                    'demo_file': os.path.basename(dem_path)
                                })
                                p += 2 + mlen - 1
                        except Exception:
                            pass
                p += 1
        elif ftype == 2:
            pass
        elif ftype == 3:
            pos += 64
        elif ftype == 4:
            pos += 32
        elif ftype == 5:
            break
        elif ftype == 6:
            pos += 96
        elif ftype == 7:
            pos += 8
        elif ftype == 8:
            if pos + 8 > len(data): break
            slen = struct.unpack('<I', data[pos+4:pos+8])[0]
            pos += 8 + slen + 16
        elif ftype == 9:
            if pos + 4 > len(data): break
            blen = struct.unpack('<I', data[pos:pos+4])[0]
            pos += 4 + blen
        else:
            break
            
    return map_name, player_names, kills

def cluster_moments(kills):
    if not kills:
        return []
        
    candidates = []
    kills.sort(key=lambda x: x['time'])
    
    # Group by killer
    by_killer = defaultdict(list)
    for k in kills:
        by_killer[k['killer']].append(k)
        
    for killer_id, klist in by_killer.items():
        i = 0
        while i < len(klist):
            group = [klist[i]]
            j = i + 1
            while j < len(klist) and (klist[j]['time'] - group[0]['time']) <= 6.0:
                group.append(klist[j])
                j += 1
                
            first_time = group[0]['time']
            last_time = group[-1]['time']
            
            # Start 2.5s before first kill, end 2.5s after last kill
            t_start = max(1.0, first_time - 2.5)
            t_end = last_time + 3.0
            duration = t_end - t_start
            
            # Clamp duration to 5.0 - 9.0 seconds
            if duration < 5.0:
                t_start = max(1.0, t_start - (5.0 - duration) / 2)
                t_end = t_start + 5.5
                duration = t_end - t_start
            elif duration > 9.5:
                duration = 9.5
                t_end = t_start + 9.5

            score = 0
            num_kills = len(group)
            
            if num_kills >= 3:
                score += 150
            elif num_kills == 2:
                score += 70
            else:
                score += 30
                
            has_hs = False
            weapons_used = set()
            for k in group:
                w = k['weapon']
                weapons_used.add(w)
                score += CS_WEAPONS.get(w, 20)
                if k['headshot']:
                    score += 35
                    has_hs = True
                    
            candidates.append({
                'score': score,
                'demo_file': group[0]['demo_file'],
                'map': group[0]['map'],
                'killer_id': killer_id,
                'killer_name': group[0]['killer_name'],
                'num_kills': num_kills,
                'kills': group,
                'weapons': list(weapons_used),
                'has_headshot': has_hs,
                'time_start': round(t_start, 2),
                'time_end': round(t_end, 2),
                'duration': round(duration, 2),
                'kill_time': round(first_time, 2)
            })
            
            i = j
            
    return candidates

def find_top_highlights(count=10):
    demo_files = sorted(glob.glob(os.path.join(DEMOS_DIR, '*.dem')))
    print(f"Scanning {len(demo_files)} demos for highlight moments...")
    
    all_candidates = []
    
    for df in demo_files:
        mname, pnames, kills = parse_demo_kills(df)
        candidates = cluster_moments(kills)
        all_candidates.extend(candidates)
        print(f"  [{os.path.basename(df)}]: {len(kills)} verified zombie kills -> {len(candidates)} candidate moments")

    all_candidates.sort(key=lambda x: -x['score'])
    
    selected = []
    seen = set()
    weapon_counts = Counter()
    
    for c in all_candidates:
        key = (c['demo_file'], c['killer_id'], int(c['time_start'] / 15))
        if key in seen:
            continue
            
        primary_w = c['weapons'][0]
        if weapon_counts[primary_w] >= 2 and len(selected) < count - 2:
            continue
            
        selected.append(c)
        seen.add(key)
        weapon_counts[primary_w] += 1
        
        if len(selected) >= count:
            break
            
    if len(selected) < count:
        for c in all_candidates:
            if c not in selected:
                selected.append(c)
                if len(selected) >= count:
                    break

    print(f"\n=======================================================")
    print(f"TOP {len(selected)} HIGHLIGHT MOMENTS SELECTED:")
    print(f"=======================================================")
    for idx, h in enumerate(selected):
        w_str = ", ".join(h['weapons']).upper()
        hs_str = " [HEADSHOT]" if h['has_headshot'] else ""
        v_str = ", ".join([f"{k['victim_name']} ({k['weapon']})" for k in h['kills']])
        print(f"#{idx+1:02d} | Score: {h['score']:3d} | Map: {h['map']:18s} | Window: {h['time_start']:6.1f}s - {h['time_end']:6.1f}s ({h['duration']}s)")
        print(f"     Killer: {h['killer_name']} ({h['num_kills']} kills) with {w_str}{hs_str}")
        print(f"     Victims: {v_str}")
        print(f"     Demo: {h['demo_file']}")
        print("-------------------------------------------------------")
        
    return selected

if __name__ == '__main__':
    find_top_highlights(10)
