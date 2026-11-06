#!/usr/bin/env python3
"""
Helper script to inspect existing Tech Pavilion projects and determine the next booth number.
"""

import glob
import os
import re

def get_next_booth(projects_dir="content/projects"):
    pattern = os.path.join(projects_dir, "*.md")
    files = glob.glob(pattern)
    booths = []
    
    for f in files:
        if os.path.basename(f) == "_index.md":
            continue
        try:
            with open(f, "r", encoding="utf-8") as fp:
                for line in fp:
                    m = re.search(r'booth_number:\s*["\']?TP-(\d+)', line)
                    if m:
                        booths.append((int(m.group(1)), os.path.basename(f)))
        except Exception as e:
            print(f"Warning reading {f}: {e}")
            
    booths.sort(key=lambda x: x[0])
    highest = booths[-1][0] if booths else 0
    next_booth = highest + 1
    
    print(f"Current Registered Tech Pavilion Projects: {len(booths)}")
    for num, fname in booths:
        print(f"  - TP-{num:02d}: {fname}")
    print(f"\nNext Available Booth Number: TP-{next_booth:02d}")
    return f"TP-{next_booth:02d}"

if __name__ == "__main__":
    get_next_booth()
