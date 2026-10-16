/* DICOM Viewer – läuft komplett im Browser. Keine Datei verlässt das Gerät. */
(function () {
  'use strict';
  const $ = (s) => document.querySelector(s);
  const TS = {
    '1.2.840.10008.1.2': 'Implicit VR Little Endian',
    '1.2.840.10008.1.2.1': 'Explicit VR Little Endian',
    '1.2.840.10008.1.2.2': 'Explicit VR Big Endian',
    '1.2.840.10008.1.2.4.50': 'JPEG Baseline (8 Bit)',
    '1.2.840.10008.1.2.4.51': 'JPEG Extended (12 Bit)',
    '1.2.840.10008.1.2.4.57': 'JPEG Lossless',
    '1.2.840.10008.1.2.4.70': 'JPEG Lossless SV1',
    '1.2.840.10008.1.2.4.80': 'JPEG-LS Lossless',
    '1.2.840.10008.1.2.4.81': 'JPEG-LS Near-Lossless',
    '1.2.840.10008.1.2.4.90': 'JPEG 2000 Lossless',
    '1.2.840.10008.1.2.4.91': 'JPEG 2000',
    '1.2.840.10008.1.2.5': 'RLE Lossless',
    '1.2.840.10008.1.2.1.99': 'Deflated Explicit VR Little Endian'
  };
  const UNCOMP = ['1.2.840.10008.1.2', '1.2.840.10008.1.2.1', '1.2.840.10008.1.2.2'];
  const JPEG_BROWSER = ['1.2.840.10008.1.2.4.50'];
  const NAMES = {
    x00020010: 'Transfer Syntax', x00080020: 'Studiendatum', x00080030: 'Studienzeit', x00080060: 'Modalität',
    x00080070: 'Hersteller', x00080080: 'Einrichtung', x00080090: 'Überweiser', x00081030: 'Studienbeschreibung',
    x0008103e: 'Serienbeschreibung', x00081090: 'Gerätemodell', x00100010: 'Patientenname', x00100020: 'Patienten-ID',
    x00100030: 'Geburtsdatum', x00100040: 'Geschlecht', x00101010: 'Alter', x00180015: 'Körperregion',
    x00180050: 'Schichtdicke', x00180080: 'Repetitionszeit (TR)', x00180081: 'Echozeit (TE)', x00180087: 'Feldstärke',
    x00181030: 'Protokoll', x0020000d: 'Study Instance UID', x0020000e: 'Series Instance UID', x00200011: 'Seriennummer',
    x00200013: 'Bildnummer', x00201041: 'Schichtposition', x00280002: 'Samples per Pixel', x00280004: 'Photometrie',
    x00280008: 'Anzahl Frames', x00280010: 'Zeilen', x00280011: 'Spalten', x00280030: 'Pixelabstand',
    x00280100: 'Bits Allocated', x00280101: 'Bits Stored', x00280103: 'Pixel-Darstellung', x00281050: 'Fensterzentrum',
    x00281051: 'Fensterbreite', x00281052: 'Rescale Intercept', x00281053: 'Rescale Slope', x7fe00010: 'Pixeldaten'
  };
  const PHI = ['x00100010', 'x00100020', 'x00100030', 'x00080080', 'x00080090'];
  const TEXT_VR = ['AE','AS','CS','DA','DS','DT','IS','LO','LT','PN','SH','ST','TM','UI','UT','UC','UR'];

  const state = { series: [], cur: null, idx: 0, ww: 400, wc: 40, zoom: 1, px: 0, py: 0, mode: 'wl', notes: [] };
  const canvas = $('#view'), ctx = canvas.getContext('2d');
  const off = document.createElement('canvas'), offCtx = off.getContext('2d');

  function msg(text, err) { const m = $('#msg'); m.textContent = text; m.className = 'msg' + (err ? ' err' : ''); m.hidden = !text; }
  function str(ds, t) { try { const v = ds.string(t); return v == null ? '' : v.trim(); } catch (e) { return ''; } }
  function num(ds, t, d) { const v = parseFloat(str(ds, t).split('\\')[0]); return isFinite(v) ? v : d; }
  function us(ds, t, d) { try { const v = ds.uint16(t); return v == null ? d : v; } catch (e) { return d; } }
  function pn(s) { return (s || '').replace(/\^+/g, ' ').trim(); }
  function dt(s) { return /^\d{8}$/.test(s) ? s.slice(6) + '.' + s.slice(4, 6) + '.' + s.slice(0, 4) : s; }

  // ---------- Dateien einsammeln (inkl. Ordner) ----------
  async function walkEntry(entry, out) {
    if (entry.isFile) { await new Promise((r) => entry.file((f) => { out.push(f); r(); }, r)); }
    else if (entry.isDirectory) {
      const reader = entry.createReader();
      let batch;
      do { batch = await new Promise((r) => reader.readEntries(r, () => r([]))); for (const e of batch) await walkEntry(e, out); } while (batch.length);
    }
  }
  async function fromDrop(dt) {
    const out = [], items = [...(dt.items || [])];
    const entries = items.map((i) => i.webkitGetAsEntry && i.webkitGetAsEntry()).filter(Boolean);
    if (entries.length) { for (const e of entries) await walkEntry(e, out); return out; }
    return [...dt.files];
  }

  // ---------- Parsen ----------
  function isDicomBuf(u8, name) {
    if (u8.length > 132 && u8[128] === 68 && u8[129] === 73 && u8[130] === 67 && u8[131] === 77) return true;
    return /\.(dcm|dicom|dic|ima)$/i.test(name); // ältere Dateien ohne Präambel
  }
  async function loadFiles(files) {
    msg('Lese ' + files.length + ' Datei(en) …');
    let ok = 0, skipped = 0, dicomdir = false; const errs = new Set();
    const map = new Map();
    for (const s of state.series) map.set(s.uid, s);
    for (const f of files) {
      if (/(^|\/)DICOMDIR$/i.test(f.name)) { dicomdir = true; continue; }
      if (f.size < 132 || f.size > 1.5e9) { skipped++; continue; }
      let u8;
      try { u8 = new Uint8Array(await f.arrayBuffer()); } catch (e) { skipped++; continue; }
      if (!isDicomBuf(u8, f.name)) { skipped++; continue; }
      let ds;
      try { ds = dicomParser.parseDicom(u8); } catch (e) { skipped++; errs.add('Nicht lesbar: ' + f.name); continue; }
      if (str(ds, 'x00041200') || str(ds, 'x00020002') === '1.2.840.10008.1.3.10') { dicomdir = true; continue; }
      if (!ds.elements.x7fe00010) { skipped++; continue; }
      const ts = str(ds, 'x00020010') || '1.2.840.10008.1.2';
      const frames = Math.max(1, parseInt(str(ds, 'x00280008')) || 1);
      const uid = str(ds, 'x0020000e') || ('datei-' + f.name);
      let s = map.get(uid);
      if (!s) {
        s = { uid, patient: pn(str(ds, 'x00100010')) || 'Unbekannt', pid: str(ds, 'x00100020'), study: str(ds, 'x00081030') || 'Studie',
          studyUid: str(ds, 'x0020000d'), date: dt(str(ds, 'x00080020')), desc: str(ds, 'x0008103e') || 'Serie ' + (str(ds, 'x00200011') || ''),
          modality: str(ds, 'x00080060'), images: [] };
        map.set(uid, s);
      }
      for (let fr = 0; fr < frames; fr++) s.images.push({ ds, u8, name: f.name, frame: fr, ts, inst: num(ds, 'x00200013', 0), loc: num(ds, 'x00201041', NaN) });
      ok++;
    }
    state.series = [...map.values()];
    state.series.forEach((s) => s.images.sort((a, b) => (isFinite(a.loc) && isFinite(b.loc) && a.inst === b.inst ? a.loc - b.loc : a.inst - b.inst) || a.frame - b.frame));
    const parts = [ok + ' DICOM-Bild(er) geladen'];
    if (dicomdir) parts.push('DICOMDIR erkannt (CD-Inhaltsverzeichnis, Bilder werden direkt gelesen)');
    if (skipped) parts.push(skipped + ' Datei(en) übersprungen');
    if (!ok) { msg('Keine DICOM-Bilder gefunden. ' + (dicomdir ? 'Es wurde nur das DICOMDIR gewählt – bitte den ganzen Ordner der CD laden.' : 'Bitte .dcm-Dateien oder den Ordner der CD wählen.'), true); return; }
    msg(parts.join(' · '));
    $('#app').hidden = false;
    renderTree();
    if (!state.cur) selectSeries(state.series[0]);
  }

  // ---------- Pixel dekodieren ----------
  async function decode(img) {
    if (img.pix) return img.pix;
    const ds = img.ds, ts = img.ts;
    const rows = us(ds, 'x00280010', 0), cols = us(ds, 'x00280011', 0);
    const spp = us(ds, 'x00280002', 1), bits = us(ds, 'x00280100', 16), signed = us(ds, 'x00280103', 0) === 1;
    const photo = str(ds, 'x00280004') || 'MONOCHROME2', planar = us(ds, 'x00280006', 0);
    const slope = num(ds, 'x00281053', 1), inter = num(ds, 'x00281052', 0);
    if (!rows || !cols) throw new Error('Bildgröße fehlt.');
    const n = rows * cols, pe = ds.elements.x7fe00010;
    let out;
    if (UNCOMP.includes(ts)) {
      const be = ts === '1.2.840.10008.1.2.2';
      const bpp = bits / 8, frameBytes = n * spp * bpp;
      const start = pe.dataOffset + img.frame * frameBytes;
      if (start + frameBytes > img.u8.length) throw new Error('Pixeldaten unvollständig.');
      const dv = new DataView(img.u8.buffer, img.u8.byteOffset + start, frameBytes);
      if (spp === 3) {
        const rgb = new Uint8ClampedArray(n * 4);
        for (let i = 0; i < n; i++) for (let c = 0; c < 3; c++) rgb[i * 4 + c] = dv.getUint8(planar ? c * n + i : i * 3 + c);
        if (/^YBR_FULL/.test(photo)) ybr(rgb);
        out = { rgb, rows, cols };
      } else {
        const v = new Float32Array(n);
        for (let i = 0; i < n; i++) {
          let x = bits === 8 ? (signed ? dv.getInt8(i) : dv.getUint8(i)) : bits === 32 ? (signed ? dv.getInt32(i * 4, !be) : dv.getUint32(i * 4, !be)) : (signed ? dv.getInt16(i * 2, !be) : dv.getUint16(i * 2, !be));
          v[i] = x * slope + inter;
        }
        out = { v, rows, cols, mono1: photo === 'MONOCHROME1' };
      }
    } else if (JPEG_BROWSER.includes(ts)) {
      let frag;
      try {
        const bot = pe.basicOffsetTable && pe.basicOffsetTable.length ? pe.basicOffsetTable : dicomParser.createJPEGBasicOffsetTable(ds, pe);
        frag = dicomParser.readEncapsulatedImageFrame(ds, pe, img.frame, bot);
      } catch (e) { frag = dicomParser.readEncapsulatedPixelDataFromFragments(ds, pe, 0); }
      const bmp = await createImageBitmap(new Blob([frag], { type: 'image/jpeg' }));
      const c = document.createElement('canvas'); c.width = bmp.width; c.height = bmp.height;
      const cx = c.getContext('2d'); cx.drawImage(bmp, 0, 0);
      const d = cx.getImageData(0, 0, c.width, c.height).data;
      if (spp === 3) out = { rgb: new Uint8ClampedArray(d), rows: c.height, cols: c.width };
      else { const v = new Float32Array(c.width * c.height); for (let i = 0; i < v.length; i++) v[i] = d[i * 4] * slope + inter; out = { v, rows: c.height, cols: c.width, mono1: photo === 'MONOCHROME1' }; }
    } else {
      throw new Error('Dieses Bild ist mit „' + (TS[ts] || ts) + '“ komprimiert. Das kann der Viewer im Browser leider noch nicht entpacken. Unterstützt: unkomprimiert und JPEG Baseline.');
    }
    if (out.v) {
      let mn = Infinity, mx = -Infinity; for (const x of out.v) { if (x < mn) mn = x; if (x > mx) mx = x; }
      out.min = mn; out.max = mx;
      const wc = num(ds, 'x00281050', NaN), ww = num(ds, 'x00281051', NaN);
      out.wc = isFinite(wc) && ww > 1 ? wc : (mn + mx) / 2; out.ww = isFinite(wc) && ww > 1 ? ww : Math.max(1, mx - mn);
    }
    img.pix = out; return out;
  }
  function ybr(a) {
    for (let i = 0; i < a.length; i += 4) { const y = a[i], cb = a[i + 1] - 128, cr = a[i + 2] - 128;
      a[i] = y + 1.402 * cr; a[i + 1] = y - 0.344136 * cb - 0.714136 * cr; a[i + 2] = y + 1.772 * cb; }
  }
  function toImageData(p, wc, ww, target) {
    const id = target.createImageData(p.cols, p.rows), d = id.data;
    if (p.rgb) { d.set(p.rgb); for (let i = 3; i < d.length; i += 4) d[i] = 255; return id; }
    const lo = wc - ww / 2, sc = 255 / ww;
    for (let i = 0, j = 0; i < p.v.length; i++, j += 4) {
      let g = (p.v[i] - lo) * sc; g = g < 0 ? 0 : g > 255 ? 255 : g; if (p.mono1) g = 255 - g;
      d[j] = d[j + 1] = d[j + 2] = g; d[j + 3] = 255;
    }
    return id;
  }

  // ---------- UI ----------
  function renderTree() {
    const tree = $('#tree'); tree.innerHTML = '';
    const byPat = {};
    state.series.forEach((s) => { (byPat[s.patient + '|' + s.pid] ||= {})[s.studyUid + '|' + s.study] ||= []; byPat[s.patient + '|' + s.pid][s.studyUid + '|' + s.study].push(s); });
    let pi = 0; const sp = $('#phiToggle').checked;
    for (const [pk, studies] of Object.entries(byPat)) { pi++;
      const pd = document.createElement('details'); pd.open = true;
      pd.innerHTML = '<summary class="phi">👤 <span></span></summary>'; pd.querySelector('span').textContent = sp ? pk.split('|')[0] : 'Patient ' + pi + ' (Name ausgeblendet)';
      for (const [sk, list] of Object.entries(studies)) {
        const sd = document.createElement('div'); sd.className = 'study';
        const h = document.createElement('div'); h.className = 'study-h'; h.textContent = sk.split('|')[1] + (list[0].date ? ' · ' + list[0].date : ''); sd.append(h);
        for (const s of list) {
          const b = document.createElement('button'); b.type = 'button'; b.className = 'series'; s.btn = b;
          const c = document.createElement('canvas'); c.width = c.height = 64; c.className = 'thumb';
          const t = document.createElement('span'); t.innerHTML = '<b></b><small></small>';
          t.querySelector('b').textContent = s.desc; t.querySelector('small').textContent = (s.modality || '') + ' · ' + s.images.length + ' Bild' + (s.images.length > 1 ? 'er' : '');
          b.append(c, t); b.onclick = () => selectSeries(s); sd.append(b);
          thumb(s, c);
        }
        pd.append(sd);
      }
      tree.append(pd);
    }
  }
  async function thumb(s, c) {
    try { const p = await decode(s.images[Math.floor(s.images.length / 2)]);
      off.width = p.cols; off.height = p.rows; offCtx.putImageData(toImageData(p, p.wc, p.ww, offCtx), 0, 0);
      const cx = c.getContext('2d'), k = Math.min(64 / p.cols, 64 / p.rows);
      cx.fillStyle = '#000'; cx.fillRect(0, 0, 64, 64); cx.drawImage(off, (64 - p.cols * k) / 2, (64 - p.rows * k) / 2, p.cols * k, p.rows * k);
    } catch (e) { const cx = c.getContext('2d'); cx.fillStyle = '#3a1d1d'; cx.fillRect(0, 0, 64, 64); cx.fillStyle = '#f87171'; cx.font = '28px sans-serif'; cx.fillText('!', 26, 42); }
  }
  async function selectSeries(s) {
    state.series.forEach((x) => x.btn && x.btn.classList.toggle('active', x === s));
    state.cur = s; state.idx = Math.floor((s.images.length - 1) / 2); state.zoom = 1; state.px = state.py = 0; state.wlSet = false;
    const sl = $('#slice'); sl.max = s.images.length - 1; sl.value = state.idx; sl.disabled = s.images.length < 2;
    await show();
  }
  async function show() {
    const s = state.cur; if (!s) return;
    const img = s.images[state.idx];
    $('#slice').value = state.idx; $('#sliceLbl').textContent = (state.idx + 1) + ' / ' + s.images.length;
    try {
      const p = await decode(img);
      if (!state.wlSet && p.v) { state.wc = p.wc; state.ww = p.ww; state.wlSet = true; }
      state.p = p; $('#err').hidden = true; draw();
    } catch (e) { state.p = null; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height); const er = $('#err'); er.textContent = e.message; er.hidden = false; }
    overlay(img); tags(img);
  }
  function fit() { const r = canvas.parentElement.getBoundingClientRect(); const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, r.width * dpr); canvas.height = Math.max(1, r.height * dpr); }
  function draw() {
    const p = state.p; if (!p) return; fit();
    off.width = p.cols; off.height = p.rows; offCtx.putImageData(toImageData(p, state.wc, state.ww, offCtx), 0, 0);
    paintRedact(offCtx, state.cur.images[state.idx], state.tmpRect);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    const k = Math.min(canvas.width / p.cols, canvas.height / p.rows) * state.zoom, dpr = window.devicePixelRatio || 1;
    ctx.imageSmoothingEnabled = k < 3;
    ctx.translate(canvas.width / 2 + state.px * dpr, canvas.height / 2 + state.py * dpr);
    ctx.drawImage(off, -p.cols * k / 2, -p.rows * k / 2, p.cols * k, p.rows * k);
    $('#wlLbl').textContent = p.v ? 'F: ' + Math.round(state.wc) + ' / ' + Math.round(state.ww) : 'Farbbild';
    $('#zoomLbl').textContent = Math.round(state.zoom * 100) + ' %';
  }
  function toImg(e) {
    const p = state.p, r = canvas.getBoundingClientRect(), dpr = window.devicePixelRatio || 1;
    const k = Math.min(canvas.width / p.cols, canvas.height / p.rows) * state.zoom;
    const sx = (e.clientX - r.left) * dpr - canvas.width / 2 - state.px * dpr, sy = (e.clientY - r.top) * dpr - canvas.height / 2 - state.py * dpr;
    return { x: Math.max(0, Math.min(p.cols, sx / k + p.cols / 2)), y: Math.max(0, Math.min(p.rows, sy / k + p.rows / 2)) };
  }
  function rects(img) { return (img.redact ||= []); }
  function paintRedact(cx, img, extra) {
    cx.fillStyle = '#000';
    for (const r of rects(img).concat(extra ? [extra] : [])) cx.fillRect(Math.min(r.x0, r.x1), Math.min(r.y0, r.y1), Math.abs(r.x1 - r.x0), Math.abs(r.y1 - r.y0));
  }
  function overlay(img) {
    const ds = img.ds, show = $('#phiToggle').checked;
    $('#ovTL').textContent = show ? pn(str(ds, 'x00100010')) + '\n' + str(ds, 'x00100020') + '\n' + dt(str(ds, 'x00100030')) : '';
    $('#ovTR').textContent = [str(ds, 'x00080060'), str(ds, 'x0008103e'), dt(str(ds, 'x00080020'))].filter(Boolean).join('\n');
    $('#ovBL').textContent = (TS[img.ts] || img.ts);
  }
  function tags(img) {
    const ds = img.ds, tb = $('#tagBody'), q = $('#tagFilter').value.toLowerCase(); tb.innerHTML = '';
    const showPhi = $('#phiToggle').checked;
    for (const [tag, el] of Object.entries(ds.elements)) {
      if (tag === 'x7fe00010') continue;
      let val = '';
      if (el.items) val = '[Sequenz, ' + el.items.length + ' Einträge]';
      else if (!el.vr || TEXT_VR.includes(el.vr)) { val = str(ds, tag); if (val.length > 120 || /[\x00-\x08]/.test(val)) val = val.replace(/[\x00-\x1f]/g, '').slice(0, 120); }
      else if (el.vr === 'US' && el.length === 2) val = String(ds.uint16(tag));
      else if (el.vr === 'UL' && el.length === 4) val = String(ds.uint32(tag));
      else val = '(' + el.length + ' Byte, ' + el.vr + ')';
      if (PHI.includes(tag) && !showPhi) val = '••• ausgeblendet';
      const name = NAMES[tag] || '';
      const t = '(' + tag.slice(1, 5) + ',' + tag.slice(5) + ')';
      if (q && !(t + name + val).toLowerCase().includes(q)) continue;
      const tr = document.createElement('tr');
      [t, el.vr || '', name, val].forEach((x) => { const td = document.createElement('td'); td.textContent = x; tr.append(td); });
      tb.append(tr);
    }
  }
  function exportImg(type) {
    const p = state.p; if (!p) return;
    const c = document.createElement('canvas'); c.width = p.cols; c.height = p.rows; const cx = c.getContext('2d');
    cx.putImageData(toImageData(p, state.wc, state.ww, cx), 0, 0);
    paintRedact(cx, state.cur.images[state.idx]);
    if ($('#phiExport').checked && $('#phiToggle').checked) {
      const ds = state.cur.images[state.idx].ds; cx.fillStyle = '#ffff00'; cx.font = Math.max(12, p.cols / 40) + 'px sans-serif';
      cx.fillText(pn(str(ds, 'x00100010')) + '  ' + dt(str(ds, 'x00080020')), 8, Math.max(16, p.cols / 30));
    }
    c.toBlob((b) => { const a = document.createElement('a'); a.href = URL.createObjectURL(b);
      a.download = 'bild-' + (state.idx + 1) + (type === 'image/png' ? '.png' : '.jpg'); a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); }, type, 0.92);
  }

  // ---------- Events ----------
  const drop = $('#drop');
  ['dragenter', 'dragover'].forEach((e) => document.addEventListener(e, (ev) => { ev.preventDefault(); drop.classList.add('over'); }));
  ['dragleave', 'drop'].forEach((e) => document.addEventListener(e, (ev) => { ev.preventDefault(); if (e === 'drop' || !ev.relatedTarget) drop.classList.remove('over'); }));
  document.addEventListener('drop', async (ev) => { const f = await fromDrop(ev.dataTransfer); if (f.length) loadFiles(f); });
  $('#fileIn').onchange = (e) => { loadFiles([...e.target.files]); e.target.value = ''; };
  $('#dirIn').onchange = (e) => { loadFiles([...e.target.files]); e.target.value = ''; };
  $('#slice').oninput = (e) => { state.idx = +e.target.value; show(); };
  document.querySelectorAll('[data-mode]').forEach((b) => b.onclick = () => { state.mode = b.dataset.mode; document.querySelectorAll('[data-mode]').forEach((x) => x.classList.toggle('on', x === b)); });
  $('#reset').onclick = () => { state.zoom = 1; state.px = state.py = 0; if (state.p && state.p.v) { state.wc = state.p.wc; state.ww = state.p.ww; } draw(); };
  $('#invert').onclick = () => { if (state.p && state.p.v) { state.p.mono1 = !state.p.mono1; draw(); } };
  $('#png').onclick = () => exportImg('image/png');
  $('#jpg').onclick = () => exportImg('image/jpeg');
  $('#phiToggle').onchange = () => { if (state.series.length) { renderTree(); state.series.forEach((x) => x.btn && x.btn.classList.toggle('active', x === state.cur)); } if (state.cur) { overlay(state.cur.images[state.idx]); tags(state.cur.images[state.idx]); } $('#phiExport').disabled = !$('#phiToggle').checked; };
  $('#tagFilter').oninput = () => state.cur && tags(state.cur.images[state.idx]);
  $('#presets').onchange = (e) => { const [c, w] = e.target.value.split(',').map(Number); if (w && state.p && state.p.v) { state.wc = c; state.ww = w; draw(); } e.target.value = ''; };
  canvas.addEventListener('wheel', (e) => { if (!state.cur) return; e.preventDefault();
    if (e.ctrlKey || e.metaKey) { state.zoom = Math.min(20, Math.max(0.1, state.zoom * (e.deltaY < 0 ? 1.1 : 0.9))); draw(); return; }
    const n = state.cur.images.length; const ni = Math.min(n - 1, Math.max(0, state.idx + (e.deltaY > 0 ? 1 : -1))); if (ni !== state.idx) { state.idx = ni; show(); } }, { passive: false });
  let drag = null;
  canvas.addEventListener('pointerdown', (e) => { if (state.mode === 'redact' && e.button === 0 && state.p) { const q = toImg(e); state.tmpRect = { x0: q.x, y0: q.y, x1: q.x, y1: q.y }; } drag = { x: e.clientX, y: e.clientY, b: e.button }; canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', (e) => { if (!drag || !state.p) return; const dx = e.clientX - drag.x, dy = e.clientY - drag.y; drag.x = e.clientX; drag.y = e.clientY;
    if (state.tmpRect) { const q = toImg(e); state.tmpRect.x1 = q.x; state.tmpRect.y1 = q.y; draw(); return; }
    const m = drag.b === 1 ? 'pan' : drag.b === 2 ? 'zoom' : state.mode;
    if (m === 'wl' && state.p.v) { const k = Math.max(1, state.ww / 300); state.ww = Math.max(1, state.ww + dx * k); state.wc += dy * k; }
    else if (m === 'pan') { state.px += dx; state.py += dy; }
    else if (m === 'zoom') { state.zoom = Math.min(20, Math.max(0.1, state.zoom * (1 - dy / 200))); }
    else if (m === 'scroll' && Math.abs(dy) > 0) { drag.acc = (drag.acc || 0) + dy; if (Math.abs(drag.acc) > 8) { const n = state.cur.images.length; state.idx = Math.min(n - 1, Math.max(0, state.idx + Math.sign(drag.acc))); drag.acc = 0; show(); return; } }
    draw(); });
  canvas.addEventListener('pointerup', () => { drag = null; const r = state.tmpRect; state.tmpRect = null; if (r && Math.abs(r.x1 - r.x0) > 1 && Math.abs(r.y1 - r.y0) > 1) rects(state.cur.images[state.idx]).push(r); if (r) draw(); });
  $('#unredact').onclick = () => { if (state.cur) { state.cur.images[state.idx].redact = []; draw(); } };
  canvas.addEventListener('contextmenu', (e) => e.preventDefault());
  document.addEventListener('keydown', (e) => { if (!state.cur || e.target.tagName === 'INPUT') return; const n = state.cur.images.length;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') state.idx = Math.min(n - 1, state.idx + 1); else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') state.idx = Math.max(0, state.idx - 1); else return; e.preventDefault(); show(); });
  window.addEventListener('resize', () => draw());
  window.dicomViewerLoad = loadFiles;
})();
