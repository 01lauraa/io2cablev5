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

from io2cable.config import load_config
from io2cable.rules import Engine
from io2cable.schema import NormRow, ClassifiedRow

cfg = load_config(r'config\kabelconfig.xlsx')
eng = Engine(cfg)
for p in ['BACnet MS/TP client', 'BACnet /IP client',
          'Priva Blue ID BACnet MS/TP client driver',
          'Priva Blue ID BACnet/IP client driver',
          'Modbus-RTU (master)', 'M-bus']:
    n = NormRow(omschrijving='X', bus_protocol=p)
    row = eng._bus_row(ClassifiedRow(norm=n, functietypes=['METING_BUS'], flags=[]), 'X')
    print(f'{p:44s} -> {row.kabel}')