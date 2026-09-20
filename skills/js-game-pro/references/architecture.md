# Game architecture in TypeScript/JavaScript

## The loop

The engine gives you a variable-delta `update(time, delta)`. Do not feed that straight into
simulation — a 12ms frame and a 90ms frame produce different physics, and the same input replays
differently on a different machine.

```ts
const STEP = 1 / 60          // seconds
const MAX_CATCHUP = 5        // steps; beyond this, drop time rather than spiral

let accumulator = 0

function tick(deltaMs: number) {
  accumulator += Math.min(deltaMs, 250) / 1000   // clamp tab-return spikes
  let steps = 0
  while (accumulator >= STEP && steps < MAX_CATCHUP) {
    simulate(STEP)                                // pure, deterministic
    accumulator -= STEP
    steps++
  }
  if (steps === MAX_CATCHUP) accumulator = 0      // give up on the backlog
  render(accumulator / STEP)                      // alpha for interpolation
}
```

Render interpolates between previous and current simulation state using `alpha`. Skipping
interpolation is acceptable at 60Hz sim on 60Hz displays and visibly stutters everywhere else.

**Determinism** requires: fixed step, a seeded PRNG (never `Math.random()` in simulation — use a
small xorshift/mulberry32 and store the seed), no iteration over unordered `Set`/object keys
where order affects results, and no floating-point reliance across engines if you plan to
lockstep-network. Store the input stream and the seed and you get free replays and bug repros.

## Layering

```
src/
  sim/        pure game logic — no phaser/three/react import, testable in node
  render/     engine-specific presentation; reads sim state
  platform/   one module per capability, native behind an interface
  ui/         DOM/React overlay
  main.ts     wiring
```

The rule that enforces it: `sim/` must never import from the other three. Add an ESLint
`no-restricted-imports` rule or a dependency-cruiser check if the project is large enough for
drift.

## State machines

Most game bugs are illegal state transitions. Model states explicitly rather than with booleans.

```ts
type PlayerState =
  | { kind: 'idle' }
  | { kind: 'running'; speed: number }
  | { kind: 'jumping'; startedAt: number; jumps: number }
  | { kind: 'hit'; invulnUntil: number }
```

Discriminated unions make impossible states unrepresentable and give exhaustive `switch` checking
with `never`. For screens/flow, a table of allowed transitions beats scattered `if` chains; XState
is worth it only when the chart is genuinely complex or designers need to read it.

## ECS — when

Use an ECS when entity counts are high and behaviour is combinatorial (bullet-hell, sim,
strategy). Do not use one for a game with a dozen distinct actors — the indirection costs more
than it saves. Options: `bitecs` (fastest, typed-array SoA, unusual API), `miniplex` (ergonomic,
object-based, React bindings), `becsy`. Phaser's display objects can act as the render view over
ECS data; keep the ECS as the source of truth and sync one way.

## TypeScript

- `strict: true`. Games accumulate `any` faster than anything else because engine types are broad;
  hold the line at module boundaries even if internals are loose.
- Brand IDs so they cannot be swapped: `type EntityId = number & { __brand: 'EntityId' }`.
- `as const` for data tables; derive types from data rather than duplicating
  (`type EnemyKind = keyof typeof ENEMIES`).
- Prefer `readonly` on config/data structures passed into sim.
- Avoid class hierarchies for entities. Composition or plain data + functions ages better; deep
  `Sprite` subclass trees are the classic Phaser trap.
- `satisfies` for config objects that must match a shape without widening literal types.

## Save data and serialisation

- Version every save: `{ v: 3, ... }`, with an explicit migration chain `v1→v2→v3`. Write the
  migration when you change the shape, not later.
- Serialise sim state only, never engine objects. If you cannot `JSON.stringify` your game state,
  the layering is wrong.
- Write on meaningful checkpoints *and* on `visibilitychange → hidden` / `pagehide` — mobile
  browsers do not reliably fire `beforeunload`. Keep the write synchronous-cheap (localStorage) or
  pre-serialised so a background transition does not lose it.
- Size: localStorage is ~5MB and synchronous. Anything larger or binary goes to IndexedDB (`idb`
  is a thin, safe wrapper).

## Testing

- Unit-test `sim/` in node — no jsdom needed, fast enough to run on every save.
- Property-test invariants that matter (health never negative, entity count conserved) with
  `fast-check` when the state space is wide.
- Golden/replay tests: record an input stream, assert final state hash. This catches determinism
  regressions that no unit test will.
- Vitest is the default for a Vite project; it shares the config and needs no extra transform.
