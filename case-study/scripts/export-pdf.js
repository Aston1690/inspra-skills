#!/usr/bin/env node
/**
 * Case Study PDF Exporter v2
 * Supports both fixed-page and scrolling editorial layouts.
 *
 * Usage: node export-pdf.js <input.html> <output.pdf> [--scroll]
 *
 * Modes:
 *   Default: A4 format with zero margins (for fixed-page designs)
 *   --scroll: Full-page capture matching the actual page height (for editorial/scrolling designs)
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const args = process.argv.slice(2);
const scrollMode = args.includes('--scroll');
const paths = args.filter(a => !a.startsWith('--'));
const [inputPath, outputPath] = paths;

if (!inputPath || !outputPath) {
  console.error('Usage: node export-pdf.js <input.html> <output.pdf> [--scroll]');
  process.exit(1);
}

const absInput = path.resolve(inputPath);
const absOutput = path.resolve(outputPath);

if (!fs.existsSync(absInput)) {
  console.error(`File not found: ${absInput}`);
  process.exit(1);
}

(async () => {
  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  console.log(`Loading ${absInput}...`);
  await page.goto(`file://${absInput}`, {
    waitUntil: 'networkidle0',
    timeout: 30000
  });

  // Wait for Google Fonts to load
  await page.evaluate(() => document.fonts.ready);

  // Wait for images to load
  await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('img'));
    await Promise.all(imgs.map(img => {
      if (img.complete) return Promise.resolve();
      return new Promise((resolve) => {
        img.onload = resolve;
        img.onerror = resolve;
        setTimeout(resolve, 5000);
      });
    }));
  });

  // Additional wait for fonts + rendering
  await new Promise(r => setTimeout(r, 2000));

  // Remove fixed nav for PDF (it overlaps content)
  await page.evaluate(() => {
    const nav = document.querySelector('.topnav');
    if (nav) nav.style.position = 'relative';
  });

  if (scrollMode) {
    // Scroll mode: capture full page height as one continuous PDF
    const bodyHeight = await page.evaluate(() => document.body.scrollHeight);
    console.log(`Scroll mode: page height = ${bodyHeight}px`);

    await page.pdf({
      path: absOutput,
      width: '1440px',
      height: `${bodyHeight}px`,
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
    });
  } else {
    // Default: A4 format
    await page.pdf({
      path: absOutput,
      format: 'A4',
      printBackground: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
      preferCSSPageSize: false
    });
  }

  await browser.close();

  const stats = fs.statSync(absOutput);
  const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);
  console.log(`Done! PDF saved (${sizeMB} MB): ${absOutput}`);
})().catch(err => {
  console.error('Export failed:', err.message);
  process.exit(1);
});
