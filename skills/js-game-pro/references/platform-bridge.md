# Bridging JS to platform APIs

The rule: **one interface per capability, native implementation behind it, no-op or web fallback
always present.** `npm run dev` in a desktop browser must keep working.

```ts
// platform/haptics.ts
export interface Haptics { impact(style: 'light' | 'medium' | 'heavy'): void }

export const haptics: Haptics = Capacitor.isNativePlatform()
  ? { impact: s => Haptics.impact({ style: s as ImpactStyle }) }
  : { impact: s => navigator.vibrate?.(s === 'heavy' ? 30 : 10) }
```

Gameplay imports `haptics`. It never imports Capacitor, never checks the platform, and never
knows a native layer exists.

## Capacitor

- `capacitor.config.ts` → `webDir` must point at the bundler output (`dist` for Vite), and the
  Vite build needs `base: './'` because the app is served from `capacitor://` / `https://localhost`,
  not a domain root.
- `npx cap sync` copies web assets **and** installs native deps — run it after every web build and
  after adding a plugin. `cap copy` alone only moves assets.
- `Capacitor.isNativePlatform()` / `Capacitor.getPlatform()` for branching, used only inside
  `platform/`.
- Core plugins worth knowing for games: `@capacitor/app` (`appStateChange`, `backButton`),
  `@capacitor/haptics`, `@capacitor/preferences` (small KV, survives updates),
  `@capacitor/filesystem`, `@capacitor/share`, `@capacitor/status-bar`,
  `@capacitor/screen-orientation`, `@capacitor/keep-awake`, `@capacitor/splash-screen`.
- **Android hardware back button** must be handled or it closes the app mid-game:
  `App.addListener('backButton', ({ canGoBack }) => ...)`.
- **Backgrounding**: `App.addListener('appStateChange', ({ isActive }) => ...)` — pause the loop,
  suspend audio, flush the save. On Android the process can be killed with no further callback;
  treat the inactive transition as the last chance to persist.
- Writing a custom plugin is a small Java/Kotlin or Swift class annotated `@CapacitorPlugin` with
  `@PluginMethod` handlers taking a `PluginCall`. Do it when no community plugin exists and the
  capability is genuinely native (billing, ads SDK, platform achievements). Keep the JS-side
  surface tiny and typed; marshal only JSON-safe values.
- Bridge calls are asynchronous and cross a serialisation boundary. Never call one per frame.
  Batch, debounce, or cache on the JS side.

## Cordova

Legacy but alive; Capacitor can consume most Cordova plugins. The `deviceready` event gates all
plugin access — nothing exists before it. If you have a choice, choose Capacitor.

## Electron

- Three processes worth distinguishing: **main** (Node, full OS access), **preload** (bridge,
  isolated), **renderer** (your game, treat as untrusted web content).
- `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`. Expose a narrow,
  hand-written API through `contextBridge.exposeInMainWorld('platform', {...})` in the preload.
  Never expose `ipcRenderer` itself — that hands the renderer arbitrary IPC.
- `ipcRenderer.invoke` / `ipcMain.handle` for request-response; `send`/`on` for fire-and-forget
  and main→renderer pushes. Validate every argument in main; a compromised renderer is the threat
  model.
- Games specifically: `powerSaveBlocker` to stop display sleep, `app.getPath('userData')` for
  saves, `globalShortcut` sparingly, and disable menu accelerators that collide with gameplay keys.
- Enable `backgroundThrottling: false` on the `BrowserWindow` webPreferences if the game must keep
  running unfocused; otherwise let it throttle and pause properly.

## Tauri

- Rust backend, system webview (no bundled Chromium — much smaller binaries, but the webview
  version varies by OS, so test rendering on Windows WebView2 *and* WKWebView).
- `#[tauri::command]` functions invoked from JS via `invoke('name', { args })`, returning a
  promise. Async by default, JSON-serialised.
- The allowlist/capabilities config is deny-by-default: a filesystem or shell call fails silently
  in dev until you grant the scope. Check the capability config first when a command "does
  nothing".

## PWA / web distribution

- Service worker for offline: precache the engine chunk and core assets, runtime-cache large
  optional assets. `vite-plugin-pwa` handles the manifest and Workbox wiring.
- A game that updates while running is a bug source — take the "prompt for reload" strategy, not
  auto-skip-waiting, and only reload between sessions.
- `display: 'fullscreen'` in the manifest, plus an install prompt captured from
  `beforeinstallprompt`.

## Browser APIs games need

| Capability | API | Notes |
|---|---|---|
| Gamepad | `navigator.getGamepads()` | Poll per frame; no events for buttons. Pads only appear after a button press. Vibration via `gamepad.vibrationActuator.playEffect('dual-rumble', {...})`, support varies. |
| Mouse look | `element.requestPointerLock()` | Requires a user gesture; async since recent Chrome. Read `movementX/Y`, not `clientX/Y`, while locked. Handle `pointerlockchange` loss on Esc. |
| Fullscreen | `element.requestFullscreen()` | Gesture-gated. iOS Safari does not support it on arbitrary elements — plan a CSS-based pseudo-fullscreen fallback. |
| Keep screen on | `navigator.wakeLock.request('screen')` | Released automatically on tab hide; re-acquire on `visibilitychange`. |
| Vibration | `navigator.vibrate()` | Android only; iOS Safari ignores it. Use Capacitor Haptics on native. |
| Orientation | `screen.orientation.lock('landscape')` | Only works in fullscreen, and not on iOS Safari. Lock in the native manifest instead when packaged. |
| Notch / safe area | `env(safe-area-inset-*)` in CSS | Needs `viewport-fit=cover` in the viewport meta. Pad HUD elements with these, or buttons sit under the notch and home indicator. |
| Storage | `localStorage`, IndexedDB, `@capacitor/preferences` | localStorage is sync and ~5MB — fine for a save blob, wrong for assets. Safari evicts IndexedDB after 7 days of inactivity for non-installed sites. |
| Audio unlock | `AudioContext.resume()` | Inside a user gesture. Re-check after backgrounding on iOS. |
| Visibility | `visibilitychange`, `pagehide` | The only reliable mobile lifecycle signals. `beforeunload` does not fire on mobile. |
| Network | `navigator.onLine`, `online`/`offline` | Reports the interface, not reachability. Confirm with a real request before trusting it. |
| Input latency | `pointerrawupdate`, `passive: false` | `touch-action: none` on the canvas to kill double-tap zoom and scroll interception. `user-select: none` to stop long-press selection. |

## Mobile web checklist

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
```
- `touch-action: none` and `overscroll-behavior: none` on the canvas container.
- `-webkit-tap-highlight-color: transparent`.
- Test on a real mid-range Android device. Chrome desktop throttling is not a substitute — thermal
  throttling, memory limits and GPU texture budgets only show up on hardware.
