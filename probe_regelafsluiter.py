from io2cable.config import load_config
from io2cable.classify import classify_row
from io2cable.schema import NormRow
from io2cable.rules import Engine

cfg = load_config(r"config\kabelconfig.xlsx")
n = NormRow(omschrijving="Aandrijving regelafsluiter", AO=1, source_ref="r18")
cr = classify_row(n, cfg)
print("functietypes:", cr.functietypes)
print("flags:", cr.flags)

eng = Engine(cfg)
for row in eng.emit(cr):
    print("CableRow:", row.onderdeel, "|", row.kabel)
