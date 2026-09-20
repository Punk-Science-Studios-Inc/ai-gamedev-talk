"""Pack a mesh and its per-vertex attributes into the flat binary a web viewer loads.

    python pack_mesh.py --src mesh.npz --out assets/model.bin \
        --attr position=V:f32:3 \
        --attr normal=N:i8n:3 \
        --attr aMu=mu:f32:3 \
        --attr aMask=masks:u8n:4

Each --attr is  shaderName=npzKey:type:components. Types:

    f32   float32, as-is
    i8n   signed byte, normalised   -- source in -1..1  (normals)
    u8n   unsigned byte, normalised -- source in  0..1  (masks, marks, wear)
    u16n  unsigned short, normalised -- source in 0..1  (when u8n bands)

Every attribute block is padded to a multiple of 4 bytes per vertex, because a
typed-array view onto a misaligned offset throws in the browser. A 3-component
i8n attribute is therefore stored as 4 and the shader ignores .w.

Faces may be triangles or quads; quads are split here so the viewer does nothing
but upload buffers.

Layout, little endian throughout:

    char[4]  'MVB1'
    u32      vertex count            V
    u32      triangle count          T
    u32      attribute count         A
    f32[6]   bounding box, min then max
    A x {
      char[12]  name, nul padded
      u8        type    0 f32, 1 i8n, 2 u8n, 3 u16n
      u8        components as declared (what the shader sees)
      u8        components as stored  (padded to 4-byte stride)
      u8        reserved
    }
    then each attribute block in descriptor order, then u32[3*T] index.
"""
import argparse
import os
import struct

import numpy as np

MAGIC = b'MVB1'
TYPES = {
    'f32':  (0, np.float32, None),
    'i8n':  (1, np.int8,    127.0),
    'u8n':  (2, np.uint8,   255.0),
    'u16n': (3, np.uint16,  65535.0),
}


def parse_attr(spec):
    name, rest = spec.split('=', 1)
    key, kind, comps = rest.split(':')
    if kind not in TYPES:
        raise SystemExit(f'unknown type {kind!r} in --attr {spec}')
    return name, key, kind, int(comps)


def encode(a, kind, comps):
    """-> (array of the stored dtype, components stored)."""
    code, dtype, scale = TYPES[kind]
    a = np.asarray(a, np.float32)
    if a.ndim == 1:
        a = a[:, None]
    if a.shape[1] != comps:
        raise SystemExit(f'attribute has {a.shape[1]} components, declared {comps}')

    stride = np.dtype(dtype).itemsize
    per = max(1, 4 // stride)                       # components per 4-byte word
    stored = ((comps + per - 1) // per) * per       # pad up to a whole word

    out = np.zeros((len(a), stored), dtype)
    if scale is None:
        out[:, :comps] = a
    else:
        lo = -scale if kind == 'i8n' else 0.0
        out[:, :comps] = np.clip(np.rint(a * scale), lo, scale).astype(dtype)
    return np.ascontiguousarray(out), stored


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='npz holding the mesh')
    ap.add_argument('--out', required=True)
    ap.add_argument('--faces', default='F', help='npz key for the face array')
    ap.add_argument('--attr', action='append', required=True,
                    help='shaderName=npzKey:type:components (repeatable)')
    args = ap.parse_args()

    d = np.load(args.src)
    attrs = [parse_attr(s) for s in args.attr]
    if attrs[0][0] != 'position':
        raise SystemExit('the first --attr must be position')

    F = np.asarray(d[args.faces])
    if F.shape[1] == 4:
        tris = np.concatenate([F[:, (0, 1, 2)], F[:, (0, 2, 3)]], 0)
    elif F.shape[1] == 3:
        tris = F
    else:
        raise SystemExit(f'faces must be tris or quads, got {F.shape[1]}-gons')
    tris = np.ascontiguousarray(tris, np.uint32)

    blocks, descs = [], []
    nvert = None
    for name, key, kind, comps in attrs:
        if key not in d:
            raise SystemExit(f'{args.src} has no array {key!r}')
        buf, stored = encode(d[key], kind, comps)
        if nvert is None:
            nvert = len(buf)
        elif len(buf) != nvert:
            raise SystemExit(f'{key}: {len(buf)} rows, expected {nvert}')
        if len(name.encode()) > 12:
            raise SystemExit(f'attribute name {name!r} is over 12 bytes')
        blocks.append(buf.tobytes())
        descs.append((name, TYPES[kind][0], comps, stored))

    pos = np.asarray(d[attrs[0][1]], np.float32)
    lo, hi = pos.min(0), pos.max(0)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or '.', exist_ok=True)
    with open(args.out, 'wb') as f:
        f.write(MAGIC)
        f.write(struct.pack('<III', nvert, len(tris), len(descs)))
        f.write(struct.pack('<6f', *lo, *hi))
        for name, code, comps, stored in descs:
            f.write(name.encode().ljust(12, b'\0'))
            f.write(struct.pack('<4B', code, comps, stored, 0))
        for b in blocks:
            f.write(b)
        f.write(tris.tobytes())

    size = os.path.getsize(args.out)
    print(f'{nvert} verts, {len(tris)} tris, {len(descs)} attrs '
          f'-> {args.out}  {size / 1e6:.1f} MB')
    print(f'bbox {lo} .. {hi}')


if __name__ == '__main__':
    main()
