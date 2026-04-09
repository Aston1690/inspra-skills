---
name: bip
description: "Generate professional Business Information Pack (BIP) documents as 16:9 landscape PDF slide decks. Use this skill when the user wants to create a BIP, business information pack, company overview deck, sales pitch deck, business intro slides, or professional company presentation. Also trigger when the user provides a website URL, brand discovery doc, or content document and asks for a business overview, company profile, pitch deck, or sales enablement slides. Handles the full pipeline: brand extraction, content mapping, content sourcing, image generation, HTML slide build, Puppeteer PDF export, and multi-point QA verification."
---

# BIP Skill — Business Information Pack Generator (v5)

> Modern, editorial-quality Business Information Packs as 16:9 landscape PDF slide decks.
> Design philosophy: minimal, typography-driven, spacious — not generic corporate templates.
> Branding is ALWAYS from the CLIENT'S OWN BRAND. Never apply another brand's colors to a client BIP.

---

## CONTENT RULES (CRITICAL — READ FIRST)

**The source document is the ONLY source of truth for content.**

1. **NEVER miss content** — every section, paragraph, stat, quote, and bullet point from the source document MUST appear in the output
2. **NEVER alter content** — do not reword headlines, taglines, quotes, or section headings. Use the exact text provided
3. **NEVER invent content** — do not create stats, testimonials, phone numbers, emails, team bios, or copy that doesn't exist in the source
4. **If the source has more content than 9 slides** — ADD slides. Never drop content to fit the template
5. **Use placeholders** for genuinely missing data: `[PHONE]`, `[TESTIMONIAL NEEDED]`, `[EMAIL]`

### Content Mapping (MANDATORY STEP)

Before writing any HTML, create a content map:
1. List every section/topic from the source document
2. Map each source section to a specific slide
3. Verify NO source content is unmapped
4. If content doesn't fit 9 slides, add more slides using the design system's alternating dark/light pattern

---

## Skills Used in This Workflow

**You MUST invoke these skills at the specified steps — do not skip them.**

| Skill | Step | Purpose |
|-------|------|---------|
| **`brand-guide-extractor`** | Step 0 | Extract client's logo, colours, fonts, and visual tone from their website |
| **`copywriting`** | Step 3 | Write slide content with strategic, benefit-focused language |
| **`taste-frontend`** | Step 5 (after first HTML draft) | Audit the slide design against premium standards |
| **`polish`** | Step 6 (after screenshots) | Final quality pass on spacing, alignment, and micro-details |

---

## INPUTS REQUIRED

| Input | Source | Required? |
|-------|--------|-----------|
| Website URL | User-provided | Strongly recommended |
| Content Document | Google Doc, PDF, or markdown | Primary content source |
| Brand Guide | File or inline text | Use if provided |
| Client Name | Extracted from sources | Required |
| Client photos/headshots | User-provided | Use if provided — never crop from screenshots |

---

## STEP 0.5 — ASK THE USER BEFORE PROCEEDING

**MANDATORY: Before doing any research or generation, ask these questions:**

1. **"Do you have an existing brand guide or brand-assets folder for this client?"**
   - If yes, ask for the path and use those assets
   - Check `brand-assets/[client-name]/` in the project directory first

2. **"Do you have a content document (Google Doc, PDF, or text) with the company information?"**
   - If yes, use that as the primary content source
   - NEVER invent content when a source document exists

3. **"Are there any specific images, team photos, or visuals you'd like to include?"**
   - If yes, use their images directly — never try to crop or extract from screenshots
   - If not, use FLUX to generate or source from Unsplash

**Only proceed to Step 0 after getting answers.**

---

## STEP 0 — BRAND EXTRACTION (MANDATORY FIRST STEP)

**Before writing a single word, extract the client's brand identity.**

### 0a. Run `brand-guide-extractor` on the Client Website

**ALWAYS run this skill FIRST:**

```
Skill("brand-guide-extractor", "https://www.clientwebsite.com")
```

This gives you: logo URLs, primary/secondary colours, fonts, screenshots, tone.

### 0b. If the user provided a brand guide

Read it and extract the relevant tokens. Skip `brand-guide-extractor` for anything the guide already covers.

### 0c. Logo Collection

1. **Check local `brand-assets/` first:**
   ```bash
   find "$(pwd)/brand-assets" -iname "*[CLIENT_NAME]*" 2>/dev/null | head -10
   ```
2. **If found locally**, copy to the output directory.
3. **If not found**, use the logo URL from `brand-guide-extractor`.
4. **Download both light and dark variants** if available.

### 0d. Logo Visibility Verification

**CRITICAL: Test every logo on both dark and light backgrounds.**

- Dark text logo on dark slide: add `filter: brightness(0) invert(1)`
- White text logo on light slide: add `filter: brightness(0)`
- If a logo doesn't render cleanly, use text instead
- **NEVER use the SVG from automateaccelerator.com** — it has broken `display:none` layers. Use PNG versions.

### Brand Mapping Rules

| BIP Token | Source | Notes |
|-----------|--------|-------|
| `--bg-dark` | Client's darkest brand colour, or darken primary by 60% | Dark slides |
| `--bg-light` | `#f8f7f4` (warm cream) or client's light bg | Light slides |
| `--accent` | Client's primary CTA / highlight colour | Headings, dividers, numbers |
| `--text-on-dark` | `#ffffff` | Always white on dark |
| `--text-on-light` | `#1a1a1e` or client's dark text | Body on light slides |
| `--text-muted` | `rgba(255,255,255,0.6)` on dark, `#8b8b96` on light | Secondary text |
| `--font` | Client's headline font or `Poppins` as fallback | Load via Google Fonts |

---

## STEP 1 — CONTENT EXTRACTION

### If the user provided a content document:
Read it. Use it as the SOLE source of truth. Do NOT invent content.

### If no content document:
1. **WebFetch the main website** — extract services, about, team, testimonials
2. **WebSearch for the company** — find press mentions, awards, metrics
3. **WebFetch key pages** — about, services, contact, testimonials

---

## STEP 2 — CONTENT MAPPING (MANDATORY)

Map ALL extracted content to slides. **Every piece of source content must be assigned to a slide.**

Create this map before writing any HTML:

```
SOURCE CONTENT → SLIDE MAPPING
─────────────────────────────────
Source Section 1: [title] → Slide [N]: [name]
Source Section 2: [title] → Slide [N]: [name]
...
UNMAPPED CONTENT: [list anything not yet assigned]
ACTION: [add slides for unmapped content]
```

**If any source content is unmapped, add more slides. Never drop content.**

---

## STEP 3 — WRITE SLIDE CONTENT

Run the `copywriting` skill:

```
Skill("copywriting", "Write BIP slide content for [CLIENT]. Tone: confident, warm, benefit-focused. No fluff. Active voice. Australian English. Content: [paste key content]")
```

### Writing Guidelines
- Active voice, benefit-focused throughout
- Specific numbers over vague claims
- Headline copy: concise, mix white and accent-coloured words
- Body copy: conversational, confident, warm — not corporate/stiff
- Forbidden: "unlock", "revolutionise", "seamless", "game-changing", "synergy", "leverage"
- Match the client's regional spelling (Australian English unless specified)
- **Only include content from source documents — never invent**
- Placeholders for missing data: `[PHONE]`, `[TESTIMONIAL NEEDED]`, `[PARTNER LOGOS]`

---

## STEP 4 — GENERATE SUPPORTING VISUALS

Run the FLUX image generation script:

```bash
python ~/.claude/skills/bip/scripts/generate_images.py \
  --company "[Client Name]" \
  --industry "[Industry]" \
  --accent-color "[ACCENT hex]" \
  --bg-color "[BG_DARK hex]" \
  --tone "[3 tone descriptors]" \
  --output-dir output/bip-work/images
```

If FLUX fails, use Unsplash stock images or CSS gradient fallbacks with `.no-image` class.

### Image Rules (CRITICAL)
- **Every image MUST be a DIFFERENT photo** — never reuse the same URL across slides
- **No Black people in stock photos** — client preference, check every image visually
- **Verify every image URL returns HTTP 200** before exporting: `curl -s -o /dev/null -w "%{http_code}" URL`
- **If user provides photos, use them directly** — never crop from screenshots or low-res sources
- If an image URL returns non-200, replace immediately before proceeding

### Image Keys

| Key | Slide | Purpose |
|-----|-------|---------|
| `cover_bg` | 1: Cover | Abstract branded background |
| `about_panel_1` | 2: About | Team collaboration |
| `about_panel_2` | 2: About | Workspace/office |
| `about_panel_3` | 2: About | Close-up hands-on-device |
| `services_visual` | 3: Services | Service representation |
| `why_choose_us_bg` | 4: Why Choose Us | Subtle geometric accent |
| `benefits_visual` | 5: How We Help | Growth/outcomes metaphor |
| `team_culture` | 6: Who We Are | Team culture |
| `testimonials_bg` | 7: Testimonials | Trust-evoking background |
| `partners_visual` | 8: Partners | Network visual |
| `contact_bg` | 9: Contact | Minimal closing background |

---

## STEP 5 — BUILD HTML SLIDES

### Design Philosophy: Modern Editorial Slides

The BIP should feel like a premium keynote presentation — NOT a generic dark corporate template.

**Core principles:**
- **Typography is the design** — large type, creative weight mixing, dramatic scale contrast
- **Whitespace is a feature** — let content breathe, don't fill every pixel
- **Alternating dark/light slides** — creates visual rhythm
- **No card borders on light slides** — use spacing and typography for hierarchy
- **Images fill space** — no small thumbnails, use full-bleed or large panels
- **Font weight: 500-600 max** — no bold (700+) fonts. Medium weight only for a refined feel.

### Design System

```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Inter:wght@400;500&display=swap');

@page { size: 1920px 1080px; margin: 0; }

:root {
  --bg-dark: /* from Step 0 */;
  --bg-light: #f8f7f4;
  --accent: /* from Step 0 */;
  --text-on-dark: #ffffff;
  --text-on-light: #1a1a1e;
  --text-muted-dark: rgba(255,255,255,0.55);
  --text-muted-light: #8b8b96;
  --font: 'Poppins', /* client font */, sans-serif;
}

.slide {
  width: 1920px; height: 1080px;
  position: relative; overflow: hidden;
  page-break-after: always;
  padding: 80px 100px;
}
```

### Typography Scale

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Cover headline | 80-96px | 600 | Large, commanding but not heavy |
| Section headline | 56-72px | 600 | Mix white + accent words |
| Sub-headline | 28-32px | 500 | Accent colour |
| Body text | 18-20px | 400 | Generous line-height (1.75) |
| Labels / footer | 14px | 400 | Muted colour |
| Stat numbers | 48-64px | 600 | Accent colour, tight tracking |

### Slide Background Pattern

| Slide # | Background | Feel |
|---------|-----------|------|
| 1 Cover | Dark + full-bleed image | Hero impact |
| 2 About | Light (warm cream) | Editorial, readable |
| 3 Services | Dark | Bold, structured |
| 4 Why Choose Us | Dark + full-bleed image | Trust, authority |
| 5 How We Help | Light | Clean, benefits-focused |
| 6 Who We Are | Dark | Intimate, team-focused |
| 7 Testimonials | Light | Open, trustworthy |
| 8 Partners | Dark | Professional, credible |
| 9 Contact | Dark + accent gradient | Warm CTA |

### Card & Component Rules

- **Dark slide cards:** `background: rgba(255,255,255,0.05)`, `border: 1px solid rgba(255,255,255,0.08)`, `border-radius: 16px`
- **Light slide elements:** NO card borders — use spacing, thin divider lines, typography hierarchy
- **Images:** `border-radius: 16px`, `object-fit: cover`
- **Logo:** Cover = top-left 60px height. Other slides = bottom-right 40px height, 80% opacity
- **Accent divider:** thin line in accent colour, used sparingly
- **Stat numbers:** accent coloured, weight 600, tight letter-spacing (-0.03em)

### Split Layout Pattern (Cover, Partners, Contact)

```css
.slide { display: flex; align-items: stretch; padding: 0; }
.slide .text { flex: 1; padding: 80px 60px 80px 100px; display: flex; flex-direction: column; justify-content: center; }
.slide .image { width: 42%; }
.slide .image img { width: 100%; height: 100%; object-fit: cover; border-radius: 24px 0 0 24px; }
```

### After HTML is built, run `taste-frontend`:

```
Skill("taste-frontend", "Audit this BIP slide deck for premium quality. Check: typography hierarchy, spacing, image placement, colour consistency, card treatments, overall editorial feel.")
```

---

## STEP 6 — EXPORT TO PDF

```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto('file://' + path.join(__dirname, 'bip.html'), {
    waitUntil: 'networkidle0',
    timeout: 30000
  });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('img'));
    await Promise.all(imgs.map(img => {
      if (img.complete) return Promise.resolve();
      return new Promise(resolve => { img.onload = resolve; img.onerror = resolve; setTimeout(resolve, 5000); });
    }));
  });
  await new Promise(r => setTimeout(r, 2000));
  await page.pdf({
    path: path.join(__dirname, '..', '[client-name]-bip-v1.pdf'),
    width: '1920px',
    height: '1080px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });
  await browser.close();
  console.log('SUCCESS');
})();
```

---

## STEP 7 — QA VERIFICATION (MANDATORY BEFORE DELIVERY)

**You MUST complete ALL QA checks before opening the PDF for the user. No exceptions.**

### 7a. Verify All Image URLs

```bash
# Extract all image URLs from the HTML and verify each returns HTTP 200
# If any return non-200, replace immediately and re-export
```

### 7b. Slide-by-Slide Screenshot Review

```javascript
// Screenshot EVERY slide individually and READ each one
const slides = await page.$$('.slide');
for (let i = 0; i < slides.length; i++) {
  await slides[i].screenshot({ path: `qa-slide-${i+1}.png`, type: 'png' });
}
```

**Read EVERY screenshot with the Read tool.** Check each slide for:
- Images loading correctly (no broken icons, no alt text visible)
- No Black people in stock photos
- Logo visible and correct version for background colour
- Text readable and properly styled
- No content overflow or clipping
- Headshots/photos clean (no artefacts, no dark backgrounds bleeding through)
- Font weights are 600 max
- Stat numbers are accent-coloured
- Generous whitespace

### 7c. Content Audit

Compare EVERY piece of content from the source document against the HTML output:
- Is ALL source content present in the slides?
- Was any content changed, reworded, or summarised?
- Was anything invented that wasn't in the source?
- Are quotes using the exact original text?
- Are contact details, phone numbers, emails from the source (not invented)?
- Are stats and metrics from the source (not invented)?

### 7d. Layout & Design Checks

- [ ] Slides alternate dark/light correctly
- [ ] Brand colours match client's actual website
- [ ] No negative spacing or overlapping elements
- [ ] All images unique (no duplicates across slides)
- [ ] Split layouts have image bleeding to edge (no gap)
- [ ] Body text minimum 18-20px (readable at 1920px)

### 7e. Run `polish` Skill

```
Skill("polish", "Final quality pass on BIP slides. Check: alignment, spacing, font consistency, colour accuracy, image quality.")
```

### QA Pass/Fail Checklist

**Only deliver the PDF when ALL items pass:**

- [ ] All image URLs return HTTP 200
- [ ] Every slide screenshot reviewed — no visual issues
- [ ] No Black people in any stock photos
- [ ] No broken images or alt text showing
- [ ] All source content is present and unaltered
- [ ] No invented content (stats, quotes, contact details, copy)
- [ ] Quotes match source text exactly
- [ ] Contact details match source exactly (or use placeholders)
- [ ] Logo visible on every slide (correct variant per bg)
- [ ] Brand colours match client website
- [ ] Slides alternate dark/light
- [ ] Font weight 600 max throughout
- [ ] Every image is unique across slides
- [ ] Headshots/photos are clean (user-provided, not cropped from screenshots)
- [ ] PDF exports at 1920x1080 per slide

---

## STEP 8 — DELIVER

Present the user with:
1. **Preview screenshots** of key slides (cover, services, contact at minimum)
2. **PDF file path**
3. **Logo status** — confirm both dark and light versions render correctly
4. **Content source** — confirm all content came from their document
5. **Slide summary** — confirm all slides are present and list what's on each
6. **QA status** — confirm all checks passed

---

## SLIDE STRUCTURE (9 slides minimum, alternating dark/light)

### Slide 1: Cover (DARK) — Split Layout

**Layout:** Two-panel split — text left (58%), image right (42%). Image bleeds to the right edge with `border-radius: 24px 0 0 24px`. Logo top-left in the text area. Massive headline (80-92px, weight 600). Accent-coloured keyword. Tagline below (22-28px, muted). Thin accent divider. Website URL bottom-left.

### Slide 2: About / Company Introduction (LIGHT)

**Layout:** Warm cream background. Top section: 3-panel photo collage (full width, 45% height). Bottom: 2-3 body paragraphs in large readable text (20px, 1.75 line-height). NO section title — let the copy lead. Logo bottom-right.

### Slide 3: What We Offer (DARK)

**Layout:** Large "What We Offer" title (56-64px, weight 600). Left column (55%): service categories with accent subheads + descriptions. Right column (40%): generated visual with border-radius. Logo bottom-right.

### Slide 4: Why Choose Us (DARK + full-bleed image)

**Layout:** Full-bleed `why_choose_us_bg` with dark overlay. Large headline left (40% width). Three value points stacked right — each with accent subhead + 2-3 sentences. Logo bottom-right.

### Slide 5: How We Help (LIGHT)

**Layout:** Warm cream background. Large headline (white + accent word mix). Lead sentence. Left column: 3 benefit sections with accent subheads. Right column: benefits visual. Logo bottom-right.

### Slide 6: Who We Are & Goals (DARK)

**Layout:** Two-column. Left (55%): headline, About Us, Mission, Vision subsections. Right (45%): team culture image. Logo bottom-right.

### Slide 7: Testimonials (LIGHT)

**Layout:** Warm cream background. Large headline. Intro sentence. 2-3 testimonial quotes — large italic text with attribution. **Use real quotes from source only.** Logo bottom-right.

### Slide 8: Partners / Trust (DARK) — Split Layout

**Layout:** Split layout — text left (55%), image right (45%) bleeding to edge. Heading + description on left. Image fills right with `border-radius: 24px 0 0 24px`. Logo bottom-right in text area.

### Slide 9: Contact (LIGHT) — Split Layout

**Layout:** Light/cream background. Split layout — text left (58%), full-bleed image right (42%). Logo top-left (dark version for light bg). Large CTA headline. Contact details. **Use exact contact details from source — never invent.**

---

## COMMON ISSUES & FIXES

### Logo Issues

| Problem | Fix |
|---------|-----|
| Logo invisible on dark slide | Use white version or `filter: brightness(0) invert(1)` |
| Logo invisible on light slide | Use dark version or `filter: brightness(0)` |
| SVG renders blank | Download PNG instead, or use text fallback |
| Logo renders HUGE / distorted | Set `height`, `width:auto`, AND `max-width` on `<img>` tags |

### Image Issues

| Problem | Fix |
|---------|-----|
| FLUX generation failed | Use Unsplash stock images matching industry |
| Image URL returns non-200 | Find alternative URL, verify with curl before using |
| Image too dark on dark slide | Add lighter overlay gradient |
| User provided a photo | Use it directly — NEVER crop from screenshots |
| Image shows Black people | Replace with alternative stock image |

### Layout Issues

| Problem | Fix |
|---------|-----|
| Text and image not aligned | Use `display:flex; align-items:stretch;` on the slide |
| Content overflows slide | Reduce heading size or let content flow from top |
| Blank space on slides | Use `justify-content:center` to vertically centre |
| Split layout has gap on right | Remove padding from image side, set `width:42-45%` with `height:100%; object-fit:cover` |

---

## COMPLIANCE RULES

- **Step 0 brand extraction is mandatory** — never skip it
- **BIP uses CLIENT branding** — not Automate Accelerator
- **Font weight 600 max** — no bold (700+) fonts
- **Ask user 3 questions before starting** (brand guide, content doc, images)
- **All source content must be present** — never skip sections to fit 9 slides
- **Never alter CTAs, quotes, or headlines** from what the source provides
- **Never invent content** — no fabricated stats, testimonials, contact details, or copy
- **No Black people in stock photos** — client preference
- **Every image must be unique** — never reuse the same URL across slides
- **Verify all image URLs** return HTTP 200 before export
- **If user provides photos, use them directly** — never crop from screenshots
- **Full QA verification mandatory** — slide-by-slide screenshots + content audit before delivery
- Run `brand-guide-extractor` before extracting brand manually
- Run `copywriting` for slide content
- Run `taste-frontend` after HTML draft
- Run `polish` after screenshots
- ALWAYS alternate dark/light slide backgrounds
- ALWAYS use Poppins as fallback font
- Output MUST be PDF in 16:9 landscape (1920x1080px)

---

*BIP Skill | v5.0 | Content-Faithful, Full QA Pipeline, Image Verified, Modern Editorial Design*
