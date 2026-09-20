# Art Bible — AI + Gamedev (2026 conference deck)

Punk Science Studios Inc · Darryl Wright · 45 min + 15 Q&A · 1920×1080 single-file HTML deck.

This document is binding. A build agent reads the Direction Contract below and never has to ask.
Prose after it explains the decisions; the contract is the machine surface.

---

## 0. Direction Contract

```yaml
direction_contract:
  version: 1
  project: "ai-gamedev-talk-deck"
  one_line: "A near-black clinical slide system where cream type and a single acid lime carry every meaning, and the lime only ever marks the thing a human still has to do."
  feeling: "unbothered"
  lineage: ["Swiss lecture slides / Müller-Brockmann grid", "terminal output", "Edward Gorey line work", "Mignola black-shape design"]
  never: ["a startup pitch deck", "a Nvidia/OpenAI keynote", "an AI-tool landing page with a purple gradient"]
  dial: expressive          # lime is a symbolic system (Storaro end), not motivated light
  sensibility:
    register: deadpan
    ground: dark
    edge: "the horse in the key illustration has no legs at all — the torso simply stops. Nobody draws attention to it. It is the argument."
    tone: "terse, lowercase, dry. no exclamation marks, no emoji, no first-person enthusiasm."
  pillars:
    - "Lime means a human decision or a human action. It is never decoration, never a highlight, never a bullet."
    - "Every piece of pasted-in media — terminal, markdown, QR, render, clip — is framed by the same 2px olive rule. One frame, one system."
    - "One idea per slide. If a slide needs a second heading, it is two slides."
  forbidden:
    - "gradients of any kind, including subtle ones"
    - "drop shadows, glows, blur, glassmorphism, rounded corners over 4px"
    - "syntax highlighting in more than two colours"
    - "stock AI imagery: brains, neural nets, circuit boards, glowing humanoid heads, robot hands touching human hands"
    - "PS Dark Olive #454E00 used as anything but the third dot of the brand mark — it is invisible on a weak projector"
    - "olive used as text at any size"
    - "icons or emoji in body copy; bullet glyphs other than the specified 8px lime square"
    - "more than one cream tile per slide"
    - "any transition other than the two defined in motion"
    - "restyling, recolouring or cropping the Bossa Games logo"
  palette:
    space: oklch            # reasoned in oklch, emitted as hex
    scheme: "achromatic warm neutral + one acid yellow-green signal; olive as structure only"
    hue_count: 3            # cream/greys (1 warm neutral), lime family (1 hue), red (1 hue, errors only)
    roles:
      ground:         { value: "#111111", on: null,      note: "PS Black. every slide." }
      plate:          { value: "#1A1A1A", on: ground,    note: "code/terminal plate, table zebra row" }
      surface:        { value: "#2D2D2D", on: ground,    note: "PS Charcoal. cards, callout boxes" }
      tile_light:     { value: "#F0EDE4", on: ground,    note: "PS Cream. QR tiles and light-source screenshots ONLY" }
      text_primary:   { value: "#F0EDE4", on: ground,    contrast: "16.14:1" }
      text_primary_on_surface: { value: "#F0EDE4", on: surface, contrast: "11.77:1" }
      text_on_light:  { value: "#1A1A1A", on: tile_light, contrast: "14.88:1" }
      text_secondary: { value: "#A8A49A", on: ground,    contrast: "7.59:1", note: "captions, sources, dates, footer" }
      text_secondary_on_surface: { value: "#A8A49A", on: surface, contrast: "5.53:1" }
      border:         { value: "#7A8800", on: ground,    contrast: "4.81:1", note: "PS Olive. the 2px media rule, diagram de-emphasis. NEVER text." }
      hairline:       { value: "#3A3A3A", on: ground,    contrast: "1.66:1", note: "decorative only. must never be load-bearing." }
      signal:         { value: "#C8DF00", on: ground,    contrast: "12.60:1", usage: "the one accent. marks a human decision, a human action, or the current position. nothing else." }
      signal_on_surface: { value: "#C8DF00", on: surface, contrast: "9.18:1" }
      danger:         { value: "#F26D6D", on: ground,    contrast: "6.46:1", note: "projector-hardened tint of PS Error #E04444 (4.57:1 fails our 7:1 floor). failure states, the failed monster render label." }
      mark_dot_1:     { value: "#C8DF00", on: ground }
      mark_dot_2:     { value: "#7A8800", on: ground }
      mark_dot_3:     { value: "#454E00", on: ground, note: "brand mark only. never functional." }
    ramps:
      grey:  ["#111111", "#1A1A1A", "#232323", "#2D2D2D", "#3A3A3A", "#4E4C48", "#6B6862", "#8B8780", "#A8A49A", "#F0EDE4"]
      lime:  ["#F2F7B8", "#E4EF7A", "#D6E73D", "#C8DF00", "#A8BB00", "#7A8800", "#5E6900", "#454E00"]
      lime_sanctioned: ["#C8DF00", "#7A8800", "#454E00"]
      lime_tints_note: "the other lime steps exist for HTML hover/active states in the deck's own nav chrome. they never appear on a projected slide."
    dark_mode: none
  contrast:
    projector: "assume a washed-out projector: measured ratios are treated as best case"
    body_min: 7.0
    caption_min: 7.0
    code_min: 7.0
    large_min: 4.5        # >= 48px
    nontext_min: 4.5      # rules, diagram strokes, table dividers
    pure_black_white: forbidden
    qr_exception: "QR modules #111111 on #F0EDE4 tile, 14.88:1 — the one place maximum contrast overrides the low-key rule"
  value:
    key: low
    range: "ground 0.6% relative luminance to cream 84.8%. no #000000, no #FFFFFF."
    cream_area_cap: "cream tiles occupy <= 50% of frame area, max one tile per slide"
  shape:
    bias: geometric
    ratio: "95/5 — the only organic form in the entire deck is the horse-and-rider illustration"
    corners: "0px default. 4px maximum, only on the cream QR/screenshot tile."
  type:
    families:
      display: { name: "Archivo Black", google: "Archivo+Black", weight: 400, fallback: "'Archivo Black', 'Arial Black', 'Helvetica Neue', Impact, sans-serif" }
      text:    { name: "Archivo", google: "Archivo:wght@400;500;600", weights: [400, 500, 600], fallback: "Archivo, 'Helvetica Neue', Arial, system-ui, sans-serif" }
      mono:    { name: "JetBrains Mono", google: "JetBrains+Mono:wght@400;700", weights: [400, 700], fallback: "'JetBrains Mono', 'Cascadia Mono', Consolas, 'DejaVu Sans Mono', monospace" }
    case: "all headings, titles and labels lowercase. sentence case in body. no ALL-CAPS anywhere."
    roles:
      section_title:  { family: display, weight: 400, size_px: 140, line_height: 1.00, tracking_em: -0.030, colour: text_primary }
      statement:      { family: display, weight: 400, size_px: 96,  line_height: 1.08, tracking_em: -0.025, colour: text_primary, measure_max_ch: 34 }
      slide_title:    { family: display, weight: 400, size_px: 76,  line_height: 1.05, tracking_em: -0.020, colour: text_primary }
      kicker:         { family: text,    weight: 600, size_px: 22,  line_height: 1.20, tracking_em:  0.140, colour: signal }
      lead:           { family: text,    weight: 500, size_px: 40,  line_height: 1.35, tracking_em: -0.005, colour: text_primary, measure_max_ch: 46 }
      body:           { family: text,    weight: 400, size_px: 34,  line_height: 1.45, tracking_em:  0.000, colour: text_primary, measure_max_ch: 54 }
      caption:        { family: text,    weight: 400, size_px: 26,  line_height: 1.40, tracking_em:  0.005, colour: text_secondary }
      code:           { family: mono,    weight: 400, size_px: 26,  line_height: 1.50, tracking_em:  0.000, colour: text_primary }
      code_emphasis:  { family: mono,    weight: 700, size_px: 26,  line_height: 1.50, colour: signal, note: "the one line being pointed at" }
      code_comment:   { family: mono,    weight: 400, size_px: 26,  line_height: 1.50, colour: text_secondary }
      table_header:   { family: text,    weight: 600, size_px: 24,  line_height: 1.30, tracking_em: 0.080, colour: text_secondary }
      table_cell:     { family: text,    weight: 400, size_px: 28,  line_height: 1.40, colour: text_primary }
      diagram_label:  { family: text,    weight: 500, size_px: 28,  line_height: 1.25, colour: text_primary }
      diagram_label_sm:{ family: text,   weight: 500, size_px: 22,  line_height: 1.25, colour: text_secondary }
      footer:         { family: text,    weight: 400, size_px: 20,  line_height: 1.00, tracking_em: 0.060, colour: text_secondary }
    min_projected_size_px: 22
  space:
    canvas: { w: 1920, h: 1080 }
    unit: 8
    scale: [8, 16, 24, 32, 48, 64, 96, 128, 192]
    margin_px: 96
    safe_area: { x: 96, y: 96, w: 1728, h: 888 }
    grid: { columns: 12, column_px: 122, gutter_px: 24, total_px: 1728 }
    vertical:
      title_rule_y: 96        # 6px x 96px lime rule, top-left of safe area
      title_baseline_y: 190
      content_top_y: 280
      footer_rule_y: 960      # 1px hairline, full safe width
      footer_baseline_y: 1000
    deviation: "the grid may be broken ONLY on: section divider (full bleed), statement slide (optically centred block), and the illustration slide (art bleeds past the right margin to x=1920). Nowhere else."
  treatments:
    screenshot_dark:
      rule: "no tile. image sits directly on ground."
      border: "2px solid #7A8800"
      padding_px: 0
      max_width_px: 1180
      caption: "below, 24px gap, caption role, flush left with image"
      note: "capture terminals in the PS palette where possible: bg #111111, fg #F0EDE4, accent #C8DF00."
    screenshot_light:
      rule: "image sits on a #F0EDE4 tile"
      tile_padding_px: 24
      border: "2px solid #7A8800"
      corner_radius_px: 4
      max_width_px: 1180
      max_frame_area_pct: 50
      limit: "one cream tile per slide"
    qr:
      module_colour: "#111111"
      tile_colour: "#F0EDE4"
      tile_px: 240
      min_tile_px: 200
      quiet_zone_modules: 4
      inner_padding_px: 20
      border: "2px solid #7A8800"
      corner_radius_px: 4
      label: "caption role, #A8A49A, centred under the tile, 16px gap, max 2 lines"
      forbidden: ["lime or coloured modules", "logo in the centre", "transparent background", "a QR smaller than 200px"]
    diagram:
      fill: "none, or #1A1A1A for a closed box"
      stroke_px: 4
      stroke_default: "#F0EDE4"
      stroke_deemphasis: "#7A8800"
      stroke_signal: "#C8DF00"
      stroke_linecap: butt
      dash_meaning: "a dashed 2px lime line means a boundary (e.g. the client/server boundary in the layered stack). solid means a thing."
      labels: diagram_label
      forbidden: ["arrowheads larger than 16px", "curved connectors", "gradient fills", "shadows", "more than 7 nodes on one diagram"]
    ring_diagram:
      geometry: "5 arc segments, r=300, stroke 28px, butt caps, 6deg gap between segments, centred in columns 4-9"
      segments: ["ideation", "preproduction", "production", "deployment", "live ops"]
      base_stroke: "#7A8800"
      overlay: "segments where AI compresses time are restroked #C8DF00 on build. segments where it does not stay olive."
      open_ring: "live ops segment is drawn with a 24deg gap at its end — the ring never closes. this gap is the whole point; do not tidy it."
      labels: "outside the ring, radial, diagram_label, never inside the stroke"
    stack_diagram:
      geometry: "5 stacked bars, 12 columns wide, 88px tall, 16px vertical gap"
      fill: "#1A1A1A"
      border: "2px solid #7A8800"
      label: "diagram_label, flush left, 32px inset"
      boundary: "the client boundary is a 2px dashed #C8DF00 line across the full bar width, label right-aligned in caption role"
    taxonomy_grid:
      geometry: "2x2 or 2x3, cells span 6 or 4 columns, 24px gutter, cell height 300px"
      fill: "#1A1A1A"
      border: "2px solid #7A8800"
      cell_title: "lead role, 32px inset from cell top-left"
      cell_body: "caption role"
      signal_use: "at most one cell carries a lime 6px top edge — the one the speaker is arguing for"
    table:
      borders: "no vertical rules. no per-row rules."
      header: "table_header role, 2px #C8DF00 rule beneath"
      zebra: "odd rows #111111, even rows #1A1A1A, full-bleed to column edges"
      foot: "2px #7A8800 rule closing the table"
      row_height_px: 64
      max_rows: 8
      max_cols: 6
      cell_padding_px: 24
      signal_use: "lime may mark exactly one cell or one column header — the recommendation"
    illustration:
      count: 1
      spec: "see section 9. inline SVG, cream line and silhouette on ground, lime confined to the harness."
    logos:
      ps_mark: "three-dot motif ● ● ● in #C8DF00 / #7A8800 / #454E00, dot dia 12px, gap 20px. appears on title slide, section dividers and closing slide only."
      ps_wordmark: "lowercase punk.science, text role 600 weight, cream"
      bossa: "title slide only. supplied asset, used as-is at its native aspect. no recolour, no crop, no lime, no olive frame. clear space = 1x logo height on all sides. sits on ground, right of the PS lockup, separated by a 1px #3A3A3A vertical hairline 64px tall."
  motion:
    allowed: 2
    transitions:
      slide_advance:
        type: "opacity cross-cut, incoming only"
        duration_ms: 120
        easing: "linear"
        note: "effectively a hard cut with one frame of grace. nothing translates, nothing scales."
      build_reveal:
        type: "opacity 0->1 plus translateY 16px->0"
        duration_ms: 180
        easing: "cubic-bezier(0.2, 0, 0, 1)"
        stagger_ms: 60
        max_steps: 5
        note: "for list items, ring-diagram overlays, table rows revealed one at a time"
    forbidden: ["slide push/slide/zoom/flip/cube", "parallax", "ken burns on any image", "looping ambient animation", "animated gradients", "any motion on the illustration", "autoplay video without a visible control"]
    reduced_motion: "prefers-reduced-motion: reduce -> both transitions become 0ms"
  budgets:
    colour: "3 hues total. 10 greys. no other colour may be introduced, including inside diagrams."
    saturation: "<= 8% of frame area above mid saturation. one lime element per slide carrying meaning, plus the 6px title rule which is structure."
    detail: "detail is spent on pasted media (screenshots, renders) and on the single illustration. everything the deck draws itself is stroke-only and flat."
  archetypes: ["title", "section_divider", "statement", "two_column", "screenshot_caption", "diagram", "table", "tips_list", "links_qr_wall", "demo_placeholder", "questions"]
```

---

## 1. The five questions — asked and self-answered

No user was available. Asked, answered, assumption recorded. Each is load-bearing.

**Q1 — The feeling. One word for the first ten seconds.**
*Answer: unbothered.* The room contains two groups who both arrive tense: professionals who suspect AI is coming for their craft, and newcomers who think they are one prompt away from a game. Anything urgent, hyped or dramatic feeds both anxieties. A deck that looks completely unbothered — clinical, flat, slightly amused — disarms the first group and quietly deflates the second. *Assumption:* the speaker's own delivery is dry. The deck matches it.

**Q2 — The lineage. Two or three it descends from, one it must never be mistaken for.**
*Answer: Swiss lecture slides, terminal output, Gorey line work.* Never mistaken for: **an AI-tool pitch deck.** The subject is AI tooling; the single worst outcome is looking like the marketing of the thing being discussed. The deck must look like a person's notes, rigorously set — not like a product.

**Q3 — The dial. Deakins or Storaro.**
*Answer: Storaro, hard.* Colour here is a symbolic system, not lighting. Lime = the human. Olive = structure and the machine's scaffolding. Cream = information. Held for 45 minutes without exception, so that by slide 20 the audience reads lime as "this bit is still yours" without being told. That is the spine of the talk rendered in colour. *Assumption:* the speaker will not need to explain the code; it works subliminally or not at all.

**Q4 — The constraint. What is genuinely fixed.**
*Answer:* PS brand spec is binding (palette, three-dot motif, lowercase tone). Bossa logo appears untouched on the title slide. 1920×1080. Single-file HTML, fonts from fonts.googleapis.com with system fallbacks. A possibly weak projector — so contrast floors are raised above WCAG: **7:1 for body, caption and code**, 4.5:1 for large type and non-text. Mixed light/dark pasted media is unavoidable. Solo build, limited hours: every decision here must be executable in CSS by one agent in one pass, which is why there are no illustrations beyond one and no bespoke per-slide layouts.

**Q5 — The stakes. What must always be findable instantly.**
*Answer: where the human is still required.* The talk's argument is "AI accelerates a discipline, it does not replace it." So the one thing the eye must find on every slide is the lime — the point where judgement, taste or a decision is still a person's job. Second priority: QR codes, which must be scannable from row fifteen by a phone camera, which is why they get the only maximum-contrast exception in the deck.

---

## 2. The direction

Near-black ground, cream type, one acid lime. The deck is set on a 12-column Swiss grid with a fixed title block, lowercase throughout, in a single type superfamily — Archivo Black for headings, Archivo for everything else, JetBrains Mono for anything the machine wrote. Nothing is centred except one slide type. Nothing has a shadow. Nothing moves except a 120ms cut and a 180ms list build. Every screenshot, render, clip and QR code is framed by the same 2px olive rule, so a dark terminal capture and a light markdown capture belong to one system rather than being two accidents.

The one idea underneath all of it: **lime marks the human.** The ring diagram strokes olive where AI compresses time and lime where it does not — design taste, QA judgement, art direction, publishing relationships. The engine table lime-marks the recommendation, not the winner. The tips slide lime-marks the verbs, because the verbs are the part the audience has to do. By the time the sovereignty slide arrives, lime has been trained into meaning "yours," and the hedge slide can be almost entirely lime without a word of explanation.

The obvious alternative — the current house style of AI-adjacent talks: deep violet, glow, gradient mesh, a neural-net motif, everything centred — was rejected because it would place the deck inside the marketing language of the very tools being examined, and because it is what the room has already seen four times this year. The second alternative, a light deck on cream for projector safety, was rejected because a 1920×1080 cream field on a bright projector in a darkened room is physically unpleasant for 45 minutes and destroys every dark terminal screenshot in the talk. Cream survives here as a *tile* — a deliberate, rationed light surface — which is the more interesting solution anyway.

---

## 3. Pillars

**1. Lime means a human decision or a human action. Nothing else.**
Because the talk's entire argument is about where the human still belongs, the signal colour is that argument made visual. *Pass:* the "art direction" segment of the ring is lime; every other segment olive. *Fail:* lime used to make a bullet list look lively, or to highlight a code keyword.

**2. Every piece of pasted-in media wears the same 2px olive rule.**
The deck mixes dark terminals, light markdown, QR tiles, renders and video stills. Without one frame they read as a scrapbook. The olive rule at 4.81:1 survives a weak projector where a grey hairline would not. *Pass:* a light markdown screenshot on a cream tile, olive-ruled, sitting next to an olive-ruled dark terminal capture, reading as siblings. *Fail:* a screenshot dropped in with no frame "because it already has a border."

**3. One idea per slide.**
Sixteen sections in 45 minutes is 2.8 minutes per section. A slide carrying two points gets neither. If a slide needs a second heading, it is two slides. *Pass:* "even if the AI wrote it, I wrote it." alone on a field of black. *Fail:* that line plus the five-property test beneath it.

---

## 4. What this is not

- Not a pitch deck. No hero statistic in 200px type, no "the future of", no upward-right arrows.
- Not an AI-tool landing page. No purple, no violet-to-blue, no mesh gradient, no glow, no glass.
- Not a keynote. No full-bleed photography of a server room, no dramatic lighting, no cinematic letterboxing.
- Not a corporate template. No logo in every corner, no gradient divider bars, no title-and-bullets slide master.
- Not edgy-dark. No skulls, no glitch effects, no scanline overlay, no "cyberpunk" neon cyan/magenta, no terminal green. The lime is brand, not hacker cosplay.
- Not cute. No mascots, no robot illustrations, no emoji in copy, no cartoon hands, no whimsical empty states.
- Not a whiteboard. No hand-drawn fonts, no sketchy strokes, no simulated marker. The drawing is precise; the joke is that it is precise.
- Not illustrated. One illustration exists in the entire deck. Every other visual is a screenshot of a real thing or a diagram drawn in flat strokes.
- Not animated. The deck does not perform. A projected talk with motion is a talk the audience watches instead of listens to.

---

## 5. Colour

### Roles

| Role | Token | Hex | Sits on | Measured |
|---|---|---|---|---|
| ground | `--ps-black` | `#111111` | — | — |
| plate (code, zebra) | `--ps-plate` | `#1A1A1A` | ground | 1.17:1 (surface separation only) |
| surface (cards) | `--ps-charcoal` | `#2D2D2D` | ground | 1.37:1 |
| light tile | `--ps-cream` | `#F0EDE4` | ground | 16.14:1 |
| primary text | `--ps-cream` | `#F0EDE4` | ground | **16.14:1** |
| primary text | `--ps-cream` | `#F0EDE4` | surface | **11.77:1** |
| text on light tile | `--ps-near-black` | `#1A1A1A` | cream tile | **14.88:1** |
| secondary text | `--ps-cream-dim` | `#A8A49A` | ground | **7.59:1** |
| secondary text | `--ps-cream-dim` | `#A8A49A` | surface | **5.53:1** |
| border / media rule | `--ps-olive` | `#7A8800` | ground | **4.81:1** (non-text) |
| hairline (decorative) | `--ps-grey` | `#3A3A3A` | ground | 1.66:1 — never load-bearing |
| **signal** | `--ps-lime` | `#C8DF00` | ground | **12.60:1** |
| signal | `--ps-lime` | `#C8DF00` | surface | **9.18:1** |
| danger | `--ps-red` | `#F26D6D` | ground | **6.46:1** |

Every value above is a measured WCAG contrast ratio, not an estimate.

### The projector hardening

Floors are raised over WCAG because a washed-out projector lifts blacks and mutes saturation, costing roughly a third of measured contrast in practice. **Body, caption and code must measure ≥ 7:1. Large type (≥48px) and non-text ≥ 4.5:1.** Three consequences, all binding:

- **PS Dark Olive `#454E00` measures 2.11:1 on ground.** It is invisible on a weak projector. It survives in the deck *only* as the third dot of the brand mark, where its job is to be the dark one. It is never a border, a fill, a stroke or a state.
- **PS Olive `#7A8800` measures 4.81:1.** Fine as a 2px rule, a diagram stroke, a table foot. **Never text, at any size.** This is the most likely mistake a build agent will make.
- **PS Error `#E04444` measures 4.57:1** and fails the 7:1 floor. Replaced by `#F26D6D` (6.46:1) for projection. Still short of 7:1, which is acceptable because error red appears only as short labels at ≥34px and never as reading copy. The brand value stays correct for screen and print; this is a projection tint, documented as such.

### Adjacency (Albers)

Sanctioned pairs — these are the only backgrounds each colour is permitted on:

| Colour | Sanctioned on | Forbidden on |
|---|---|---|
| cream `#F0EDE4` | ground, plate, surface | cream tile |
| cream-dim `#A8A49A` | ground, plate, surface | cream tile |
| near-black `#1A1A1A` | cream tile | ground, plate, surface |
| lime `#C8DF00` | ground, plate, surface | cream tile (2.1:1 — vibrates, illegible) |
| olive `#7A8800` | ground, plate, surface | cream tile, and never behind text |
| red `#F26D6D` | ground, plate, surface | cream tile |

The cream tile is a foreign country. Nothing from the dark palette crosses into it except the olive frame that surrounds it from outside. Anything printed *on* a cream tile is `#1A1A1A`. This is why QR codes work and why a markdown screenshot can be pasted in unaltered.

### Ramps

**Grey** (warm-shifted above step 4 so the top of the ramp lands on cream rather than on a cold white):

```
0 #111111   1 #1A1A1A   2 #232323   3 #2D2D2D   4 #3A3A3A
5 #4E4C48   6 #6B6862   7 #8B8780   8 #A8A49A   9 #F0EDE4
```

Steps 0–4 are backgrounds and hairlines. Steps 5–7 exist for diagram de-emphasis if olive is already spoken for on that slide. Steps 8–9 are text. No step outside this ramp.

**Lime** (only three steps are sanctioned on a slide):

```
100 #F2F7B8   200 #E4EF7A   300 #D6E73D   400 #C8DF00 *
500 #A8BB00   600 #7A8800 *  700 #5E6900   800 #454E00 *
```

`*` = sanctioned. `300` is permitted for hover/active in the deck's own HTML navigation chrome, which is never projected. The rest exist so a build agent has somewhere legal to go and does not invent a colour.

### The signal

`#C8DF00` means **a human decision or a human action**. In practice:

- ring diagram: the stages AI does not compress (design taste, QA judgement, art direction, publishing relationships)
- engine table: the recommendation column
- tips slide: the imperative verb of each line
- planning pipeline: the "grill" step, because grilling is a person interrogating a plan
- sovereignty slide: the hedge
- harness illustration: the harness itself — the rider's grip
- code samples: the one line the speaker is pointing at

It is not a bullet colour, not a link colour, not a hover colour, not an underline, not a background fill behind text. One lime element per slide carrying meaning. The 6px lime title rule is brand structure and is exempt from the count.

---

## 6. Value & light

**Low key. Range 0.6% to 84.8% relative luminance. No pure black, no pure white.** The deck has no lighting model — it is a flat field. What reads as "light" is the cream tile and the cream type; both are rationed.

Cream tiles are capped at 50% of frame area, one per slide. A bright rectangle on a dark field in a dark room is a physical event for the audience's eyes; two of them per slide, thirty slides deep, is fatigue. The QR wall is the single sanctioned exception: a grid of small cream tiles is acceptable because each is ≤240px and the negative space between them keeps the field dark.

**Squint test.** Blur any slide to 20px. What must remain: the title block (big cream mass, top-left, with a lime tick above it), the one lime element, and the shape of the media block. If the lime disappears into the general brightness at blur, it is too small or sitting on too bright a surface — enlarge it or move it onto ground.

Temperature: the whole deck is warm-neutral (cream `#F0EDE4` is warm, grey ramp is warm above step 4). Lime is yellow-green, also warm. There is no cool in the palette at all. That is deliberate — it is the one contrast (Itten: cold-warm) the deck explicitly refuses, because every AI deck in the room will be cool blue. The carrying contrast is **saturation**: one saturated hue in a field of neutral.

---

## 7. Shape & silhouette

**Geometric, 95/5.** Rectangles, circles, straight lines, arcs. Corner radius 0 by default; 4px permitted only on cream tiles, where it signals "this is a pasted object, not part of the deck."

The only organic form in 45 minutes is the horse-and-rider. That is the point: it arrives at minute 8 into a deck of perfect rectangles and is the only thing that was drawn rather than measured. Its strangeness is structural, not decorative.

**Density rhythm.** Detail is spent on pasted media — screenshots, renders, the failed monster, the gravity-drive stills. Everything the deck draws itself is stroke-only, flat, unshaded. A slide with a dense screenshot gets nothing else but a title and a caption. A slide with a diagram gets no screenshot. Diagrams are capped at **7 nodes**; past 7, split the slide.

**Blackout test.** The horse-and-rider must be identifiable as a rearing horse with a figure coming off it, from silhouette alone, at 360px wide. The ring diagram must be identifiable as an open ring at 200px. Anything that fails is over-detailed.

---

## 8. Type

One superfamily, three roles. Archivo is a grotesque in the Univers lineage — the correct descendant of the brand wordmark face, available on Google Fonts, and it holds its weight at projection distance where Univers Light Condensed would thin out and vanish. Archivo Black is used at a single weight for every heading; it is blunt and unfashionable and reads from the back wall.

```
Archivo Black  — display, 400 (its only weight)
Archivo        — text, 400 / 500 / 600
JetBrains Mono — code + terminal, 400 / 700
```

Load exactly these. No fourth family. No icon font.

| Role | Family | Weight | Size | Line-height | Tracking | Colour |
|---|---|---|---|---|---|---|
| section title | Archivo Black | 400 | 140px | 1.00 | −0.030em | cream |
| statement | Archivo Black | 400 | 96px | 1.08 | −0.025em | cream |
| slide title | Archivo Black | 400 | 76px | 1.05 | −0.020em | cream |
| kicker | Archivo | 600 | 22px | 1.20 | +0.140em | lime |
| lead | Archivo | 500 | 40px | 1.35 | −0.005em | cream |
| body | Archivo | 400 | 34px | 1.45 | 0 | cream |
| caption | Archivo | 400 | 26px | 1.40 | +0.005em | cream-dim |
| code / terminal | JetBrains Mono | 400 | 26px | 1.50 | 0 | cream |
| code emphasis | JetBrains Mono | 700 | 26px | 1.50 | 0 | lime |
| code comment | JetBrains Mono | 400 | 26px | 1.50 | 0 | cream-dim |
| table header | Archivo | 600 | 24px | 1.30 | +0.080em | cream-dim |
| table cell | Archivo | 400 | 28px | 1.40 | 0 | cream |
| diagram label | Archivo | 500 | 28px | 1.25 | 0 | cream |
| diagram label (small) | Archivo | 500 | 22px | 1.25 | 0 | cream-dim |
| footer | Archivo | 400 | 20px | 1.00 | +0.060em | cream-dim |

**Nothing below 22px is ever projected.** A 20px footer is the one exception and it carries nothing the audience needs.

**Case.** Everything lowercase: titles, section headings, labels, kickers, table headers, captions. Sentence case in body prose. No ALL-CAPS anywhere in the deck — the brand forbids it in digital UI and it would fight the lowercase wordmark. Proper nouns keep their capitals (Unity, Godot, Claude Code, OpenRouter, Blender, Halifax).

**Measure.** Body ≤ 54 characters. Lead ≤ 46. Statement ≤ 34. A body paragraph therefore occupies at most 7 of 12 columns; a two-column layout gives each side 6 columns (852px), which lands near 50ch at 34px. Never full-width body text.

**Tracking.** Negative on display sizes (Archivo Black at 76px+ opens up otherwise), zero on body, positive only on the two small tracked roles — kicker and table header — where letter-spacing does the work a size increase would otherwise do.

---

## 9. Composition & space

**Canvas 1920×1080. Margin 96px. Safe area 1728×888 at (96, 96).**
**Grid: 12 columns × 122px, 24px gutters, total 1728px.**
**Spacing unit 8. Scale: 8 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 192.** No arbitrary values.

**The fixed title block** — identical on every content slide, so that thirty slides feel like one document:

```
y=96    6px × 96px lime rule, flush left at x=96
y=132   kicker (optional, section name, lime, 22px tracked)
y=190   slide title baseline (Archivo Black 76px, flush left, lowercase)
y=280   content top — nothing above this line but the title block
y=960   1px #3A3A3A hairline, full safe width
y=1000  footer baseline: "punk.science" left · section name centre · slide number right
```

**Sanctioned deviations from the grid — three, and only three:**

1. **Section divider** — full bleed. Title optically centred in the frame, three-dot mark beneath. No title block, no footer.
2. **Statement slide** — the single line is optically centred in the safe area (vertical centre raised 5% for optical balance). No title block. Footer stays.
3. **Illustration slide** — the horse-and-rider bleeds past the right margin to x=1920. Nothing else in the deck bleeds.

Everything else, including every diagram, screenshot, table and QR wall, snaps to the 12-column grid and sits between y=280 and y=930.

---

## 10. Material & finish

The deck has no material. It is flat ink on a flat ground — no lighting, no depth, no texture, no paper, no grain, no noise overlay. Surfaces are distinguished by value alone (`#111111` → `#1A1A1A` → `#2D2D2D`), never by shadow, border-glow or bevel. Edges are hard: 2px olive rules, 6px lime rules, 1px hairlines, all butt-ended.

Where the brief might invite a Xerox/cut-up punk texture — this is the wrong surface for it. Grain scanned onto a projected slide reads as a dirty lens, not as a chosen constraint. The punk here is in the *restraint*: an information design so plain it refuses to sell you anything, in a room full of decks that are selling.

**Pasted media is the only place with texture,** and it arrives with its own. That is precisely why it is all framed identically — the olive rule is the deck saying "this is a quotation."

---

## 11. Motion

Two transitions. Both short. Neither is noticed.

| Name | What | Duration | Easing |
|---|---|---|---|
| `slide_advance` | opacity 0→1 on the incoming slide only | **120ms** | linear |
| `build_reveal` | opacity 0→1 + translateY 16px→0 | **180ms** | `cubic-bezier(0.2, 0, 0, 1)`, 60ms stagger, max 5 steps |

`slide_advance` is a hard cut with a single frame of grace so the projector's response curve does not tear. The outgoing slide does not animate — it is simply gone.

`build_reveal` exists for exactly three jobs: revealing list items one at a time, dropping the lime overlay onto the ring diagram, and revealing table rows. Maximum five staggered steps; beyond five the audience is waiting rather than listening.

**Forbidden:** push, slide, zoom, flip, cube, dissolve, parallax, Ken Burns, looping ambient animation, animated gradients, any motion whatsoever on the illustration, autoplay video without a visible control. Fallback video clips are manually started by the speaker and show a still frame until then.

`prefers-reduced-motion: reduce` sets both durations to 0ms.

---

## 12. The illustration — horse, rider, harness

One illustration in the deck. Inline SVG. It lands on the harness slide (section 5, minute ~8) with the caption **"no legs, no direction."**

### The idea

A horse rearing, mid-panic, with a small rider holding on. The horse **has no legs** — the torso simply ends, cleanly, where the legs would attach. It is not injured, not bleeding, not stumps. The forms just stop, as if the legs were never specified. The horse is nonetheless rearing violently. The rider is drawn completely composed: upright posture, tidy, hands closed on the harness, expression neutral. Nobody in the picture acknowledges the missing legs.

That is the whole argument in one image. The model is enormous power with no way to touch the world. The rider's grip is the harness. The caption is flat and does not explain the joke, and neither does the speaker — the spoken line ("a bare model is not wild, it is inert") lands *against* the picture, which is where the wit lives.

### Shape language

Mignola logic inverted for a dark ground. Design in **cream masses first**, black negative space eats the detail.

- Horse: one solid cream silhouette (`#F0EDE4`), no internal shading, no gradient. Anatomy is described by **negative-space notches cut out of the mass in ground colour `#111111`** — the line of the jaw, the trough of the neck, the crease behind the shoulder, the barrel of the ribs. Four to six notches total. Not more.
- Triangle bias in the horse: the head is a wedge, the neck a long triangle, the rearing pose a diagonal. Triangle = dynamic/threatening, and the horse is the threat.
- Rider: a smaller solid cream silhouette, built from **squares and circles** — a rectangular torso, a circular head, a straight-line arm. Square = stable/reliable. The shape language does the joke: a stable geometry attached to a violent one.
- Line weight: **5px**, uniform, no tapering, butt caps. Used only for the harness line and the rider's arms. Everything else is filled mass, not stroke.
- No ground line, no horizon, no environment, no motion lines, no dust. Removing them changes nothing, so they are removed.

### Palette

| Element | Role | Value |
|---|---|---|
| horse mass | text_primary | `#F0EDE4` |
| anatomy notches | ground | `#111111` |
| rider mass | text_primary | `#F0EDE4` |
| harness strap + reins | **signal** | `#C8DF00`, 5px stroke |
| the cut where the legs end | ground | `#111111` — a hard, straight, unapologetic edge |

Lime appears **only** on the harness. It is the single lime element on that slide. It runs from the rider's closed hands, up the neck, to the noseband — one continuous 5px lime path, which is the most legible thing in the frame after the silhouette.

### Composition & geometry

- Viewbox `0 0 900 700`. Placed in columns 7–12, bleeding right to x=1920. Caption sits under the left half of the slide at body size.
- Horse head at approximately (230, 110). Neck descends on a **58° diagonal** to the chest at (430, 330). Barrel continues down-right, terminating in a hard horizontal cut at **y=560**, spanning roughly x=420 to x=720. That cut is the punchline and must be dead straight.
- Rider seated at (560, 250), body pitched back at **38° from vertical**, feet trailing right and up. Arms straight, both hands closed at (390, 250) on the lime rein.
- The lime rein path: from (390, 250) → control through (300, 190) → to the noseband at (215, 145). One quadratic curve. Do not add buckles, rings or straps; one path.
- Whole mark fits inside 900×700 with 40px of empty margin on all sides so it can be lifted into other collateral.

### What must be legible from the back of the room

At 360px reproduction width, in silhouette, three things and only three:

1. **It is a horse, rearing.** The head-wedge and the neck diagonal carry this.
2. **A person is on it, holding something.** The rider must read as a separate mass, clearly detached in posture from the horse's line — a visible gap of ground colour between rider's back and horse's neck.
3. **A lime line connects hands to head.** This must survive first; if the mark is scaled until only one thing remains, it is the lime rein.

The missing legs are a second-read detail. They do not need to land from row fifteen — they land when the audience looks again, which is better.

### Constraints

- Reducible mark, not a painting. No rendering, no shading, no cross-hatch, no texture, no outline around the silhouette.
- Total path count target: **under 20**. If it needs more, it is being drawn rather than designed.
- Never animated. Never flipped. Never recoloured. Never placed on a cream tile.
- Passes the degradation test at one colour: drop the lime to cream and the image still reads as horse-and-rider. Drop everything to a single flat cream on black and it still reads.

---

## 13. Applied — slide archetypes

Eleven archetypes. Every slide in the deck is one of these. If a slide needs a twelfth, it is two slides.

| # | Archetype | Layout rule |
|---|---|---|
| 1 | **title** | No title block. `punk.science` lockup + three-dot mark at optical centre-left (cols 2–7); Bossa logo right of a 64px `#3A3A3A` vertical hairline, native aspect, untouched. Talk title in Archivo Black 140px beneath, lowercase. Speaker name and city in caption role at the foot. No lime except the three-dot mark. |
| 2 | **section_divider** | Full bleed, no title block, no footer. Section name in Archivo Black 140px, optically centred, lowercase. Three-dot mark 64px beneath, centred. Running-order number in caption role top-right. Nothing else on the slide. |
| 3 | **statement** | One line, nothing else. Archivo Black 96px, ≤34ch, optically centred in the safe area with the vertical centre raised 5%. No title block, no image, no bullet, no attribution. Footer only. A single word or phrase may be lime if it is the human part of the claim. |
| 4 | **two_column** | Title block, then two 6-column wells (852px each) at y=280 with a 24px gutter. Both wells top-aligned; unequal heights are fine and are not balanced. Each well gets at most one lead line and one body block, or one media object. A 1px `#3A3A3A` vertical hairline between columns is optional and decorative only. |
| 5 | **screenshot_caption** | Title block, then one media object, max 1180px wide, left-aligned to column 1 or centred across cols 2–11 — pick one per deck and never mix. Dark captures sit on ground with a 2px olive rule; light captures sit on a cream tile (24px padding, 4px radius, 2px olive rule). Caption below at 24px gap, flush left with the media, ≤2 lines. No body copy on this slide. |
| 6 | **diagram** | Title block, then a stroke-only drawing occupying cols 2–11 between y=300 and y=900. 4px strokes: cream = structure, olive = de-emphasis, lime = the one thing being argued. Max 7 nodes. Labels outside the geometry, never inside a stroke. Overlays arrive via `build_reveal`. No caption; the labels are the caption. |
| 7 | **table** | Title block, then a full-12-column table. No vertical rules, no row rules. Header in table_header role with a 2px lime rule beneath; zebra rows `#111111`/`#1A1A1A`; 2px olive rule closing the foot. Max 8 rows × 6 columns, 64px row height, 24px cell padding. Lime marks exactly one cell or one column header — the recommendation. A date-pulled note goes in caption role under the foot rule. |
| 8 | **tips_list** | Title block, then up to 7 lines at body size (34px), flush left in cols 1–8, 32px leading between items. Bullet is an 8px lime square, baseline-aligned, 24px from the text. The imperative verb of each line is lime and weight 600; the rest is cream 400. This is the slide the room photographs — it must be legible at 26px on a phone screenshot, so nothing else goes on it. |
| 9 | **links_qr_wall** | Title block, then a grid of QR tiles: 4 across × up to 2 down, each 240px on cream with a 2px olive rule and 4px radius, 48px gutters, centred in cols 2–11. Label beneath each tile in caption role, ≤2 lines, centred. The sanctioned exception to the one-cream-tile rule. Nothing else on the slide — no body copy, no URLs as text. |
| 10 | **demo_placeholder** | Title block, then the fallback still frame at up to 1180px with a 2px olive rule. A lime kicker above the media reads `live demo — fallback ready`. Caption below gives the URL in mono 26px plus one 240px QR tile to the right of the media. Video never autoplays; the still frame is what shows until the speaker starts it. |
| 11 | **questions** | Title block replaced by a single lowercase `questions.` in Archivo Black 140px, flush left. Contact block in cols 8–12 at body size: name, `punk.science`, and up to three 240px QR tiles stacked. Three-dot mark bottom-right in the footer band. This is the slide that stays up for 15 minutes — it carries no argument, only coordinates. |

**Applied notes for the specific slides in the plan:**

- **Game dev cycle ring** — archetype 6. Five arc segments, r=300, 28px stroke, 6° gaps, olive base. On build, the segments AI does not compress restroke lime. The live-ops segment ends with a **24° gap**: the ring never closes. Do not tidy that gap; it is the argument.
- **Defining terms stack** — archetype 6. Five bars, 12 columns wide, 88px tall, 16px gaps, `#1A1A1A` fill, 2px olive rule, label flush left with 32px inset. The client boundary is a 2px **dashed lime** line across the full width with its label right-aligned in caption role. Dashed = boundary, solid = thing, everywhere in the deck.
- **Model taxonomy** — archetype 6, grid variant. 2×2 or 2×3 cells, 6 or 4 columns wide, 300px tall, `#1A1A1A` fill, 2px olive rule. At most one cell carries a 6px lime top edge.
- **Chat vs harness contrast** — archetype 4, two `screenshot_caption` wells side by side. Both dark captures, both olive-ruled, identical widths. No arrow between them, no "vs" glyph. The layout says it.
- **AGENTS.md beside GDD** — archetype 4. Both light markdown captures, so both on cream tiles: the one slide where the one-cream-tile rule is relaxed to two, because the comparison is the point. Cap combined cream area at 50% of frame.
- **Failed monster beside working drive** — archetype 4. The failure gets a `#F26D6D` caption label in lowercase, the success gets a cream one. No red X, no green check, no border colour change. The caption does the work.
- **Model-count stats** — archetype 7 or 3. Every date-sensitive number carries `pulled YYYY-MM-DD` in caption role directly beneath it. Non-negotiable.
- **"Even if the AI wrote it, I wrote it."** — archetype 3, lowercase, nothing else on the slide. The two instances of "I" are lime. Nothing else.

---

## 14. Decisions & rejected alternatives

| Axis | Chosen | Rejected | Why |
|---|---|---|---|
| Emotional through-line | unbothered | "urgent" / "exciting" | Urgency feeds both audience anxieties and sells the tools being critiqued. |
| Lineage | Swiss lecture slides + terminal + Gorey line | Cyberpunk / terminal-green hacker aesthetic | Terminal green is costume. The brand already owns a better acid. |
| Ground | `#111111` dark | Cream `#F0EDE4` light deck (projector-safe) | A full-frame cream field for 45 min is physically tiring and destroys every dark terminal screenshot. Cream survives as a rationed tile. |
| Dial | Storaro — lime as symbolic system | Deakins — colour motivated by the media | There is no light source to motivate; a flat deck has no lighting model. A symbolic system carries the talk's actual thesis. |
| Palette scheme | Neutral + one acid signal | Full PS three-green scheme as functional colours | Dark Olive measures 2.11:1 and disappears on a weak projector. Demoted to the brand mark only. |
| Carrying contrast | Saturation (Itten) | Cold-warm | Every other AI deck in the room is cool blue. Refusing cool entirely is the cheapest way to not look like them. |
| Error colour | `#F26D6D` (6.46:1) | Brand `#E04444` (4.57:1) | Fails the projector floor. Documented as a projection tint, not a brand change. |
| Display face | Archivo Black | Univers Light Condensed (brand wordmark face) | Light condensed thins out and vanishes on a weak projector at distance. Archivo is the same grotesque lineage with the weight to survive. |
| Display face | Archivo Black | Oswald / Bebas Neue / Space Grotesk | Conference-deck defaults. Archivo Black is blunter and less fashionable, which ages better in a recorded talk. |
| Type families | One superfamily + one mono | Display + unrelated body pairing | Vignelli: fewer faces, more rigour. Archivo/Archivo Black share skeletons, so 30 slides read as one document. |
| Mono | JetBrains Mono | Fira Code / Courier / IBM Plex Mono | Tall x-height and unambiguous `0 O l 1` at projection distance; no ligatures to misread on screen. |
| Media framing | One 2px olive rule on everything | Per-medium treatment (dark unframed, light tiled) | The deck mixes five media types. One frame makes them a system; five treatments make a scrapbook. |
| QR | Black modules on cream tile, 240px | Lime modules, brand-consistent | Scanners fail on low-contrast and coloured modules. Scannability beats brand consistency; the olive frame carries the brand instead. |
| Table | Zebra rows, no rules | Full grid rules | Rules at 2:1 on a weak projector vanish anyway. Zebra survives washout; Vignelli approves. |
| Motion | 120ms cut + 180ms build | Slide/push transitions, ambient motion | A projected talk with motion is a talk being watched instead of heard. |
| Illustration count | One | A recurring illustrated motif across sections | One illustration in a deck of rectangles is an event. Four is a style, and styles are cheaper. |
| Illustration content | Legless rearing horse, composed rider | Wild horse with legs, dramatic dust and motion lines | Legless *is* the argument ("no legs, no direction") and is funnier delivered flat. Dust and motion lines are trying hard; trying hard is the failure mode. |
| Humour placement | Structural — the legless cut, the open ring, the deadpan rider | A caption gag or a mascot | The joke has to survive being delivered with a straight face. A mascot delivers it for you. |
| Light mode | None | A light variant for print handouts | Print handouts are a different medium and would need their own bible. Not in scope; say so rather than half-do it. |

---

## 15. Review checklist

Run this before any slide is considered done. Cite the clause when failing something.

- [ ] Does the slide have exactly **one** idea? (Pillar 3)
- [ ] Is there **exactly one** lime element carrying meaning, and does it mark a human decision or action? (Pillar 1)
- [ ] Is every pasted media object framed by the same **2px olive rule**? (Pillar 2)
- [ ] Is olive used as text anywhere? **Must be zero.**
- [ ] Is `#454E00` used as anything but the third brand dot? **Must be zero.**
- [ ] Is any text below **22px**? (Footer at 20px is the only exception.)
- [ ] **Contrast audit:** every text/background pair measured, not eyeballed. Body/caption/code ≥ 7:1, large ≥ 4.5:1, non-text ≥ 4.5:1.
- [ ] Any pure `#000000` or `#FFFFFF`? **Must be zero.**
- [ ] More than one cream tile? (Only the QR wall and the AGENTS.md/GDD comparison are exempt.) Cream area ≤ 50% of frame?
- [ ] Is anything centred that is not a section divider or a statement slide?
- [ ] Does the slide sit on the 12-column grid, between y=280 and y=930, with the fixed title block intact?
- [ ] **Greyscale test:** strip colour. Does hierarchy survive on value alone?
- [ ] **Squint test:** blur to 20px. Title mass, lime element and media block still read?
- [ ] **Thumbnail test:** at 10%, is the slide's type identifiable (statement vs diagram vs table)?
- [ ] **Deletion test:** remove each element in turn. Anything that breaks nothing stays removed.
- [ ] Any gradient, shadow, glow, blur or radius over 4px? **Must be zero.**
- [ ] Any transition other than `slide_advance` (120ms) and `build_reveal` (180ms)? **Must be zero.**
- [ ] Every date-sensitive number carries `pulled YYYY-MM-DD`?
- [ ] Every link or GitHub reference has a QR ≥ 200px, black on cream, 4-module quiet zone, no logo in the centre?
- [ ] Every live demo has a fallback still in place, not autoplaying?
- [ ] Bossa logo: untouched, native aspect, title slide only, 1× clear space?
- [ ] **Pleasantness test:** could this be any competent studio's deck? If nothing here would annoy a designer, find the choice with teeth.
- [ ] **Straight-face test:** does the wit survive with no wink? No mascot, no exclamation mark, no nudge?
```
