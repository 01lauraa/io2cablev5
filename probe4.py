from io2cable.config import load_config
from io2cable.classify import classify_row
from io2cable.schema import NormRow
import inspect, io2cable.classify as C

cfg = load_config(r"config\kabelconfig.xlsx")
n = NormRow(procescode="Dakafvoerkap (droog)", omschrijving="Servomotor Open/Dicht",
            fabricaat="Levering CWD/W", voltage="230", DO=1)
print("DO =", repr(n.DO), " DI =", repr(n.DI), " AI =", repr(n.AI), " AO =", repr(n.AO))
print("bus_protocol =", repr(n.bus_protocol), " va =", repr(n.va), " voltage =", repr(n.voltage))
cr = classify_row(n, cfg)
print("functietypes:", cr.functietypes)
print("flags:", cr.flags)
print("--- classify.py actually loaded from:", C.__file__)
src = inspect.getsource(classify_row)
for i, line in enumerate(src.splitlines(), 1):
    if "not hits" in line or "norm.D" in line or "norm.A" in line or "hits.append" in line:
        print(f"{i:4d}  {line}")
