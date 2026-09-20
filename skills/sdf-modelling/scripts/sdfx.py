"""Signed-distance modelling kit for the Paimon build.

Pure numpy, no Blender.  Two things live here:

  * a small SDF algebra -- one workhorse primitive (`Chain`, a swept ellipsoid
    chain) plus `Box`, combined with polynomial smooth min/max so muscle bellies
    fuse into each other the way flesh does rather than intersecting like solids;
  * a mesher -- naive surface nets, then alternating Laplacian smoothing and
    gradient reprojection, which turns the blocky dual mesh into a clean
    isosurface.

The field is evaluated two ways: over a regular grid (sliced per primitive
against its AABB, which is what makes a 20M-cell grid tractable) and over loose
point sets, for reprojection and for the detail pass.
"""
import numpy as np

BIG = np.float32(1e9)


# ---------------------------------------------------------------- combinators

def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + h * ((a - b) - k * (1.0 - h))


def smax(a, b, k):
    return -smin(-a, -b, k)


# ---------------------------------------------------------------- primitives

class Prim:
    def aabb(self):
        raise NotImplementedError

    def dist(self, P):
        raise NotImplementedError


class Chain(Prim):
    """Swept ellipsoid along a polyline.

    pts    (n,3) centres
    radii  (n,3) semi-axes, in the primitive's local frame
    axes   (3,3) orthonormal rows: the directions radii[:,0..2] refer to.
           Defaults to world XYZ.

    Distance is the scaled-sphere estimate of each swept segment, minimised over
    segments.  It underestimates near sharp tapers, which only ever makes the
    surface a touch fatter -- harmless here, and it stays C1, which is what the
    reprojection pass needs.
    """

    def __init__(self, pts, radii, axes=None):
        self.p = np.asarray(pts, np.float32).reshape(-1, 3)
        r = np.asarray(radii, np.float32)
        if r.ndim == 0:
            r = np.tile(r.reshape(1, 1), (len(self.p), 3))
        elif r.ndim == 1:
            if r.size == 3 and len(self.p) != 3:
                r = np.tile(r.reshape(1, 3), (len(self.p), 1))
            else:
                r = np.tile(r.reshape(-1, 1), (1, 3))
        self.r = np.ascontiguousarray(r, np.float32).reshape(-1, 3)
        assert len(self.p) == len(self.r) and len(self.p) >= 2, 'chain length mismatch'
        self.R = np.eye(3, dtype=np.float32) if axes is None \
            else np.ascontiguousarray(axes, np.float32).reshape(3, 3)

    def aabb(self):
        e = (np.abs(self.R).T @ self.r.T).T          # world extent of each ellipsoid
        return (self.p - e).min(0), (self.p + e).max(0)

    def dist(self, P):
        L = (P - self.p[0]) @ self.R.T               # into the local frame once
        a = (self.p - self.p[0]) @ self.R.T
        out = np.full(len(P), BIG, np.float32)
        for i in range(len(a) - 1):
            p0, p1 = a[i], a[i + 1]
            r0, r1 = self.r[i], self.r[i + 1]
            ab = p1 - p0
            den = float(ab @ ab)
            if den < 1e-12:
                t = np.zeros(len(L), np.float32)
            else:
                t = np.clip(((L - p0) @ ab) / den, 0.0, 1.0).astype(np.float32)
            c = p0 + t[:, None] * ab
            r = r0 + t[:, None] * (r1 - r0)
            q = (L - c) / r
            d = (np.sqrt((q * q).sum(1)) - 1.0) * r.min(1)
            np.minimum(out, d.astype(np.float32), out=out)
        return out


class Box(Prim):
    """Rounded box.  Used for carving -- the mouth slit, the pectoral cross."""

    def __init__(self, centre, half, axes=None, round=0.0):
        self.c = np.asarray(centre, np.float32)
        self.h = np.asarray(half, np.float32) - round
        self.rd = float(round)
        self.R = np.eye(3, dtype=np.float32) if axes is None \
            else np.ascontiguousarray(axes, np.float32).reshape(3, 3)

    def aabb(self):
        e = np.abs(self.R).T @ (self.h + self.rd)
        return self.c - e, self.c + e

    def dist(self, P):
        L = (P - self.c) @ self.R.T
        q = np.abs(L) - self.h
        outside = np.linalg.norm(np.maximum(q, 0.0), axis=1)
        inside = np.minimum(q.max(1), 0.0)
        return (outside + inside - self.rd).astype(np.float32)


# ---------------------------------------------------------------- the field

class Field:
    def __init__(self):
        self.ops = []

    def add(self, prim, k=0.0, tag=0):
        self.ops.append(('u', prim, float(k), int(tag)))
        return prim

    def sub(self, prim, k=0.0, tag=0):
        self.ops.append(('s', prim, float(k), int(tag)))
        return prim

    def bounds(self, pad=0.05):
        lo = np.full(3, 1e9, np.float32)
        hi = np.full(3, -1e9, np.float32)
        for mode, prim, k, _ in self.ops:
            if mode != 'u':
                continue
            a, b = prim.aabb()
            lo = np.minimum(lo, a)
            hi = np.maximum(hi, b)
        return lo - pad, hi + pad

    # -- grid evaluation, sliced per primitive
    def eval_grid(self, origin, voxel, shape, tags=False):
        G = np.full(shape, BIG, np.float32)
        T = np.zeros(shape, np.uint8) if tags else None
        ax = [origin[i] + voxel * np.arange(shape[i], dtype=np.float32) for i in range(3)]
        for mode, prim, k, tag in self.ops:
            lo, hi = prim.aabb()
            pad = k + 2.5 * voxel
            i0 = [max(0, int(np.floor((lo[i] - pad - origin[i]) / voxel))) for i in range(3)]
            i1 = [min(shape[i], int(np.ceil((hi[i] + pad - origin[i]) / voxel)) + 1) for i in range(3)]
            if any(i1[i] <= i0[i] for i in range(3)):
                continue
            sl = tuple(slice(i0[i], i1[i]) for i in range(3))
            gx, gy, gz = np.meshgrid(ax[0][sl[0]], ax[1][sl[1]], ax[2][sl[2]], indexing='ij')
            P = np.stack([gx.ravel(), gy.ravel(), gz.ravel()], 1)
            d = prim.dist(P).reshape(gx.shape)
            cur = G[sl]
            if mode == 'u':
                if T is not None:
                    T[sl] = np.where(d < cur, np.uint8(tag), T[sl])
                G[sl] = smin(cur, d, k)
            else:
                G[sl] = smax(cur, -d, k)
        return (G, T) if tags else G

    # -- loose point evaluation
    def eval(self, P):
        P = np.ascontiguousarray(P, np.float32)
        d = np.full(len(P), BIG, np.float32)
        for mode, prim, k, _ in self.ops:
            lo, hi = prim.aabb()
            pad = k + 1e-3
            m = np.all((P >= lo - pad) & (P <= hi + pad), 1)
            if not m.any():
                continue
            if mode == 'u':
                d[m] = smin(d[m], prim.dist(P[m]), k)
            else:
                d[m] = smax(d[m], -prim.dist(P[m]), k)
        return d

    def normals(self, P, e=2e-4):
        """Surface normal from the field gradient.

        Points outside every primitive's bounding box evaluate to BIG on both
        sides, so their gradient is zero and no direction can be recovered.
        Those get a fallback that at least points away from the body axis,
        rather than a silent zero that leaves a caller's projection untouched.
        """
        g = np.empty_like(P)
        for i in range(3):
            o = np.zeros(3, np.float32)
            o[i] = e
            g[:, i] = self.eval(P + o) - self.eval(P - o)
        n = np.linalg.norm(g, axis=1, keepdims=True)
        dead = (n < 1e-9).ravel()
        if dead.any():
            f = P[dead].copy()
            f[:, 2] = 0.0
            fn = np.linalg.norm(f, axis=1, keepdims=True)
            g[dead] = np.where(fn > 1e-6, f / np.maximum(fn, 1e-9),
                               np.array([0.0, 1.0, 0.0], np.float32))
            n = np.linalg.norm(g, axis=1, keepdims=True)
        return g / np.maximum(n, 1e-12)


# ---------------------------------------------------------------- surface nets

_CORN = [(i >> 2 & 1, i >> 1 & 1, i & 1) for i in range(8)]
_EDGES = [(a, b) for a in range(8) for b in range(a + 1, 8)
          if sum(abs(_CORN[a][i] - _CORN[b][i]) for i in range(3)) == 1]


def surface_nets(G, origin, voxel):
    """One vertex per sign-changing cell, one quad per sign-changing grid edge."""
    nx, ny, nz = G.shape
    c = [G[dx:nx - 1 + dx, dy:ny - 1 + dy, dz:nz - 1 + dz] for dx, dy, dz in _CORN]
    s = [x < 0 for x in c]
    acc = np.zeros((nx - 1, ny - 1, nz - 1, 3), np.float32)
    cnt = np.zeros((nx - 1, ny - 1, nz - 1), np.float32)
    for a, b in _EDGES:
        cross = s[a] ^ s[b]
        if not cross.any():
            continue
        ca, cb = c[a], c[b]
        den = ca - cb
        t = np.where(cross, ca / np.where(np.abs(den) < 1e-20, 1e-20, den), 0.0)
        t = np.clip(t, 0.0, 1.0).astype(np.float32)
        pa = np.array(_CORN[a], np.float32)
        pb = np.array(_CORN[b], np.float32)
        for i in range(3):
            acc[..., i] += np.where(cross, pa[i] + t * (pb[i] - pa[i]), 0.0)
        cnt += cross
    active = cnt > 0
    idx = np.full((nx - 1, ny - 1, nz - 1), -1, np.int64)
    n = int(active.sum())
    idx[active] = np.arange(n)
    ci, cj, ck = np.nonzero(active)
    off = acc[active] / cnt[active][:, None]
    V = (np.stack([ci, cj, ck], 1).astype(np.float32) + off) * voxel + np.asarray(origin, np.float32)

    quads = []
    sg = G < 0
    for axis in range(3):
        sl0 = [slice(1, None)] * 3
        sl1 = [slice(1, None)] * 3
        sl0[axis] = slice(0, -1)
        sl1[axis] = slice(1, None)
        a = sg[tuple(sl0)]
        b = sg[tuple(sl1)]
        cross = a ^ b
        if not cross.any():
            continue
        loc = list(np.nonzero(cross))
        base = [loc[0], loc[1], loc[2]]
        base[axis] = base[axis]                     # grid index along the edge axis
        d1, d2 = (axis + 1) % 3, (axis + 2) % 3
        corners = []
        for o1, o2 in ((0, 0), (1, 0), (1, 1), (0, 1)):
            ci_ = [None] * 3
            ci_[axis] = base[axis]
            ci_[d1] = base[d1] - 1 + o1 + 1
            ci_[d2] = base[d2] - 1 + o2 + 1
            corners.append(idx[ci_[0], ci_[1], ci_[2]])
        q = np.stack(corners, 1)
        ok = (q >= 0).all(1)
        q = q[ok]
        flip = ~a[tuple(loc)][ok]
        q = np.where(flip[:, None], q[:, ::-1], q)
        quads.append(q)
    F = np.concatenate(quads, 0) if quads else np.zeros((0, 4), np.int64)
    return V, F


def adjacency(V, F):
    a = F
    b = np.roll(F, -1, axis=1)
    i = np.concatenate([a.ravel(), b.ravel()])
    j = np.concatenate([b.ravel(), a.ravel()])
    return i, j


def relax(field, V, F, rounds=5, lam=0.55, project=True, proj_steps=1, e=3e-4):
    """Laplacian smoothing alternated with a Newton step back onto the surface.

    The gradient uses forward differences and reuses the centre sample, so a
    projection costs four field evaluations rather than seven -- on a 165k-vertex
    mesh over a 300-primitive field that is the difference between a minute and
    a quarter of one."""
    i, j = adjacency(V, F)
    deg = np.bincount(i, minlength=len(V)).astype(np.float32)
    deg[deg == 0] = 1.0
    for _ in range(rounds):
        s = np.zeros_like(V)
        np.add.at(s, i, V[j])
        V = V + lam * (s / deg[:, None] - V)
        if project:
            for _ in range(proj_steps):
                d = field.eval(V)
                g = np.empty_like(V)
                for ax in range(3):
                    o = np.zeros(3, np.float32)
                    o[ax] = e
                    g[:, ax] = field.eval(V + o) - d
                nrm = np.linalg.norm(g, axis=1, keepdims=True)
                g = g / np.maximum(nrm, 1e-12)
                V = V - g * d[:, None]
    return np.ascontiguousarray(V, np.float32)


def vertex_normals(V, F):
    N = np.zeros_like(V)
    for t in ((0, 1, 2), (0, 2, 3)):
        p0, p1, p2 = V[F[:, t[0]]], V[F[:, t[1]]], V[F[:, t[2]]]
        fn = np.cross(p1 - p0, p2 - p0)
        for c in t:
            np.add.at(N, F[:, c], fn)
    n = np.linalg.norm(N, axis=1, keepdims=True)
    return N / np.maximum(n, 1e-12)


def smooth_attr(V, F, A, rounds=2, lam=0.5):
    i, j = adjacency(V, F)
    deg = np.bincount(i, minlength=len(V)).astype(np.float32)
    deg[deg == 0] = 1.0
    A = np.array(A, np.float32)
    two = A.ndim == 2
    for _ in range(rounds):
        s = np.zeros_like(A)
        np.add.at(s, i, A[j])
        m = s / (deg[:, None] if two else deg)
        A = A + lam * (m - A)
    return A
