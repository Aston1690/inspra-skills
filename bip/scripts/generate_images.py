#!/usr/bin/env python3
"""
BIP Image Generator — Generates supporting visuals for Business Information Pack slides
using FLUX 2 Pro via OpenRouter API.

Usage:
    python generate_images.py \
        --company "Acme Corp" \
        --industry "SaaS / Project Management" \
        --accent-color "#FF6B35" \
        --bg-color "#0A1628" \
        --tone "modern, bold, tech" \
        --output-dir ./output/bip-work/images

Each image is saved as a PNG file named by slide purpose (e.g., cover_bg.png, about_panel_1.png).
Outputs a JSON manifest (image_manifest.json) mapping slide roles to file paths.
"""

import argparse
import base64
import json
import os
import sys
import time
import requests
from pathlib import Path


def load_api_key():
    """Load OpenRouter API key from environment or .env file."""
    key = os.environ.get("FLUX_API_KEY")
    if key:
        return key

    # Walk up from script location to find .env
    search_dir = Path(__file__).resolve().parent
    for _ in range(5):
        env_file = search_dir / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("FLUX_API_KEY="):
                    return line.split("=", 1)[1].strip()
        search_dir = search_dir.parent

    print("ERROR: FLUX_API_KEY not found in environment or .env file", file=sys.stderr)
    sys.exit(1)


def generate_image(api_key: str, prompt: str, retries: int = 2):
    """Call OpenRouter FLUX API and return base64 image data URL, or None on failure."""
    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "model": "black-forest-labs/flux.2-pro",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "modalities": ["image"]
                }),
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()

            if result.get("choices"):
                message = result["choices"][0]["message"]
                if message.get("images"):
                    return message["images"][0]["image_url"]["url"]

            print(f"  Warning: No image in response (attempt {attempt + 1})", file=sys.stderr)

        except requests.exceptions.RequestException as e:
            print(f"  Request error (attempt {attempt + 1}): {e}", file=sys.stderr)

        if attempt < retries:
            time.sleep(3)

    return None


def save_image(data_url: str, filepath: Path) -> bool:
    """Save a base64 data URL to a file. Returns True on success."""
    try:
        # data:image/png;base64,... or data:image/jpeg;base64,...
        if "," in data_url:
            b64_data = data_url.split(",", 1)[1]
        else:
            b64_data = data_url

        img_bytes = base64.b64decode(b64_data)
        filepath.write_bytes(img_bytes)
        return True
    except Exception as e:
        print(f"  Error saving {filepath}: {e}", file=sys.stderr)
        return False


def build_prompts(company: str, industry: str, accent_color: str, bg_color: str, tone: str) -> dict:
    """
    Build image generation prompts for each BIP slide that needs a visual.
    Returns dict mapping image_key -> prompt string.
    """
    tone_desc = tone if tone else "professional, modern, clean"
    base_style = (
        f"Professional corporate photography style, {tone_desc} aesthetic, "
        f"high quality, 16:9 aspect ratio, suitable for a dark-themed business presentation. "
        f"Color palette hints: accent color {accent_color}, dark background {bg_color}. "
        f"No text, no logos, no watermarks."
    )

    return {
        # Slide 1: Cover — abstract branded background
        "cover_bg": (
            f"Abstract geometric background for a {industry} company called {company}. "
            f"Dark moody atmosphere with subtle glowing accent lines in {accent_color}. "
            f"Flowing gradients, depth, light particles. Cinematic, premium feel. "
            f"{base_style}"
        ),

        # Slide 2: About — 3 photo panels
        "about_panel_1": (
            f"Professional team collaboration in a modern office environment for a {industry} company. "
            f"People working together at a table with laptops, natural lighting, warm atmosphere. "
            f"{base_style}"
        ),
        "about_panel_2": (
            f"Modern workspace interior, clean desk setup with monitors, plants, "
            f"natural light streaming in, representing a {industry} company culture. "
            f"{base_style}"
        ),
        "about_panel_3": (
            f"Close-up of hands working on a laptop or digital device in a professional setting, "
            f"representing {industry} innovation and craftsmanship. Shallow depth of field. "
            f"{base_style}"
        ),

        # Slide 3: Services — product/service visual
        "services_visual": (
            f"Visual representation of {industry} services and solutions. "
            f"Abstract technology or service delivery concept, showing connected elements, "
            f"digital interface elements, professional and aspirational. "
            f"{base_style}"
        ),

        # Slide 4: Why Choose Us — subtle accent visual
        "why_choose_us_bg": (
            f"Abstract minimal background with subtle geometric patterns and soft light. "
            f"Dark theme with hints of {accent_color}. Conveys trust, reliability, expertise. "
            f"Very subtle, not distracting — meant to sit behind text. "
            f"{base_style}"
        ),

        # Slide 5: How We Help — benefits visual
        "benefits_visual": (
            f"Visual metaphor for business growth and positive outcomes in {industry}. "
            f"Upward trajectory, expanding networks, or flourishing results. "
            f"Abstract or semi-realistic, optimistic mood. "
            f"{base_style}"
        ),

        # Slide 6: Who We Are — team/culture image
        "team_culture": (
            f"Diverse professional team in a modern setting for a {industry} company. "
            f"Group photo style but candid, showing genuine engagement and company culture. "
            f"Warm lighting, professional but approachable atmosphere. "
            f"{base_style}"
        ),

        # Slide 7: Testimonials — subtle background
        "testimonials_bg": (
            f"Soft abstract background suggesting trust and social proof. "
            f"Gentle gradient with subtle bokeh or light dots, dark theme with {accent_color} hints. "
            f"Very muted and non-distracting — will have testimonial cards overlaid on top. "
            f"{base_style}"
        ),

        # Slide 8: Partners — trust visual
        "partners_visual": (
            f"Abstract visual representing partnerships, connections, and trust in {industry}. "
            f"Interconnected nodes, handshake concept, or network visualization. "
            f"Professional, conveying reliability and established relationships. "
            f"{base_style}"
        ),

        # Slide 9: Contact — clean closing visual
        "contact_bg": (
            f"Clean minimal abstract background for a contact/closing slide. "
            f"Dark theme with a subtle warm glow or gradient in {accent_color}. "
            f"Inviting, open feeling. Very minimal — mostly dark with accent lighting. "
            f"{base_style}"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate BIP supporting visuals via FLUX")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--industry", required=True, help="Industry or sector description")
    parser.add_argument("--accent-color", required=True, help="Brand accent color (hex)")
    parser.add_argument("--bg-color", default="#0A1628", help="Background color (hex)")
    parser.add_argument("--tone", default="modern, professional, clean", help="Visual tone descriptors")
    parser.add_argument("--output-dir", required=True, help="Directory to save images")
    parser.add_argument("--slides", default="all", help="Comma-separated image keys to generate, or 'all'")
    args = parser.parse_args()

    api_key = load_api_key()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompts = build_prompts(
        company=args.company,
        industry=args.industry,
        accent_color=args.accent_color,
        bg_color=args.bg_color,
        tone=args.tone,
    )

    # Filter to requested slides
    if args.slides != "all":
        requested = [s.strip() for s in args.slides.split(",")]
        prompts = {k: v for k, v in prompts.items() if k in requested}

    manifest = {}
    total = len(prompts)

    print(f"Generating {total} images for {args.company} BIP...")
    print(f"Output directory: {output_dir}")
    print()

    for i, (key, prompt) in enumerate(prompts.items(), 1):
        print(f"[{i}/{total}] Generating: {key}")
        data_url = generate_image(api_key, prompt)

        if data_url:
            # Determine extension from data URL
            ext = "png"
            if "image/jpeg" in data_url[:30]:
                ext = "jpeg"
            elif "image/webp" in data_url[:30]:
                ext = "webp"

            filepath = output_dir / f"{key}.{ext}"
            if save_image(data_url, filepath):
                manifest[key] = str(filepath)
                print(f"  Saved: {filepath}")
            else:
                manifest[key] = None
                print(f"  FAILED to save: {key}")
        else:
            manifest[key] = None
            print(f"  FAILED to generate: {key}")

        print()

    # Write manifest
    manifest_path = output_dir / "image_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest written to: {manifest_path}")

    # Summary
    success = sum(1 for v in manifest.values() if v is not None)
    print(f"\nDone: {success}/{total} images generated successfully.")

    if success < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
