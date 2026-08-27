"""Patch io2cable/pipeline.py: restore section-banner grouping in write_cable_list.
Run from the repo root: python patch_write_cable_list.py
Then verify: git diff io2cable\\pipeline.py
"""
import re

PATH = "io2cable/pipeline.py"

NEW_FUNC = '''def write_cable_list(result, cfg, path, rk_naam):
    wb = Workbook()
    ws = wb.active
    ws.append(["nr", "onderdeel", "ws", "proces code", "kabel soort en doorsnede"])
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF", name="Arial", size=10)
        c.fill = PatternFill("solid", start_color="1F4E78")
    ws.append([])
    ws.append(["", cfg.texts["VOEDINGEN"]]); ws.cell(ws.max_row, 2).font = BLUE
    for i, r in enumerate(result["voedingen"], 1):
        ws.append([i, r.onderdeel, r.ws, r.procescode, r.kabel])
    ws.append([])
    ws.append(["", cfg.texts["TOT_DERDEN"], result["tot_derden"]])
    ws.append(["", cfg.texts["TOT_WS"], result["tot_ws"]])
    for rr in (ws.max_row - 1, ws.max_row):
        ws.cell(rr, 2).font = BOLD
        ws.cell(rr, 3).font = Font(bold=True, color="0000FF", name="Arial", size=10)
    ws.append([])
    nr = 0
    current_section = None
    for r in result["devices"]:
        if r.section != current_section:
            if current_section is not None:
                ws.append([])
            ws.append(["", r.section]); ws.cell(ws.max_row, 2).font = BLUE
            current_section = r.section
        nr += 1
        flag = " [?]" if r.flags else ""
        ws.append([nr, r.onderdeel + flag, r.ws, r.procescode, r.kabel])
    ws.append([])
    ws.append(["", cfg.texts["ONDERSTATION"]]); ws.cell(ws.max_row, 2).font = BLUE
    for r in result["onderstation"]:
        nr += 1
        ws.append([nr, r.onderdeel, r.ws, r.procescode, r.kabel])
    for col, w in zip("ABCDE", (5, 46, 5, 12, 58)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wb.save(path)
'''

with open(PATH, encoding="utf-8") as f:
    src = f.read()

# Match from 'def write_cable_list(' up to (not including) the next top-level 'def '
pattern = re.compile(r"def write_cable_list\(.*?\n(?=def )", re.DOTALL)
m = pattern.search(src)
if not m:
    raise SystemExit("Could not find write_cable_list in " + PATH + " -- nothing changed.")

old_func = m.group(0)
if "current_section" in old_func:
    print("Already patched -- no change made.")
else:
    new_src = src[:m.start()] + NEW_FUNC + "\n\n" + src[m.end():]
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(new_src)
    print("Patched:", PATH)
    print("Replaced", len(old_func.splitlines()), "lines with", len(NEW_FUNC.splitlines()), "lines.")