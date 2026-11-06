---
name: onboard-talks-speakers-schedule
description: Use this skill when onboarding new speakers, talks/sessions, and schedule slots into DevCarnival (content/people/, content/session/, and data/schedule.yaml). Validates speaker profiles, session abstracts, takeaways, and schedule slot assignments, prompts user for clarification if details are missing, and verifies site build integrity.
---

# DevCarnival Talks, Speakers & Schedule Onboarding Skill

This skill guides the agent through onboarding **speakers**, **talks/sessions**, and **schedule slots** into DevCarnival 2027.

The site architecture connects these three entities dynamically:
1. **Speaker Profile:** `content/people/<speaker-slug>.md`
2. **Talk / Session Abstract:** `content/session/<session-slug>.md` (links to speaker slug)
3. **Schedule Placement:** `data/schedule.yaml` (places session slug into Day, Hall, and Time slot)

---

## 1. Requirements & Validation Checklist

Before creating or editing any files, inspect the user's provided input. If **any** required field is missing, ambiguous, or incomplete, **pause and ask the user to clarify** before proceeding.

### 1.1 Speaker Requirements Checklist (`content/people/`)

| Field | Description | If Missing |
| :--- | :--- | :--- |
| **Speaker Name** | Full name with prefix/titles if applicable (e.g. "Prof. Kamakoti Veezhinathan") | **Ask user** |
| **Designation** | Professional title/role (e.g. "Director", "Principal Architect", "Developer Advocate") | **Ask user** |
| **Company / Institution** | Organization name (e.g. "IIT Madras", "JetBrains", "Google") | **Ask user** |
| **Biography** | 2–4 paragraphs detailing experience, technical focus, and achievements | Draft from provided notes or **ask user** |
| **GitHub Handle** | GitHub username (critical: renders speaker avatar fallback on schedule & speaker cards) | **Ask user** |
| **LinkedIn URL** | LinkedIn profile link | **Ask user** |
| **Photo / Image** | Local image in `static/images/people/<slug>.<ext>` or fallback via GitHub handle | Use GitHub avatar if no photo file provided |
| **Keynote Flag** | `keynote: true` if this speaker delivers an official Keynote | Default: `false` unless explicitly stated |

### 1.2 Talk / Session Requirements Checklist (`content/session/`)

| Field | Description | If Missing |
| :--- | :--- | :--- |
| **Session Title** | Full descriptive title of the session | **Ask user** |
| **Abstract / Description** | 2–4 paragraphs explaining technical problem, architecture, and solution | **Ask user** |
| **Key Takeaways** | 3–4 bulleted points of concrete learnings | Synthesize from abstract and confirm, or **ask user** |
| **Target Audience** | Who should attend (e.g. Backend Engineers, Systems Architects) | Infer from topic and confirm, or **ask user** |
| **Prerequisites** | Background knowledge or technical proficiency needed | Infer from depth or **ask user** |
| **Track** | Conference track (e.g. "AI Agents & Developer Productivity", "Cloud & DevOps") | Match to closest track or **ask user** |
| **Session Type** | `"Keynote"`, `"Talk"`, or `"Workshop"` | Default: `"Talk"` |
| **Duration** | Expected length (e.g. `"45 mins"`, `"60 mins"`, `"90 mins"`) | Infer from session type / schedule slot |
| **Year** | Conference edition year: `["2027"]` | Always `["2027"]` |

### 1.3 Schedule Placement Checklist (`data/schedule.yaml`)

| Field | Description | If Missing |
| :--- | :--- | :--- |
| **Conference Day** | `day1` (Jan 8, 2027) or `day2` (Jan 9, 2027) | **Ask user** if schedule placement is requested |
| **Venue / Hall** | Hall name (Main Hall for Keynotes; Nalantha, Harvard, Cambridge, Ganga, Warren buffet for tracks) | **Ask user** or infer from track |
| **Time Slot** | Start and end time (e.g. "10:00 AM – 10:45 AM") | **Ask user** |

---

## 2. Interactive Clarification Flow (When Data is Insufficient)

If any required detail is missing, ambiguous, or contradictory, do not invent dummy details or use placeholder values like `TBD` or `unknown`. Immediately prompt the user with a structured questionnaire:

```markdown
I have reviewed the details for the proposed speaker and session: **[Title / Speaker Name]**. To ensure full adherence to DevCarnival standards and proper rendering across the Speaker Directory, Session Details, and Schedule Grid, please provide the following missing details:

1. **Speaker Profile Details:**
   - Full Name & Honorifics:
   - Designation / Role: (e.g., Lead AI Architect)
   - Company / University / Organization:
   - GitHub Username: (Required for avatar rendering)
   - LinkedIn Profile URL:
   - Speaker Bio (or bullet points to draft from):
   - Is this speaker delivering an official Keynote? (Yes / No)

2. **Session / Talk Details:**
   - Talk Title:
   - Target Track: (e.g., AI Agents & Developer Productivity, Cloud & DevOps, Applied AI & Systems, etc.)
   - Session Type: (Talk / Workshop / Keynote)
   - Core Abstract / Problem Statement:
   - Key Takeaways (3–4 takeaways):
   - Target Audience & Prerequisites:

3. **Schedule Placement (Optional):**
   - Day: (Day 1 - Jan 8 / Day 2 - Jan 9)
   - Hall / Venue: (Nalantha, Harvard, Cambridge, Ganga, Warren buffet, Main Hall)
   - Time Slot: (e.g., 10:45 AM – 11:30 AM)
```

Once the user provides the answers, proceed with implementation.

---

## 3. Step-by-Step Onboarding Procedure

### Step 3.1: Generate Slugs
- Speaker Slug: Convert full name to lowercase kebab-case (e.g., "Jane Doe" -> `jane-doe`).
- Session Slug: Convert talk title to lowercase kebab-case (e.g., "Architecting Resilient Multi-Agent AI Workflows" -> `architecting-resilient-multi-agent-ai-workflows`).

### Step 3.2: Create Speaker Profile (`content/people/<speaker-slug>.md`)
Check if the speaker file already exists. If not, create it:

```yaml
---
title: "<Speaker Name>"
designation: "<Designation>"
company: "<Company>"
image: "<images/people/slug.jpeg or omit if relying on GitHub avatar>"
keynote: <true/false>
weight: <optional integer>
socials:
  github: "<github_username>"
  linkedin: "<linkedin_url>"
  twitter: "<twitter_url or omit>"
  website: "<website_url or omit>"
---

<Speaker biography narrative paragraphs.>
```

If a headshot file was provided by the user, copy it to `static/images/people/<speaker-slug>.<ext>` and reference it in the `image` field.

### Step 3.3: Create Talk / Session (`content/session/<session-slug>.md`)
Create the session file, ensuring the `speakers` array references the exact speaker slug from Step 3.2:

```yaml
---
title: "<Session Title>"
slug: "<session-slug>"
speakers:
  - "<speaker-slug>"
communities:
  - "<community-slug if affiliated, e.g. tamilnadu-java-user-group>"
years: ["2027"]
track: "<Track Name>"
session_type: "<Talk / Workshop / Keynote>"
duration: "<Duration, e.g. 45 mins>"
weight: <optional integer>
---

<2–4 paragraphs of deep technical abstract describing the problem, challenges, and solution.>

### Key Takeaways
- **<Highlight 1>:** <Detail>
- **<Highlight 2>:** <Detail>
- **<Highlight 3>:** <Detail>

### Target Audience
- <Target roles and technical profiles>

### Prerequisites
- <Recommended knowledge and technical background>
```

### Step 3.4: Integrate with Schedule (`data/schedule.yaml`)
If the user specified a time slot and hall, integrate the session into `data/schedule.yaml`:

- **For Keynotes:**
  Add under `days -> [day1/day2] -> keynotes -> slots`:
  ```yaml
  - time: "<Time Range>"
    title: "<Keynote Title>"
    session: "<session-slug>"
  ```

- **For Parallel Track Talks:**
  Find the row corresponding to `<Time Range>` in `days -> [day1/day2] -> rows`, and add to `cells`:
  ```yaml
  - hall: "<Hall Name>"
    session: "<session-slug>"
  ```

- **For Multi-slot Workshops:**
  Specify `range` and `rowspan`:
  ```yaml
  - hall: "Warren buffet"
    session: "<session-slug>"
    range: "10:00 AM – 11:30 AM · Hands-on Workshop"
    rowspan: 2
  ```

---

## 4. Verification and Integrity Check

Always run both validation checks after onboarding:

1. **Cross-Reference & Schema Integrity Script:**
   ```bash
   python3 .agents/skills/onboard-talks-speakers-schedule/scripts/validate_schedule_and_speakers.py
   ```
   Verify that:
   - Script exits with `code 0`.
   - All session speaker references map to valid people files.
   - All schedule session references map to valid session files.

2. **Hugo Site Build:**
   ```bash
   hugo
   ```
   Verify that:
   - Hugo exits with status `0` without template errors.
   - New pages exist in `public/session/<session-slug>/index.html` and speaker profile is present on `/speakers/`.
   - If scheduled, verify `/schedule/` displays the talk card with linked speaker info and avatar.

3. **Report to User:**
   Summarize the newly onboarded speaker, talk, and schedule slot with direct markdown links to the created files, noting verification status and any next steps.
