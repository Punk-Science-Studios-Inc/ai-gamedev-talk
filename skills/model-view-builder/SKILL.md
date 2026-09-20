---
name: model-view-builder
description: Ship an offline-built 3D mesh as a self-contained WebGL viewer page whose shading matches the offline render. Use when asked to put a model on the web, build a turntable or model viewer, preview a Blender/SDF/scanned mesh in a browser, port a Blender or Cycles/EEVEE material to GLSL, or when a mesh carries custom per-vertex attributes that glTF will not round-trip. Covers the flat binary format and its packer, the streaming loader, the aliasing trap that ruins every procedural material on the web, the camera-locked light rig, and the one-file bundle.
---

# Model view builder

An offline renderer gets hundreds of samples a pixel, an hour a frame, and a
real world to light from. A browser gets one sample, sixteen milliseconds, and
whatever you can afford to evaluate analytically. A viewer that ignores that
difference does not look like a slightly cheaper render — it looks broken, and
in a specific, diagnosable way.

This is the pipeline for taking a mesh that already exists — from Blender, from
a signed-distance build, from a scan — and putting it on a page a stranger can
open, drag, and recognise as the same object.

It assumes the mesh is **finished**. This is not a modelling skill; see
`sdf-modelling` for building the thing in the first place.

---

## The pipeline

```
mesh + per-vertex attributes         .npz / .obj / whatever the builder wrote
   │  pack                           scripts/pack_mesh.py
   ▼
one flat binary                      assets/model.bin      <- NOT inlined
   │  fetch + typed-array views      scripts/mesh_loader.js
   ▼
BufferGeometry, straight to GPU
   │  hand-ported material           viewer.js
   ▼
one self-contained HTML page         build_web.mjs -> model.html
   │  served, never opened off disk
   ▼
static server
```

Three files you write once and reuse — the packer, the loader, the bundler —
and one you write per model: the viewer, which is mostly its fragment shader.

---

## Rule 1 — inline the code, never the mesh

Everything that is code goes into the page: the three.js build, any small
library, the viewer source, the CSS, the markup. One file, no network fetch, no
build server, mail it to someone.

The mesh does not. At any interesting resolution it is megabytes, and a
multi-megabyte base64 blob or array literal has to be *parsed* by the JavaScript
engine before a single byte reaches the GPU. Keep it a separate binary and fetch
it as an `ArrayBuffer`.

The consequence is that **the page must be served, not opened**. `file://`
blocks `fetch`. Ship a twenty-line static server alongside it and make the
loader's failure message say so outright:

```js
.catch(err => {
  boot.textContent = 'FAILED: ' + err.message +
    '  —  serve the folder, do not open the file directly';
});
```

That one string saves the next person twenty minutes.

---

## Rule 2 — a flat binary, not glTF

Reach for glTF when the mesh is ordinary and something else has to read it.
Write your own when either of these is true, which for this kind of work is
usually both:

- **The mesh carries attributes glTF has no name for.** A material ported from a
  DCC reads whatever the build baked — a muscle- or fibre-local coordinate,
  region masks, a curvature term, per-vertex wear. In glTF those become
  `_CUSTOM0` and a pile of extension wrangling. In your own format they are just
  blocks.
- **You want zero parsing.** Lay the file out as 4-byte-aligned blocks of
  exactly the types the GPU wants, and decoding is a handful of typed-array
  *views onto the same buffer*. No copy, no loop, no allocation per vertex.

`scripts/pack_mesh.py` and `scripts/mesh_loader.js` are that pair, generalised.
The format is self-describing — the header names each attribute and its type —
so the loader never needs editing when the model gains a channel.

Three things the packer must do, none of which belong in the browser:

- **Triangulate.** Quads become two triangles at pack time. The viewer should do
  nothing but upload.
- **Quantise.** Normals to `i8n` (signed byte, normalised), masks and marks to
  `u8n`. A normal does not need 32 bits and neither does a 0..1 mask; three
  channels of `u8n` is a quarter the bytes of `f32` and reads identically.
  Position, and any coordinate a shader multiplies by a large frequency, stay
  `f32`.
- **Pad to 4 bytes.** A typed-array view onto a misaligned offset throws. Give
  every quantised attribute a padding component — three channels stored as four
  — and the problem never arises.

Carry a **magic string and a bounding box** in the header. The magic turns "the
model is invisible" into a one-line error, and the bbox lets the page frame the
model before the geometry is uploaded.

---

## Rule 3 — the shader is a hand port, and parity is the point

The offline material and the web material are the same numbers written twice:
same ramp stops, same layer frequencies, same masks, same weights. Not
"similar". If the page is meant to *be* the render, a mismatch is a defect, and
writing the two as independent guesses guarantees drift.

Port it layer by layer, in the same order, with the offline node names kept in
the comments. Where you deliberately diverge — and you will, twice, below — say
so at the divergence.

What the port is allowed to replace:

- **A world or HDRI becomes a hemisphere ambient.**
  `mix(ground, sky, N.up*0.5+0.5)` times albedo. Two colours, one lerp, and it
  holds up because the eye is reading the key light.
- **Subsurface becomes wrapped diffuse.** `clamp((N·L + w) / (1 + w), 0, 1)`,
  plus a back-facing term keyed on `-L·V` for the translucent rim. Stop there.
- **A path-traced specular becomes one GGX lobe, clamped.**
  `min(ggx(...), 12.0)` — unclamped on a near-mirror surface it produces
  fireflies that bloom into white blobs.
- **Anything Voronoi becomes ridged noise.** Distance-to-edge Voronoi is 27 cell
  hashes in 2D and 54 in 3D, per pixel, to produce a reticulated network. Two
  octaves of ridged value noise read the same at viewing distance for a
  twentieth of the cost.

What it must not replace: the albedo ramp, the layer frequencies, or the masks.
Those are the identity of the surface.

---

## Rule 4 — every procedural layer must fade out as it goes subpixel

**This is the trap that ruins web ports of offline materials, and it does not
present as an aliasing problem. It presents as the model being made of
glitter.**

The offline render supersamples. The page renders one sample per pixel. Any
procedural feature finer than a pixel therefore samples a different random value
every frame as the camera moves, and the whole surface boils.

Fade each layer to its own mean once its features go subpixel:

```glsl
// footprint of q, in q's own units
float band(vec3 q) {
  return 1.0 - smoothstep(0.20, 0.85, length(fwidth(q)));
}
// the layer, faded to its mean (0.5 for fbm) as it goes subpixel
float layer(vec3 q, int oct, float fade) {
  return fade < 0.01 ? 0.5 : mix(0.5, fbm(q, oct), fade);
}
```

**Measure the footprint in the layer's own coordinate.** Not in world space, not
from the distance to the camera, not from a guessed scale factor. `fwidth(q)` on
the exact vector you feed the noise is the only measure that is right for every
layer at once, and it costs two instructions.

Deriving it from world size instead is the mistake that takes longest to spot,
because it is *nearly* right. Worked example: if a layer's coordinate is a unit
circle around a limb scaled by a frequency `around`, that limb carries
`2π·around` features round its circumference, not `around`. Every layer has its
own such factor. `fwidth` knows them all and you do not.

Two corollaries:

- The `fade < 0.01` early-out is worth having on its own. It skips the octave
  loop entirely on distant geometry, which is most of the pixels in a turntable.
- Expose a `uDetail` uniform that scales the finest layers' fade toward zero. It
  is a one-line quality knob for weak GPUs and costs nothing at 1.

---

## Rule 5 — bump without a tangent frame

A mesh from surface nets, marching cubes or a scan has no UVs and no tangents.
Do not generate them just to get a bump map. Use screen-space derivatives
(Mikkelsen):

```glsl
vec3 bumpNormal(vec3 N, vec3 P, float h) {
  vec3 dpdx = dFdx(P), dpdy = dFdy(P);
  float dhdx = dFdx(h), dhdy = dFdy(h);
  vec3 r1 = cross(dpdy, N), r2 = cross(N, dpdx);
  float det = dot(dpdx, r1);
  vec3 grad = sign(det) * (dhdx * r1 + dhdy * r2);
  return normalize(abs(det) * N - grad);
}
```

Build `h` as a weighted sum of the same faded layers the albedo used, so the
bump disappears exactly when the detail it represents does. Scale it down on
hard materials — horn, claw, metal — using the same mask that set their
roughness.

---

## Rule 6 — the light rig travels with the camera

A rig fixed in world space lights the front of the model. Orbit round the back
and the viewer is looking at a silhouette. This is not a subtle degradation; it
is half the turntable rendering as a black shape.

Rotate the rig about the up axis by the camera's yaw every frame:

```js
const cy = Math.cos(state.yaw), sy = Math.sin(state.yaw);
for (let i = 0; i < RIG.length; i++) {
  const L = RIG[i];
  u.uLightPos.value[i].set(L.pos[0]*cy - L.pos[1]*sy,
                           L.pos[0]*sy + L.pos[1]*cy,
                           L.pos[2]);
}
```

Keep the rig's **positions and powers identical to the offline rig** — it is the
same three or four lights, they just swing. Offline turnaround renders usually
light every plate frontally for exactly this reason, so matching the render
means swinging the rig, not fixing it.

Finish the silhouette with a fresnel rim: `pow(1 - N·V, 4)` times a cool colour
at low weight. Against a dark backdrop it is the difference between a shape and
a hole.

---

## Rule 7 — match the offline view transform, and mind the up axis

```js
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;      // match the render's exposure
renderer.outputColorSpace = THREE.SRGBColorSpace;
camera.up.set(0, 0, 1);                   // Blender is Z-up; three.js is Y-up
```

Getting the up axis wrong is survivable but poisons every camera number you tune
afterwards, and it is one line. Set it before touching the rig.

---

## Rule 8 — one script tag, and mind the shared scope

Concatenate, in order: the three.js build, any libraries, your own modules, the
viewer — all inside a single `<script type="module">` in a template literal in
the bundler.

Two mechanical facts that will each cost an afternoon:

- **three.js ships as ESM.** Rewrite its trailing `export{A as B, ...}` into
  `const THREE = { B: A, ... }` once, into a vendored `three.inline.js`, and
  regenerate that only on a version bump. It is what lets the library sit in an
  inline module with no fetch.
- **Everything shares one scope, and minified three.js has already taken the
  short names.** Avoid one- and two-letter *top-level* names in your own source.
  Any library that is minified and *not* module-shaped must be boxed in its own
  IIFE before concatenation, or two bundles collide on a name like `Ae` and the
  page dies at parse with `Identifier 'Ae' has already been declared` — no
  stack, no line that means anything.

The shader source lives in a JS template literal, so **no backticks in GLSL
comments**, and `${` is a substitution. Both fail as a syntax error a hundred
lines from the cause.

---

## Rule 9 — a debug handle, and a progress readout

Expose the internals on `window`:

```js
window.__mv = { state, material, camera, scene, renderer, RIG };
```

One line. It is how you tune the material without a rebuild, how you drive the
page from a capture script, and how anyone else diagnoses it.

Read the fetch with a reader loop rather than `await res.arrayBuffer()`, so a
multi-megabyte mesh shows a percentage instead of a blank screen:

```js
const total = Number(res.headers.get('content-length') || 0);
const reader = res.body.getReader();
for (;;) {
  const { done, value } = await reader.read();
  if (done) break;
  chunks.push(value); got += value.length;
  onProgress(total ? got / total : 0, got);
}
```

`content-length` is absent under some compression settings, hence the
byte-count fallback in the message.

---

## Controls worth having

Cheap, and each earns its key:

| input | does |
|---|---|
| drag | orbit — yaw free, pitch clamped |
| scroll | dolly, clamped both ends |
| ←/→, ↑/↓ | turn, raise the look-at target |
| space | auto-spin on/off |
| named keys | **view presets** — whole figure, head, any detail worth a bookmark |
| H | hide the chrome, for screenshots |

The view presets matter more than they look. A turntable that only orbits makes
the viewer hunt for the framing that shows the work; a key that jumps straight
to it is the difference between a demo and a toy. Store each as the full camera
state — distance, pitch, target height — not just a distance.

Kill auto-spin on the first drag and never restart it on its own.

---

## Checklist

- [ ] Mesh packed to a flat binary with a magic string, counts and a bbox
- [ ] Quads triangulated and normals quantised **in the packer**
- [ ] Every block 4-byte aligned; typed-array views, no per-vertex loop
- [ ] Page serves rather than opens, and says so when it fails
- [ ] Material ported layer by layer, offline node names in the comments
- [ ] Every procedural layer faded on `fwidth` **of its own coordinate**
- [ ] `uDetail` knob wired to the finest layers
- [ ] Bump from screen-space derivatives, scaled down by the hard-material masks
- [ ] Light rig identical to the offline rig, and swung with the camera yaw
- [ ] Fresnel rim so the silhouette reads
- [ ] ACES + sRGB + the render's exposure; `camera.up` matching the DCC
- [ ] No short top-level names; non-module libraries boxed in an IIFE
- [ ] `window.__mv` handle, and a streaming progress readout
