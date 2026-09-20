# The framework landscape

Pick by what the game actually is. Adding a second engine to a working project is almost never
the right call.

## Renderers and engines

| Library | Use it for | Avoid when |
|---|---|---|
| **Phaser 3** | Full-service 2D: scenes, physics, input, audio, tilemaps, loader. Fastest path to a shippable 2D game. | You need 3D, or you want a minimal renderer you compose yourself. |
| **PixiJS** | Pure 2D WebGL/WebGPU renderer. Best raw 2D throughput and the most control. Bring your own loop, physics, input. | You want batteries included — you will rebuild half of Phaser. |
| **three.js** | Anything 3D. Huge ecosystem, glTF pipeline, postprocessing. Not a game engine: no game loop opinion, no physics, no scene serialisation. See [`threejs.md`](threejs.md). | Pure 2D — the overhead and API surface buy you nothing. |
| **Babylon.js** | 3D with an engine's worth of built-ins: physics plugins, animation system, inspector, GUI, WebXR. Heavier bundle than three. | You want minimal payload or the three.js ecosystem specifically. |
| **Excalibur.js** | TypeScript-first 2D with ECS-ish actors and strong typing. Small community. | You need the plugin/tutorial depth Phaser has. |
| **Kaplay (ex-Kaboom)** | Jams, prototypes, teaching. Terse API. | Long-lived production code. |
| **PlayCanvas** | 3D with a hosted editor and strong mobile perf; engine is open source. | You want everything in-repo with no editor dependency. |

## Physics

- **Arcade / Matter** — in Phaser, use these before adding anything.
- **Rapier** (Rust/WASM, `@dimforge/rapier2d`/`3d`) — fast, deterministic given identical builds,
  good for 3D or heavy 2D. WASM load is async; account for it in boot.
- **Planck.js** — Box2D port, mature 2D, plain JS.
- **cannon-es** — legacy-ish 3D; Rapier is the better default now.

## Networking and multiplayer

- **Colyseus** — authoritative room server, schema-based state sync with delta patching, Node.
  The default for small-team real-time multiplayer.
- **Socket.IO / raw WebSocket** — fine for turn-based, lobbies, async play. No state sync for you.
- **PeerJS / raw WebRTC** — P2P, low latency, but NAT traversal needs TURN and P2P is trivially
  cheatable. Only for co-op/friendly play.
- **Geckos.io** — UDP-ish over WebRTC data channels for real-time action.
- For async/turn-based (correspondence-style), skip real-time entirely: HTTP + a state document,
  server-validated moves. Cheaper and it survives flaky mobile connections.

Always validate on the server for anything competitive. A browser client is fully controlled by
the player; treat all client input as hostile.

## Audio

- **Howler.js** — sprite-based playback, pooling, cross-browser unlock handling. The pragmatic
  default when you are not using an engine's audio system.
- **Web Audio directly** — needed for dynamic music, precise scheduling, DSP. Schedule against
  `audioContext.currentTime`, never `setTimeout`. Look ahead ~100ms.
- Every browser requires a user gesture before an `AudioContext` leaves `suspended`. Resume in the
  first `pointerdown`, and re-check on tab return: iOS suspends contexts on backgrounding.
- One audio sprite (a single file with an offset table) beats dozens of small files on mobile.

## State and data

- Game state belongs in your own plain modules, not in a UI state library.
- If UI must observe game state, expose a small subscribe API or an event emitter and let the UI
  layer adapt it. Do not put the simulation in Redux/Zustand — you will pay reactivity cost per
  frame for nothing.
- **Zustand** is the least intrusive option when React genuinely needs shared state; keep it for
  UI concerns (menus, settings, inventory panels).

## React / Vue / Svelte hosting a canvas

The canvas is not a React component tree. The correct shape:

```tsx
function GameHost() {
  const ref = useRef<HTMLDivElement>(null)
  const gameRef = useRef<Phaser.Game | null>(null)

  useEffect(() => {
    if (gameRef.current) return                 // StrictMode double-invoke guard
    gameRef.current = new Phaser.Game({ ...config, parent: ref.current! })
    return () => { gameRef.current?.destroy(true); gameRef.current = null }
  }, [])

  return <div ref={ref} />
}
```

Rules:
- **Mount once.** React 18 StrictMode runs effects twice in dev; without the guard you boot two
  games and chase phantom double-input bugs.
- **Never re-render on game state.** Bridge with an event emitter and let the overlay component
  subscribe to only the values it displays. A `useState` updated at 60fps re-renders the tree 60
  times a second.
- **The game never reads React state.** One direction only: game → events → UI.
- DOM overlay for menus/HUD is legitimate and often better than in-canvas UI — real text
  rendering, accessibility, CSS layout, no bitmap font pipeline. Absolutely position it over the
  canvas and set `pointer-events: none` on the container, `auto` on interactive children.
- **react-three-fiber** is the exception: it is a real React reconciler for three.js and the
  declarative model works. Even there, keep per-frame mutation inside `useFrame` and out of state.
- Next.js/SSR: engines touch `window` at import. Dynamic-import the game host with `ssr: false`.

## Build tooling

- **Vite** is the default: fast dev, Rollup production build, first-class TS, `import.meta.glob`
  for asset manifests. Vitest shares its config.
- Keep the engine in its own chunk (`build.rollupOptions.output.manualChunks`) so gameplay code
  changes do not bust the engine cache.
- Large binary assets go through `publicDir` or an explicit copy step, not through the bundler —
  base64 inlining is off by default above `assetsInlineLimit`, keep it that way for games.
- `base: './'` for Capacitor/Electron/itch.io builds, where the app is not served from a domain
  root.
