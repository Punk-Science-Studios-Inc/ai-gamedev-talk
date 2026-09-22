# AGENTS.md

Project-specific context for AI coding agents operating in this repository.

## Project overview

Slide deck and companion artifacts for "ai + gamedev" — a talk by Darryl Wright (Punk Science Studios Inc) on building games with AI tools. The repo holds a static offline slide deck and the subagents/skills the talk installs. The thesis: AI does not one-shot a game; it accelerates a discipline.

## Stack

| Layer | Technology |
|-------|-----------|
| Deck | Vanilla HTML/CSS/JS — `deck/index.html`, `deck.css`, `deck.js`. No framework, no build step, no package.json |
| Skill scripts | Python (sdf-modelling, model-view-builder), bash, JS (mesh loader) |
| Slide renderer | Playwright via `deck/tools/shoot.mjs` — borrowed from a sibling project, see Commands |
| Packaging | None. The deck is opened directly in a browser |
| Distribution | `install.sh` / `install.ps1` copy `agents/` and `skills/` into `~/.agents` and `~/.claude` |
| Licence | MIT (Bossa Games logo excepted) |

## Commands

- **View the deck:** open `deck/index.html` in a browser. Works fully offline — no server needed
- **Render every slide to PNG:** `node deck/tools/shoot.mjs` (output: `deck/renders/`). Use `--frags` to include fragment/build states
  - Requires Playwright: borrows `C:/Users/darry/projects/oneill/node_modules/playwright` unless `PW_DIR` is set; Chromium path unless `CHROME` is set
- **Install agents and skills:** `./install.sh` (bash) or `./install.ps1` (PowerShell). Optional target dirs as arguments; default `~/.agents` and `~/.claude`

## Project structure

- `deck/` — the slides. `index.html` (all slide content), `deck.css`, `deck.js`
  - `assets/` — fonts, images, QR codes, `demos/gravity-drive.html` (live demo embedded in a slide)
  - `deck-docs/` — `art-bible.md` (deck art direction, enforced constraints), `research.md` (sources for every number on the slides, dated)
  - `tools/` — `shoot.mjs` slide screenshot tool
- `agents/` — subagent definitions: `art.md` (art director), `unity-engineer.md` (Unity systems engineer)
- `skills/` — eight SKILL.md skills referenced by the talk, each a directory with `SKILL.md` plus optional `references/` and `scripts/`

## Conventions

- **Offline is a hard constraint:** all deck assets are local files — no CDNs, no external fetches at view time
- **README install section is written in ASD-STE100 Simplified Technical English** so agents can follow it without a human — preserve that register when editing
- **Line endings:** `.gitattributes` forces LF for text (`*.sh`, `*.ps1` explicitly), binary treatment for PNG/WOFF2
- **Installer contract:** installers write only this repo's entries into target dirs, replacing whole skill directories; they never delete anything not owned by this repo — keep that guarantee intact when modifying
- **Slides are data in HTML:** slide content lives directly in `deck/index.html`; build-step fragments use CSS classes managed by `deck.js`

## Documentation

- `README.md` — repo overview, deck controls, install/update/delete procedures
- `deck/deck-docs/art-bible.md` — art direction the deck must obey
- `deck/deck-docs/research.md` — citations backing claims on slides

## Notes

- After editing a skill or agent, remember installed copies elsewhere (e.g. `~/.agents`, `~/.claude`) go stale — rerunning the installer refreshes them
- Live version of the embedded demo: https://punkscience.ca/gravity-drive/
- Deck keyboard nav supports presentation clickers (Page Down/Page Up); check `deck.js` after touching navigation code
