# Performance

## Method

Measure before changing anything. In order:

1. **Establish the budget.** 60fps = 16.6ms per frame; on mobile assume you get ~10ms of it after
   the browser's own overhead. Name the target device.
2. **Chrome DevTools Performance panel**, 10–20 seconds of real gameplay. Read the flame chart:
   long yellow (script) is your code, purple (rendering) is layout/paint, green (painting) is GPU
   compositing.
3. **Distinguish CPU-bound from GPU-bound.** If frame time drops when you shrink the canvas, you
   are fill-rate bound (GPU). If it does not, you are script bound (CPU).
4. **Memory panel → allocation timeline** for GC. A sawtooth allocation graph plus periodic frame
   spikes means you are allocating in the loop.
5. Only then optimise, and re-measure. Undo anything that did not move the number.

Engine counters: Phaser `game.renderer` / the `Phaser.Renderer.WebGL` batch stats; three.js
`renderer.info`. Keep an on-screen debug readout of frame time, draw calls and entity count during
development — most regressions are noticed by eye long before a profiling session.

## The frame budget killers

**Allocation in the loop.** Every `new Vector2()`, array literal, closure, or string concatenation
inside `update()` feeds the GC, and a major GC is a visible hitch.
- Reuse scratch objects hoisted to module scope.
- Pool everything spawned in bulk: bullets, particles, enemies, damage numbers. `setActive(false)`
  + `setVisible(false)` and recycle, rather than `destroy()` + `new`.
- Avoid `array.map/filter/forEach` in hot paths — closures allocate; a plain `for` loop does not.
- Do not build strings per frame (`` `Score: ${n}` ``). Update on change only.

**Draw calls.** Every texture switch breaks the batch.
- 2D: one atlas per scene, ordered so same-texture sprites are adjacent in the display list.
- 3D: instancing and merged geometry (see `threejs.md`).
- Text: bitmap fonts, not per-frame canvas text rasterisation.

**Overdraw / fill rate.** Full-screen effects, large alpha-blended particles and stacked
transparent layers are the usual mobile killer. Fewer, larger particles beat many small ones.
Cap `devicePixelRatio` at 2.

**Layout thrash.** Reading `offsetWidth`/`getBoundingClientRect` after writing DOM styles forces a
synchronous reflow. In games this shows up in DOM HUDs — cache dimensions, update on resize only.

**Physics.** Broad-phase cost scales with body count. Sleep static bodies, use collision
categories/masks so unrelated pairs never test, and reduce the fixed step rate before you reduce
fidelity elsewhere.

## Load and memory

- **Bundle**: engine in its own vendor chunk; lazy-load level assets. `rollup-plugin-visualizer`
  to see what is actually in there. A 2MB JS bundle is ~1s of parse time on a mid-range phone
  before anything renders.
- **Textures dominate memory**, not code. Uncompressed VRAM cost is `w × h × 4` bytes regardless
  of PNG file size — a 2048² PNG is 16MB in VRAM. Use compressed formats (KTX2/Basis) for 3D;
  for 2D, keep atlases at the smallest size that still looks right and use power-of-two dimensions.
- **Free per-level assets explicitly.** Phaser: `textures.remove(key)`. three: `dispose()` on
  geometry, material and every texture. Neither engine does it for you, and mobile OSes kill the
  tab rather than swapping.
- **Audio**: decoded audio is uncompressed in memory. Stream music (`html5: true` in Howler,
  or an `<audio>` element), decode only short SFX.
- Cold start: splash → engine boot → minimal first scene → background-load the rest. Do not block
  the first frame on assets the first screen does not show.

## Mobile specifics

- Thermal throttling means minute-three performance is not minute-one performance. Profile a long
  session, not a burst.
- Background tabs get rAF at 0Hz and throttled timers; anything time-based must reconcile against
  `performance.now()` on resume rather than assume continuity.
- Low-end Android GPUs handle far fewer texture units and smaller max texture size (test 2048 as
  the ceiling). A 4096 atlas silently fails on some devices.
- Battery: an uncapped loop on a menu screen is a review complaint. Cap or pause the loop when
  nothing animates.
