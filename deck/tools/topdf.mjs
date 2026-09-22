// Export the deck to presentation.pdf at the repository root.
// Renders every slide with all build steps (frags) revealed, then assembles a one-page-per-slide PDF.
// Prerequisites: playwright in node_modules (npm i --no-save playwright) and Python with img2pdf + pypdf.
// Usage: node deck/tools/topdf.mjs   (honours PW_DIR and CHROME, same as tools/shoot.mjs)
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const here = path.dirname(fileURLToPath(import.meta.url));
const deckDir = path.resolve(here, '..');
const root = path.resolve(deckDir, '..');
import fs from 'node:fs';
const slideCount = (fs.readFileSync(path.join(deckDir, 'index.html'), 'utf8').match(/<section\b/g) || []).length;

// 1) Render all slides, fragments on (final state of each build step)
execFileSync(process.execPath, [path.join(deckDir, 'tools', 'shoot.mjs'), path.join(deckDir, 'renders'), '--frags'], { stdio: 'inherit' });

// 2) Assemble the PDF
const py = process.platform === 'win32' ? 'python' : 'python3';
const script = [
  'import glob, json, os, sys',
  'from pypdf import PdfReader, PdfWriter',
  'import img2pdf',
  'outdir, pdf, slides = json.loads(sys.argv[1]), json.loads(sys.argv[2]), json.loads(sys.argv[3])',
  'files = sorted(glob.glob(os.path.join(outdir, "slide-*.png")))',
  'assert len(files) == slides, f"expected {slides} slides, got {len(files)}"',
  'layout = img2pdf.get_layout_fun((img2pdf.mm_to_pt(330.2), img2pdf.mm_to_pt(185.42)))',
  'with open(pdf, "wb") as fh:',
  '    fh.write(img2pdf.convert(files, layout_fun=layout))',
  'r = PdfReader(pdf)',
  'w = PdfWriter()',
  'w.append(r)',
  "w.add_metadata({'/Title': 'AI + Gamedev \\u2014 a talk by Darryl Wright, Punk Science Studios Inc',",
  "                '/Author': 'Darryl Wright',",
  "                '/Subject': 'Building games with AI tools: how to start, and how not to.'})",
  'with open(pdf, "wb") as fh:',
  '    w.write(fh)',
  'print(pdf, "-", len(r.pages), "pages")',
].join('\n');
execFileSync(py, ['-c', script, JSON.stringify(path.join(deckDir, 'renders')), JSON.stringify(path.join(root, 'presentation.pdf')), String(slideCount)], { stdio: 'inherit' });
