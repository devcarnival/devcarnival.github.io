---
name: onboard-tech-pavilion
description: Use this skill when onboarding new student or developer showcase projects and teams into the DevCarnival Tech Pavilion (content/projects/). Validates required project and team data, queries the user if any details are missing, auto-assigns next booth ID (TP-XX), generates Hugo markdown conforming to site templates, and verifies build integrity.
---

# Tech Pavilion Project & Team Onboarding Skill

This skill guides the agent through onboarding projects and their team presenters into the DevCarnival **Tech Pavilion** (`content/projects/`) for **Expo 2027**.

The Tech Pavilion is a 2-day hands-on exhibition allowing student innovators and developer teams (maximum **2 members** per team) to showcase functional prototypes, open-source projects, and developer tools to conference attendees, mentors, and industry leaders at DevCarnival 2027 (Expo 2027).

---

## 1. Requirements & Validation Checklist

Before creating a project file, inspect the user's provided input. If **any** required field is missing or ambiguous, **pause and ask the user to provide the missing details** before proceeding.

### Required Fields Checklist

| Field | Description | If Missing |
| :--- | :--- | :--- |
| **Project Title** | Name of the project (e.g. "Alumnex Connect") | **Ask user** |
| **Summary** | 1–2 concise sentences explaining what the project does (~140 chars) | Can draft from description and confirm with user |
| **Participants (1–2 members max)** | • Full Name<br>• Role (default: "Student Innovator")<br>• Email address<br>• GitHub username or URL (critical for avatar)<br>• LinkedIn profile URL | **Ask user** if missing name, email, or GitHub |
| **Institution** | College / University / Organization (e.g., "Kongu Engineering College") | **Ask user** |
| **Business Domain** | List of domains (e.g., "Education", "Developer Tools", "AgriTech", "FinTech", "HealthTech") | Infer from project description or **ask user** |
| **Tech Domain** | List of tech categories (e.g., "Web Systems", "Cloud", "AI/ML", "DevOps", "IoT", "Testing") | Infer from tech stack or **ask user** |
| **Tech Stack / Tags** | Technologies and frameworks used (e.g. `React`, `Node.js`, `Go`, `Docker`) | Extract from description or **ask user** |
| **Project Type** | e.g. `"OPEN SOURCE"`, `"Friendly Coders"`, `"Student Innovation"`, `"Prototype"` | Default to `"Student Innovation"` or `"OPEN SOURCE"` |

### Optional Fields Checklist
- `demo_url`: Live deployment or web app link
- `github_url`: GitHub source repository URL
- `community`: Affiliated ecosystem partner community (e.g. "TAMILNADU JAVA USERS GROUP")
- `hero_image`: Image under `/images/projects/...` (optional)
- `booth_number`: e.g. `TP-04` (auto-assigned if not specified)

---

## 2. Interactive Clarification Flow (When Data is Insufficient)

When any of the required details are missing, do not guess or use placeholder values like `TBD` or `unknown@example.com`. Prompt the user with a structured questionnaire:

```markdown
I have reviewed the project details for **[Project Title]**. To complete the Tech Pavilion onboarding according to DevCarnival standards, please provide the following missing details:

1. **Team Participants (Max 2 members):**
   - Member 1: Full Name, Email, GitHub profile URL, LinkedIn profile URL, Role (default: "Student Innovator")
   - Member 2 (if any): Full Name, Email, GitHub profile URL, LinkedIn profile URL, Role
2. **Institution / College Name:** (e.g. Kongu Engineering College, Anna University)
3. **Target Domains:**
   - Business Domain: (e.g. Developer Tools, Education, HealthTech, etc.)
   - Technical Domain: (e.g. Web Systems, Cloud, AI/ML, DevOps, Testing, etc.)
4. **Links (Optional but recommended):**
   - Live Demo URL:
   - GitHub Repository URL:
```

Once the user provides the missing details, proceed immediately to onboarding.

---

## 3. Step-by-Step Onboarding Procedure

### Step 3.1: Determine Next Booth Number (`TP-XX`)
Check existing project booth numbers using the helper script:
```bash
python3 .agents/skills/onboard-tech-pavilion/scripts/get_next_booth.py
```
Or inspect `content/projects/*.md` for the highest existing `TP-XX`. Assign the next sequential booth (e.g., if TP-01, TP-02, TP-03 exist, use `TP-04`).

### Step 3.2: Generate File Slug and Path
1. Convert the project title to lowercase, hyphen-separated kebab-case (e.g., "Sixter Tunnel" -> `sixter-tunnel`).
2. Target file path: `content/projects/<slug>.md`.

### Step 3.3: Compose YAML Frontmatter
Ensure the frontmatter matches the exact schema used in `content/projects/`:

```yaml
---
title: "<Project Title>"
date: <Current Timestamp in ISO format, e.g. 2027-01-08T10:00:00+05:30>
draft: false
summary: "<1-2 sentence punchy summary>"
demo_url: "<Demo URL or omit if not provided>"
github_url: "<Repo URL or omit if not provided>"
project_type: "<Project Type, e.g. OPEN SOURCE / Student Innovation>"
booth_number: "<TP-XX>"
community: "<Community Name if affiliated>"
institution: "<College / University Name>"
participant_type: "Students"

business_domains:
  - "<Business Domain>"

tech_domains:
  - "<Tech Domain>"

tags:
  - "<Tag 1>"
  - "<Tag 2>"

participants:
  - name: "<Participant 1 Name>"
    role: "<Role, default Student Innovator>"
    email: "<email@domain.com>"
    linkedin: "<LinkedIn URL>"
    github: "<GitHub URL>"
  - name: "<Participant 2 Name>"
    role: "<Role, default Student Innovator>"
    email: "<email@domain.com>"
    linkedin: "<LinkedIn URL>"
    github: "<GitHub URL>"
---
```

> **Important Avatar Note:** `layouts/projects/single.html` parses GitHub handles from `github` URLs to render the presenter's avatar (`https://github.com/<user>.png?size=160`). Always ensure valid GitHub URLs or usernames are included for participants.

### Step 3.4: Compose Markdown Body Content
Structure the body narrative with clear engineering depth:

```markdown
## Overview

<Describe the industry or educational problem, why existing workflows fail, and the concrete solution this project provides. Reference relevant UN Sustainable Development Goals (e.g. SDG 4, SDG 8, SDG 9) if applicable.>

### <Feature / Workflow / Key Capability 1>

<Detailed walkthrough of primary user flows, system modules, or capabilities.>

### Architecture & Technology Stack

- **Frontend:** <Frameworks, UI libraries, state management, design tokens>
- **Backend:** <Language, web framework, concurrency/routing model>
- **Database / Storage:** <Databases, caching layers, schemas>
- **Security & Authentication:** <Auth methods, session tokens, rate limiting>
- **APIs & Integrations:** <Third-party APIs, AI endpoints, webhooks>

### Future Roadmap (Optional)

<Planned milestones, scalability goals, or production rollout.>
```

### Step 3.5: Create the File
Write the content to `content/projects/<slug>.md`.

---

## 4. Verification and Site Build Check

Always verify the newly created project:
1. Run the Hugo build to check for template or syntax errors:
   ```bash
   hugo
   ```
2. Verify that:
   - Output includes the new page (e.g. `public/projects/<slug>/index.html`).
   - Hugo exits with status `0` without template rendering failures.
3. Inform the user of the created project, its assigned booth number, its URL (`/projects/<slug>/`), and summarize the onboarded team.
