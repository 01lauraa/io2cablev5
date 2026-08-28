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


def _pattern_matches(pat, text):
    if "&" not in pat:
        return pat in text
    return all(p.strip() in text for p in pat.split("&"))


def _pattern_length(pat):
    if "&" not in pat:
        return len(pat)
    return sum(len(p.strip()) for p in pat.split("&"))


def classify_row(norm, cfg):
    text = f"{norm.procescode} {norm.omschrijving} {norm.type} {norm.opmerking}".lower()
    flags = []

    # collect matches as (prio, len, type); primary = best
    matches = [(prio, _pattern_length(pat), ftype) for pat, ftype, prio in cfg.synonyms if _pattern_matches(pat, text)]
    seen, hits = set(), []
    for prio, ln, ftype in sorted(matches, key=lambda m: (-m[0], -m[1])):
        if ftype not in seen:
            hits.append(ftype)
            seen.add(ftype)

    # DERDEN is a scope attribute, not a device class: never let it be primary
    if len(hits) > 1 and (hits[0] == "DERDEN" or (hits[0] == "REGELKAST" and "regelkast" not in norm.omschrijving.lower())):
        hits.append(hits.pop(0))

    # A pump's signal cable follows the NUMBER of signals on the row, not the
    # pump type (Rick 2026-08-18, confirmed against the CCA dictionary and the
    # 7222 manual): 2 signals (vrijgave/storing) -> 1x4x0,8; 3 signals
    # (vrijgave/storing/sturing) -> 3x2x0,8.  Counted from the I/O columns so
    # it does not depend on how the description is worded.
    # NB pump-specific: the dictionary gives a 3-signal KETEL 1x4x0,8 and a
    # 2-signal VENTILATOR 2x2x0,8, so this must NOT be generalised.
    if "POMP" in hits:
        _n_sig = sum(1 for _v in (norm.DI, norm.DO, norm.AO) if _v)
        if _n_sig >= 3:
            hits.insert(0, "POMP_3_SIGNALEN")
        elif _n_sig == 2:
            hits.insert(0, "POMP_2_SIGNALEN")

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
        elif norm.DO:
            hits.append("KLEP_OD_ZONDER_TERUGMELDING")
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
