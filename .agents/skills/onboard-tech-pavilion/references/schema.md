# Tech Pavilion Project Schema & Reference Guide

This document defines the data schema, conventions, and formatting requirements for Tech Pavilion projects in DevCarnival (`content/projects/`) for **Expo 2027**.

## File Location & Naming
- **Directory:** `content/projects/`
- **Filename:** `<project-slug>.md` (kebab-case, e.g. `alumnex-connect.md`, `sixter-tunnel.md`, `raithu-agritech.md`)
- **URL Path:** `/projects/<project-slug>/`

## Frontmatter Fields (YAML)

| Field | Type | Required? | Description & Constraints |
| :--- | :--- | :--- | :--- |
| `title` | string | **Yes** | Project name displayed on the card and detail page. |
| `date` | timestamp | **Yes** | ISO-8601 timestamp with IST offset, e.g., `2027-01-08T10:00:00+05:30`. |
| `draft` | boolean | **Yes** | Set to `false` for active published projects. |
| `summary` | string | **Yes** | 1–2 sentence punchy overview (rendered in card preview, truncated at 140 chars in list). |
| `booth_number` | string | **Yes** | Booth identifier in the format `TP-XX` (e.g., `TP-01`, `TP-04`). Auto-incremented sequentially. |
| `project_type` | string | **Yes** | Project categorization (e.g., `"OPEN SOURCE"`, `"Friendly Coders"`, `"Student Innovation"`, `"Prototype"`). |
| `institution` | string | **Yes** | University or college name (e.g., `"Kongu Engineering College"`, `"IIT Madras"`). |
| `participant_type` | string | **Yes** | Primary participant demographic (`"Students"`, `"Professionals"`, `"Researchers"`). Default: `"Students"`. |
| `business_domains` | list of strings | **Yes** | Business domains used by the list page filter dropdown (e.g., `["Education"]`, `["Developer Tools"]`, `["AgriTech"]`). |
| `tech_domains` | list of strings | **Yes** | Technical domains used by the list page filter dropdown (e.g., `["Web Systems"]`, `["Cloud"]`, `["AI/ML"]`). |
| `tags` | list of strings | Recommended | Technologies, frameworks, and architecture tags (e.g., `["React", "Node.js", "Docker"]`). |
| `demo_url` | string (URL) | Optional | Live deployment or demo site URL. |
| `github_url` | string (URL) | Optional | Project source repository URL. |
| `community` | string | Optional | Partner tech community (e.g., `"TAMILNADU JAVA USERS GROUP"`, `"Cloud Native Chennai"`). |
| `hero_image` | string | Optional | Path to hero image in `/images/projects/...`. |
| `participants` | list of objects | **Yes** | List of team members / presenters. **Max 2 members** per Tech Pavilion regulations. |

### Participant Object Schema

```yaml
participants:
  - name: "Full Name"
    role: "Student Innovator"              # Role title (e.g., "Student Innovator", "Lead Developer")
    email: "email@domain.com"              # Contact email
    linkedin: "https://www.linkedin.com/in/..." # Optional LinkedIn URL
    github: "https://github.com/username"  # Required for avatar rendering: https://github.com/<username>.png?size=160
```

> **GitHub Avatar Mechanism:** The layout `layouts/projects/single.html` extracts the GitHub username from the `github` field URL using regex and pulls their profile picture via `https://github.com/<username>.png?size=160`. If absent, an initial badge is rendered.

## Taxonomies & Filtering

The DevCarnival site (`config.toml`) indexes two dedicated taxonomies for Tech Pavilion filtering:
1. `business_domains`: Powers `<select id="businessFilter">` on `/projects/`.
   - Examples: `Education`, `Developer Tools`, `AgriTech`, `HealthTech`, `FinTech`, `Cybersecurity`, `E-Commerce`.
2. `tech_domains`: Powers `<select id="techFilter">` on `/projects/`.
   - Examples: `Web Systems`, `Cloud`, `DevOps`, `AI/ML`, `Mobile`, `IoT & Embedded`, `Distributed Systems`.

New values added to these arrays in project markdown files automatically appear in the filter dropdowns upon Hugo build.

## Markdown Body Content Standard

The body markdown should follow this structured narrative:

1. `## Overview`
   - Problem Statement: What problem does this solve? Why is it difficult or inefficient today?
   - Solution & Value Proposition: How does the project solve it?
   - Social or Industry Impact (mention relevant UN SDGs, e.g. SDG 4 Quality Education, SDG 8 Decent Work, SDG 9 Innovation, if applicable).
2. `### Key Highlights & Features` or Feature Subsections
   - Detail key modules, user journeys, or unique innovations.
3. `### Architecture & Technology Stack`
   - Bulleted breakdown covering Frontend, Backend, Database, Security & Authentication, DevOps/Infrastructure, and Integrations/APIs.
4. `### Roadmap & Future Enhancements` (Optional)
   - Planned capabilities, multi-node scaling, or future releases.
