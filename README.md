# Inspra Skills

Claude Code skills for generating premium business documents.

## Install

**Case Study only:**
```bash
curl -sL https://raw.githubusercontent.com/Aston1690/inspra-skills/main/install-case-study.sh | bash
```

**BIP only:**
```bash
curl -sL https://raw.githubusercontent.com/Aston1690/inspra-skills/main/install-bip.sh | bash
```

**Both:**
```bash
curl -sL https://raw.githubusercontent.com/Aston1690/inspra-skills/main/install.sh | bash
```

Skills install to `~/.claude/skills/`.

## Skills

### `/case-study` - Case Study Generator

Generates editorial-style case study web pages with PDF export. Always branded as Automate Accelerator showcasing the client engagement.

**Features:**
- Editorial magazine-style design (not card-based templates)
- Poppins typography, weight 600 max
- Alternating dark/light sections
- Full-bleed images
- Puppeteer PDF export

**Usage:** Type `/case-study` in Claude Code, provide a website URL and content document.

### `/bip` - Business Information Pack

Generates 9-slide 16:9 landscape PDF presentation decks. Always branded with the client's own brand colours and identity.

**Features:**
- 9 slides alternating dark/light
- Client brand extraction via Firecrawl
- Split layout pattern (text left, full-bleed image right)
- Poppins typography, weight 600 max
- FLUX AI image generation or Unsplash fallback
- Puppeteer PDF export at 1920x1080

**Usage:** Type `/bip` in Claude Code, provide a website URL and content document.

## Prerequisites

- Node.js 18+
- Claude Code CLI
- Firecrawl API key (set as `FIRECRAWL_API_KEY` in `.env`) for brand extraction

## Integrated Skills

Both skills use these Claude Code skills during execution:
- `brand-guide-extractor` - Client brand/logo extraction
- `copywriting` - Professional content writing
- `taste-frontend` - Design quality audit
- `polish` - Final refinement pass
