"""Step 2 — Classification. Maps each normalized row to canonical function types
via the estimator-maintained synonym dictionary. Deterministic; unknowns are
flagged, never guessed. Every manual correction belongs in tab 1_Synoniemen.

v2 change (Boerhaave lesson): one PRIMARY type per row — the highest-priority,
longest matching pattern — placed at functietypes[0]. Secondary hits follow.
This stops substring over-matching ('Elektrameter warmtepomp' is a meter, not a
heat pump)."""
from .schema import ClassifiedRow

# types that suppress the generic signal-cable logic in the rules engine
STRUCTURAL = {"REGELKAST", "NTB", "DERDEN", "BUS_INTERFACE", "BRANDMELDING"}


def classify_row(norm, cfg):
    text = f"{norm.omschrijving} {norm.type} {norm.opmerking}".lower()
    flags = []

    # collect matches as (prio, len, type); primary = best
    matches = [(prio, len(pat), ftype) for pat, ftype, prio in cfg.synonyms if pat in text]
    seen, hits = set(), []
    for prio, ln, ftype in sorted(matches, key=lambda m: (-m[0], -m[1])):
        if ftype not in seen:
            hits.append(ftype)
            seen.add(ftype)

    # DERDEN is a scope attribute, not a device class: never let it be primary
    if len(hits) > 1 and hits[0] == "DERDEN":
        hits.append(hits.pop(0))

    # I/O-signature fallbacks when the dictionary is silent
    if not hits:
        if norm.bus_protocol:
            hits.append("BUS_MODBUS")
        elif norm.AI and not (norm.va or norm.voltage):
            hits.append("METING_PASSIEF")
        elif norm.AI:
            hits.append("METING_ACTIEF")
        elif norm.DI == 1:
            hits.append("MELDING")
        elif norm.AO:
            hits.append("STURING_0_10V")
        else:
            flags.append(f"UNKNOWN: '{norm.omschrijving}' not in dictionary and no I/O signature ({norm.source_ref})")

    # refinement: a passive temp sensor that has a supply is actually active
    if hits and hits[0] == "METING_PASSIEF" and (norm.va or "24" in str(norm.voltage)):
        hits[0] = "METING_ACTIEF"

    # bus protocol from the data column: append as secondary, never primary
    if norm.bus_protocol and not any(h.startswith("BUS") or h in
            ("ENERGIEMETER", "EVERDELER_METER", "WARMTEPOMP", "POMP", "APPARAAT_230V", "E_KETEL")
            for h in hits):
        hits.append("BUS_MODBUS")

    # standing human decision points
    if norm.derden_flag:
        flags.append(f"Confirm third-party (derden) scope: '{norm.omschrijving}' ({norm.opmerking})")
    if "n.t.b" in text:
        flags.append(f"n.t.b. item: '{norm.omschrijving}' — omitted until scope is known")
    if "tracing" in text or "leidingverwarming" in text:
        flags.append("Tracing scope: precedent = Erco feeds from the RK; the input remark may differ")
    if hits and hits[0] == "WARMTEPOMP" and norm.DI:
        flags.append("WP hybrid: bus + hardwired meldingen — confirm the data-vs-hardwired choice")
    if "[!" in norm.opmerking:
        flags.append(f"DATA QUALITY: '{norm.omschrijving}' had broken cells in the source — verify in review ({norm.opmerking})")

    return ClassifiedRow(norm=norm, functietypes=hits, flags=flags)


def classify(rows, cfg):
    return [classify_row(r, cfg) for r in rows]
