"""Brandventilatieschakeling pairing - replaces the earlier _device_key approach.

Rick 2026-08-18: 'Brandschakelaar toevoer' + 'Brandschakelaar afvoer' are two
rows in the functielijst but ONE cable in the kabellijst, listed as
'Brandventilatieschakeling'.

This is a PAIRING rule, not a deduplication rule, and is kept separate from
dedupe_devices on purpose:
  - dedupe_devices answers "is this one device described twice, or two devices
    with similar names?" - a global question whose key carries group and name
    stem so that e.g. Boerhaave's three heat pumps stay three.
  - this answers "these two named rows are the two halves of one cable" - always
    exactly two, always adjacent, no ambiguity to resolve.
Routing the second through the first made the merge depend on rk/group values
that are identical across panels, which produced a phantom cable.

Runs as a pre-pass in run(), before dedupe_devices, so everything downstream
sees one ordinary device.

This script:
  1. REVERTS the earlier patch (_device_key branch, _merge_group rename)
  2. adds _pair_brandventilatie() and calls it from run()
  3. leaves the sig_priority entry in place (still needed)

Run from C:\\dev\\io2cable. Idempotent.
"""
import io, re, sys

p = r'io2cable\rules.py'
s = io.open(p, encoding='utf-8').read()
done = []

# ---- 1. revert the _device_key branch -----------------------------------
old_key = '''    if prim == "BRANDVENTILATIESCHAKELING" and n.DI:
        # toevoer + afvoer are two input rows but one cable in the manual.
        # The DI test keeps rows that merely REPORT the signal from another
        # panel (7-nieuw RK1: 'VANUIT RK 2 Sport', no I/O) out of the merge -
        # those correctly emit nothing.
        return (n.rk, prim, n.group)
'''
if old_key in s:
    s = s.replace(old_key, '', 1); done.append('reverted _device_key branch')

# ---- 2. revert the _merge_group rename ----------------------------------
old_ren = '''    if len(rows) > 1 and base.functietypes and \\
            base.functietypes[0] == "BRANDVENTILATIESCHAKELING":
        # the merged pair is listed under its own name, not the first row's
        base.norm.omschrijving = "Brandventilatieschakeling"
'''
if old_ren in s:
    s = s.replace(old_ren, '', 1); done.append('reverted _merge_group rename')

# ---- 3. add the pairing pass --------------------------------------------
if '_pair_brandventilatie' not in s:
    func = '''

def _pair_brandventilatie(classified, flags):
    """Collapse an adjacent 'toevoer' + 'afvoer' pair into one cable row.

    Rick 2026-08-18. The pair must be ADJACENT and in that order; the I/O counts
    are unioned so a downstream signal-count rule still sees the whole device.
    An unmatched half is flagged rather than silently emitted: a lone toevoer is
    more likely a data problem than a real single-ended device.

    Evidence: 7-nieuw RK2 r93+r94 -> manual #58 'Brandventilatieschakeling'.
    7-nieuw RK1 r24+r25 carry the same two names with no I/O and the remark
    'VANUIT RK 2 Sport' (the signal arrives from the other panel); its manual has
    no brandventilatieschakeling row, so that pair is flagged, not emitted.
    """
    T = "BRANDVENTILATIESCHAKELING"
    out, i = [], 0
    while i < len(classified):
        cr = classified[i]
        prim = cr.functietypes[0] if cr.functietypes else ""
        if prim != T:
            out.append(cr); i += 1; continue
        name = (cr.norm.omschrijving or "").lower()
        nxt = classified[i + 1] if i + 1 < len(classified) else None
        nxt_prim = (nxt.functietypes[0] if nxt and nxt.functietypes else "")
        nxt_name = (nxt.norm.omschrijving or "").lower() if nxt else ""
        if "toevoer" in name and nxt_prim == T and "afvoer" in nxt_name:
            n, e = cr.norm, nxt.norm
            n.AI += e.AI; n.AO += e.AO; n.DI += e.DI; n.DO += e.DO
            if e.opmerking and e.opmerking not in n.opmerking:
                n.opmerking = (n.opmerking + " | " + e.opmerking).strip(" |")
            n.derden_flag = n.derden_flag or e.derden_flag
            n.omschrijving = "Brandventilatieschakeling"
            out.append(cr); i += 2
        else:
            flags.append(
                f"UNPAIRED brandschakelaar: {cr.norm.omschrijving} - expected an "
                f"adjacent toevoer+afvoer pair, no cable emitted "
                f"({cr.norm.source_ref})")
            i += 1
    return out
'''
    anchor = '\ndef run(classified, cfg):'
    if anchor not in s:
        raise SystemExit('run() not found')
    s = s.replace(anchor, func + anchor, 1)
    done.append('added _pair_brandventilatie')

# ---- 4. call it from run() ----------------------------------------------
a4 = '''    classified = _apply_location_headers(classified, cfg)
    classified = dedupe_devices(classified)
    eng = Engine(cfg)'''
b4 = '''    classified = _apply_location_headers(classified, cfg)
    eng = Engine(cfg)
    classified = _pair_brandventilatie(classified, eng.flags)
    classified = dedupe_devices(classified)'''
if a4 in s:
    s = s.replace(a4, b4, 1); done.append('wired into run()')
elif '_pair_brandventilatie(classified' in s:
    done.append('already wired')
else:
    raise SystemExit('run() body anchor not found - send me the first lines of run()')

if not done:
    print('nothing to do'); sys.exit(0)
io.open(p, 'w', encoding='utf-8').write(s)
print('patched:', '; '.join(done))