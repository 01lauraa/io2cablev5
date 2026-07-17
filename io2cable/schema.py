"""Canonical schemas. Everything downstream reads only these, never raw files."""
from dataclasses import dataclass, field, asdict
from typing import Optional

NORM_COLUMNS = [
    "rk", "group", "procescode", "omschrijving", "fabricaat", "type",
    "aantal", "AI", "AO", "DI", "DO", "UI", "SOFT",
    "voltage", "power_kw", "current_a", "va",
    "bus_protocol", "bus_naam", "derden_flag", "locatie", "opmerking", "source_ref",
]


@dataclass
class NormRow:
    """One normalized I/O-list row (output of Step 1, input of Step 2)."""
    rk: str = ""
    group: str = ""
    procescode: str = ""
    omschrijving: str = ""
    fabricaat: str = ""
    type: str = ""
    aantal: int = 1
    AI: int = 0
    AO: int = 0
    DI: int = 0
    DO: int = 0
    UI: int = 0
    SOFT: int = 0
    voltage: str = ""          # "230", "400", "24V DC", ...
    power_kw: Optional[float] = None
    current_a: Optional[float] = None
    va: Optional[float] = None
    bus_protocol: str = ""     # "Modbus RTU", "Modbus IP", "BACnet IP", "M-bus", ...
    bus_naam: str = ""         # chain id, e.g. "Modbus1"
    derden_flag: bool = False
    locatie: str = ""      # cabling-to location, e.g. "op dak", "in TR" (Layer B / human input)
    opmerking: str = ""
    source_ref: str = ""       # file/page/row for audit trace-back

    def as_dict(self):
        return asdict(self)


@dataclass
class ClassifiedRow:
    """Step 2 output: NormRow + canonical function type(s) + flags."""
    norm: NormRow
    functietypes: list = field(default_factory=list)   # e.g. ["VOEDING_230", "BUS_MODBUS"]
    flags: list = field(default_factory=list)          # human decision points


@dataclass
class CableRow:
    """One physical cable = one output row (Step 3 output)."""
    section: str            # "Voedingen" | group name | "Onderstation algemeen"
    onderdeel: str
    ws: str = ""
    procescode: str = ""
    kabel: str = ""
    bekabeling_naar: str = ""
    flags: list = field(default_factory=list)
    source_ref: str = ""
    sort_key: tuple = ()
