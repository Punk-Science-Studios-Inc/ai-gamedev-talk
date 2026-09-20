/* Streaming loader for the binary written by scripts/pack_mesh.py.
 *
 * No imports and no exports: this is meant to be concatenated into the one
 * inline <script type="module"> alongside the vendored three.js build, so
 * `THREE` is already in scope. Keep the top-level names long - minified three
 * has taken every short one.
 *
 * Decoding is views onto the fetched ArrayBuffer, so nothing is copied and
 * nothing is allocated per vertex. The format is self-describing, so this file
 * does not change when the model gains an attribute.
 */

const MESHBIN_TYPES = [
  { Ctor: Float32Array, normalized: false },   // 0 f32
  { Ctor: Int8Array,    normalized: true  },   // 1 i8n
  { Ctor: Uint8Array,   normalized: true  },   // 2 u8n
  { Ctor: Uint16Array,  normalized: true  },   // 3 u16n
];

/* Fetch with a progress callback. Deliberately not res.arrayBuffer(): a
 * multi-megabyte mesh has to show a percentage or the page reads as hung.
 * content-length is absent under some compression settings, hence the byte
 * count fallback the caller can fall back on displaying. */
async function fetchMeshBuffer(url, onProgress) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(url + ': ' + res.status);
  const total = Number(res.headers.get('content-length') || 0);
  const chunks = [];
  let got = 0;
  const reader = res.body.getReader();
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    got += value.length;
    if (onProgress) onProgress(total ? got / total : 0, got);
  }
  const buf = new Uint8Array(got);
  let off = 0;
  for (const c of chunks) { buf.set(c, off); off += c.length; }
  return buf.buffer;
}

function decodeMeshBuffer(buffer) {
  const head = new DataView(buffer);
  const magic = String.fromCharCode(head.getUint8(0), head.getUint8(1),
                                    head.getUint8(2), head.getUint8(3));
  // A magic check turns "the model is invisible" into a one-line error.
  if (magic !== 'MVB1') throw new Error('bad mesh magic: ' + magic);

  const nVert = head.getUint32(4, true);
  const nTri = head.getUint32(8, true);
  const nAttr = head.getUint32(12, true);
  const bbox = {
    min: [head.getFloat32(16, true), head.getFloat32(20, true), head.getFloat32(24, true)],
    max: [head.getFloat32(28, true), head.getFloat32(32, true), head.getFloat32(36, true)],
  };

  let p = 40;
  const descs = [];
  for (let i = 0; i < nAttr; i++) {
    let name = '';
    for (let c = 0; c < 12; c++) {
      const ch = head.getUint8(p + c);
      if (ch) name += String.fromCharCode(ch);
    }
    descs.push({
      name,
      type: head.getUint8(p + 12),
      comps: head.getUint8(p + 13),
      stored: head.getUint8(p + 14),
    });
    p += 16;
  }

  const geometry = new THREE.BufferGeometry();
  for (const d of descs) {
    const t = MESHBIN_TYPES[d.type];
    if (!t) throw new Error('unknown attribute type ' + d.type + ' for ' + d.name);
    const view = new t.Ctor(buffer, p, nVert * d.stored);
    p += view.byteLength;
    // `stored` is the padded stride, so itemSize is the padded width, not the
    // declared one. That is safe even for `normal`, which three.js declares as
    // a vec3 in its own vertex prefix: a vec3 fed a 4-wide attribute pointer
    // takes x, y, z and drops the padding channel.
    geometry.setAttribute(d.name,
      new THREE.BufferAttribute(view, d.stored, t.normalized));
  }
  geometry.setIndex(new THREE.BufferAttribute(new Uint32Array(buffer, p, nTri * 3), 1));
  geometry.computeBoundingSphere();

  return { geometry, verts: nVert, tris: nTri, bbox };
}

async function loadMesh(url, onProgress) {
  return decodeMeshBuffer(await fetchMeshBuffer(url, onProgress));
}
