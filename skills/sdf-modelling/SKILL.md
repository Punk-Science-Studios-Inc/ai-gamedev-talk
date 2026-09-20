---
name: sdf-modelling
description: Build a 3D model parametrically as a signed-distance field in numpy, solved against reference images, then mesh it and finish it in Blender. Use when asked to recreate a creature, character, prop or vehicle from a reference photo or turnaround sheet; when a model must be driven by numbers rather than sculpted by hand; when "make it match the reference" or "sculpted parity" is the goal; or whenever an agent (which cannot sculpt) has to produce organic geometry. Covers the measure-first parity harness, the SDF kit, the six traps that cost the most to find, and exactly where to stop and hand over to Blender.
---

# SDF modelling from reference

An agent cannot sculpt. It has no hand on a brush and no eye on a viewport at
60 fps. What it *can* do is write numbers, measure the result, and close the
loop — hundreds of times, without getting bored.

So do not try to sculpt. Build the model as a **signed-distance field defined by
a parameter file**, and build a **measurement harness that scores it against the
reference in seconds**. The harness is the skill. Everything else is mechanical.

This works for anything that can be described as fused masses and cut seams:
creatures, characters, monsters, organic props, weathered hard surface. It is a
poor fit for anything defined by sheet material, panel lines, or precise
engineering — model those from profiles and lofts instead.

---

## The pipeline

```
reference plates
   │  segment + normalise            tools/<name>_ref.py, <name>_curves.py
   ▼
measured curves (JSON)               half-widths, depths, joint heights
   │  hand-written parameters        spec.py     <- the whole model lives here
   ▼
signed-distance field                sdfx.py     Chain + Box, smooth min/max
   │  sample + surface nets + relax
   ▼
mesh + baked vertex attributes       build.py -> mesh.npz
   │
   ▼
Blender: shading, light, camera      assemble.py
```

Five files. `spec.py` is the model; everything else is machinery you write once
and reuse. `scripts/sdfx.py` in this skill is that machinery, ready to copy.

---

## Rule 1 — build the parity harness before the model

Do this **first**, before a single primitive exists.

1. **Segment the reference.** For a figure on a plain backdrop, a colour-dominance
   test beats luminance: skin is red-dominant, fog and grey cards are not. Grow a
   few pixels into dark trim (claws, hair, shadowed rim) so you keep it, then take
   the largest connected component to drop captions and background haze.
2. **Normalise by something you can find on both.** Not image height — the plates
   are framed differently. Pick a landmark pair the subject defines: floor to top
   of skull, or wheelbase, or muzzle to buttplate. Every measurement becomes a
   fraction of that.
3. **Write every spec number in those same units.** If the spec says
   `waist halfWidth 0.068` and the measured curve says `0.070`, that is a
   one-line check. If the spec is in centimetres and the reference in pixels,
   you will be eyeballing forever.
4. **Score the field, not the render.** You already sample the SDF on a grid to
   mesh it. `(G < 0).any(axis=1)` is the front silhouette and
   `(G < 0).any(axis=0)` is the side, for free. Overlay them on the segmented
   plate, print IoU, and print **per-height edge deltas** — the signed number for
   each landmark row saying which way to move it and how far. IoU tells you if
   you are winning; the deltas tell you what to type.

That check must run in **seconds**. Ours ran in three. It was used well over a
hundred times. Nothing else in the project mattered as much.

Expect a **front IoU around 0.80** for a figure with fingers and spikes. Above
0.85 you are fitting the segmentation's own error. Below 0.70 something is
structurally wrong, not slightly off.

### Read the plates before you trust their labels

Turnaround sheets — especially generated ones — lie. Ours had a panel captioned
"LEFT SIDE VIEW" that was a second *front* view in a different arm pose, and its
"RIGHT SIDE" plate had the arms lowered while the front plates had them out.
Score against the plates that actually agree with the pose you are building, and
say plainly in the write-up which ones cannot match and why. A parity number you
have not explained is worse than no number.

---

## Rule 2 — one primitive does almost everything

Resist a library of primitives. Two carry a whole creature:

- **`Chain`** — a swept ellipsoid along a polyline, with per-knot 3-axis radii
  and an optional local frame. This is a torso section stack, a limb, a muscle
  belly, a finger, a horn, a claw, a vertebral scute, a groove-cutter. Everything.
- **`Box`** — a rounded box, for cuts that need a flat face.

Combined with polynomial `smin` / `smax`. That is the entire modelling
vocabulary, and it keeps the spec readable, which is what lets you tune it.

The distance from a swept ellipsoid is an *underestimate*, not exact. That only
ever makes the surface slightly fatter near sharp tapers, and it stays C1, which
is what the reprojection pass needs. Don't chase exactness.

### Meshing

Naive **surface nets**, then alternate Laplacian smoothing with a Newton step
back onto the isosurface. Four or five rounds takes the blocky dual mesh to a
clean surface with essentially zero residual. Use forward differences for the
gradient and reuse the centre sample — four field evaluations per projection
instead of seven, which on a 400k-vertex mesh is the difference between a minute
and fifteen seconds.

Surface nets gives **quads, watertight, no topology decisions**. It also gives
you no edge flow and no UVs. That is the trade; see "Defer to Blender" below.

---

## Rule 3 — the six traps

These are not style preferences. Each of them produced a visibly wrong model and
each took a rebuild to find.

### 1. Blend radius is the difference between anatomy and a mannequin

At human scale a 20 mm smooth-union radius melts every muscle into the torso.
The first render was a smooth pink dummy with no anatomy at all. Muscle unions
want **6–9 mm at 2 m tall** — small enough that each belly keeps a groove around
it. Keep a single `BLEND` scalar scaling every muscle union so you can sweep it.

Pair it with two more scalars: shrink the core shell (`CORE_SCALE ≈ 0.86`) and
swell the bellies (`MUSCLE_SCALE ≈ 1.13`). The silhouette stays where the
measurements put it and the bellies stand proud instead of sinking into the mass.

### 2. Carve depth is measured from the surface, never from the carve's own axis

A groove chain whose centre sits on the skin removes a hole **one radius** deep.
Our abdomen came out punched full of round holes.

Give every carve an explicit `depth`, then slide each knot onto the surface along
the field gradient and back out by `(radius - depth)`:

```python
def ride_out(F, pts, rad, depth):
    P = np.asarray(pts, np.float32)
    d = np.clip(F.eval(P), -0.12, 0.12)     # a knot nowhere near the surface
    n = F.normals(P)                         # is a spec error, not a projection
    r = np.asarray([x[0] for x in rad], np.float32)
    return P - n * d[:, None] + n * (r - depth)[:, None]
```

The clamp matters. Without it a mis-specified knot gets projected across half the
model and you spend an hour looking for the resulting hole.

### 3. Never warp world position by a per-vertex direction field

The obvious way to make noise run along a muscle is to compress world position
along the fibre direction. It does not work. `dot(P, t)` is multiplied by the
noise frequency, so a fraction of a degree of wobble in `t` swings the sample a
whole period, and the entire skin renders as **speckle**.

Bake a proper surface parameterisation instead. Ours is `mu`: for each vertex,
find the nearest muscle segment and store `(cos, sin)` around it plus arc length
along it. Texture scaled hard in `mu.xy` and softly in `mu.z` reads as fibre —
in the displacement pass and in the shader, from the same numbers.

Give **one frame per chain**, taken from the chain's overall direction, not one
per segment. Per-segment frames flip and leave seams down a limb.

### 4. A region *id* cannot survive interpolation

Baking one float — skin 0, horn 1, claw 2, eye 3, tooth 4 — and selecting
materials from ranges means every face joining skin to a tooth sweeps through
horn, claw and eye. Our eye's emission shader lit up as an orange halo around
every vertebral bead.

Bake **one 0..1 mask per class**, packed into vector attributes. Interpolation
then only ever blends the two materials that actually meet.

### 5. A field returns nothing outside its bounding boxes

`Field.eval` is sliced per primitive against padded AABBs for speed. A point
outside every box evaluates to `BIG`, so its **gradient is zero and the normal is
undefined**. We seeded the spine chain well behind the body intending to project
it forward onto the back; every bead got a zero normal, never moved, and floated
6 cm off the body.

Seed projections from **inside** the body. Make `normals()` fall back to a radial
direction rather than returning silent zeros.

### 6. Geometry can only hold detail the mesh can resolve

At a 4 mm voxel, anything finer than ~20 mm aliases into stipple. Our first
detailed render was sandpaper. Split the budget explicitly:

- **mesh** carries the ropes and folds — 20 mm and up;
- **shader bump** carries fibre, pores and reticulation.

Both driven off the same `mu`, so they agree.

---

## Rule 4 — ordering is part of the spec

Anything that rides on the surface — carved seams, scutes, plates, projected
detail — is evaluated against **the field as built so far**. It must be added
after the masses it sits on. Write `build_field()` in explicit stages and keep
the comments that say why each stage is where it is.

## Rule 5 — a chain carries one frame for its whole length

If a cut must follow a curve that turns — a mouth around a face, a seam around a
shoulder — sample the curve and emit **many short chains, each with its own
frame**. Two mirrored halves meeting at a midline cut diagonally and miss each
other; our creature's grin stayed sealed shut through three rebuilds.

And get the axis order right. For a slit, radii in the local frame are
`(into the surface, gape, along)`. Given as `(gape, into, along)` the cut becomes
a deep vertical slot that destroys the jaw.

---

## Where to defer to Blender

Do **not** try to do these in the field. Every one of them is faster, better and
more controllable in Blender, and two of them are impossible in an SDF.

| Task | Why Blender |
|---|---|
| **Shading, lighting, camera, render** | Always. Build the node graph from Python — it is verbose but deterministic and diffable. Nothing about materials belongs in the geometry pass. |
| **UVs and edge flow** | Surface nets gives neither. If the asset needs texture painting or deformation, retopologise in Blender (or QuadRemesher) using the SDF mesh as the reference surface. |
| **Rigging, skinning, animation** | An SDF has no skeleton and dual-contoured topology deforms badly. Export the mesh, rig it in Blender. If you need a posed variant, it is usually cheaper to add a pose parameter to the spec and rebuild than to rig. |
| **Asymmetric, authored detail** | A specific scar in a specific place, a chipped tooth, a hand-placed wound. Sculpt it in Blender on top; do not contort the spec to place one feature. |
| **Scattering over a surface** | Scales, studs, quills, barnacles. Geometry Nodes distributing instances on the finished mesh beats hundreds of SDF primitives, and stays editable. |
| **Fur, hair, cloth, physics** | Not expressible. |
| **Normal/AO/curvature map baking** | Multires or a high-to-low bake. If the target is a game asset, the SDF mesh is your high poly. |
| **Final decimation / LODs** | Blender's decimate and remesh modifiers, non-destructively. |
| **Anything an artist wants to nudge** | The moment a human is in the loop on a specific spot, hand them a mesh. The spec is for things that are *measured*; sculpting is for things that are *judged*. |

Conversely, keep in the field: overall proportion, silhouette, mass placement,
muscle layout, seams, anything symmetric, anything repeated (a fan of horns, a
row of scutes), and anything you will want to re-derive when a measurement
changes. Those are the things that are painful to re-sculpt and trivial to
re-run.

**Do not use an SDF at all** when you already have a good base mesh, when the
form is defined by clean lofted profiles, or when the deliverable is a rigged
character. Sculpt or loft instead.

---

## Porting the look to real time

If the model also has to run in a browser, the baked attributes are the whole
trick: ship `mu`, the mark weights and the per-class masks in the vertex buffer
and the fragment shader is a direct transliteration of the offline material —
same ramps, same layer frequencies, same numbers. Nothing needs baking to texture
and there are no UVs to invent.

Two things change, and both bite:

- **Fade every procedural layer out as it goes subpixel.** Offline you had many
  samples per pixel; in a browser you have one, and anatomical detail is around a
  millimetre across. Measure the footprint in **the layer's own coordinate** —
  `1.0 - smoothstep(0.2, 0.85, length(fwidth(q)))` — and mix the layer towards its
  mean. Deriving the footprint from world scale is wrong: if the coordinate is a
  unit circle scaled by a frequency, the surface carries 2π times that many
  features around it, not that many.
- **Swap the expensive primitives.** Distance-to-edge Voronoi is 54 hashes per
  pixel; two octaves of ridged noise give the same reticulated read.

Compute the bump normal from screen-space derivatives of a scalar height
(Mikkelsen) rather than inventing a tangent frame — surface nets gives you no UVs
to build one from.

---

## Do it right the first time

In order. Do not skip ahead — every one of these was learned by skipping it.

1. **Segment and measure the reference. Write the parity check. Run it.** Before
   any geometry.
2. **Write a surface probe.** Ten lines: given a spec coordinate, print the
   field's signed distance and its nearest-surface point. This single tool would
   have caught, immediately: back muscles specified inside the torso shell, a
   mouth curve floating outside the face, and spine beads seeded outside every
   bounding box. All three cost a rebuild each to find by rendering.
3. **Measure the surface, spec the surface.** The biggest recurring error was
   reasoning "belly centre + radius = where the skin ends" in my head, over and
   over, and getting it wrong on the back. Write spec entries as *where the skin
   should be* and let the builder solve the centre. Where you cannot, at least
   record the resulting surface position in a comment.
4. **Fix the depth datum once, explicitly.** Establish, from the side plate, the
   surface depth at every landmark height. Print it. Tape it to the wall. Every
   depth number in the spec is then checkable at a glance rather than by render.
5. **Choose the detail parameterisation before writing any displacement.**
   Not after.
6. **Bake per-class masks from the start.** Never a single id.
7. **Give every carve an explicit surface-relative depth from the start.**
8. **Orbit the light rig with the camera from the start.** A fixed rig renders
   every back view as a silhouette and you will misjudge the model for hours.
9. **Render close-ups from the first pass.** A 300-pixel turnaround panel hides
   everything. Our head was wrong through six iterations because it was four
   percent of the frame.
10. **Add a crop-and-rebuild mode early.** Meshing only the head at high
    resolution took a 90-second rebuild down to 40 and made the face iterable at
    all. Whatever the hard part is, make it cheap to rebuild alone.
11. **Budget the head — or whatever the identity-carrying part is — at half the
    total effort.** It is not proportional to its volume. Nobody looks at a
    forearm.

---

## What I would do differently next time

- **Write the surface probe on day one.** Three of the six traps were probe-shaped
  problems found by rendering instead. This is the single highest-value change.
- **Spec surfaces, not centres** (point 3 above). Most spec churn was arithmetic
  I was doing in my head.
- **Build the head first, not last.** It sets the character, it is the hardest
  part, and everything else is easier to judge once it is right. Doing it last
  meant the body was tuned against a placeholder.
- **Give the head its own parity check.** The body had numeric feedback and got
  close fast. The head had only my eye, and it wandered — a flat face plate
  rebuilt as a snout, then back. Landmark points (eye corners, mouth corners,
  crest tips) projected into the plate would have converged in a third of the
  passes.
- **Break symmetry deliberately.** The model is perfectly bilateral and reads
  synthetic because of it. A small per-side jitter on muscle radii and a few
  asymmetric marks would cost ten lines.
- **Separate "measured" from "invented" in the spec.** Some numbers are traceable
  to the plates; some I made up because the plates do not show them (interior
  depths, the far side of anything). Mark them. When something looks wrong, you
  want to know instantly which kind of number you are touching.
- **Keep a rendered iteration log.** One thumbnail per build, appended. Reviewing
  ten passes at once shows drift that consecutive comparisons hide.
- **Stop tuning silhouette at IoU ≈ 0.80** and move to shaded renders. The last
  few points of IoU came from fingertips and spike tips and changed nothing about
  how the model reads.

---

## Reference

`scripts/sdfx.py` — the modelling kit, ready to copy: `smin`/`smax`, `Chain`,
`Box`, a sliced-AABB `Field` with grid and point evaluation, surface nets, and
the relax/reproject loop. Pure numpy, no Blender, no dependencies beyond numpy.

Typical costs, for a 2.2 m creature at a 4 mm voxel (67M cells, ~470k quads):
field build 1 s, grid sample 20 s, surface nets 20 s, relax 85 s, attribute bake
28 s, displacement 5 s. Under three minutes end to end; the parity check alone is
three seconds. Keep both, and use the fast one constantly.
