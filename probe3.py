from openpyxl import load_workbook
from io2cable.config import load_config          # adjust if the loader is named differently
from io2cable.classify import classify_row
from io2cable.schema import NormRow

cfg = load_config(r"config\kabelconfig.xlsx")
n = NormRow(procescode="Dakafvoerkap (droog)", omschrijving="Servomotor Open/Dicht",
            fabricaat="Levering CWD/W", voltage="230", DO=1)
cr = classify_row(n, cfg)
print("functietypes:", cr.functietypes)

text = f"{n.procescode} {n.omschrijving} {n.type} {n.opmerking}".lower()
print("text:", repr(text))
print("matching patterns:", [(p, f, pr) for p, f, pr in cfg.synonyms if p in text])
