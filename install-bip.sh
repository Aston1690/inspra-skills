#!/bin/bash
# BIP Skill Installer
# Usage: curl -sL https://raw.githubusercontent.com/Aston1690/inspra-skills/main/install-bip.sh | bash

set -e

SKILLS_DIR="$HOME/.claude/skills"
REPO="https://raw.githubusercontent.com/Aston1690/inspra-skills/main"

echo "Installing BIP skill..."
mkdir -p "$SKILLS_DIR/bip/scripts"
curl -sL "$REPO/bip/SKILL.md" -o "$SKILLS_DIR/bip/SKILL.md"
curl -sL "$REPO/bip/scripts/generate_images.py" -o "$SKILLS_DIR/bip/scripts/generate_images.py"

echo ""
echo "BIP skill installed! Use /bip in Claude Code."
