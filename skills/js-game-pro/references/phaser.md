# Phaser 3

Phaser 3 is a 2D engine: WebGL renderer with Canvas fallback, scene graph, three physics
options, loader, input, tween and audio subsystems. It is not an ECS and not opinionated
about architecture — you supply that.

## Config and boot

```js
new Phaser.Game({
  type: Phaser.AUTO,          // WEBGL, falls back to CANVAS
  parent: 'game',             // DOM id; omit and Phaser appends to body
  backgroundColor: '#101014',
  scale: {
    mode: Phaser.Scale.FIT,   // or RESIZE / ENVELOP / EXPAND
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: 720, height: 1280, // design resolution, not device resolution
  },
  physics: { default: 'arcade', arcade: { gravity: { y: 0 }, debug: false } },
  scene: [BootScene, PreloadScene, GameScene],
})
```

- **FIT** letterboxes and keeps the design resolution — simplest, safest for a game designed at
  one aspect. **RESIZE** gives the scene the real viewport size and fires `resize` on the scale
  manager; you must lay out responsively and handle the event. Do not mix: picking RESIZE then
  hard-coding positions against the design size is the most common layout bug.
- `roundPixels: true` and `pixelArt: true` for pixel art; `pixelArt` sets nearest-neighbour
  filtering globally. Per-texture: `texture.setFilter(Phaser.Textures.FilterMode.NEAREST)`.
- On mobile set `input: { activePointers: 3 }` if you need multitouch; default tracks fewer.

## Scene lifecycle

`init(data)` → `preload()` → `create(data)` → `update(time, delta)` per frame.

- `delta` is milliseconds since the last frame. Multiply movement by `delta / 1000`, or use the
  physics engine's own integration — never both.
- Scenes are objects that persist. `scene.start(key)` shuts a scene down and re-runs
  init/preload/create; `scene.launch(key)` runs one in parallel (HUD over gameplay);
  `scene.pause` / `scene.resume` keep it alive but stop `update`.
- **Every listener you add outside the scene's own emitter must be removed.** Register cleanup in
  `this.events.once(Phaser.Scenes.Events.SHUTDOWN, ...)`. Leaked DOM/global listeners that fire
  against a dead scene are the number one source of "works until you restart the level" bugs.
- Cross-scene messaging: `this.scene.get('HUD').events.emit(...)` or a shared event bus module.
  Prefer a plain `Phaser.Events.EventEmitter` singleton for game-domain events; keep it typed.

## Physics: choosing

- **Arcade** — AABB only, no rotation on bodies, extremely fast. Platformers, top-down, shooters,
  anything where boxes and circles suffice. Default choice.
- **Matter.js** — full rigid body, constraints, compound shapes, rotation, restitution. Use only
  when the game is *about* physics. Costs an order of magnitude more CPU and is harder to make
  deterministic.
- **Impact** — removed from core in modern Phaser 3; do not reach for it.

Arcade specifics that catch people:
- `body.setSize()` vs `setDisplaySize()` — the first changes the collision body, the second
  scales the sprite. They are not linked; set the body offset after scaling.
- `collider` resolves overlap and separates; `overlap` only reports. Store the returned object if
  you need to destroy it later.
- Tilemap collision: `map.setCollisionByProperty({ collides: true })` after creating the layer,
  and `this.physics.add.collider(sprite, layer)`.
- Bodies do not exist until the sprite is added to the physics world. `this.physics.add.sprite()`
  or `this.physics.world.enable(existingSprite)`.

## Input

- Pointer covers mouse and touch uniformly: `this.input.on('pointerdown', p => ...)`.
  `p.worldX/worldY` for camera-corrected coordinates; `p.x/y` are screen space.
- Per-object: `sprite.setInteractive()` then `sprite.on('pointerdown', ...)`. Give it an explicit
  hit area for irregular sprites; the default is the full frame rect including transparency.
- Keyboard: `this.input.keyboard.createCursorKeys()` or `addKeys('W,A,S,D')`. Poll in `update`
  for held state; use events only for discrete presses.
- Gamepad needs `input: { gamepad: true }` in config and a user gesture before the browser
  exposes pads. See platform-bridge.md.
- Mobile: bind gameplay start to `pointerdown`, not `pointerup`, and unlock audio there — see
  the audio note below.

## Assets

- Preload in a dedicated scene with a progress bar bound to
  `this.load.on('progress', v => ...)`; `complete` fires before `create` of the next scene.
- **Use a texture atlas.** One `atlas(key, png, json)` beats fifty `image()` calls: fewer
  requests, and the renderer batches quads that share a texture. TexturePacker, free-tex-packer
  or `@phaserjs/...` community tooling all emit the JSON hash format Phaser reads.
- Audio: load both `.ogg` and `.m4a`/`.mp3` — Phaser picks by browser support. Web Audio is
  suspended until a user gesture; call `this.sound.unlock()` or rely on Phaser's auto-unlock, and
  never assume `sound.play()` in `create()` produced sound.
- Bitmap fonts render far cheaper than `Text` objects. Every `setText()` on a `Text` object
  re-rasterises to a canvas and re-uploads a texture — do not do it every frame for a score;
  update on change, or use `BitmapText`.

## Tweens, timers, cameras

- `this.tweens.add({ targets, x, duration, ease, yoyo, repeat, onComplete })`. Tweens are owned by
  the scene and die with it. `this.tweens.killTweensOf(target)` before destroying a target you
  tweened, or the tween writes to a dead object.
- `this.time.addEvent({ delay, callback, loop })` for game-time timers — these respect scene pause,
  `setTimeout` does not. Never use `setTimeout`/`setInterval` for gameplay timing.
- `this.cameras.main.startFollow(sprite, true, lerpX, lerpY)`, `setBounds`, `setZoom`, `shake`,
  `fade`. A second camera with `ignore()` lists is how you render a HUD unaffected by zoom — but
  a separate HUD scene is usually simpler.

## Destruction and leaks

- `sprite.destroy()` removes it from the display list and physics world. It does **not** free the
  texture — textures live in the global `TextureManager` across scenes. Free explicitly with
  `this.textures.remove(key)` when a level's atlas will not be reused.
- Groups: `group.clear(true, true)` (removeFromScene, destroyChild) — the two booleans matter.
- Restarting a scene does not reset module-level state. Anything you kept in a module `let`
  survives; that is either the point or a bug, so be deliberate.

## Testing

Phaser needs a DOM and a canvas, so headless unit tests should target your own logic modules,
not scenes. Under vitest, `environment: 'jsdom'` plus `type: Phaser.HEADLESS` can boot a game for
integration tests, but it is slow and brittle — keep the tested surface in plain modules instead.
