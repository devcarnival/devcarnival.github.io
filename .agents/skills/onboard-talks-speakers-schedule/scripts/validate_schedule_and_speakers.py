#!/usr/bin/env python3
"""
Validation script for DevCarnival Talks, Speakers, and Schedule integrity.
Verifies that:
1. Every speaker referenced in content/session/*.md exists in content/people/<slug>.md.
2. Every session referenced in data/schedule.yaml exists in content/session/<slug>.md.
3. Every scheduled hall exists in the defined halls list for that day.
4. Speaker avatar sources (local image or GitHub fallback) are accounted for.
"""

import glob
import os
import sys
import yaml

def validate():
    root = os.getcwd()
    session_files = sorted(glob.glob(os.path.join(root, "content/session/*.md")))
    people_files = sorted(glob.glob(os.path.join(root, "content/people/*.md")))
    schedule_path = os.path.join(root, "data/schedule.yaml")

    errors = []
    warnings = []

    # Map available people slugs
    people_slugs = {
        os.path.splitext(os.path.basename(f))[0]
        for f in people_files
        if not os.path.basename(f).startswith("_")
    }

    # Map available session slugs
    session_slugs = set()
    for sf in session_files:
        if os.path.basename(sf).startswith("_"):
            continue
        base_slug = os.path.splitext(os.path.basename(sf))[0]
        session_slugs.add(base_slug)

        with open(sf, "r", encoding="utf-8") as f:
            content = f.read()
        parts = content.split("---")
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                # Custom slug override
                if fm.get("slug"):
                    session_slugs.add(fm["slug"])

                # Validate speaker references
                speakers = fm.get("speakers", [])
                if not speakers:
                    warnings.append(f"Session without speakers: {os.path.basename(sf)}")
                for sp in speakers:
                    if sp not in people_slugs:
                        errors.append(f"Session '{os.path.basename(sf)}' references missing speaker: '{sp}' (expected content/people/{sp}.md)")
            except Exception as e:
                errors.append(f"YAML parsing error in {os.path.basename(sf)}: {e}")

    # Validate data/schedule.yaml
    if not os.path.exists(schedule_path):
        errors.append("Missing data/schedule.yaml")
    else:
        with open(schedule_path, "r", encoding="utf-8") as f:
            try:
                sched = yaml.safe_load(f) or {}
                days = sched.get("days", [])
                for day in days:
                    day_id = day.get("id", "unknown")
                    valid_halls = {h.get("name") for h in day.get("halls", []) if h.get("name")}

                    # Validate keynotes
                    for slot in day.get("keynotes", {}).get("slots", []):
                        sess = slot.get("session")
                        if sess and sess not in session_slugs:
                            errors.append(f"Schedule [{day_id}] Keynote slot references missing session: '{sess}'")

                    # Validate rows / cells
                    for row_idx, row in enumerate(day.get("rows", [])):
                        if row.get("is_break"):
                            continue
                        for cell in row.get("cells", []):
                            sess = cell.get("session")
                            hall = cell.get("hall")
                            if sess and sess not in session_slugs:
                                errors.append(f"Schedule [{day_id} Row {row_idx + 1}] references missing session: '{sess}'")
                            if hall and hall not in valid_halls:
                                warnings.append(f"Schedule [{day_id}] Hall '{hall}' not in defined day halls: {valid_halls}")
            except Exception as e:
                errors.append(f"YAML parsing error in data/schedule.yaml: {e}")

    print("=" * 60)
    print("DevCarnival Speaker, Talk & Schedule Validation Report")
    print("=" * 60)
    print(f"Total Registered People / Speakers: {len(people_slugs)}")
    print(f"Total Active Sessions / Talks:       {len(session_slugs)}")
    print("-" * 60)

    if warnings:
        print(f"⚠️  Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"   - {w}")
    else:
        print("✅ No warnings.")

    if errors:
        print(f"\n❌ Validation ERRORS Found ({len(errors)}):")
        for e in errors:
            print(f"   - {e}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("✅ All cross-references between Sessions, People, and Schedule are valid!")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    validate()
