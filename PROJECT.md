# DevCarnival Site — Project Overview

The public website for **DevCarnival**, a two-day global tech festival in Chennai
(Infosys, Mahindra City) that brings together tech communities, industry, and
academia. Tagline: *"Technology. People. Purpose."*

This document describes how the site is built, the content model it relies on,
and the known rough edges.

---

## 1. Stack

| Aspect | Choice |
| --- | --- |
| Generator | **Hugo** (extended, `0.120.4` pinned in CI) |
| Config | `config.toml` (single file, no environment overrides) |
| Theme | **None** — every template is hand-written in `layouts/` |
| CSS framework | Bootstrap **5.3.2** via jsDelivr CDN |
| Custom CSS | `static/css/style.css` — plain CSS, design tokens in `:root` |
| Fonts | Plus Jakarta Sans (Google Fonts) |
| JS | Bootstrap bundle (CDN) + one inline script for project filtering |
| Build tooling | None. No `package.json`, no npm, no Sass sources |
| Hosting | GitHub Pages via `.github/workflows/hugo.yml` |

Local development:

```sh
hugo server --cleanDestinationDir --disableFastRender
```

Deployment is fully automatic: any push to `main` (or a manual
`workflow_dispatch`) builds with `hugo --minify` and publishes `./public` to
GitHub Pages. `baseURL` is injected at build time from
`actions/configure-pages`, so the `https://example.com/` placeholder in
`config.toml` only affects local builds.

---

## 2. Design language

Defined entirely through CSS custom properties in `static/css/style.css`:

- **Light, near-white surfaces** (`--dc-bg: #fcfcfd`), slate text ramp
  (`#0f172a` → `#475569` → `#94a3b8`), hairline borders.
- **Signature accent**: a 135° indigo → violet → pink gradient
  (`#4f46e5 → #7c3aed → #db2777`), applied as `.text-gradient` on the word
  users should notice ("Purpose.", "Pavilion") and as a soft radial wash behind
  hero sections.
- **Glassmorphic sticky navbar** (translucent white + `backdrop-filter: blur`).
- **Motion**: consistent `cubic-bezier(0.16, 1, 0.3, 1)` easing; cards and
  buttons lift 2–4px on hover with a soft shadow.
- Two button styles only: `.btn-minimal` (solid near-black) and
  `.btn-outline-minimal` (hairline outline).
- The footer is `fixed-bottom`; `body` carries `padding-bottom: 80px` to
  compensate.

Note that layouts mix these custom classes with raw Bootstrap utilities, and
mix `rounded-0` (sharp cards in session/community/team layouts) with
`--dc-radius-*` rounded cards (projects, home). The visual language is not
fully unified across sections.

---

## 3. Content model

The interesting part of this project. Content is a small **relational model
expressed through front matter**, with `layouts/` doing the joins.

### Sections

| Section | Purpose | URL |
| --- | --- | --- |
| `content/people/` | One file per **person** — the canonical profile store | `/people/<slug>/` |
| `content/team/` | Organizing committees; reference people by slug | `/team/<slug>/` |
| `content/session/` | Talk abstracts; reference speakers by slug | `/session/<slug>/` |
| `content/communities/` | Partner community profiles | `/communities/<slug>/` |
| `content/projects/` | Tech Pavilion expo projects | `/projects/<slug>/` |
| `content/schedule.html` | Hand-authored two-day grid | `/schedule/` |
| `content/_index.md` | Homepage — all copy lives in front matter | `/` |

### The person-reference pattern

`people/` is the single source of truth for a human. Teams and sessions never
duplicate a name or bio — they store a **list of slugs**, and templates resolve
them at build time with `Site.GetPage`:

```go-html-template
{{ range .Params.people }}
  {{ with $.Site.GetPage (printf "people/%s.md" .) }}
    ... render name, designation, socials, avatar ...
  {{ else }}
    Member profile reference missing (`people/{{ . }}.md`).
  {{ end }}
{{ end }}
```

Two consequences worth knowing:

- **The `else` branch is deliberate.** A broken slug renders a visible dashed
  placeholder rather than silently vanishing — the failure mode is designed to
  be noticed during review.
- **Avatars are not stored in the repo.** `people/single.html`,
  `team/single.html`, and `session/single.html` all derive the profile picture
  from `https://github.com/<socials.github>.png?size=N`. A person's GitHub
  handle *is* their avatar. No image assets to manage — but a wrong handle
  silently shows the wrong face (see §6).

`content/people/_index.md` sets `_build: {render: never, list: local}`, so
there is no public `/people/` directory listing; individual profiles are still
built and linked to from team and session pages.

### Front-matter contracts

```yaml
# people/<slug>.md
title: "Full Name"
designation: "Core Organizer"
weight: 1
socials: { github: "handle", linkedin: "https://..." }
# body = bio (also used as .Summary in cards)

# team/<slug>.md
title: "Team Name"
people: ["slug", "slug"]        # → resolved against people/
# body = the team's purpose statement

# session/<slug>.md
title: "Talk Title"
speakers: ["slug"]              # → resolved against people/
years: ["2026"]                 # → edition filtering + taxonomy
# body = abstract

# communities/<slug>.md
title: "Community Name"
logo: "https://..."             # external URL
years: ["2026"]
socials: { github: "org", linkedin: "https://...", twitter: "https://..." }

# projects/<slug>.md
title, date, draft, summary, hero_image, github_url, demo_url
booth_number: "TP-42"
business_domains: ["AgriTech"]  # → taxonomy + client-side filter
tech_domains: ["AI", "..."]     # → taxonomy + client-side filter
```

### Taxonomies and the "edition year" mechanism

`config.toml` declares five taxonomies: `years`, `tags`, `categories`,
`business_domains`, `tech_domains`.

`years` drives the multi-edition story. Session and community list pages don't
hardcode a year — they collect every value from every page, sort descending,
treat index 0 as the **current edition**, render only those pages in the main
grid, and emit "Archive" pill links to `/years/<year>/` for all older editions.
Adding a `years: ["2027"]` page is all it takes to roll the site to the next
edition.

`business_domains` / `tech_domains` power the Tech Pavilion filter. Both
`<select>` menus are populated from `Site.Taxonomies`, while the actual
filtering is **client-side**: each card carries `data-business` /
`data-tech` attributes of urlized terms, and an inline `filterProjects()`
toggles `display`. No page reloads, no JS dependencies — but also no
shareable filtered URLs, and the filter is a hard AND across the two menus.

### Homepage as data

`content/_index.md` contains no prose body at all — the hero heading,
highlighted word, subheading, CTA, event label/date/location, and the three
pillars are all front-matter fields, each with a template-level `default`
fallback in `layouts/index.html`. The highlight effect works by string
subtraction: `replace $heading $highlight ""` yields the plain part, then the
highlight is re-appended inside a `.text-gradient` span.

---

## 4. Layout inventory

```
layouts/
├── _default/
│   ├── baseof.html       # shell: full SEO/OG/Twitter meta, favicons, CDN links
│   ├── single.html       # bare fallback — just .Content in a container
│   ├── taxonomy.html     # /years/<year>/ term pages
│   └── year-archive.html # unused (see §6)
├── index.html            # homepage: hero + event card + 3 pillars
├── partials/
│   ├── header.html       # glass navbar from Site.Menus.main + "Submit a Talk"
│   └── footer.html       # fixed footer, © year, GitHub/LinkedIn
├── people/single.html
├── team/{list,single}.html
├── session/{list,single}.html
├── communities/{list,single}.html
└── projects/{list,single}.html
```

`baseof.html` is the most substantial piece of infrastructure: it computes a
title (site title on home, `Page | Site` elsewhere), cascades the description
through `.Description → .Summary → Site.Params.description → hardcoded
default` (plainified, truncated to 160), and picks an Open Graph image from
`hero_image → image → whatsapp-thumbnail.png`. Full Open Graph and Twitter
card tag sets are present — social sharing was clearly a priority.

---

## 5. Current content state

- **Event dates**: Fri Jan 8 – Sat Jan 9, 2027, at Infosys Mahindra City, Chennai.
- **14 people**, grouped into **6 teams**: Core Organizing Committee, Academia,
  Corporate Connect, AI Team, Hackathon Team, Technical Review Committee.
- **4 sessions** published (Spring AI agentic patterns, designing for the AI age,
  AI robustness/security & privacy by design, software development in the AI age)
  — all tagged `years: ["2026"]`. The programme is heavily AI-oriented.
- **4 communities**: Tamilnadu JUG, Cloud Native, Rust Rustaceans,
  Tech Cohere.
- **4 projects** in the Tech Pavilion (Raithu AgriTech platform, Azul JDK,
  SQLComponents, TNeBooks) — against a stated ambition of "100 curated projects".
- **Schedule** (`content/schedule.html`, ~390 lines of hand-written Bootstrap):
  two Bootstrap pill tabs — *Day 1: AI Day & Workshops*, *Day 2: Tech Talks*.
  Each day opens with three 20-minute keynotes in the Main Hall, then parallel
  tracks across four rooms — **Cambridge**, **Harvard**, **Nalantha**, and
  **Ganga** (the academia track). Runs 09:00–17:20. Slots are still
  placeholders ("Keynote 1", "Workshop 3B").

Overall the site is **structurally complete and content-incomplete**: the
templates and content model support far more than has been filled in.

---

## 6. Known gaps and issues

Ordered roughly by user impact.

1. **Broken social-share image.** `baseof.html` defaults `og:image` to
   `whatsapp-thumbnail.png`, and links `apple-touch-icon.png` — neither file
   exists in `static/`. Every page without a `hero_image` shares with a broken
   preview. *(Fix: add the two assets, or point at `devcarnival-logo.svg`.)*

2. **Wrong avatar on a profile.** `content/people/anandbabur.md` has
   `socials.github: "sathish"`, so Anand Babu's page and every team/session
   card render **Sathish's** GitHub photo and link to Sathish's GitHub.

3. **Dead CTAs.** The navbar's "Submit a Talk" points to `#cfp` and the hero's
   "Register Now" to `#register`; neither anchor exists anywhere on the site.
   The two primary conversion actions currently do nothing.

4. **Edition-year vs. event-date mismatch.** All content is tagged
   `years: ["2026"]` and project cards read "Expo 2026", but the advertised
   event is January **2027**. Whichever convention is intended, it should be
   consistent — the year taxonomy is what drives archive/current-edition logic.

5. **`/years/` term-list page won't render.** There is no
   `_default/terms.html` *or* `_default/list.html`, so Hugo has no template for
   the taxonomy index. Individual `/years/2026/` pages work (`taxonomy.html`);
   the parent listing does not.

6. **`_default/taxonomy.html` copy is community-specific.** It reads
   "Ecosystem Archive… active community footprints" and links "← Back to Active
   Communities", but the same template also serves archived **sessions**,
   `tags`, `categories`, `business_domains`, and `tech_domains` terms.

7. **`layouts/_default/year-archive.html` is dead code.** It expects
   `archive_section` / `archive_year` params; no content file sets either, and
   no `layout: year-archive` reference exists. The archive links in the session
   and community list pages go to `/years/<year>/` instead.

8. **Unguarded `index $sortedYears 0`.** `session/list.html` and
   `communities/list.html` take the first element of the collected year slice
   with no length check. If every page in a section ever lacks a `years` value,
   the build fails rather than degrading.

9. **Homepage pillars section has `id="team"`.** Misleading anchor — it's the
   three-pillar block, not the team roster.

10. **CI installs unused tooling.** The workflow installs Dart Sass and
    conditionally runs `npm ci`, but the repo has no `.scss` files and no
    `package.json`. Harmless, just noise (and a reason the pinned
    `hugo_extended` build is needed only nominally).

11. **`.gitignore` references `themes/my-resume`**, a leftover from an earlier
    themed setup. `.DS_Store` is committed and not ignored.

12. **Git hygiene.** Several commits are named `DDD`, `DDDD`, `Sch`, `IC`.
    History is hard to read.

---

## 7. How to extend it

| Task | Action |
| --- | --- |
| Add a person | Create `content/people/<slug>.md` with `title`, `designation`, `socials`. Avatar comes free from the GitHub handle. |
| Add them to a team | Append `<slug>` to that team file's `people:` list. |
| Add a session | Create `content/session/<slug>.md` with `speakers: [<slug>]` and `years: ["<edition>"]`. |
| Add a Pavilion project | Create `content/projects/<slug>.md` with `summary`, `booth_number`, and both domain arrays. New domain values appear in the filter dropdowns automatically. |
| Roll to a new edition | Publish sessions/communities with the new `years` value — list pages promote the highest year and archive the rest with no template changes. |
| Change homepage copy | Edit front matter in `content/_index.md`; no template edits needed. |
| Add a nav item | Add a `[[menu.main]]` block in `config.toml`. |
| Restyle | Edit the `:root` tokens in `static/css/style.css` — the gradient, type ramp, radii, and easing are all centralized. |
