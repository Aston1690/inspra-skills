#!/bin/bash
# Inspra Skills Installer
# Usage: curl -sL https://raw.githubusercontent.com/Aston1690/inspra-skills/main/install.sh | bash

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO="https://raw.githubusercontent.com/Aston1690/inspra-skills/main"

echo "Installing Inspra Skills..."
echo ""

# Install Case Study skill
echo "  Installing case-study skill..."
mkdir -p "$SKILLS_DIR/case-study/scripts" "$SKILLS_DIR/case-study/templates"
curl -sL "$REPO/case-study/SKILL.md" -o "$SKILLS_DIR/case-study/SKILL.md"
curl -sL "$REPO/case-study/scripts/export-pdf.js" -o "$SKILLS_DIR/case-study/scripts/export-pdf.js"
curl -sL "$REPO/case-study/scripts/package.json" -o "$SKILLS_DIR/case-study/scripts/package.json"
curl -sL "$REPO/case-study/templates/case-study-template.html" -o "$SKILLS_DIR/case-study/templates/case-study-template.html"
echo "  Done."

# Install BIP skill
echo "  Installing bip skill..."
mkdir -p "$SKILLS_DIR/bip/scripts"
curl -sL "$REPO/bip/SKILL.md" -o "$SKILLS_DIR/bip/SKILL.md"
curl -sL "$REPO/bip/scripts/generate_images.py" -o "$SKILLS_DIR/bip/scripts/generate_images.py"
echo "  Done."

echo ""
echo "Inspra Skills installed successfully!"
echo ""
echo "Available skills:"
echo "  /case-study  - Generate premium case study PDFs (Automate Accelerator branded)"
echo "  /bip         - Generate 9-slide BIP presentation PDFs (client branded)"
echo ""
echo "Run these commands in Claude Code to use them."
