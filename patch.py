"""Add REGELAFSLUITER_OD to sig_priority.

Rick 2026-08-21: a regelafsluiter WITH open/dicht takes 8x0,8 (DRAK, both fire
classes) / 12X1 (B2CA JOBA) / 10X1 (CCA JOBA). Without open/dicht it stays
REGELAFSLUITER_0_10V at 4x0,8 / 5X1, which was already correct.

A new type is needed rather than reusing KLEP_OD, because KLEP_OD is also reached
by klep (30), afsluiter (20) and kogelafsluiter (40) - generic catch-alls with no
evidence behind them - and changing its JOBA columns would move all three.

Placed directly ABOVE KLEP_OD in sig_priority: both can be candidates on the same
row, and the more specific type must win.

Run from C:\\dev\\io2cable. Idempotent; refuses to write if the anchor is missing.
"""
import io, sys

p = r'io2cable\rules.py'
s = io.open(p, encoding='utf-8').read()

if 'REGELAFSLUITER_OD' in s:
    print('already patched'); sys.exit(0)

for a, b in [
    ('"KLEP_STURING_MELDING",\n                        "KLEP_OD",',
     '"KLEP_STURING_MELDING",\n                        "REGELAFSLUITER_OD", "KLEP_OD",'),
    ('"KLEP_STURING_MELDING", "KLEP_OD",',
     '"KLEP_STURING_MELDING", "REGELAFSLUITER_OD", "KLEP_OD",'),
]:
    if a in s:
        s = s.replace(a, b, 1)
        io.open(p, 'w', encoding='utf-8').write(s)
        print('patched: REGELAFSLUITER_OD added above KLEP_OD in sig_priority')
        sys.exit(0)

raise SystemExit('sig_priority anchor not found - send me the sig_priority block')