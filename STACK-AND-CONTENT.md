# DevCarnival — Stack & Content Inventory

Purpose: rebuild the **UI / experience**. Keep the **stack**. Keep the **content**.
This doc = everything you need. No need to re-read the repo.

Companion docs: [PROJECT.md](PROJECT.md) (architecture), [LOGO-BRIEF.md](LOGO-BRIEF.md) (identity).

---

## PART 1 — STACK (do not change)

### 1.1 Hard facts

| Thing | Value |
| --- | --- |
| Generator | Hugo **extended**, `0.120.4` (pinned in CI) |
| Config | `config.toml`, single file, no env overrides |
| Theme | none. All templates hand-written in `layouts/` |
| CSS framework | Bootstrap **5.3.2**, jsDelivr CDN |
| Custom CSS | `static/css/style.css` — 187 lines, plain CSS, tokens in `:root` |
| Font | Plus Jakarta Sans (Google Fonts, weights 400/500/700) |
| JS | Bootstrap 5.3.2 bundle (CDN) + one inline `<script>` in `projects/list.html` |
| Build tooling | **none**. No `package.json`, no npm, no Sass, no bundler |
| Hosting | GitHub Pages, `.github/workflows/hugo.yml`, push to `main` |
| Site title | `DevCarnival` |
| baseURL | `https://example.com/` placeholder — real one injected by `actions/configure-pages` |

Dev command:

```sh
hugo server --cleanDestinationDir --disableFastRender
```

### 1.2 Rules the stack imposes

- No build step. New CSS = edit `static/css/style.css` or add a file in `static/`.
- Sass is *possible* (hugo extended + Dart Sass in CI) but **unused today**. Adding `.scss` means moving to `assets/` + `resources.Get`/`toCSS`.
- JS must be inline or a plain file in `static/`. No imports, no npm packages.
- All CSS/JS/font from CDN → offline dev is degraded. Keep that or self-host.
- Hugo 0.120.4 is old: **no** `.Store`, no `hugo.IsServer` in some forms, no newer `layouts/_partials` naming. Stick to `Site.GetPage`, `partial`, `where`, `apply`, `delimit`.

### 1.3 CDN + external runtime deps

```
https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css
https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js
https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700&display=swap
https://github.com/<handle>.png?size=N     ← every human avatar
```

### 1.4 Bootstrap components actually in use

`navbar` + `navbar-expand-lg` + `fixed-top` + `collapse` toggler · `nav-pills` +
`data-bs-toggle="pill"` tabs (schedule) · `card` · `badge` · `btn` · `form-select` ·
`sticky-top` · grid `row`/`col-*`/`g-*` · utilities everywhere.

Only two JS behaviours exist: **navbar collapse** and **schedule pill tabs**. Both from
the Bootstrap bundle. Plus `filterProjects()` / `resetFilters()` inline.

### 1.5 Layout files

```
layouts/
├── _default/
│   ├── baseof.html        shell: meta/SEO/OG/Twitter, favicons, CDN, header+footer partials
│   ├── single.html        bare fallback — .Content in a container
│   ├── taxonomy.html      /years/<year>/ term pages  (copy is community-flavoured — see 4.3)
│   └── year-archive.html  DEAD CODE, unreferenced
├── index.html             homepage: hero + event card + 3 pillars
├── partials/header.html   glass navbar, Site.Menus.main + "Submit a Talk"
├── partials/footer.html   fixed-bottom, © year, GitHub/LinkedIn
├── people/single.html
├── team/{list,single}.html
├── session/{list,single}.html
├── communities/{list,single}.html
└── projects/{list,single}.html
```

Missing on purpose/by accident: **no `_default/list.html`, no `_default/terms.html`**.
So `/years/` index does not render. Add if the new UI wants a taxonomy hub.

### 1.6 Design tokens today (`static/css/style.css`)

```css
--dc-bg: #fcfcfd;            --dc-surface: #ffffff;
--dc-text-primary: #0f172a;  --dc-text-secondary: #475569;  --dc-text-muted: #94a3b8;
--dc-border: #e2e8f0;        --dc-border-hover: #cbd5e1;
--dc-gradient-accent: linear-gradient(135deg,#4f46e5 0%,#7c3aed 50%,#db2777 100%);
--dc-gradient-subtle: linear-gradient(135deg,rgba(79,70,229,.05) 0%,rgba(219,39,119,.05) 100%);
--dc-font-sans: 'Plus Jakarta Sans', -apple-system, ... ;
--dc-radius-sm: 8px;  --dc-radius-md: 12px;  --dc-radius-lg: 20px;
--dc-shadow-sm / --dc-shadow-hover
--dc-transition-fast: all .2s cubic-bezier(.16,1,.3,1);
--dc-transition-smooth: all .35s cubic-bezier(.16,1,.3,1);
```

Custom classes — the **whole** list (12):

`.text-gradient` `.navbar` `.nav-link` `.nav-link.active` `.hero-section` `.hero-logo`
`.section-divider` `.btn-minimal` `.btn-outline-minimal` `.feature-card` `.feature-number`
`.meta-badge`

Notes for redesign:
- `body { padding-bottom: 80px }` exists only because footer is `fixed-bottom`. Drop the fixed footer → drop the padding.
- `.hero-section { padding: 10rem 0 6rem }` — the `10rem` top is clearing the `fixed-top` navbar. Used on **every** inner page, not just the hero.
- Templates reference classes that **do not exist in CSS**: `hover-underline`, `line-height-sm`, `line-height-md`, `tracking-wider`, `tracking-tight`, `fs-7`, `border-dashed`, `article-content`, `italic`. Currently no-ops. Either implement or strip.
- `.feature-number` is defined but never used. `--dc-gradient-subtle` and `--dc-radius-lg` also unused.
- Inconsistency to resolve: `rounded-0` sharp cards (session/team/communities/taxonomy) vs `--dc-radius-*` soft cards (projects/home).

### 1.7 CI (`.github/workflows/hugo.yml`)

Trigger: push to `main` + `workflow_dispatch`. Steps: install hugo_extended 0.120.4 deb →
install Dart Sass (snap, **unused**) → checkout (submodules recursive) → `configure-pages` →
conditional `npm ci` (**no lockfile, no-ops**) → `hugo --minify --baseURL <pages url>` →
upload `./public` → deploy.

---

## PART 2 — MEDIA INVENTORY

### 2.1 In-repo assets (`static/`)

| File | Used by |
| --- | --- |
| `devcarnival-logo.svg` | homepage hero (`width=250`), navbar (`max-height:28px`). 60KB Inkscape export, ~207×211mm viewBox, near-square. Palette `#f06e23 #1a959c #933489 #e83646` — clashes with site gradient. |
| `favicon.ico`, `favicon-16x16.png`, `favicon-32x32.png`, `favicon-96x96.png` | favicons (96 not linked) |
| `apple-icon*.png` (57/60/72/76/114/120/144/152/180, `apple-icon.png`, `-precomposed`) | **none linked** |
| `android-icon-*.png` (36/48/72/96/144/192) | listed in `manifest.json` |
| `ms-icon-*.png` (70/144/150/310), `browserconfig.xml` | **not linked** |
| `manifest.json` | **not linked** from `baseof.html`; `"name": "App"` placeholder |
| `css/style.css` | linked as `/css/style.css` (absolute — breaks under a subpath baseURL) |

### 2.2 Referenced but MISSING (live bugs)

| Path | Referenced at | Effect |
| --- | --- | --- |
| `whatsapp-thumbnail.png` | `baseof.html:11` (og:image + twitter:image default) | every page without `hero_image` shares a broken preview |
| `apple-touch-icon.png` | `baseof.html:45` | broken iOS icon (`apple-icon-180x180.png` exists — just repoint) |
| `static/images/projects/azul.jpg` | `projects/azul-jdk.md` | broken hero + broken og:image |
| `static/images/projects/sqlcomponents.jpg` | `projects/sqlcomponents.md` | same |
| `static/images/projects/tnebooks.jpg` | `projects/tnebooks.md` | same |
| `static/images/communities/cnc-logo.png` | `communities/cloud-native.md` | broken logo |
| `static/images/communities/madras-rust.png` | `communities/rust-rustaceans.md` | broken logo |

**`static/images/` does not exist at all.** Note: `hero_image` also feeds `og:image`, so
project pages currently share broken previews too. Note also that project `hero_image` is
**never rendered in any template** — only consumed as og:image. A redesign that shows
project cards with images needs to add that markup.

### 2.3 External media (hotlinked, no local copies)

| Source | Where |
| --- | --- |
| `https://github.com/<handle>.png?size=200` | `people/single.html` avatar (112×112 render) |
| `https://github.com/<handle>.png?size=80` | `team/single.html` avatar (56×56 render) |
| `https://tamilnadujug.org/assets/tamil_jug-dZMYtDXl.jpeg` | Tamilnadu JUG logo |
| `https://cdn5.telesco.pe/file/v0k_huJ...jpg` (Telegram CDN, long signed URL) | Tamil Linux logo — **fragile, likely to expire** |
| `https://javafest.org/images/infosys_logo.jpeg` | TechCohere logo |
| `https://avatars.githubusercontent.com/u/80134844?s=200&v=4` | OpenSearch Chennai logo |
| `https://lh3.googleusercontent.com/sitesv/AG8ngQW...=w16383` (Google Sites) | Raithu hero — **fragile** |

Avatar rule: **a person's GitHub handle IS their avatar.** No image assets per person.
No `github` field → no avatar rendered at all (only `michealJoshuva` today).

`session/single.html` and `communities/*` render **no** images except the community `logo`.

### 2.4 Iconography

No icon set. Zero SVG icons, no Bootstrap Icons, no Font Awesome. Visual accents are:
emoji in `schedule.html` (⏰ 🗓️ ☕ 🥗 🎉 🤝), emoji inside two bios (🖥️ 🔧 ⚙️ 🤖 🤝),
HTML entities `&larr;` `&rarr;`, literal `→` `←` `↗`, and text badges.
**If the new UI wants icons, you are adding a dependency that doesn't exist yet.**

---

## PART 3 — TEXT CONTENT

Two kinds. **(A) Chrome** = hardcoded in templates, you will rewrite it.
**(B) Content** = markdown/front matter, you should preserve it.

### 3.A CHROME — every hardcoded string, by template

**`baseof.html`**
- Title rule: home → `DevCarnival`; else → `<Page Title> | DevCarnival`
- Description cascade: `.Description → .Summary → Site.Params.description → hardcoded default`, `plainify | truncate 160`
- Hardcoded default description (also `config.toml [params].description`):
  *"Inspired by the spirit of a true carnival, DevCarnival is a two-day global tech festival in Chennai uniting industry, developers, and academia for purpose-oriented engineering."*
- OG: `og:type` article|website, `og:url`, `og:title`, `og:description`, `og:image` (+ `1200×630` declared), `twitter:card=summary_large_image` + url/title/description/image.

**`partials/header.html`**
- brand: logo img + `DevCarnival`
- nav from `config.toml` menu: `Sessions` `/session` · `Schedule` `/schedule` · `Tech Pavilion` `/projects` · `Community` `/communities` · `Team` `/team`
- CTA: **`Submit a Talk`** → `#cfp` ← **dead anchor, exists nowhere**

**`partials/footer.html`**
- `© <current year> DevCarnival. Worldwide.`
- links: `GitHub` → `https://github.com/devcarnival` · `LinkedIn` → `https://www.linkedin.com/company/dev-carnival`
- `config.toml` also holds unused `email = "contact@devcarnival.com"`

**`index.html`** (all values from `content/_index.md`, defaults in template)
- eyebrow: `DevCarnival` (site title, `display-6`)
- h1: `Technology. People. Purpose.` with `Purpose.` in `.text-gradient`
  — mechanism: `replace $heading $highlight ""` then re-append highlight in a span
- lead: *"Inspired by the spirit of a true carnival, DevCarnival is a two-day global festival uniting tech communities, industry, and academia. A celebration of fulfillment and purpose-oriented engineering."*
- CTA: **`Register Now`** → `#register` ← **dead anchor, exists nowhere**
- event card: `Global Gathering` / `Fri, Jan 8, 2027 & Sat, Jan 9, 2027` / `Infosys, Mahindra City, Chennai`
- pillars block has `id="team"` (misleading), items numbered `01 / …` via `printf "%02d"`

**`session/list.html`** — h1 `Technical Sessions` · lead *"Deep dives, keynotes, and masterclasses from industry practitioners."* · h2 `<year> Schedule & Tracks` · badge `Live Track` · card CTA `View Abstract` · footer `Session Archives:` + `<year> Catalog`

**`session/single.html`** — back `← Back to all sessions` · badge `<year> Edition` · sidebar `Presenting Speakers` · links `LinkedIn` / `GitHub` · missing-ref fallback ``Speaker profile metadata file missing (`people/<slug>.md`)``

**`team/list.html`** — h1 `Festival Operations Teams` · lead *"The crews engineering the DevCarnival ecosystem framework."* · CTA `View Purpose & Members` · badge `<n> Members` · empty state *"No operational teams have been registered yet."*

**`team/single.html`** — back `← Back to all teams` · sidebar `Team Roster` · missing-ref fallback ``Member profile reference missing (`people/<slug>.md`)``

**`communities/list.html`** — h1 `Ecosystem Communities` · lead *"The developer groups, open-source cohorts, and engineering circles driving DevCarnival."* · h2 `<year> Cohort Partners` · badge `Active` (green) · CTA `Explore Portal` · badge `<n> Leads` (never fires — no community has `people`) · footer `Communities Archive:` + `<year> Catalog`

**`communities/single.html`** — back `← Back to all communities` · badge `<year> Cohort` · sidebar `Connect & Engage` + *"Follow this community's updates, collaborative repositories, and active social channels."* · buttons `Twitter / X` `GitHub Ecosystem` `LinkedIn Page` · empty *"No social ecosystem links registered for this year."*

**`projects/list.html`** — badge `Innovation Expo` · h1 `Tech Pavilion` (`Pavilion` gradient; note double space in source) · lead *"Tech Pavilion is a showcase of 100 carefully selected projects from communities, startups, academia, enterprises, and open-source ecosystems."* · filter labels `Business Domain` / `Technical Domain`, options `All Business Domains` / `All Technical Domains`, button `Reset` · card: booth badge (default `Tech Pavilion`), `Expo 2026` **hardcoded**, CTA `View Project →`

**`projects/single.html`** — back `← Back to Pavilion Projects` · badge `Booth <n>` · labels `Business Domain:` `Tech Domain:` · CTAs `Live Demo / Site ↗` `GitHub Repo ↗`

**`people/single.html`** — back `← Return Home` · section `Professional Profiles` · buttons `LinkedIn Profile` `GitHub Workspace` · empty *"No public code or career metrics registered."*

**`_default/taxonomy.html`** — h1 `<term> Ecosystem Archive` · lead *"Reviewing active community footprints and contributions from the <term> festival track."* · CTA `View Details` · empty *"No community modules found registered under this cohort year."* · back `← Back to Active Communities`
⚠️ This one template also serves archived **sessions**, `tags`, `categories`, `business_domains`, `tech_domains` — copy is wrong for all of them.

### 3.B CONTENT — the data you must carry over

Bodies (bios, abstracts, purpose statements, project write-ups) live in the markdown files
and are long; they are **not** duplicated here. Below is the shape + all identifiers.

#### Homepage (`content/_index.md`) — front matter only, no body
`title`, `hero.{heading,highlight,subheading,cta_text,cta_link}`,
`event.{label,date,location}`, `pillars[].{title,description}`

Pillars: **Cross-Technology** · **Unified Experience** · **Industry & Academia**
(one paragraph each — verbatim in the file).

#### People — 15 files, `content/people/<slug>.md`

Contract: `title`, `designation`, `weight`, `socials.{github,linkedin}`, body = bio (also `.Summary`).

| slug | title | designation | github | bio |
| --- | --- | --- | --- | --- |
| `anandbabur` | Anand Babu | Core Organizer | `sathish` ⚠️ **wrong — Sathish's handle** | long |
| `hari-nikesh` | Hari Nikesh | Core Organizer | `hari-nikesh-r` | med |
| `ksivaprasadreddy` | K Siva Prasad Reddy | AI Team Organizer | `sivaprasadreddy` | long |
| `manickalai` | Manickalai Rajan | Core Organizer | `samkamer` ⚠️ same as `samir` | very long |
| `michealJoshuva` | Micheal Joshuva | Speaker | *(none)* ⚠️ no avatar | long |
| `mutheeshwaran` | Mutheeshwaran S | Core Organizer | `hari-nikesh-r` ⚠️ duplicate | long |
| `ravindran` | Ravindran P | Core Organizer | `hari-nikesh-r` ⚠️ duplicate | short |
| `rohan` | Rohan J | Core Organizer | `http://github.com/apt-get2update` ⚠️ full URL, not handle | med |
| `samir` | Samir Kamerkar | Core Organizer | `samkamer` | very long |
| `saro` | Saravana Kumar Vithyananthan | Tech Review Member | `hari-nikesh-r` ⚠️ duplicate | short (same text as `ravindran`) |
| `sathish` | Sathish Kumar Thiyagarajan | Core Organizer | `sathishk` | med |
| `sree-sharmila` | Sree Sharmila T | Core Organizer | `sharmila-shree` | long |
| `thamaraikanni` | Thamaraikanni P | AI Team Organizer | `https://github.com/ThamaraiP` ⚠️ full URL | long |
| `thiru` | Thiru Murugan | Core Organizer | `http://github.com/apt-get2update` ⚠️ full URL + dup | short |
| `udayani` | Udayani V | AI Team Organizer | `https://github.com/vudayani` ⚠️ full URL | long |

⚠️ The 5 "full URL" handles produce `https://github.com/https://github.com/x.png` →
broken avatars and broken links **right now**. `michealJoshuva` also has key typo
`inkedin:` (never read) pointing at **Thamaraikanni's** LinkedIn.

`content/people/_index.md` sets `_build: {render: never, list: local}` → **no public
`/people/` index**; profiles exist at `/people/<slug>/`, reachable only from team pages.

#### Teams — 6 files, `content/team/<slug>.md`

Contract: `title`, `people: [slug…]`, body = purpose statement.
`content/team/_index.md` title = `Festival Operations Teams`.

| file | title | members |
| --- | --- | --- |
| `core-organizers` | Core Organizing Committee | anandbabur, ravindran, mutheeshwaran |
| `academia` | Academia | samir, sree-sharmila *(`sathish` commented out)* |
| `corporate` | Corporate Connect | manickalai |
| `ai` | AI Team | thamaraikanni, udayani, ksivaprasadreddy |
| `hackathon` | Hackathon Team | thiru, rohan |
| `technical-committee` | Technical Review Committee | hari-nikesh, saro |

#### Sessions — 5 files, `content/session/<slug>.md`

Contract: `title`, `speakers: [slug…]`, `years: ["2026"]`, body = abstract.
`_index.md` title = `Festival Sessions`. Permalink `/session/:slug/`.

| slug | title | speaker |
| --- | --- | --- |
| `agentic-patterns-with-spring-ai` | Agentic Patterns with Spring AI | ksivaprasadreddy |
| `designing-for-the-age-of-ai` | Designing for the Age of AI | ksivaprasadreddy ⚠️ likely placeholder |
| `software-development-in-the-age-of-ai` | Software Development In The Age of AI | ksivaprasadreddy ⚠️ likely placeholder |
| `enhancing-ai-robustness-through-security-and-privacy-by-design` | Enhancing AI Robustness through Security and Privacy by Design | ksivaprasadreddy ⚠️ likely placeholder |
| `live-data-poisoning-and-backdoor-attacks` | When AI Learns the Wrong Lessons: Live Data Poisoning and Backdoor Attacks with ART | michealJoshuva |

All `years: ["2026"]`. All AI-themed.

#### Communities — 6 files, `content/communities/<slug>.md`

Contract: `title`, `logo`, `years[]`, `socials.{github,linkedin,twitter}`, body = blurb.
`_index.md` title = `Our Communities`. Permalink `/communities/:slug/`.

| slug | title | years | logo |
| --- | --- | --- | --- |
| `tamil-jug` | Tamilnadu Java User Group | 2026 | external (tamilnadujug.org) |
| `tamil-linux` | Tamil Linux Community | 2026 | external (telesco.pe, fragile) |
| `tech-cohere` | TechCohere | 2025, 2026 | external (javafest.org) |
| `tech-meetup` | OpenSearch Project Chennai | 2026, 2025 | external (githubusercontent) |
| `cloud-native` | Cloud Native Chennai | 2025 | `images/communities/cnc-logo.png` **missing** |
| `rust-rustaceans` | Madras Rustaceans | 2025 | `images/communities/madras-rust.png` **missing** |

⚠️ `tech-meetup.md` is titled *OpenSearch Project Chennai* — file name is stale.
`tamil-linux` `socials.linkedin` is actually a Telegram link (`t.me/tamillinux`) and renders as "LinkedIn Page".

#### Projects — 4 files, `content/projects/<slug>.md`

Contract: `title`, `date`, `draft`, `summary`, `hero_image`, `github_url`, `demo_url`,
`booth_number`, `business_domains[]`, `tech_domains[]`, body = markdown (`## Overview`,
`### Key Features`, `### Impact`…).
`_index.md`: title `Tech Pavilion`, description *"Explore 100+ curated projects, open-source initiatives, startups, and enterprise tech at the DevCarnival Innovation Expo."*

| slug | title | booth | business_domains | tech_domains |
| --- | --- | --- | --- | --- |
| `raithu` | Raithu Platform | TP-42 | AgriTech | AI, Remote Sensing, Data Analytics |
| `sqlcomponents` | SQL Components | TP-42 ⚠️ **dup** | Developer Tools, Enterprise Software | Java, SQL, Code Generation, Database, Open Source |
| `azul-jdk` | Azul Zulu Enterprise JDK | TP-55 | Enterprise Infrastructure, Banking, E-Commerce | Java, Developer Tools, Cloud |
| `tnebooks` | TNEBooks (Tamil Nadu School Education Portal) | TP-08 | Education, Government | Cloud, Web Systems |

Distinct taxonomy terms available for filter UI:
**business_domains** — AgriTech, Banking, Developer Tools, E-Commerce, Education, Enterprise Infrastructure, Enterprise Software, Government
**tech_domains** — AI, Cloud, Code Generation, Data Analytics, Database, Developer Tools, Java, Open Source, Remote Sensing, SQL, Web Systems

#### Schedule — `content/schedule.html`, 393 lines of hand-written Bootstrap

Front matter: `title: "Schedule"`, `date: 2026-08-03`, `draft: false`.
Rendered through `_default/single.html` (raw HTML body, **no Hugo data model**).
A UI redesign either rewrites this HTML by hand or promotes it to front-matter data +
a real template. Content today:

Header: h1 `Schedule` · lead `Keynotes, Hands-on Workshops & Tech Talks` · badge `⏰ 9:00 AM – 5:20 PM`
Tabs: `🗓️ Day 1: AI Day & Workshops` · `🗓️ Day 2: Tech Talks`
Rooms: **Nalantha**, **Harvard**, **Cambridge**, **Ganga** (Ganga = Academia Track on Day 1) + **Main Hall** for keynotes.

**Day 1** — Main Hall `Morning Keynotes`: Keynote 1 (09:00–09:20), Keynote 2 (09:20–09:40), Keynote 3 (09:40–10:00).
`Parallel Workshops & Academia Track` table (col 1 = `Time Slot`):

| Slot | Nalantha | Harvard | Cambridge | Ganga (Academia) |
| --- | --- | --- | --- | --- |
| 10:00–10:45 | Workshop 1A · Cloud & DevOps (10:00–11:30) | Workshop 1B · Full Stack Development (10:00–11:30) | Workshop 1C · AI & Machine Learning (10:00–11:30) | Talk 1D · Academic Research & Innovation |
| 10:45–11:30 | ↑ | ↑ | ↑ | Talk 2D · Industry Collaboration in Academia |
| ☕ 11:30–11:40 | Morning Tea Break (10 Mins) | | | |
| 11:40–12:25 | Workshop 2A · Docker & Kubernetes (11:40–13:10) | Workshop 2B · System Design (11:40–13:10) | Workshop 2C · Data Engineering (11:40–13:10) | Talk 3D · Future of Engineering Education |
| 12:25–13:10 | ↑ | ↑ | ↑ | Talk 4D · Student Innovation Showcase |
| 🥗 13:10–13:55 | Lunch Break (45 Mins) | | | |
| 13:55–14:40 | Workshop 3A · Cloud Native Development (13:55–15:25) | Workshop 3B · Modern Java (13:55–15:25) | Workshop 3C · AI Applications (13:55–15:25) | Talk 5D · Research to Product Journey |
| 14:40–15:25 | ↑ | ↑ | ↑ | Talk 6D · Academia & Open Source |
| ☕ 15:25–15:35 | Evening Tea Break (10 Mins) | | | |
| 15:35–16:20 | Workshop 4A · DevOps at Scale (15:35–17:05) | Workshop 4B · Architecture Patterns (15:35–17:05) | Workshop 4C · Advanced AI Engineering (15:35–17:05) | Talk 7D · Emerging Technologies |
| 16:20–17:05 | ↑ | ↑ | ↑ | Talk 8D · Academic Leadership Panel |
| 17:05–17:20 | 🎉 Valedictory & Day 1 Wrap-up | | | |

**Day 2** — same keynote block, then `Parallel Tech Talks`, 4 rooms × 8 slots, all
placeholders `Talk 1A … Talk 8D` (only slots 1–7 titled + a closing session):
10:00–10:45 (1x) · ☕ 10:45–10:55 · 10:55–11:40 (2x) · 11:40–12:25 (3x) · 🥗 12:25–13:10 ·
13:10–13:55 (4x) · 13:55–14:40 (5x) · 14:40–15:25 (6x) · ☕ 15:25–15:35 · 15:35–16:20 (7x) ·
16:20–17:20 `🤝 Networking Session & Community Connect (60 Mins)`.

⚠️ Header badge says 5:20 PM; Day 1 ends 17:20 — consistent. Everything else is placeholder.

---

## PART 4 — CONTRACTS THE NEW UI MUST HONOUR

### 4.1 The person-reference join

`content/people/` is the **single source of truth for a human**. Teams and sessions store
*slugs only*, resolved at build time:

```go-html-template
{{ range .Params.people }}
  {{ with $.Site.GetPage (printf "people/%s.md" .) }}
    ... name, designation, socials, avatar ...
  {{ else }}
    Member profile reference missing (`people/{{ . }}.md`).
  {{ end }}
{{ end }}
```

The `else` branch is **deliberate** — a bad slug renders a visible dashed placeholder
instead of vanishing. Keep that behaviour in any redesign.

### 4.2 The `years` edition mechanism

`config.toml` taxonomies: `year=years`, `tag=tags`, `category=categories`,
`business_domain=business_domains`, `tech_domain=tech_domains`.

`session/list.html` and `communities/list.html` both: collect every `years` value in the
section → `uniq` → `sort "value" "desc"` → **index 0 = current edition** → render only
those → emit archive pills to `/years/<year>/` for the rest.

Publishing a `years: ["2027"]` page rolls the site forward with zero template edits.
⚠️ `index $sortedYears 0` is **unguarded** — a section where no page has `years` fails the build.

### 4.3 URL surface (keep these or set up redirects)

```
/                       home
/session/               session list        /session/<slug>/
/schedule/              hand-authored HTML
/projects/              Tech Pavilion       /projects/<slug>/
/communities/           community list      /communities/<slug>/
/team/                  team list           /team/<slug>/
/people/<slug>/         profile (no /people/ index by design)
/years/<year>/          taxonomy term page (parent /years/ DOES NOT RENDER)
/business_domains/<t>/  linked from projects/single.html
/tech_domains/<t>/      linked from projects/single.html
/tags/, /categories/    declared, unused
```

### 4.4 Front-matter keys the templates read

Change these and content breaks. Full list:

```
_index.md   hero.heading hero.highlight hero.subheading hero.cta_text hero.cta_link
            event.label event.date event.location pillars[].title pillars[].description
people      title designation weight socials.github socials.linkedin
team        title people[]
session     title speakers[] years[]
communities title logo years[] socials.github socials.linkedin socials.twitter
projects    title date draft summary hero_image github_url demo_url booth_number
            business_domains[] tech_domains[]
any page    description image hero_image   (→ SEO/OG in baseof.html)
```

### 4.5 Client-side project filter

Cards carry `data-business` / `data-tech` = space-joined `urlize`d terms.
`<select>` options are populated from `Site.Taxonomies.*` (`urlize` value, `humanize` label).
`filterProjects()` toggles `style.display`. Behaviour: **hard AND** across both menus,
no URL state, no shareable filtered links, no result count, no empty state.
All four of those are open improvements for a redesign.

---

## PART 5 — BUGS TO FIX OR CARRY (ranked)

1. **5 people have full GitHub URLs instead of handles** (`rohan`, `thiru`, `thamaraikanni`, `udayani`, plus `michealJoshuva` has none) → broken avatars + broken links today.
2. **`anandbabur` has `github: "sathish"`** → renders Sathish's face and links Sathish's profile.
3. **`michealJoshuva`: `inkedin:` typo + the URL is Thamaraikanni's LinkedIn** → no socials shown, and wrong-person data in the repo.
4. **3 duplicate GitHub handles** — `hari-nikesh-r` on 4 people, `samkamer` on 2 → wrong faces.
5. **7 missing image files** (§2.2), incl. every project hero and 2 community logos.
6. **Dead CTAs** — `Submit a Talk` → `#cfp`, `Register Now` → `#register`. Both anchors nonexistent. The two primary conversions do nothing.
7. **4 of 5 sessions credit the same speaker** — looks like copy-paste; confirm with organizers.
8. **Edition/date mismatch** — sessions all `years: ["2026"]` + hardcoded `Expo 2026`, but the event is **Jan 2027**. Communities span 2025/2026, so the archive path *is* live.
9. **`/years/` won't render** — no `_default/terms.html` / `list.html`.
10. **`taxonomy.html` copy is community-only** but serves sessions/tags/categories/domains too.
11. **Duplicate booth `TP-42`** (raithu + sqlcomponents).
12. **`index $sortedYears 0` unguarded** (build-breaker).
13. **`id="team"` on the pillars section** — misleading anchor.
14. **`/css/style.css` absolute path** — breaks under a subpath baseURL; use `relURL`.
15. **Dead code / noise** — `_default/year-archive.html`, `.feature-number`, `--dc-gradient-subtle`, `--dc-radius-lg`, unlinked `manifest.json` + `browserconfig.xml` + all `ms-icon`/`apple-icon` files, CI Dart Sass + `npm ci`, `.gitignore` has both `themes/` and `themes/my-resume`, `.DS_Store` committed.

---

## PART 6 — REDESIGN CHECKLIST

Stack stays. So a UI rebuild = these files, nothing else:

- [ ] `static/css/style.css` — retoken. Everything visual funnels through `:root`.
- [ ] `layouts/_default/baseof.html` — shell, meta, asset links
- [ ] `layouts/partials/{header,footer}.html` — nav + footer pattern (drop `fixed-bottom` → drop `body{padding-bottom:80px}`)
- [ ] `layouts/index.html` — hero + event card + pillars
- [ ] 9 section templates — reuse the same `Site.GetPage` joins (§4.1) and `years` logic (§4.2)
- [ ] `content/schedule.html` — the only content file holding markup; rewrite with the new card/table language
- [ ] Add `_default/list.html` + `_default/terms.html` if you want the taxonomy hub
- [ ] Decide: keep CDN Bootstrap, or self-host / swap. Remember — **no build step exists.**
- [ ] Decide on `rounded-0` vs `--dc-radius-*` (currently split by section)
- [ ] Implement or delete the 9 phantom classes in §1.6
- [ ] Ship a dark mode? Nothing today assumes one; `--dc-*` tokens make it cheap.
- [ ] Add the missing media (§2.2) — `whatsapp-thumbnail.png` 1200×630 is the highest-impact single file.
