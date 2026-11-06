# DevCarnival Talks, Speakers & Schedule Schema Guide

This document defines the schema, data models, cross-reference rules, and validation constraints for onboarding speakers, talks/sessions, and schedule slots in DevCarnival.

---

## 1. Directory Structure & File Relationships

```
devcarnival.github.io/
├── content/
│   ├── people/
│   │   └── <speaker-slug>.md        <-- Speaker Bio & Socials
│   └── session/
│       └── <session-slug>.md       <-- Talk/Session Abstract & Speaker Link
├── data/
│   └── schedule.yaml               <-- Day, Hall & Time Slot Placements
└── static/
    └── images/
        └── people/
            └── <speaker-slug>.<ext> <-- Local Headshot (optional, fallback to GitHub)
```

### Tripartite Linkage Contract

```
[content/people/<speaker-slug>.md]
              ▲
              │ referenced by `speakers: ["<speaker-slug>"]`
              │
[content/session/<session-slug>.md]
              ▲
              │ referenced by `session: "<session-slug>"`
              │
[data/schedule.yaml] (Keynotes slots OR Parallel track rows/cells)
```

1. **Speakers on `/speakers`** are dynamically aggregated from all active sessions where `speakers: ["<slug>"]` points to `content/people/<slug>.md`.
2. **Session Detail Pages (`/session/<slug>/`)** dynamically lookup `data/schedule.yaml` to display the scheduled Day, Time, and Hall badge.
3. **Schedule Pages (`/schedule/`)** dynamically fetch session titles, descriptions, and linked speaker headshots, company, and role from `content/session/` and `content/people/`.

---

## 2. Speaker Schema (`content/people/<speaker-slug>.md`)

### File Path
`content/people/<speaker-slug>.md` (kebab-case, e.g. `jane-doe.md`, `ksivaprasadreddy.md`)

### Frontmatter Schema (YAML)

| Field | Type | Required? | Description & Constraints |
| :--- | :--- | :--- | :--- |
| `title` | string | **Yes** | Speaker's full display name (e.g. `"Dr. Jane Doe"`). |
| `designation` | string | **Yes** | Professional title/role (e.g. `"Principal AI Architect"`, `"Professor"`). |
| `company` | string | **Yes** | Company, university, or organization name (e.g. `"IIT Madras"`, `"JetBrains"`). |
| `image` | string | Recommended | Path to local headshot relative to static root (e.g. `"images/people/jane-doe.jpeg"`). |
| `keynote` | boolean | Optional | Set to `true` if this person delivers an official Keynote (prioritizes them at the top of `/speakers`). |
| `weight` | integer | Optional | Ordering weight for speaker directory display (lower = higher priority). |
| `socials` | object | **Yes** | Map of social links: |
| `socials.github` | string | Recommended | GitHub username (critical: powers fallback avatar `https://github.com/<user>.png?size=100`). |
| `socials.linkedin`| string | Recommended | Full LinkedIn profile URL. |
| `socials.twitter` | string | Optional | Full Twitter / X profile URL. |
| `socials.website` | string | Optional | Personal website or blog URL. |

### Avatar Resolution Hierarchy
1. Local image from `image` param (`images/people/<slug>.<ext>`)
2. Local image from `images` array (`images: [...]`)
3. GitHub avatar fallback generated via `https://github.com/<socials.github>.png?size=100`
4. First-letter monogram badge (`substr .name 0 1`)

### Markdown Body Content
Write 2–4 paragraphs summarizing:
- Current role and core areas of technical expertise.
- Architecture, systems, research, or product contributions.
- Community leadership, publications, patents, open-source projects, or past speaking engagements.

---

## 3. Session / Talk Schema (`content/session/<session-slug>.md`)

### File Path
`content/session/<session-slug>.md` (kebab-case, e.g. `architecting-resilient-ai-agents.md`)

### Frontmatter Schema (YAML)

| Field | Type | Required? | Description & Constraints |
| :--- | :--- | :--- | :--- |
| `title` | string | **Yes** | Full title of the talk or workshop. |
| `slug` | string | Optional | Explicit URL slug override. Defaults to file basename. |
| `speakers` | list of strings | **Yes** | List of speaker slugs matching `content/people/<slug>.md`. |
| `years` | list of strings | **Yes** | Conference edition year, e.g. `["2027"]`. |
| `track` | string | **Yes** | Official conference track name (see valid tracks below). |
| `session_type` | string | **Yes** | Type: `"Keynote"`, `"Talk"`, or `"Workshop"`. |
| `duration` | string | **Yes** | Expected runtime, e.g. `"45 mins"`, `"60 mins"`, `"90 mins"`. |
| `communities` | list of strings | Optional | Ecosystem partner slug (e.g. `["tamilnadu-java-user-group"]`, `["chennai-react"]`). |
| `weight` | integer | Optional | Priority sort weight. |

### Valid Conference Tracks
- `AI Agents & Developer Productivity`
- `Applied AI & Systems`
- `AI Security, Infrastructure & DevOps`
- `Building AI-Powered Applications`
- `Core Java & Systems`
- `Cloud & DevOps`
- `Cyber Security`
- `Academia`

### Markdown Body Structure
Sessions must strictly follow this 4-part structure:
```markdown
<2–4 paragraphs of detailed technical abstract explaining the problem, architectural hurdles, trade-offs, and practical solution.>

### Key Takeaways
- **Takeaway 1:** Concise learning outcome.
- **Takeaway 2:** Architectural or operational pattern.
- **Takeaway 3:** Production consideration or performance metric.

### Target Audience
- <Bullet list of target engineering roles, e.g. Backend Engineers, Systems Architects, ML Practitioners>

### Prerequisites
- <Bullet list of recommended languages, frameworks, or conceptual foundations>
```

---

## 4. Schedule Schema (`data/schedule.yaml`)

### Days & Halls Configuration

#### Day 1 · AI Day & Workshops (Jan 8, 2027)
- `Main Hall`: Morning Keynotes (9:00 AM – 10:00 AM)
- `Nalantha`: Java AI Track
- `Harvard`: Applied AI & Systems Track
- `Cambridge`: Cloud & DevOps AI Track
- `Ganga`: Academia Track
- `Warren buffet`: Hands-on AI Workshops

#### Day 2 · Tech Talks (Jan 9, 2027)
- `Main Hall`: Morning Keynotes (9:00 AM – 10:00 AM)
- `Nalantha`: Core Java & Systems Track
- `Harvard`: AI Systems & Engineering Track
- `Cambridge`: Cloud & DevOps Track
- `Ganga`: Cyber Security Track
- `Warren buffet`: Applied AI & Deep Tech Track

### Schedule Entry Types

#### Type A: Keynote Slot (Main Hall)
Placed under `days -> [id: "day1" / "day2"] -> keynotes -> slots`:
```yaml
- time: "09:00 AM – 09:20 AM"
  title: "Title of Keynote"
  session: "session-slug"
```

#### Type B: Standard Track Talk
Placed under `days -> [id: "day1" / "day2"] -> rows -> [matching time] -> cells`:
```yaml
- hall: "Nalantha"
  session: "session-slug"
```

#### Type C: Extended Workshop / Multi-Slot Session
Placed under `cells` with `range` and `rowspan`:
```yaml
- hall: "Warren buffet"
  session: "session-slug"
  range: "10:00 AM – 11:30 AM · Hands-on Workshop"
  rowspan: 2
```
