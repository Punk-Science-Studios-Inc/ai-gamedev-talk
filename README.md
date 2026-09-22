# ai + gamedev

A talk by Darryl Wright (Punk Science Studios Inc, Halifax, Nova Scotia) on building games with AI tools: how to start, and how not to. This repository holds the slide deck and the agents and skills the talk refers to.

The thesis: AI does not one-shot a game. It accelerates a discipline.

```
deck/       the slides. a static site. open deck/index.html in a browser. works offline.
agents/     two subagents: art (an art director) and unity-engineer (a Unity systems engineer)
skills/     eight SKILL.md skills: planning, research, 3D, web games, Linux verification
install.sh  copies agents/ and skills/ into ~/.agents and ~/.claude
install.ps1 the same, for PowerShell
```

## The deck

Open `deck/index.html`. You do not need a server. Fonts, images and QR codes are local files.

| Key | Action |
|---|---|
| Right arrow, Page Down, Space, Enter | next build step, then next slide |
| Left arrow, Page Up, Backspace | previous |
| Home, End | first slide, last slide |
| F or F5 | fullscreen |
| B or period | black screen |
| O | overview. Click a slide to jump to it. |
| Escape | leave overview or black screen |

A Microsoft presentation clicker sends Page Down and Page Up. Both work.

The gravity drive slide shows screenshots of the demo. The live version, playable in the browser, is at https://punkscience.ca/gravity-drive/.

The art direction for the deck is in `deck/deck-docs/art-bible.md`. The `art` agent in this repository wrote it. Sources for every number on the slides are in `deck/deck-docs/research.md`, dated 2026-09-20.

## Install the agents and skills

These instructions use ASD-STE100 Simplified Technical English. An agent can follow them without a human.

### Requirements

1. You have Git.
2. You have a harness that reads `SKILL.md` files. Claude Code, Codex CLI, OpenCode and Pi read them.
3. Your harness reads skills from `~/.claude/skills` or `~/.agents/skills`. If it reads a different directory, give that directory to the installer.

### Procedure

1. Clone this repository.

   ```
   git clone https://github.com/Punk-Science-Studios-Inc/ai-gamedev-talk.git
   ```

2. Go into the repository.

   ```
   cd ai-gamedev-talk
   ```

3. Run the installer for your shell. Run only one.

   ```
   ./install.sh
   ```

   ```
   ./install.ps1
   ```

4. Read the output. The installer prints one line for each target directory. The default targets are `~/.agents` and `~/.claude`.

5. Start a new session in your harness. The harness reads skills at the start of a session.

### Install into a different directory

Give each target directory as an argument.

```
./install.sh ~/.config/opencode
```

```
./install.ps1 -Target ~/.config/opencode
```

### Install for more than one agent

Each agent reads its own harness directory. Run the installer one time for each directory. The installer writes only the files in this repository. It does not delete other files in the target.

Example. Two harnesses on one machine:

```
./install.sh ~/.claude ~/.config/opencode
```

### Update

1. Pull the repository.

   ```
   git pull
   ```

2. Run the installer again. The installer replaces each agent and each skill with the new copy.

### Delete

Delete the installed files. The installer does not have a delete command.

```
rm -rf ~/.claude/skills/{ps-project-init,ps-brainstorm,sdf-modelling,model-view-builder,js-game-pro,wsl-linux-verify,storm-research,research-multi-perspective}
rm -f  ~/.claude/agents/{art,unity-engineer}.md
```

Do the same for `~/.agents`.

## Agents

| Agent | What it does |
|---|---|
| `art` | A senior art director. Takes a stated vision and constrains it into an enforceable art bible: colour, value, shape, light, type, composition, material, motion. The bible opens with a Direction Contract, a YAML block other agents parse. |
| `unity-engineer` | Frame, a senior Unity systems and gameplay engineer. Surveys an existing Unity codebase, plans and implements features, and debugs runtime problems against the project's coding standard. |

## Skills

| Skill | Use it when |
|---|---|
| `ps-project-init` | You start a project. It scans the folder, writes `AGENTS.md` and a `CLAUDE.md` pointer, inits git, and makes the first commit. |
| `ps-brainstorm` | You have a raw idea. It pressure-tests the idea and produces an execution plan when you have answered every open question. |
| `sdf-modelling` | You must build organic 3D geometry from reference images as a signed-distance field, then mesh it and finish it in Blender. |
| `model-view-builder` | You must ship an offline-built mesh as a self-contained WebGL viewer whose shading matches the offline render. |
| `js-game-pro` | You build or debug a browser or hybrid-native game in Phaser, three.js, PixiJS, Babylon.js or Excalibur. |
| `wsl-linux-verify` | You develop on Windows and the target is Linux. It runs the tests in WSL and baselines pre-existing failures. |
| `storm-research` | You need a cited, verification-first research article rather than an overview. |
| `research-multi-perspective` | You need one topic analysed by five voices: practitioner, skeptic, economist, historian, academic. |

## Skills the talk links to, but does not copy

These are public upstream. Install them from their own repositories.

- Grill Me and other engineering skills: https://github.com/mattpocock/skills
- Brainstorm and the `uw-*` Unity workflow: https://github.com/devdavv/unity-ai-workflow
- Game studio design skills: https://github.com/donchitos/claude-code-game-studios
- ASD-STE100 Simplified Technical English: https://github.com/danyuchn/asd-ste100-skill
- APT, Chocolatey and wiki skills: https://github.com/punkscience/agent-skills
- The official skill set: https://github.com/anthropics/skills

## Licence

MIT. See `LICENSE`. The Bossa Games logo on the title slide belongs to Bossa Games and is not covered.
