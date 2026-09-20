# three.js

three.js is a renderer and scene graph, not a game engine. It gives you cameras, materials,
lights, loaders, animation and postprocessing. It gives you no game loop opinion, no physics, no
entity model, no serialisation, no input abstraction. Supply those yourself (see
`architecture.md`) or use Babylon/PlayCanvas instead.

## Boot shape

```ts
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' })
renderer.setPixelRatio(Math.min(devicePixelRatio, 2))   // 2 is the cap that matters on mobile
renderer.setSize(innerWidth, innerHeight)

const scene  = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 200)

const clock = new THREE.Clock()
renderer.setAnimationLoop(() => {          // not requestAnimationFrame — this is XR-compatible
  const dt = Math.min(clock.getDelta(), 0.1)
  update(dt)
  renderer.render(scene, camera)
})
```

- **`setAnimationLoop`, not `requestAnimationFrame`.** It is the only loop WebXR can drive, and
  switching later means rewriting the loop.
- **Clamp the near/far ratio.** `near: 0.1, far: 200` is a healthy range; `near: 0.001` with
  `far: 10000` produces z-fighting no amount of polygon nudging fixes. Widen `near` before you
  reach for `logarithmicDepthBuffer`.
- **Cap `pixelRatio` at 2.** A 3x phone screen renders 9x the fragments for no visible gain and
  halves your frame rate.
- On resize: update `camera.aspect`, call `camera.updateProjectionMatrix()`, then
  `renderer.setSize()`. Missing the projection update is the standard "everything is stretched"
  bug.

## Colour and tone mapping

Modern three defaults to a colour-managed pipeline, and getting this wrong is why hobby scenes
look washed out or blown out.

- `renderer.outputColorSpace = THREE.SRGBColorSpace` (the default in current versions).
- Colour textures (albedo, emissive) must be `texture.colorSpace = THREE.SRGBColorSpace`.
  Data textures — normal, roughness/metalness, AO, displacement — must stay
  `THREE.NoColorSpace`. glTF loaders set this correctly; manual `TextureLoader` calls do not.
- `renderer.toneMapping = THREE.ACESFilmicToneMapping` with `toneMappingExposure` as your
  exposure dial. Without tone mapping, any HDR/lit scene clips to white.
- Lights and materials are physically scaled. If a scene is black, check light intensity units
  and that you have an environment map — PBR materials with no environment reflect nothing.

## Materials, lighting, environment

| Material | Cost | Use |
|---|---|---|
| `MeshBasicMaterial` | trivial | Unlit, UI, sprites, debug |
| `MeshLambert/Phong` | low | Legacy stylised look, cheap lighting |
| `MeshStandardMaterial` | medium | PBR default |
| `MeshPhysicalMaterial` | high | Clearcoat, transmission, iridescence — only when needed |
| `ShaderMaterial` / `MeshStandard` + `onBeforeCompile` | varies | Custom effects; prefer patching the standard material over writing lighting from scratch |

- One `RoomEnvironment` or HDRI through `PMREMGenerator` set as `scene.environment` does more for
  visual quality than adding lights. Real-time lights are expensive; bake where you can.
- Shadows: `renderer.shadowMap.enabled`, and set `castShadow`/`receiveShadow` **selectively**.
  Tighten the directional light's shadow camera frustum to the play area — a loose frustum is why
  shadows are blocky. `shadowMap.type = THREE.PCFSoftShadowMap` for quality,
  `VSMShadowMap` only if you know why.
- Every distinct material is a distinct shader program. Compiling shaders mid-play causes hitches;
  warm them with `renderer.compile(scene, camera)` or `WebGLRenderer.compileAsync` before
  gameplay starts.

## Loading assets

- **glTF/GLB is the format.** `GLTFLoader` + `DRACOLoader` (geometry compression) +
  `KTX2Loader`/`MeshoptDecoder` (GPU-compressed textures). Run models through `gltf-transform` or
  `gltfpack` in the build — it routinely cuts payload by 5–10x.
- KTX2/Basis textures stay compressed in VRAM. A 4096² PNG costs ~64MB uncompressed on the GPU;
  the same as KTX2 costs a fraction. On mobile this is the difference between running and being
  killed by the OS.
- `useDraco`/`useKTX2` loaders need their decoder files copied into the served output — a
  Vite build will not bundle them for you.
- `THREE.Cache.enabled = true` if you re-load the same URLs; otherwise manage instances yourself.

## Performance

Draw calls, not triangles, are usually the ceiling.

- **Instancing** — `InstancedMesh` for many copies of one geometry+material (foliage, bullets,
  crowds). One draw call for thousands. Set `instanceMatrix.needsUpdate = true` after writing
  matrices; use `setColorAt` for per-instance tint.
- **Merge static geometry** — `BufferGeometryUtils.mergeGeometries` for level chunks that never
  move separately.
- **Frustum culling is per-object and on by default**; it does not help if everything is one
  merged mesh. Balance merging against culling.
- **LOD** — `THREE.LOD` with 2–3 levels for anything with a distance range.
- **Reuse geometries and materials.** Creating them in the loop allocates GPU resources every
  frame. Hoist to module scope or a cache.
- Profile with `renderer.info` (`render.calls`, `render.triangles`, `memory.geometries`,
  `memory.textures`). `memory.*` climbing over time is a leak, full stop.
- **Postprocessing costs full-screen passes.** `EffectComposer` with bloom + SSAO + FXAA can
  triple frame cost. Use the `postprocessing` package's merged-pass `EffectComposer` if you need
  several effects on a budget, and disable most of it on mobile.
- Prefer `WebGPURenderer` only if you know the target browsers support it and you have a fallback
  path; the WebGL renderer remains the safe default.

## Disposal — the mandatory part

three does not garbage-collect GPU resources. Removing a mesh from the scene frees nothing.

```ts
function disposeObject(root: THREE.Object3D) {
  root.traverse(o => {
    const m = o as THREE.Mesh
    m.geometry?.dispose()
    const mats = Array.isArray(m.material) ? m.material : m.material ? [m.material] : []
    for (const mat of mats) {
      for (const v of Object.values(mat)) {
        if (v && (v as THREE.Texture).isTexture) (v as THREE.Texture).dispose()
      }
      mat.dispose()
    }
  })
  root.removeFromParent()
}
```

Also dispose render targets, `EffectComposer` passes, and the `PMREMGenerator`. Call
`renderer.dispose()` on teardown. Watch `renderer.info.memory` across a level reload: if the
numbers do not return to baseline, you are leaking, and on mobile that ends as a browser kill
rather than a slow leak.

## Animation

- `AnimationMixer` per animated model; `mixer.update(dt)` in the loop. Clips come from the glTF.
- Crossfade with `action.crossFadeTo(next, duration, true)`; call `next.play()` first or you fade
  to nothing.
- Skinned meshes are CPU-costly at high bone counts on mobile. Share skeletons via `SkeletonUtils.clone`
  when spawning many copies of one character — a plain `.clone()` breaks skinning.

## Raycasting and input

- `Raycaster` from normalised device coordinates: `(x/w)*2-1`, `-(y/h)*2+1`. Restrict candidates
  to an explicit array of pickable objects — raycasting the whole scene every pointer move is a
  real cost.
- For physics-driven games, raycast the physics world (Rapier) rather than the render scene; they
  will otherwise disagree by a frame.

## React
`@react-three/fiber` is a genuine React reconciler for three, and `@react-three/drei` supplies the
helpers you would otherwise write. It is a legitimate choice for 3D web apps and lighter games.
Keep every per-frame mutation inside `useFrame` and out of component state — a `setState` per
frame re-renders the tree at 60Hz. Load assets with `useGLTF` + `<Suspense>`, and preload before
the scene mounts to avoid a pop-in stall.
