import io

p = r'io2cable\classify.py'
s = io.open(p, encoding='utf-8').read()
changed = []

a1 = 'text = f"{norm.omschrijving} {norm.type} {norm.opmerking}".lower()'
b1 = 'text = f"{norm.procescode} {norm.omschrijving} {norm.type} {norm.opmerking}".lower()'
if a1 in s:
    s = s.replace(a1, b1, 1)
    changed.append('procescode')
elif 'norm.procescode' in s:
    changed.append('procescode already there')

a2 = '        elif norm.DI == 1:\n            hits.append("MELDING")\n        elif norm.AO:'
b2 = ('        elif norm.DI == 1:\n            hits.append("MELDING")\n'
      '        elif norm.DO:\n'
      '            hits.append("KLEP_OD_ZONDER_TERUGMELDING")\n'
      '        elif norm.AO:')
if a2 in s:
    s = s.replace(a2, b2, 1)
    changed.append('DO branch')
elif 'norm.DO' in s:
    changed.append('DO already there')

if not changed:
    raise SystemExit('NO ANCHOR MATCHED - send me lines 14-30 of classify.py')

io.open(p, 'w', encoding='utf-8').write(s)
print('written:', changed)