"""Surface probe -- write this on day one.

Given spec coordinates, print where the surface actually is relative to them.
Three of the worst bugs in the build this skill came from were probe-shaped and
were instead found by rendering, at a rebuild each:

  * back muscles specified at depths that put them inside the torso shell, so
    the whole back rendered as a bare slab;
  * a mouth curve floating outside the face, so the cut never reached the skin;
  * spine beads seeded outside every primitive's bounding box, where the field
    has no gradient, so they never projected and floated off the body.

All three are one line of output here.

Adapt the two imports and `COORD` to the project, then:

    python probe.py 0.70 0.026 0.010        # a single spec coordinate
    python probe.py --scan back 0.45 0.85   # the surface depth up a whole run
"""
import argparse
import sys

import numpy as np

import spec as S            # the project's parameter file
import build as B           # the project's field builder (build_field())


def probe(F, coords):
    """coords: iterable of spec-space tuples, e.g. (h, x, d)"""
    P = np.asarray([S.P(*c) for c in coords], np.float32)
    d = F.eval(P)
    n = F.normals(P)
    surf = P - n * d[:, None]
    print(f'{"coordinate":>26}  {"sdf":>9}  nearest surface (world)')
    for c, dist, s in zip(coords, d, surf):
        flag = ''
        if dist > 1e8:
            flag = '   <-- OUTSIDE EVERY BOUNDING BOX: no gradient here'
        elif dist > 0.02:
            flag = '   <-- floating clear of the surface'
        elif dist < -0.02:
            flag = '   <-- buried inside the mass'
        txt = ', '.join(f'{v:+.3f}' for v in c)
        print(f'  ({txt:>22})  {dist:+9.4f}  '
              f'({s[0]:+.3f}, {s[1]:+.3f}, {s[2]:+.3f}){flag}')


def scan(F, side, lo, hi, n=16, x=0.0):
    """Walk a height range and report where the front and back of the form sit.

    This is the table to check every depth number in the spec against.  Keep it
    printed; guessing it per-muscle is where the arithmetic errors come from.
    """
    print(f'{"h":>6}  {"back d":>8}  {"front d":>8}  {"depth":>8}')
    for h in np.linspace(lo, hi, n):
        row = []
        for d in np.linspace(-0.10, 0.30, 401):
            row.append(F.eval(np.asarray([S.P(h, x, d)], np.float32))[0])
        row = np.asarray(row)
        inside = np.nonzero(row < 0)[0]
        if len(inside) == 0:
            print(f'{h:6.3f}       --        --        --')
            continue
        ds = np.linspace(-0.10, 0.30, 401)
        print(f'{h:6.3f}  {ds[inside[0]]:8.3f}  {ds[inside[-1]]:8.3f}  '
              f'{ds[inside[-1]] - ds[inside[0]]:8.3f}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('coords', nargs='*', type=float)
    ap.add_argument('--scan', nargs=3, metavar=('SIDE', 'LO', 'HI'))
    ap.add_argument('--x', type=float, default=0.0)
    a = ap.parse_args()

    F = B.build_field()
    if a.scan:
        scan(F, a.scan[0], float(a.scan[1]), float(a.scan[2]), x=a.x)
        return
    if len(a.coords) % 3:
        sys.exit('give coordinates in triples')
    probe(F, [tuple(a.coords[i:i + 3]) for i in range(0, len(a.coords), 3)])


if __name__ == '__main__':
    main()
