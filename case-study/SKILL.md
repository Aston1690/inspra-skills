---
name: case-study
description: >
  Generate a professional, branded case study webpage from any company website URL.
  Use this skill whenever the user asks to create, build, design, or generate a case study,
  client story, success story, or customer showcase. Also trigger when the user mentions
  "case study" alongside words like "create", "build", "make", "design", or "generate".
  This skill handles the full workflow: brand extraction from the target website, content
  research, professional HTML generation with responsive design, and PDF export via Puppeteer.
  Do NOT trigger for: blog posts, landing pages, newsletters, pitch decks, or non-case-study content.
---

# Case Study Generator Skill (v3)

You are a Senior Content Designer creating **premium, agency-quality case studies** using brand-matched HTML templates and Puppeteer PDF export. The output must match the quality of a top-tier design agency — alternating dark/light sections, circular data visualizations, colour-coded breakdowns, dual branding, and polished typography.

**IMPORTANT:** The case study is ALWAYS branded as an **Automate Accelerator** deliverable showcasing the client's engagement. The design system, accent colour, and overall identity come from Automate Accelerator (`#ff6900` orange accent), NOT from the client's brand. Client branding (logo, name) appears as the "featured client" alongside the Automate Accelerator identity.

## Skills Used in This Workflow

This skill orchestrates multiple Claude Code skills. **You MUST invoke these skills at the specified steps — do not skip them.**

| Skill | Step | Purpose |
|-------|------|---------|
| **`brand-guide-extractor`** | Step 0 | Extract client's logo URLs, colours, fonts, and brand assets from their website. This is the PRIMARY method for logo discovery and brand research. |
| **`taste-frontend`** | Step 3 (before coding) | Audit the generated HTML against premium design standards. Ensures the output doesn't look like a generic template. |
| **`soft-visual-design`** | Step 3 (alternative to taste-frontend) | Establish visual design system rules if taste-frontend is unavailable. |
| **`copywriting`** | Step 2 | Write case study content (challenge narratives, solution descriptions, CTA copy) with strategic, non-fluffy language. |
| **`playwright-cli`** | Step 4 | Automate browser screenshots for visual verification. |
| **`polish`** | Step 4 (after first draft) | Final quality pass on spacing, alignment, consistency, and micro-details. |

### How to Invoke Skills

When you reach a step that requires a skill, invoke it using the Skill tool:
```
Skill("brand-guide-extractor", "https://www.clientwebsite.com")
Skill("taste-frontend", "Audit this case study HTML for premium quality...")
Skill("copywriting", "Write the challenge section for [client]...")
Skill("polish", "Final pass on the case study HTML...")
```

## Prerequisites

This skill requires:
1. **Node.js** (v18+) installed
2. **Puppeteer** — install dependencies by running:
   ```bash
   SKILL_DIR=$(dirname "$(find ~/.claude -path "*/case-study/SKILL.md" 2>/dev/null | head -1)")
   cd "$SKILL_DIR/scripts" && npm install
   ```

### Auto-Setup (run at start of every session)

**ALWAYS run this block before any design work.**

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/case-study/SKILL.md" 2>/dev/null | head -1)")

if [ ! -d "$SKILL_DIR/scripts/node_modules" ]; then
  echo "Installing Puppeteer dependencies..."
  cd "$SKILL_DIR/scripts" && npm install
fi

echo "Case Study skill ready."
```

---

## INPUTS REQUIRED

| Input | Source | Required? |
|-------|--------|-----------|
| Website URL | User-provided | Required |
| Company/Product Name | Extracted from URL or user-provided | Required |
| Content Document | Google Doc, PDF, markdown, or pasted text | Optional (enhances depth) |
| Hero Image | User-provided or sourced from website | Optional |
| Target Audience | User-provided | Optional |
| Specific Metrics | User-provided or researched | Optional |

---

## STEP 0 — LOGO & BRAND ASSET COLLECTION (MANDATORY FIRST STEP)

**This is the #1 source of bugs. Follow this process exactly.**

### 0a. Run `brand-guide-extractor` on the Client Website

**ALWAYS run this skill FIRST.** It extracts logos, colours, fonts, and brand assets properly.

```
Skill("brand-guide-extractor", "https://www.clientwebsite.com")
```

This gives you:
- Client logo URL(s) — light and dark variants if available
- Primary/secondary brand colours (for reference, NOT for the design system)
- Font names
- Screenshots of the client's site
- Tagline and key messaging

### 0b. Agency Logo (Automate Accelerator)

**IMPORTANT: Use the PNG version (`AA-logo-white.png`), NOT the SVG. The SVG from the website has broken `display:none` layers and does not render correctly.**

The agency logo MUST be sourced in this priority order:

1. **Check local brand-assets first (PNG preferred):**
   ```bash
   # Look for existing AA logos — prefer PNG over SVG
   find "$(pwd)" -maxdepth 5 -iname "AA-logo-white.png" 2>/dev/null | head -5
   find "$(pwd)/brand-assets/logos" -iname "AA-logo*" 2>/dev/null | head -5
   ```
   The correct file is `brand-assets/logos/AA-logo-white.png` (666x174, white text + orange accents on transparent bg).
   Also available: `AA-logo-dark.png` (dark text version for light backgrounds).

2. **If found locally**, copy it to the output directory as `agency-logo.png`.
3. **If NOT found locally**, check the Diagram-Skill package:
   ```bash
   find "$(pwd)/../" -maxdepth 5 -iname "AA-logo-white.png" 2>/dev/null | head -5
   ```
4. **NEVER use `AA-logo-white.svg`** — it has rendering bugs (display:none layers, broken at small sizes).

### 0c. Client Logo

1. **Check local brand-assets first:**
   ```bash
   find "$(pwd)/brand-assets" -iname "*[CLIENT_NAME]*" 2>/dev/null | head -10
   ```
2. **If found locally**, copy it to the output directory.
3. **If NOT found locally**, use the logo URL from `brand-guide-extractor` output:
   ```bash
   curl -sL "[CLIENT_LOGO_URL_FROM_BRAND_EXTRACTOR]" -o "$OUTPUT_DIR/client-logo.png"
   ```
4. **If brand-guide-extractor didn't find a logo**, use `WebFetch` as fallback:
   ```bash
   # WebFetch the client site and search for logo img tags
   curl -sL "[LOGO_URL]" -o "$OUTPUT_DIR/client-logo.png"
   ```

### 0c. CRITICAL: Logo Visibility Verification

**Every logo MUST be tested on both dark and light backgrounds.**

After downloading/copying logos, verify them:

1. **Check file type and validity:**
   ```bash
   file "$OUTPUT_DIR/agency-logo.svg"
   file "$OUTPUT_DIR/client-logo.png"
   ```

2. **For SVG logos** — open the file and check for these issues:
   - `display:none` on the main group (broken SVG export)
   - White fills (`#FFFFFF`, `.st6{fill:#FFFFFF}`) that disappear on white backgrounds
   - Dark fills (`#000000`) that disappear on dark backgrounds
   - Multi-layer SVGs where the visible layer isn't the first one

3. **For PNG logos** — check if the logo has:
   - Dark text on transparent background (invisible on dark sections)
   - White text on transparent background (invisible on light sections)

4. **Fix visibility issues using CSS filters:**
   - Logo on dark background with dark text: add `filter: brightness(0) invert(1)` in the `<img>` style
   - Logo on light background with white text: add `filter: brightness(0)` in the `<img>` style
   - NEVER rely on a single logo version working everywhere — always test

5. **In the hero section** — the logo pills should use:
   - Orange pill for "Automate" (text only, no logo image needed)
   - Outline pill for client with `<img>` tag + appropriate filter
   - If the client logo is unreadable even with filters, use plain text instead

### Logo Usage Across Sections

| Section | Background | Agency Logo | Client Logo |
|---------|-----------|-------------|-------------|
| Hero pills | Dark | `AA-logo-white.png` inside orange pill (`height:28px`) | Client logo in outline pill (inverted if needed) |
| CTA | Orange gradient | White text "Automate Accelerator" | White text "[Client Name]" |
| Footer | Dark | Text only | Text only |

**RULE: If a logo doesn't render cleanly, use text. Never ship a case study with invisible or broken logos.**

---

## STEP 0.5 — ASK THE USER BEFORE PROCEEDING

**MANDATORY: Before doing any research or generation, ask the user these questions:**

1. **"Do you have an existing brand guide or brand-assets folder for this client?"**
   - If yes, ask for the path and use those assets instead of extracting from the website
   - Check `brand-assets/[client-name]/` in the project directory first

2. **"Do you have a content document (Google Doc, PDF, or text) with the case study content?"**
   - If yes, ask for the path/link and use that as the primary content source
   - This replaces most of Step 2 (content research) and ensures accuracy
   - NEVER invent content when a source document exists

3. **"Is there a hero image you'd like to use, or should I source one?"**
   - If they have one, use it
   - If not, source from the client's website or use a relevant stock image

**Only proceed to Step 1 after getting answers to these questions.**

---

## STEP 1 — CLIENT BRAND RESEARCH

### If brand-guide-extractor was run in Step 0:
Use the extracted data (logo URLs, colours, fonts, industry info) as your starting point. Supplement with `WebFetch` if needed.

### If the user provided a brand guide:
Read it and extract the relevant information. Skip WebFetch for brand data.

### Otherwise:
Use `WebFetch` on the client website to understand their business. Extract:

- **Industry / vertical**
- **Core product/service description**
- **Key metrics** — any numbers, percentages, or stats on their site
- **Client testimonials or quotes**
- **Years in business, team size, location**
- **Target audience**

**NOTE:** The case study design uses the Automate Accelerator brand system (orange `#ff6900` accent, Outfit + Inter fonts, dark/light alternating sections). Client brand colours are NOT used in the design — only the client's content, logo, and name.

### Brand Extraction Output

```
CLIENT PROFILE — [Company Name]
────────────────────────────────
Industry:       ______
Years:          ______
Size:           ______
Location:       ______
Services:       ______
Key Metrics:    ______
AGENCY LOGO:    [path] (verified on dark bg)
CLIENT LOGO:    [path] (verified on dark bg)
```

---

## STEP 2 — CONTENT RESEARCH & COPYWRITING

### If the user provided a content document:
Read the document thoroughly. Use it as the SOLE source of truth for all content. Do NOT invent metrics, quotes, or claims that aren't in the document.

### If no content document was provided:
Research the company:
1. **WebFetch the main website** — extract product descriptions, features, value props
2. **WebSearch for the company** — find press mentions, metrics, customer stories
3. **WebFetch any linked case studies or testimonials** on their site
4. **Identify quantified results** — revenue growth, time saved, conversion rates, appointments booked

### Use `copywriting` skill for content writing

After gathering raw content, run the `copywriting` skill to write the case study sections:

```
Skill("copywriting", "Write case study content for [CLIENT_NAME]. Tone: strategic, consultative, no fluff. Sections needed: challenge narrative, solution descriptions, results summary. Source material: [paste key content]")
```

This ensures the copy is professional and consistent across all case studies your team generates.

Build a content brief mapping to the **7 template sections**:

### Section Content Map

| Section | Content Needed |
|---------|---------------|
| **1. Hero (Dark)** | Headline (accent keyword on its own line), subtitle, hero image, 3 stats in dark cards |
| **2. Business Overview (Light)** | Page label "PAGE 02", 3 info cards (years, size, location) with orange icon squares, "Who They Are" paragraphs, dark Challenge card with titled bullet points |
| **3. The Solution (Dark)** | Page label, headline, 4 step cards with coloured icons (orange/green/teal/purple), descriptions, pill sub-items, step numbers right-aligned |
| **4. Performance Metrics (Light)** | Page label, 3 top metrics with circular progress rings, 4 breakdown cards with colour-coded left borders + percentage ring badges, dark Follow-Up callout card |
| **5. Key Results (Dark)** | Page label, 4 stat cards with coloured icon squares, gradient metric banner, 2 detail cards |
| **6. What Made This Work (Light)** | Page label, 3 pillar cards with orange icon squares, framework checklist with green check dots, dark impact summary card with 4 stats |
| **7. CTA (Orange gradient)** | Headline, subtitle, frosted glass outline button, text-based dual branding, tagline |

---

## STEP 3 — GENERATE THE CASE STUDY HTML

### Before writing code: Run `taste-frontend` for design audit

After generating the first draft HTML, ALWAYS run the `taste-frontend` skill to audit it:

```
Skill("taste-frontend", "Audit this case study page for premium agency quality. Check: typography hierarchy, card depth/shadows, hover interactions, colour consistency, spacing rhythm, icon quality. The brand uses #ff6900 orange accent on alternating dark/light sections.")
```

Apply any recommendations from `taste-frontend` before proceeding to Step 4.

### Generate the HTML

Create a single, self-contained HTML file using the reference template. Read the template:

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/case-study/SKILL.md" 2>/dev/null | head -1)")
cat "$SKILL_DIR/templates/case-study-template.html"
```

### Design System (Fixed — Automate Accelerator Brand)

```css
/* These values are FIXED for all case studies */
--bg-dark:       #0c0c0e;
--bg-dark-alt:   #141417;
--bg-dark-card:  #18181c;
--bg-light:      #fafafa;
--bg-light-alt:  #f3f3f5;
--bg-white:      #ffffff;
--accent:        #ff6900;     /* Automate Accelerator orange */
--accent-hover:  #ff8533;
--green:         #34c759;
--blue:          #007aff;
--purple:        #af52de;
--teal:          #5ac8fa;
--orange:        #ff9500;
--font-display:  'Outfit';    /* Headlines */
--font-body:     'Inter';     /* Body text */
```

### Template Section Structure (7 sections)

1. **Hero (Dark)** — "Success Story" badge pill, massive Outfit headline (accent keyword on its own line), subtitle, logo pills (orange "Automate" + outline client), hero image with border glow, 3 dark stat cards at bottom

2. **Business Overview (Light)** — "PAGE 02" label in orange, section heading, orange underline bar, 3 info cards with solid orange icon squares (horizontal layout: icon left, text right), two-column: "Who They Are" text + dark Challenge card with titled bullet points (each challenge has a bold title + description)

3. **The Solution (Dark)** — "PAGE 03" label, headline, subtitle, 4 full-width dark step cards each with: coloured icon square (orange/green/teal/purple), bold title, description, pill tags row, and step number "01"-"04" faded on the right

4. **Performance Metrics (Light)** — "PAGE 04" label, headline, subtitle, 3 metric cards with circular SVG progress rings + icons inside, breakdown heading + subtitle, 4 breakdown cards with colour-coded left border bars (blue/purple/orange/green), each containing: label + percentage ring badge, 3 metric cells, dark "Follow-Up Success" callout card at bottom with orange icon

5. **Key Results (Dark)** — "PAGE 05" label, headline, subtitle, 4 stat cards with coloured icon squares (purple/green/orange/blue), bold gradient metric banner with large number, 2 detail cards

6. **What Made This Work (Light)** — "PAGE 06" label, centred heading, "The 3 Pillars of Success" subtitle, 3 pillar cards with orange bordered icon squares, two-column: framework checklist with green circle checkmarks + dark impact summary card with 4 stat boxes

7. **CTA (Orange gradient)** — Full orange gradient background, white headline, subtitle, frosted glass outline button, text-based dual branding ("Automate Accelerator" — divider — "[Client Name]"), tagline

### Typography Rules

- **Font:** Outfit for headlines, Inter for body. Load via Google Fonts.
- **Headlines:** `font-weight: 800-900`, `letter-spacing: -0.035em`, `line-height: 1.1`
- **Body:** `font-size: 14-16px`, `line-height: 1.65-1.7`, `color: var(--text-dark-secondary)` or `var(--text-light-secondary)`
- **Labels:** `font-size: 11px`, `font-weight: 600`, `letter-spacing: 2px`, `text-transform: uppercase`
- **Stat numbers:** `font-weight: 900`, `letter-spacing: -0.03em`
- **NEVER use emojis** — use SVG stroke icons for all iconography

### Icon Rules

- All icons are inline SVGs with `stroke` styling, NOT fill-based
- `stroke-width: 1.8-2`, `stroke-linecap: round`, `stroke-linejoin: round`, `fill: none`
- Icon squares: solid colour background with white or brand-coloured stroke icon inside
- Step cards: each gets a unique colour (orange, green, teal, purple)
- Breakdown rows: each gets a unique colour for the left border bar
- Voice stat cards: each gets a unique coloured icon square

### Card & Component Rules

- Border radius: `20-24px` for large cards, `10-14px` for small elements
- Dark cards: `background: #18181c`, `border: 1px solid rgba(255,255,255,0.07)`
- Light cards: `background: #ffffff`, `border: 1px solid #e5e5ea`, `box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04)`
- Hover: `translateY(-2px)` + subtle shadow increase
- Metric banner: `linear-gradient(135deg, #e05500, #ff6900, #ff8533)` with inner radial glow and top edge highlight line
- CTA section: full orange gradient with `backdrop-filter: blur(8px)` frosted glass button

### Content Rules

- **Write like a strategist, not a marketer.** No fluff, no buzzwords, no exclamation marks.
- Lead with the business problem, not the product features
- Every metric must have context (e.g. "40% increase in conversion rate")
- Challenge card items each get a **bold title** (e.g. "Passive Outreach") + description paragraph
- Solution step pills name specific tactics/tools, not vague descriptions
- Breakdown rows show a clear funnel (e.g. sent, opens, replies)
- The banner metric is the single most impressive number from the engagement
- Framework checklist items are specific and actionable
- Impact stats summarize total engagement outcomes

---

## STEP 4 — PREVIEW AND VERIFY

**MANDATORY: Take a Playwright screenshot and visually inspect before presenting to the user.**

1. Start a preview server:
   ```bash
   npx -y serve "$OUTPUT_DIR" -l 3458 --no-clipboard &
   sleep 2
   ```

2. Take screenshots:
   ```bash
   # Full page
   npx -y playwright screenshot --full-page --viewport-size="1440,900" "http://localhost:3458" "$OUTPUT_DIR/preview-full.png"
   # Hero close-up
   npx -y playwright screenshot --viewport-size="1440,900" "http://localhost:3458" "$OUTPUT_DIR/preview-hero.png"
   ```

3. **Visually verify (READ the screenshot):**
   - [ ] Both logos visible in hero pills (not broken/invisible)
   - [ ] Alternating dark/light sections render correctly
   - [ ] Orange accent colour is consistent
   - [ ] All SVG icons render (not blank squares)
   - [ ] Circular progress rings have correct stroke-dashoffset
   - [ ] Colour-coded left borders on breakdown cards
   - [ ] Metric banner gradient renders
   - [ ] CTA has full orange gradient background
   - [ ] No text is invisible (white-on-white or dark-on-dark)

4. Kill the server:
   ```bash
   kill $(lsof -ti:3458) 2>/dev/null
   ```

**If ANY logo is invisible or broken, fix it before proceeding. Use CSS `filter: brightness(0) invert(1)` or switch to text.**

### Run `polish` for final refinement

After the screenshot passes visual checks, run the `polish` skill for a final quality pass:

```
Skill("polish", "Final quality pass on this case study. Check: alignment, spacing consistency, micro-details, card border consistency, font weight hierarchy, colour accuracy.")
```

This catches subtle issues like inconsistent padding, misaligned elements, or font weight mismatches that screenshots alone won't reveal.

---

## STEP 5 — EXPORT TO PDF

The export script supports two modes:

```bash
SKILL_DIR=$(dirname "$(find ~/.claude -path "*/case-study/SKILL.md" 2>/dev/null | head -1)")

# For the v3 editorial scrolling design (RECOMMENDED):
node "$SKILL_DIR/scripts/export-pdf.js" "$OUTPUT_DIR/index.html" "$OUTPUT_DIR/[client-name]-case-study.pdf" --scroll

# For fixed A4 page designs:
node "$SKILL_DIR/scripts/export-pdf.js" "$OUTPUT_DIR/index.html" "$OUTPUT_DIR/[client-name]-case-study.pdf"
```

**Always use `--scroll` for the editorial template** — it captures the full page height as one continuous PDF. The default A4 mode is for fixed-page designs only.

The script:
- Waits for Google Fonts to load
- Waits for all images to load (with 5s timeout per image)
- Renders at 1440px width with all backgrounds intact
- Outputs the full page as a single continuous PDF

---

## STEP 6 — DELIVER

Present the user with:
1. **Preview screenshot** of the hero section
2. **File paths** for both HTML and PDF
3. **Key stats** used in the case study
4. **Section summary** — confirm all 7 sections rendered correctly
5. **Logo status** — confirm both logos are visible and rendering correctly
6. **Deployment note** — the HTML is self-contained and can be deployed to any static host or opened in Chrome for PDF export

---

## COMMON ISSUES & FIXES

### Logo Issues (Most Common Problem)

| Problem | Cause | Fix |
|---------|-------|-----|
| Logo invisible on dark bg | PNG has dark text on transparent bg | Add `style="filter: brightness(0) invert(1)"` to the `<img>` tag |
| Logo invisible on light bg | SVG has white fills | Add `style="filter: brightness(0)"` to the `<img>` tag |
| SVG renders blank | SVG has `display:none` on main group | Download a different variant or use text instead |
| Logo renders but is distorted | SVG viewBox doesn't match content | Set explicit `height` on the `<img>` tag, let width auto |
| Website logo URL returns 404 | CDN path changed | Check `brand-assets/` folder first, or try alternative selectors on the page |

### Font Issues

| Problem | Fix |
|---------|-----|
| Outfit font not loading | Check Google Fonts URL includes `family=Outfit:wght@300;400;500;600;700;800;900` |
| Fonts look different in PDF | Puppeteer `export-pdf.js` already waits for `document.fonts.ready` — ensure network is idle |

### Layout Issues

| Problem | Fix |
|---------|-----|
| Sections not alternating | Check background colours: odd sections = dark, even = light (except CTA = orange) |
| Cards overlapping on mobile | Ensure all grids collapse to `grid-template-columns: 1fr` at 600px |
| Circular rings not rendering | Check `stroke-dasharray` and `stroke-dashoffset` values are calculated correctly |

### Circular Progress Ring Math

To draw a ring at X% filled:
```
circumference = 2 * PI * radius = 2 * 3.14159 * r
dasharray = circumference
dashoffset = circumference * (1 - percentage/100)
```

For the template's rings (r=24 in top metrics, r=18 in breakdown):
- Top metrics: `circumference = 150.8`, so 75% = `dashoffset: 37.7`
- Breakdown: `circumference = 113.1`, so 75% = `dashoffset: 28.3`

---

## QUALITY CHECKLIST

Before delivering, verify ALL of the following:

### Logos & Branding
- [ ] Agency logo pill visible in hero (orange "Automate" pill)
- [ ] Client logo/name visible in hero (outline pill, inverted if needed)
- [ ] CTA shows both brand names as text on orange gradient
- [ ] No broken image icons anywhere on the page

### Visual Design
- [ ] Sections alternate: dark, light, dark, light, dark, light, orange-gradient
- [ ] Page labels appear ("PAGE 02", "PAGE 03", etc.)
- [ ] Orange underline bar below Business Overview heading
- [ ] Info cards have solid orange icon squares (horizontal layout)
- [ ] Challenge card is DARK (not orange gradient)
- [ ] Solution step cards have 4 different coloured icons
- [ ] Step numbers "01"-"04" appear faded on the right
- [ ] Performance metrics have circular SVG progress rings
- [ ] Breakdown cards have colour-coded left border bars
- [ ] Percentage ring badges on each breakdown card
- [ ] Follow-up callout is a dark card with orange icon
- [ ] Voice stats have coloured icon squares
- [ ] Metric banner has bold orange gradient with inner glow
- [ ] Pillar cards have orange bordered icon squares
- [ ] Checklist uses green circle checkmarks
- [ ] Impact card is dark within the light section
- [ ] CTA has full orange gradient background
- [ ] CTA button has frosted glass / outline style

### Content
- [ ] All metrics are real numbers from the engagement (not invented)
- [ ] Challenge items each have a bold title + description
- [ ] Solution pills name specific tactics
- [ ] Breakdown shows funnel data (sent, opens, replies)
- [ ] Framework checklist has 5+ specific items

### Technical
- [ ] Page is fully responsive (test at 900px and 600px)
- [ ] No console errors
- [ ] Google Fonts load correctly (Outfit + Inter)
- [ ] All SVG icons render (no blank squares or emojis)
- [ ] PDF exports with all backgrounds intact
