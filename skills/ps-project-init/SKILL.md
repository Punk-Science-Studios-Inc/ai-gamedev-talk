---
name: ps-project-init
description: >
  Initialize a project workspace — scan the codebase for existing setup and documentation,
  generate a project-specific AGENTS.md, create a CLAUDE.md pointer, init a git repo if none
  exists, and make the initial commit. Use when the user says "Initialize this workspace",
  "Init this repo", "Let's start a project", "Set up this project", "Bootstrap the repo",
  "Project init", or any similar request to turn a loose directory into a properly documented
  project with agent context.
---

# PS-Project-Init — scan → document → initialize

Take any project directory and turn it into a well-documented agent-ready workspace in four
steps: **scan** what's here, **write** AGENTS.md + CLAUDE.md, **git init** if needed, and
**commit**.

## The rule

**One question at a time when asking the user.** Only ask when you genuinely can't determine
something from the scan. Never batch questions. Reflect each answer back before moving on.

**Never guess.** If a scan can't determine something (project purpose, stack version), flag it
as `[UNKNOWN]` in AGENTS.md and move on — don't invent an answer.

## Phase 1 — Scan

Inventory the project root and one level deep. Look for:

### Identity
- `README.md`, `README`, `readme.md` — project name, description, badges
- `package.json` → `name`, `description`, `keywords`
- `go.mod` → module path
- `Cargo.toml` → `[package]` name, description
- `pyproject.toml` / `setup.py` / `setup.cfg` → project metadata
- `Makefile`, `Taskfile.yml`, `justfile` — named targets that describe what the project does
- `docker-compose.yml`, `Dockerfile` — service names, exposed ports
- `.github/`, `.gitlab-ci.yml`, `Jenkinsfile` — CI pipeline descriptions
- `docs/`, `documentation/` — any architecture or design docs
- `CONTRIBUTING.md`, `ARCHITECTURE.md`, `DESIGN.md`

### Stack detection
- Language-specific files: `*.go`, `*.rs`, `*.py`, `*.ts`, `*.js`, `*.tsx`, `*.jsx`, `*.cs`, `*.csproj`, `*.sln`
- Package managers: lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `go.sum`, `Cargo.lock`, `poetry.lock`, `Pipfile.lock`)
- Frameworks: look for imports/dependencies in package manifests, `next.config.*`, `svelte.config.*`, `nuxt.config.*`, `astro.config.*`
- Testing: `*_test.go`, `*.test.*`, `__tests__/`, `*.spec.*`, `tests/`, `pytest.ini`, `jest.config.*`, `vitest.config.*`
- Linting/formatting: `.eslintrc*`, `.prettierrc*`, `.golangci.yml`, `pyproject.toml` tool configs, `.editorconfig`
- Build: `Makefile`, `build/`, `dist/`, `out/`, `target/`, build scripts

### Git state
- Is `.git/` present? If not, we'll init one.
- If `.git/` exists: current branch, remote(s), commit count, any uncommitted changes (`git status --porcelain`).
- `.gitignore` — does one exist? If the stack is detected, ensure it covers the obvious (node_modules, target/, dist/, .env, etc.).

### Existing agent context
- Already have `AGENTS.md` or `CLAUDE.md`? Note their contents; don't overwrite blindly.
- `CODEBUDDY.md`, `CURSOR.md` — if present, inform the user these exist and offer to fold their material into the new AGENTS.md.

### Structure
- Top-level directories and their apparent purpose (inferred from names and contents).
- Monorepo? Multiple language artifacts in subdirectories.

## Phase 2 — Write AGENTS.md

Write `AGENTS.md` to the project root. It should be a concise reference for any AI coding
agent operating in this project. Follow this structure:

```markdown
# AGENTS.md

Project-specific context for AI coding agents operating in this repository.

## Project overview

[1-3 sentences: what this project is, who it's for, the primary problem it solves.
Pull from README, package.json description, or module path. If unknown, say so.]

## Stack

| Layer | Technology |
|-------|-----------|
| Language | [language + version if detectable] |
| Runtime   | [Node, Go, Python, etc. — version if in .tool-versions, .nvmrc, go.mod go line, etc.] |
| Framework | [Next.js, SvelteKit, etc. — if detected] |
| Package manager | [npm, yarn, pnpm, go modules, cargo, pip, poetry] |
| Testing | [framework + run command if found] |
| Linting/formatting | [tools + config files found] |
| Build | [commands or tools] |
| Database | [if detected from connection strings, ORM configs, docker-compose services] |

## Commands

[Synthesize the key commands an agent might need:]

- **Install dependencies:** `[command]`
- **Run tests:** `[command]`
- **Lint:** `[command]`
- **Format:** `[command]`
- **Build:** `[command]`
- **Run dev server:** `[command]`

[For each, pull from package.json scripts, Makefile targets, or convention. If a command
isn't found, omit that line rather than guessing.]

## Project structure

[Bullet list of top-level directories with one-line descriptions inferred from their
names and contents. Example:]

- `src/` — application source
- `tests/` — test suite
- `docs/` — architecture and design docs
- `scripts/` — build and utility scripts

## Conventions

[Capture anything discernible from the codebase:]

- **Code style:** [if a formatter/linter config is found, note it]
- **Module layout:** [how code is organized — by feature? by layer? flat?]
- **Naming:** [any obvious patterns — PascalCase files, snake_case, etc.]
- **Git workflow:** [if CONTRIBUTING.md or CI config describes a branch strategy]

## Documentation

- [Link to README.md if it exists]
- [Link to any other key docs found during scan]

## Notes

[Anything else the scan surfaced that an agent should know. [UNKNOWN] markers
for things that couldn't be determined.]
```

Adapt the sections to what was actually found. If a section would be empty, omit it.
The file should be informative but not padded — every line should tell an agent something
it can't learn from reading the code itself.

## Phase 3 — Write CLAUDE.md

Create `CLAUDE.md` in the project root. It should be a minimal pointer:

```markdown
# CLAUDE.md

See [AGENTS.md](AGENTS.md) for project context and instructions for AI coding agents.
```

If `CLAUDE.md` already exists, check its contents. If it already points to `AGENTS.md`,
leave it alone. If it contains substantive project instructions, ask the user whether to
merge them into AGENTS.md or leave CLAUDE.md as-is.

## Phase 4 — Git init (if needed)

If no `.git/` directory exists:

1. Run `git init`.
2. If a `.gitignore` doesn't exist, create one covering the detected stack's standard
   ignores plus universal ones (`.env`, `.DS_Store`, IDE directories). Use the stack's
   canonical gitignore patterns — don't invent them.
3. If a `.gitignore` already exists, review it against the detected stack and note any
   obvious gaps (don't edit without asking).

If `.git/` already exists:
- Report current branch, remote(s), and whether there are uncommitted changes.
- If there are uncommitted changes, ask whether to include them in the init commit or
  only commit the new AGENTS.md + CLAUDE.md.

### Rename master to main

After git init (or when operating in an existing repo), if the current branch is named
`master`, rename it to `main`:

```bash
git branch -m master main
```

This must happen before the initial commit so the commit lands on `main`.

## Phase 5 — Initial commit

Stage and commit:

```bash
git add AGENTS.md CLAUDE.md .gitignore   # .gitignore only if we created it
git commit -m "chore: initialize project with AGENTS.md and CLAUDE.md"
```

If the repo was already initialized and had uncommitted work, the commit message should
reflect that context:

```bash
git commit -m "chore: add AGENTS.md and CLAUDE.md for agent context"
```

Do not `git push` — that's the user's call.

## Phase 6 — Report

Summarize what was done in a compact table:

| Step | Result |
|------|--------|
| Scan | Found [stack], [N] source files, [N] test files |
| AGENTS.md | Created with [sections populated] |
| CLAUDE.md | Created, points to AGENTS.md |
| Git | [Initialized new repo / Repo already existed on branch X] |
| Commit | `[commit hash]` — [files committed] |

## Edge cases

- **Empty directory**: AGENTS.md gets minimal content with `[UNKNOWN]` markers; ask the
  user one question about what the project will be.
- **AGENTS.md already exists**: Don't overwrite. Offer to update it with new findings
  from the scan. Show a diff of proposed changes and ask before applying.
- **No detected language/stack**: Note it in AGENTS.md. The file is still useful for
  documentation pointers and structure. Ask the user one question about the stack.
- **Existing git with dirty working tree**: List the dirty files, ask whether to include
  them in the commit or only commit the new files.
- **Monorepo / multiple stacks**: Detect each sub-project, note all stacks in the table,
  describe the monorepo structure in the project structure section.
- **Branch already named `main`**: Skip the rename — nothing to do.