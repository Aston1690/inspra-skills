#!/bin/bash
# Case Study Skill Installer
# Usage: curl -sL https://raw.githubusercontent.com/Aston1690/inspra-skills/main/install-case-study.sh | bash

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO="https://raw.githubusercontent.com/Aston1690/inspra-skills/main"

echo "Installing Case Study skill..."
mkdir -p "$SKILLS_DIR/case-study/scripts" "$SKILLS_DIR/case-study/templates"
curl -sL "$REPO/case-study/SKILL.md" -o "$SKILLS_DIR/case-study/SKILL.md"
curl -sL "$REPO/case-study/scripts/export-pdf.js" -o "$SKILLS_DIR/case-study/scripts/export-pdf.js"
curl -sL "$REPO/case-study/scripts/package.json" -o "$SKILLS_DIR/case-study/scripts/package.json"
curl -sL "$REPO/case-study/templates/case-study-template.html" -o "$SKILLS_DIR/case-study/templates/case-study-template.html"

echo ""
echo "Case Study skill installed! Use /case-study in Claude Code."
