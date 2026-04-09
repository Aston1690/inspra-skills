---
name: bip
description: "Generate professional Business Information Pack (BIP) documents as 16:9 landscape PDF slide decks. Use this skill when the user wants to create a BIP, business information pack, company overview deck, sales pitch deck, business intro slides, or professional company presentation. Also trigger when the user provides a website URL, brand discovery doc, or content document and asks for a business overview, company profile, pitch deck, or sales enablement slides. Handles the full pipeline: brand extraction, content sourcing, FLUX image generation, HTML slide build, and Puppeteer PDF export."
---

# BIP Skill — Business Information Pack Generator (v4)

> Modern, editorial-quality Business Information Packs as 16:9 landscape PDF slide decks.
> Design philosophy: minimal, typography-driven, spacious — not generic corporate templates.
> Branding is ALWAYS from the CLIENT'S OWN BRAND. Never apply another brand's colors to a client BIP.

---

## Skills Used in This Workflow

**You MUST invoke these skills at the specified steps — do not skip them.**

| Skill | Step | Purpose |
|-------|------|---------|
| **`brand-guide-extractor`** | Step 0 | Extract client's logo, colours, fonts, and visual tone from their website. PRIMARY method for brand discovery. |
| **`copywriting`** | Step 3 | Write slide content with strategic, benefit-focused language. |
| **`taste-frontend`** | Step 5 (after first HTML draft) | Audit the slide design against premium standards. |
| **`polish`** | Step 6 (after screenshots) | Final quality pass on spacing, alignment, and micro-details. |

### How to Invoke Skills

```
Skill("brand-guide-extractor", "https://www.clientwebsite.com")
Skill("copywriting", "Write BIP slide content for [client]. Tone: confident, warm, benefit-focused...")
Skill("taste-frontend", "Audit this BIP slide deck for premium design quality...")
Skill("polish", "Final pass on the BIP slides...")
```

---

## INPUTS REQUIRED

| Input | Source | Required? |
|-------|--------|-----------|
| Website URL | User-provided | Strongly recommended |
| Content Document | Google Doc, PDF, or markdown | Primary content source |
| Brand Guide | File or inline text | Use if provided |
| Client Name | Extracted from sources | Required |

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
   - If yes, use their images
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

Map extracted values to the BIP design system:

| BIP Token | Source | Notes |
|-----------|--------|-------|
| `--bg-dark` | Client's darkest brand colour, or darken primary by 60% | Dark slides |
| `--bg-light` | `#f8f7f4` (warm cream) or client's light bg | Light slides |
| `--accent` | Client's primary CTA / highlight colour | Headings, dividers, numbers |
| `--text-on-dark` | `#ffffff` | Always white on dark |
| `--text-on-light` | `#1a1a1e` or client's dark text | Body on light slides |
| `--text-muted` | `rgba(255,255,255,0.6)` on dark, `#8b8b96` on light | Secondary text |
| `--font` | Client's headline font or `Poppins` as fallback | Load via Google Fonts |

### Brand Extraction Output

```
BRAND TOKENS — [Client Name]
──────────────────────────────
BG_DARK:    #______
BG_LIGHT:   #______
ACCENT:     #______
FONT:       ______
LOGO:       [path] (verified on dark + light bg)
TONE:       [3 descriptors]
```

---

## STEP 1 — CONTENT EXTRACTION

### If the user provided a content document:
Read it. Use it as the SOLE source of truth. Do NOT invent content.

### If no content document:
1. **WebFetch the main website** — extract services, about, team, testimonials
2. **WebSearch for the company** — find press mentions, awards, metrics
3. **WebFetch key pages** — about, services, contact, testimonials

---

## STEP 2 — CONTENT MAPPING

Map extracted content to the 9 slides. Use placeholders for anything missing.

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
- Only include content from source documents
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
- **Alternating dark/light slides** — creates visual rhythm (dark cover, light about, dark services, etc.)
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

### Typography Scale (Poppins or client font)

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
- **Light slide elements:** NO card borders — use spacing, thin divider lines (`1px solid rgba(0,0,0,0.06)`), and typography hierarchy
- **Images:** `border-radius: 16px`, `object-fit: cover`
- **Logo:** Cover = top-left 60px height. Other slides = bottom-right 40px height, 80% opacity
- **Accent divider:** thin line in accent colour, used sparingly between sections
- **Stat numbers:** accent coloured, weight 600, tight letter-spacing (-0.03em)

### After HTML is built, run `taste-frontend`:

```
Skill("taste-frontend", "Audit this BIP slide deck for premium quality. Check: typography hierarchy, spacing, image placement, colour consistency, card treatments, overall editorial feel.")
```

---

## STEP 6 — PREVIEW AND VERIFY

**MANDATORY: Screenshot every slide before exporting.**

```bash
# Start preview server
npx -y serve "$OUTPUT_DIR" -l 3460 --no-clipboard &
sleep 2

# Full-page screenshot
npx -y playwright screenshot --full-page --viewport-size="1920,1080" "http://localhost:3460" "$OUTPUT_DIR/preview.png"

# Kill server
kill $(lsof -ti:3460) 2>/dev/null
```

**Visually verify:**
- [ ] Client logo visible on cover (correct version for dark bg)
- [ ] Logo visible on all other slides (correct version per bg colour)
- [ ] Brand colours match client's actual website
- [ ] Slides alternate dark/light correctly
- [ ] Images render (no broken images or blank spaces)
- [ ] Font weights are 600 max (no heavy bold)
- [ ] Stat numbers are accent-coloured
- [ ] Generous whitespace on every slide
- [ ] Body text is readable (18-20px, good contrast)

### Run `polish` for final refinement:

```
Skill("polish", "Final quality pass on BIP slides. Check: alignment, spacing, font consistency, colour accuracy, image quality.")
```

---

## STEP 7 — EXPORT TO PDF

```bash
cd output/bip-work
node export-pdf.js bip.html "[client-name]-bip-v1.pdf"
```

### Puppeteer Export Script

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
    path: path.join(__dirname, '..', process.argv[3] || 'bip.pdf'),
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

## STEP 8 — DELIVER

Present the user with:
1. **Preview screenshot** of the cover slide
2. **PDF file path**
3. **Logo status** — confirm both dark and light versions render correctly
4. **Content source** — confirm all content came from their document
5. **Slide summary** — confirm all 9 slides are present

---

## SLIDE STRUCTURE (9 slides, alternating dark/light)

### Slide 1: Cover (DARK) — Split Layout

**Layout:** Two-panel split — text left (58%), image right (42%). Image bleeds to the right edge with `border-radius: 24px 0 0 24px`. Logo top-left in the text area. Massive headline (80-92px, weight 600). Accent-coloured keyword. Tagline below (22-28px, muted). Thin accent divider. Website URL bottom-left.

**IMPORTANT: This split layout (text left, full-bleed image right) is the signature BIP pattern. Use it for Cover, Partners/Trust, and Contact slides.**

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

**Layout:** Warm cream background. Large headline. Intro sentence. 2-3 testimonial quotes — large italic text with attribution. Use real quotes only. Logo bottom-right.

### Slide 8: Partners / Trust (DARK) — Split Layout

**Layout:** Split layout (same as Cover) — text left (55%), image right (45%) bleeding to edge. Heading + description on left. Image fills right with `border-radius: 24px 0 0 24px`. City names listed below text with accent dot separators. Logo bottom-right in text area.

**NO padding on right side** — image must touch the right edge of the slide.

### Slide 9: Contact (LIGHT) — Split Layout

**Layout:** Light/cream background. Split layout — text left (58%), full-bleed image right (42%). Logo top-left (dark version for light bg). Large CTA headline. Subtitle. Thin accent divider. Contact details (website, email, phone) in a horizontal row. CTA line at bottom in accent. Image bleeds to right edge.

**This mirrors the Cover slide but inverted — light bg instead of dark, dark logo instead of light.**

---

## COMMON ISSUES & FIXES

### Logo Issues

| Problem | Fix |
|---------|-----|
| Logo invisible on dark slide | Use white version or `filter: brightness(0) invert(1)` |
| Logo invisible on light slide | Use dark version or `filter: brightness(0)` |
| SVG renders blank | Download PNG instead, or use text fallback |
| Logo renders HUGE / distorted | ALWAYS set `height`, `width:auto`, AND `max-width` on logo `<img>` tags. CSS class alone is not enough — use inline `style="height:50px; width:auto; max-width:200px;"` |

### Image Issues

| Problem | Fix |
|---------|-----|
| FLUX generation failed | Use Unsplash stock images matching industry |
| Image too dark on dark slide | Add lighter overlay gradient |
| Image missing | Add `.no-image` class for CSS gradient fallback |
| Image floats with gap beside text | Use split layout: `display:flex; align-items:stretch; padding:0;` on the slide, text in a padded flex child, image in a `width:42-45%` div with `height:100%; object-fit:cover;` |

### Layout Issues

| Problem | Fix |
|---------|-----|
| Text and image not aligned side by side | Use `display:flex; align-items:stretch;` on the slide div. Remove `padding:0` from the slide, put padding only on the text side. Image div gets `width:42-45%` with image at `100%` width and height |
| Content overflows slide bottom | Reduce heading size or remove `justify-content:center` — let content flow naturally from top |
| Blank space on slides | Slides are 1080px fixed height — if content is short, use `justify-content:center` on the padded content div to vertically centre it |

### Font Issues

| Problem | Fix |
|---------|-----|
| Client font not on Google Fonts | Fall back to Poppins |
| Font looks too heavy | Ensure max weight is 600, never 700+ |
| Font sizes too small for 1920px slides | Minimum sizes: headlines 56-92px, subheads 26-34px, body 20-24px, labels 14-16px. The slide is 1920px wide — desktop web sizes will look tiny |

### Split Layout Pattern (Cover, Partners, Contact)

The signature BIP layout for slides with images:
```css
/* Slide container */
.slide { display: flex; align-items: stretch; padding: 0; }

/* Text side */
.slide .text { flex: 1; padding: 80px 60px 80px 100px; display: flex; flex-direction: column; justify-content: center; }

/* Image side — bleeds to edge */
.slide .image { width: 42%; }
.slide .image img { width: 100%; height: 100%; object-fit: cover; border-radius: 24px 0 0 24px; }
```

---

## COMPLIANCE RULES

- **Step 0 brand extraction is mandatory** — never skip it
- **BIP uses CLIENT branding** — not Automate Accelerator
- **Font weight 600 max** — no bold (700+) fonts
- **Ask user 3 questions before starting** (brand guide, content doc, images)
- Run `brand-guide-extractor` before extracting brand manually
- Run `copywriting` for slide content
- Run `taste-frontend` after HTML draft
- Run `polish` after screenshots
- ONLY include the 9 slides defined
- ALWAYS follow the slide order
- NEVER invent metrics, testimonials, phone numbers, or emails
- Use placeholders for missing data
- ALWAYS alternate dark/light slide backgrounds
- ALWAYS use Poppins as fallback font
- Output MUST be PDF in 16:9 landscape (1920x1080px)

---

*BIP Skill | v4.0 | Modern Editorial Design, Client-Branded, Skill-Integrated, Poppins Typography*
