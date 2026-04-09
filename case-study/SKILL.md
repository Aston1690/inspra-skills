---
name: case-study
description: "Generate a professional, branded case study webpage from any company website URL. Use this skill whenever the user wants to create a case study, client success story, project results document, campaign performance report, or any results-focused PDF showcasing work done for a client. Also trigger when the user provides stats, metrics, campaign results, or a content document and asks for a case study, success story, results deck, or client showcase. Handles the full pipeline: brand extraction, content mapping, HTML build, Puppeteer single-page PDF export, and multi-point QA verification."
---

# Case Study Skill — Client Success Story Generator v4

> This skill generates a premium, editorial-style Case Study as a long-scroll webpage exported to a single-page PDF.
> **Design reference: the BGES case study** at `/Users/akhilaston/Desktop/Inspra/C_Hub/case-study-skill/output/bges-case-study/v2.html`
> **ALWAYS read that file first** to get the exact CSS, HTML structure, and design tokens before writing any code.
> Branding is ALWAYS from Automate Accelerator (the presenting company).

---

## CANONICAL TEMPLATE (CRITICAL)

**Before writing ANY HTML, you MUST read the template file:**

```
/Users/akhilaston/Desktop/Inspra/C_Hub/case-study-skill/output/bges-case-study/v2.html
```

This is the single source of truth for:
- CSS variables, fonts, spacing, colors
- Component patterns (timeline, stats, pillars, etc.)
- Typography scale and weights
- Responsive breakpoints

**Copy the CSS verbatim from the template.** Only change the content — never the design system.

**CSS Fix Required:** Add `line-height: 1.15` to `.highlight-big` — the template's body line-height (1.8) is too loose for this element.

---

## CONTENT RULES (CRITICAL — READ FIRST)

**The source document is the ONLY source of truth for content.**

1. **NEVER miss content** — every section, paragraph, stat, quote, and bullet point from the source document MUST appear in the output
2. **NEVER alter content** — do not reword headlines, CTAs, quotes, or section headings. Use the exact text provided
3. **NEVER invent content** — do not create stats, table data, descriptions, or copy that doesn't exist in the source
4. **If the source has more sections than the template** — ADD sections to the template. Never drop content to fit a template
5. **Use placeholders** for genuinely missing data: `[METRIC]`, `[CLIENT TESTIMONIAL NEEDED]`

### Content Mapping (MANDATORY STEP)

Before writing any HTML, create a content map:
1. List every section/page from the source document
2. Map each source section to an output section
3. Verify NO source content is unmapped
4. If content doesn't fit existing template sections, create new sections using the template's design patterns

---

## INPUTS REQUIRED

| Input | Source | Required? |
|-------|--------|-----------|
| Client Website URL | User-provided | Strongly recommended |
| Content Document | PDF, doc, markdown, or inline text | Primary content source |
| Client Name | Extracted from sources | Required |
| Client headshot/photo | User-provided or from website | If testimonial exists |

---

## BRANDING RULES

**The case study is ALWAYS branded as Automate Accelerator.**

1. **Run `/brand-guide-extractor` on automateaccelerator.com FIRST** to get AA's brand assets (logo SVG)
2. **Run `/brand-guide-extractor [client-website]`** to get client logo
3. AA logo appears in: hero logos section and CTA brands footer
4. Client logo appears in: hero logos section (with `filter: brightness(0) invert(1)` for white-on-dark)
5. Brand footer text: `Automate Accelerator — [Client Name]`

---

## DESIGN SYSTEM (from BGES template)

### Color Tokens
```css
:root {
  --dark: #0c0c0e;
  --dark-surface: #161619;
  --light: #f8f7f4;
  --text-primary: #1a1a1e;
  --text-muted: #8b8b96;
  --accent: #ff6900;
  --accent-soft: rgba(255,105,0,0.08);
}
```

### Typography
```
Headline:  'Poppins', sans-serif (300-700 weight)
Body:      'Inter', sans-serif (400-500 weight)
```

### Key Rules
- Headlines use `clamp()` for responsive sizing
- Letter-spacing: `-0.03em` on large headlines, `-0.02em` on section titles
- Body: 17px, line-height 1.8
- Accent text: `<span class="accent">text</span>` (orange)
- Section labels: title + horizontal orange line
- Section padding: `140px 0`
- Max-width: `1200px` with `40px` horizontal padding

---

## SECTION STRUCTURE

The base template has these sections. **Add more sections if the source document has content that doesn't fit these.**

| # | Section | Background | Key Components |
|---|---------|------------|----------------|
| 1 | Hero | `--dark` | Badge, headline with accent, subtitle, two logos, cover image, 3 floating stat cards |
| 2 | Business Overview | `--light` | Section label with line, narrative grid (text + quick facts), challenge items (2x2 grid) |
| 3 | The Solution | `--dark` | Title + description with side image, timeline with dots |
| 4+ | **Additional content sections** | Alternating | **Map ALL remaining source pages here — do NOT skip any** |
| N-2 | Highlight Band | `--accent` | Full-width orange band with key stat headline |
| N-1 | Testimonial | `--dark` | Large quote mark, italic quote, author with headshot |
| N | What Made This Work | `--light` | 3 pillars, framework list, partnership quote |
| N+1 | CTA | `--dark` | Original CTA headline from source, orange pill button |

### Adding Extra Sections

When the source has content beyond the base template (e.g., Email Campaigns, Voice Outreach, Results):
- Use `--light` background for data/content sections (reuse `.results` / `.overview` CSS)
- Use `--dark` background for process/story sections (reuse `.solution` CSS with timeline)
- Alternate dark/light for visual rhythm
- Use existing component patterns: timeline for processes, tables for breakdowns, grids for comparisons

---

## STOCK IMAGES

### Rules
- **Every image MUST be a DIFFERENT photo** — never reuse the same URL across sections
- **No Black people in stock photos** — this is a client preference, check every image
- **Verify every URL returns HTTP 200** before exporting — use `curl -s -o /dev/null -w "%{http_code}" URL`
- If a URL returns 404, find an alternative immediately
- Use Unsplash URLs directly in `<img>` tags

### Image Sizes
```
Cover/hero:    ?w=1400&h=500&fit=crop&q=85
Overview:      ?w=700&h=360&fit=crop&q=85
Solution:      ?w=600&h=400&fit=crop&q=85
Content pages: ?w=1200&h=400&fit=crop&q=85
What Worked:   ?w=600&h=500&fit=crop&q=85
```

### Client Headshots
- If the user provides a headshot image, copy it directly — do NOT try to crop from screenshots
- If no headshot is available, ask the user for one rather than using a low-quality crop
- Display headshots at 64px circular with `object-fit: cover; border: 2px solid rgba(255,255,255,0.15)`

---

## PRODUCTION STEPS

1. **Read the BGES template** — copy its full CSS
2. **Run `/brand-guide-extractor`** for both AA and client — download logos
3. **Map ALL source content** — list every section, verify nothing is unmapped
4. **Write HTML** — using template CSS, all source content, unique images
5. **Verify all image URLs** — curl each one, confirm HTTP 200
6. **Export to single-page PDF** — using Puppeteer with dynamic height
7. **Run full QA** — see QA section below
8. **Open the PDF** for the user

---

## TECHNICAL PIPELINE

### Working Directory
```bash
cd output/case-study-work
npm install puppeteer  # if not already installed
```

### Puppeteer Export (SINGLE PAGE — NOT A4 PAGINATED)

```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 800 });
  await page.goto('file://' + path.join(__dirname, 'case-study.html'), {
    waitUntil: 'networkidle0',
    timeout: 30000
  });

  // Get actual content height for single-page export
  const bodyHeight = await page.evaluate(() => document.body.scrollHeight);

  // Export as SINGLE PAGE matching exact content height
  await page.pdf({
    path: path.join(__dirname, '..', '[client-name]-case-study-v1.pdf'),
    width: '1200px',
    height: bodyHeight + 'px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  await browser.close();
  console.log('SUCCESS — single-page PDF');
})();
```

**IMPORTANT:** Use dynamic height (`bodyHeight + 'px'`), NOT `format: 'A4'`. A4 causes content to overflow across page boundaries.

---

## QA VERIFICATION (MANDATORY BEFORE DELIVERY)

**You MUST complete ALL QA checks before opening the PDF for the user. No exceptions.**

### Step 1: Verify All Image URLs
```bash
# curl every Unsplash URL in the HTML and confirm HTTP 200
# If any return non-200, replace immediately
```

### Step 2: Full-Page Screenshot Review
```javascript
// Take a full-page screenshot and READ it with the Read tool
await page.screenshot({ path: 'full-review.png', fullPage: true, type: 'png' });
```
Visually inspect the ENTIRE page top-to-bottom. Check for:
- Broken image icons
- Layout overflow or clipping
- Excessive whitespace or negative spacing
- Text cutoff or overlap
- Font loading issues

### Step 3: Section-by-Section Screenshot
```javascript
// Screenshot EVERY section individually and READ each one
const sections = await page.$$('section');
for (let i = 0; i < sections.length; i++) {
  await sections[i].screenshot({ path: `qa-section-${i+1}.png` });
}
```
Check each section for:
- Images loading correctly (no broken icons, no placeholder alt text visible)
- No Black people in stock photos
- Text is readable and properly styled
- Headshots display cleanly (no artefacts, dark backgrounds, white borders)
- Line heights are correct (especially highlight band)

### Step 4: Content Audit
Compare EVERY paragraph, quote, stat, and section title from the source document against the HTML output:
- Is ALL source content present?
- Was any content changed or reworded?
- Was anything invented that wasn't in the source?
- Are CTAs using the original wording?
- Are quotes exact?

### QA Pass/Fail
Only deliver the PDF when ALL checks pass:
- [ ] All image URLs return HTTP 200
- [ ] Full-page screenshot shows no visual issues
- [ ] Every section screenshot is clean
- [ ] No Black people in any stock photos
- [ ] No broken images or alt text showing
- [ ] All source content is present and unaltered
- [ ] No invented content
- [ ] CTAs match source wording exactly
- [ ] Quotes match source text exactly
- [ ] Highlight band line-height is tight (1.15)
- [ ] Headshots are clean (use user-provided images, not screenshot crops)
- [ ] PDF is single-page (no content cut across page boundaries)

---

## WRITING GUIDELINES

- Australian English spelling throughout
- Active voice, results-focused, data-dense
- Specific numbers over vague claims — numbers are the hero
- Body copy: professional, confident, warm — not stiff
- Forbidden words: "unlock", "revolutionise", "seamless", "game-changing", "synergy", "leverage" (as verb)
- Connect every result to a tangible business outcome
- **Only include content from source documents — never invent stats, table data, or copy**
- Use placeholders for missing data: `[METRIC]`, `[CLIENT TESTIMONIAL NEEDED]`

---

## COMPLIANCE RULES

- **Branding is ALWAYS Automate Accelerator** — never brand as the client
- **Read the BGES template HTML first** — copy its CSS verbatim
- **Run `/brand-guide-extractor` for both AA and client** before starting
- **Stock images from Unsplash are mandatory** — never ship without real photography
- **No Black people in stock photos** — client preference
- **Every image must be unique** — never reuse the same Unsplash URL
- **All source content must be present** — never skip sections to fit a template
- **Never alter CTAs, quotes, or headlines** from what the source provides
- **Never invent content** — no fabricated stats, table data, or descriptions
- **Single-page PDF export** — use dynamic height, NOT A4 pagination
- **Full QA verification mandatory** — full-page + section screenshots + content audit before delivery
- If user provides a headshot, use it directly — never try to crop from screenshots
- Highlight band `line-height: 1.15` override is required
- Timeline layout for solution processes
- Testimonial section with large quote mark and author headshot
- CTA uses the EXACT wording from the source document

---

*Case Study Skill | v4.0 | BGES Reference Design — Content-Faithful, Single-Page PDF, Full QA Pipeline*
