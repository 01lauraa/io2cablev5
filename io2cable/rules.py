"""Step 3 — Deterministic rules engine. Classified rows + config → cable rows.
No AI here: identical input + config must always yield identical output.

Encodes rules v2 (validated on Duitslandlaan RK071):
- one row per physical cable; feeds always separate
- group order = ascending process-code prefix; input order within a group
- 'Totaal voedingen derden aansluiten' counts only cables arriving at the RK
- bus doorlussen: first device gets its location, subsequent ones 'doorlussen'
- Modbus IP field devices ride the BMS cable
- energiemeter = bus + separate 24V supply; meter option sensors = aansluitsnoer
- WP = bus + one big meldingen bundle; WP/E-ketel feeds = 'Werkzaamheden derden'
- E-ketel signals split: vrijgave/storing + separate sturing
- tracing: Erco feed from RK (ws=1) + terugmelding
- brandmelding always closes the list in Onderstation algemeen
"""
import re
from .schema import CableRow
from .classify import STRUCTURAL


def _prefix(code):
    m = re.match(r"(\d{2,4})", code or "")
    return int(m.group(1)) if m else 0  # rows without a procescode (WP, tracing) lead


def _naar_feed(template, norm, default_loc):
    if not template:
        return default_loc
    kw = f"{norm.power_kw:g}".replace(".", ",") if norm.power_kw else "?"
    a = f"{norm.current_a:g}".replace(".", ",") if norm.current_a else "?"
    t = str(template)
    if "{" in t:
        return t.format(kw=kw, a=a) if (norm.power_kw or norm.current_a) else default_loc
    return t  # literal template, e.g. "voeding doorlussen"


def _feed_class(norm):
    v = str(norm.voltage)
    if "400" in v:
        return "400V_3F_zonder_N"   # frequency-controlled pumps: no N (rules v2)
    if "230" in v:
        return "230V_1F"
    return None


class Engine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.default_loc = str(cfg.parameters.get("locatie_veld_standaard") or "in TR")
        self.bus_seen = {}          # bus_naam -> count of devices already on chain
        self.flags = []

    # ---------------------------------------------------------------- helpers
    def _bus_row(self, cr, label):
        n, cfg = cr.norm, self.cfg
        bp = (n.bus_protocol or "Modbus RTU").lower()
        if "m-bus" in bp:
            key = "MBUS_DERDEN"
        elif "ip" in bp and "modbus" in bp:
            key = "MODBUS_IP_VELD"
        elif "bacnet" in bp and "ip" in bp:
            key = "BACNET_IP"
        else:
            key = "MODBUS_RTU"
        cab = cfg.bus[key]["kabel"]
        naar = n.locatie or self.default_loc
        if cfg.bus[key]["doorlus_gedrag"] == "doorlussen":
            chain = n.bus_naam or "bus1"
            self.bus_seen[chain] = self.bus_seen.get(chain, 0) + 1
            if self.bus_seen[chain] > 1:
                naar = "doorlussen"
        return CableRow("", f"{label} MODbus koppeling", "", n.procescode, cab, naar,
                        source_ref=n.source_ref)

    def _signal_row(self, cr, ftype, label, naar=None):
        cab = self.cfg.signal_cable(ftype)
        if cab is None:
            self.flags.append(f"NO CABLE RULE for function type {ftype} ({cr.norm.source_ref})")
            cab = f"[? {ftype}]"
        return CableRow("", label, "", cr.norm.procescode, cab,
                        naar or cr.norm.locatie or self.default_loc,
                        source_ref=cr.norm.source_ref)

    def _feed_row(self, cr, label, klasse=None):
        n = cr.norm
        klasse = klasse or _feed_class(n)
        if not klasse:
            return None
        cab, ws, tmpl = self.cfg.feed_cable(klasse)
        return CableRow("", f"{label} voeding", ws, n.procescode, cab,
                        _naar_feed(tmpl, n, n.locatie or self.default_loc), source_ref=n.source_ref)

    # ---------------------------------------------------------------- devices
    def emit(self, cr):
        """Yield CableRows for one classified row. Order: voeding, bus, signalen."""
        n, t = cr.norm, cr.functietypes
        label = n.omschrijving
        prim = t[0] if t else None
        has = lambda *k: prim in k

        if has("NTB"):
            self.flags.append(f"OMITTED (n.t.b.): {label} ({n.source_ref})")
            return
        if has("PANEL_INTERN"):
            # Panel-internal meldingen (reset button, installation automats,
            # netwachter): the signal never leaves the cabinet, so no field
            # cable. Evidence: 2195-06 (RS-01, IA-01, NW-01) and 7267
            # (Resetknop, Automaat 230V/24V) -- neither manual lists a cable.
            self.flags.append(f"PANEL-INTERNAL (no field cable): {label} ({n.source_ref})")
            return
        if has("REGELKAST"):
            cab, _, _ = self.cfg.feed_cable("DERDEN_RK")
            yield CableRow("Voedingen", "Regelkast", "", "", cab, "", source_ref=n.source_ref)
            return
        if has("BRANDMELDING"):
            return  # emitted once at the end regardless

        # -- third-party fed devices: one Voedingen row, then their signals/bus
        if has("WARMTEPOMP"):
            if "reeds aangesloten" in n.opmerking.lower():
                cab = self.cfg.texts.get("VOEDING_REEDS", "Voeding reeds aangesloten")
            elif str(self.cfg.parameters.get("wp_aansluiten_erco", "")).lower() == "ja":
                cab = self.cfg.texts.get("DERDEN_WP",
                    "Kabel levering derde totaan WP, aansluiten WPzijde Erco")
            else:
                cab, _, _ = self.cfg.feed_cable("DERDEN_TOESTEL")
            yield CableRow("Voedingen", label, "", "", cab, "", source_ref=n.source_ref)
            if n.bus_protocol:
                yield self._bus_row(cr, "Warmtepomp")
            if n.DI:
                yield self._signal_row(cr, "MELDINGEN_GROOT", "Warmtepomp bedrijfsmeldingen")
            return
        if has("E_KETEL"):
            cab, _, _ = self.cfg.feed_cable("DERDEN_TOESTEL")
            yield CableRow("Voedingen", "Elektrische ketel", "", "", cab, "", source_ref=n.source_ref)
            yield self._signal_row(cr, "VRIJGAVE_STORING", "Elektrische ketel vrijgave/storing")
            if n.AO:
                yield self._signal_row(cr, "STURING_0_10V", "Elektrische ketel sturing")
            return
        if has("TRACING"):
            scope = str(self.cfg.parameters.get("tracing_scope") or "erco").lower()
            if scope == "erco":
                fr = self._feed_row(cr, "Tracing", "TRACING")
                if fr:
                    yield fr
                if n.DI:
                    yield self._signal_row(cr, "TRACING_TERUGMELDING", "Tracing terugmelding")
            else:
                cab, _, _ = self.cfg.feed_cable("DERDEN_TOESTEL")
                yield CableRow("Voedingen", "Tracing", "", "", cab, "", source_ref=n.source_ref)
            return
        if has("METER_OPTIE_VOELER"):
            yield CableRow("", label, "", n.procescode,
                           self.cfg.texts["AANSLUITSNOER"], "", source_ref=n.source_ref)
            return
        if has("EVERDELER_METER"):
            row = self._bus_row(cr, label)
            row.section = "ONDERSTATION"
            yield row
            return
        if has("ENERGIEMETER"):
            if "aansluitsnoer" not in n.opmerking.lower():
                yield self._signal_row(cr, "METER_VOEDING_24V", f"{label} 24V voeding")
            if n.bus_protocol:
                yield self._bus_row(cr, label)
            return
        # -- generic: feed (if 230/400V) + bus (if protocol) + signal (by type)
        # A 230V smoorafsluiter takes NO separate feed: the 7G1,5 carries power and
        # control on one cable (Tilburg manual: 7G1,5 is the only row per valve).
        kracht_valve = "SMOORAFSLUITER" in t or "SMOORAFSLUITER_KRACHT" in t
        fr = None if kracht_valve else self._feed_row(cr, label)
        if fr:
            yield fr
        if n.bus_protocol:
            yield self._bus_row(cr, label)

        # SMOORAFSLUITER cable follows voltage (house standard 'Standaarden CCA'):
        #   r151 'Smoorklep verdamper 7g1,5' (note: smoorklep = smoorafsluiter) ->
        #   230V / Hulprelais 24V/230VAC -> DRAK HULT 7G1,5 (Tilburg, all 10 rows)
        #   24V / no voltage -> stuurstroom variant (Boerhaave 7X1 -- documented
        #   deviation from the standard's generic 4x0,8, r298). Rule has known
        #   exceptions; rows stay flagged for review.
        if "SMOORAFSLUITER" in t:
            # Route on the AUTHORITATIVE spec only: the voltage column and the panel
            # column (regelkast_spec). Free-text remarks are excluded on purpose --
            # Boerhaave carries 'Hulprelais 24V/230VAC' in a remark yet its validated
            # manual uses the 24V stuurstroom cable (the documented exception).
            spec = f"{n.voltage} {n.regelkast_spec}".lower()
            if "230" in spec:
                t = ["SMOORAFSLUITER_KRACHT" if x == "SMOORAFSLUITER" else x for x in t]
                prim = t[0]
        # KLEP_OD_ZONDER_TERUGMELDING sits directly after KLEP_OD: same device
        # class, fewer conductors. KLEP_OD is the WITH-feedback variant
        # ("open/close + feedback(s)", 8X0,8 = 2 eindcontacten); the no-feedback
        # variant is 4X0,8. Evidence: 7222 manual 139-142 Dakafvoerkap
        # (droog/nat) open/dicht -> DRAK B2CA GY 4X0,8 MT, against
        # 'Regelafsluiter open/dicht + 2 eindcontacten' -> 8X0,8 (x48).
        # NB the 6X0,8 middle case (Luchtklepservo, x8) is NOT modelled -- the
        # core count appears to track the number of feedback contacts, but that
        # is one project's evidence and is an open ASK.
        sig_priority = ["SMOORAFSLUITER_KRACHT", "SMOORAFSLUITER", "KLEP_STURING_MELDING",
                        "KLEP_OD", "KLEP_OD_ZONDER_TERUGMELDING", "BRANDKLEP", "MELDINGEN_GROOT",
                        "EC_VENTILATOR", "POMP_3_SIGNALEN", "POMP_2_SIGNALEN",
                        "REGELAFSLUITER_0_10V", "METING_ACTIEF",
                        "METING_BUS", "METING_PASSIEF", "BEDRIJF_STORING", "VRIJGAVE", "STURING_0_10V",
                        "MELDING"]
        sig_candidates = [prim] + [x for x in t[1:]]
        def _ok(f):
            # Each signal type requires the I/O that physically carries it.
            # DO is deliberately NOT accepted here: a digital OUTPUT is not a
            # melding and not a 0-10V sturing. DO-only devices are typed by the
            # I/O-signature fallback in classify.py (-> KLEP_OD_ZONDER_TERUGMELDING).
            # Widening these guards to DO made every DO-only row select
            # BEDRIJF_STORING (6X0,8) -- wrong cable, and it masked the new type.
            if f.startswith("METING") and f != "METING_BUS" and not n.AI: return False
            if f in ("MELDING", "VRIJGAVE", "BEDRIJF_STORING") and not n.DI: return False
            if f == "STURING_0_10V" and not n.AO: return False
            return True
        ftype = next((f for f in sig_priority if f in sig_candidates and _ok(f)), None)
        if ftype is None and n.DI:
            ftype = "MELDING"
        if ftype == "VRIJGAVE":
            ftype = "MELDING"  # single volt-free contact
        if ftype:
            per_klep = ftype == "BRANDKLEP"
            count = n.aantal if (per_klep or n.aantal > 1 and ftype in ("METING_PASSIEF", "METING_ACTIEF")) else 1
            for i in range(count):
                suffix = f" ({i+1})" if count > 1 else ""
                yield self._signal_row(cr, ftype, label + suffix)
        elif not fr and not n.bus_protocol and not set(t) & STRUCTURAL:
            self.flags.append(f"NO CABLE DERIVED: {label} — types {t or 'none'} ({n.source_ref})")


def _stem(text):
    """Device name with feed-role qualifiers stripped, so the two rows of one
    device reduce to the same stem:
      'Warmtepompcentrale (hoofdvoeding + condensor)'   -> 'warmtepompcentrale'
      'Warmtepompcentrale (secundaire voeding + verdamper)' -> 'warmtepompcentrale'
    but distinct devices keep distinct stems:
      'Warmtepomp 1' -> 'warmtepomp 1'   'Warmtepomp 2' -> 'warmtepomp 2'
    """
    s = str(text).lower().split("(")[0]
    return " ".join(s.split()).strip(" -:")


def _device_key(cr):
    """Identity of the physical device a row belongs to. Rows sharing a key are
    the same device described from several angles and must collapse to one set of
    cables.

    Evidence:
    - Fonkel PR20267276: two 'Regelkast' rows -> manual has ONE Voedingen row;
      WP hoofd- + secundaire voeding -> manual has ONE 'Warmtepomp' row and ONE
      12X1 meldingen bundle.
    - Duitslandlaan PR20267283: identical WP pattern, same bundling in the manual.
    - Boerhaave PR20267275.1: THREE physical heat pumps (Warmtepomp 1/2/3) which
      must NOT be collapsed -- hence the key carries group + name stem, not just
      the function type.
    """
    n = cr.norm
    prim = cr.functietypes[0] if cr.functietypes else ""
    if prim == "REGELKAST":
        return (n.rk, "REGELKAST")           # at most one panel row per RK
    if prim in ("WARMTEPOMP", "E_KETEL"):
        return (n.rk, prim, n.group, _stem(n.omschrijving))
    return None                              # everything else stays distinct


def _merge_group(rows):
    """Merge duplicate rows of one device: keep the first, but union the I/O
    counts and remarks so nothing is lost (e.g. WP meldingen split 2+2 across
    the hoofd- and secundaire-voeding rows)."""
    base = rows[0]
    for extra in rows[1:]:
        n, e = base.norm, extra.norm
        n.AI += e.AI; n.AO += e.AO; n.DI += e.DI; n.DO += e.DO
        n.SOFT = max(n.SOFT, e.SOFT)
        if e.bus_protocol and not n.bus_protocol:
            n.bus_protocol, n.bus_naam = e.bus_protocol, e.bus_naam
        if e.opmerking and e.opmerking not in n.opmerking:
            n.opmerking = (n.opmerking + " | " + e.opmerking).strip(" |")
        n.derden_flag = n.derden_flag or e.derden_flag
        for f in extra.flags:
            if f not in base.flags:
                base.flags.append(f)
    return base


def dedupe_devices(classified):
    """Collapse rows describing the same physical device. Order preserved."""
    out, groups = [], {}
    for cr in classified:
        k = _device_key(cr)
        if k is None:
            out.append(cr)
            continue
        if k in groups:
            groups[k].append(cr)
        else:
            groups[k] = [cr]
            out.append(("PLACEHOLDER", k))
    return [_merge_group(groups[x[1]]) if isinstance(x, tuple) else x for x in out]


def _apply_location_headers(classified, cfg):
    """An input group header may be a LOCATION banner rather than an equipment
    section (Fonkel: 'Installaties op het dak', 'Installaties buiten bij
    buffervat'). Such a group sets the row's 'bekabeling naar' and is replaced as
    a section by the configured fallback -- matching how the estimator reads it.
    Boerhaave's groups ('Warmtepomp 1/2/3') are equipment names and are untouched.
    """
    for cr in classified:
        g = (cr.norm.group or "").lower()
        if not g:
            continue
        for pat, loc, fallback in cfg.locatiekoppen:
            if pat in g:
                if loc and not cr.norm.locatie:
                    cr.norm.locatie = loc
                cr.norm.group = fallback  # "" -> section resolved from procescode
                break
    return classified


def run(classified, cfg):
    """Full Step 3: emit, order, number, totalize. Returns (result_dict, flags)."""
    classified = _apply_location_headers(classified, cfg)
    classified = dedupe_devices(classified)
    eng = Engine(cfg)
    voedingen, devices, onderstation_extra = [], [], []
    for idx, cr in enumerate(classified):
        eng.flags.extend(cr.flags)
        for row in eng.emit(cr):
            row.sort_key = (_prefix(cr.norm.procescode), idx)
            row.flags = list(cr.flags)
            if row.section == "ONDERSTATION":
                onderstation_extra.append(row)
                continue
            if row.section != "Voedingen":
                row.section = cr.norm.group or f"proces {row.sort_key[0]:03d}"
            (voedingen if row.section == "Voedingen" else devices).append(row)

    # every list opens with a Regelkast row; existing panels get the renovation text
    if not any(r.onderdeel.lower().startswith("regelkast") for r in voedingen):
        if str(cfg.parameters.get("regelkast_bestaand", "")).lower() == "ja":
            cab = cfg.texts.get("BESTAAND_RK", "Bestaande regelkast geen aanpassingen")
        else:
            cab, _, _ = cfg.feed_cable("DERDEN_RK")
        voedingen.insert(0, CableRow("Voedingen", "Regelkast 1", "", "", cab, ""))

    # RK's own feed first in Voedingen; keep the rest in input order
    voedingen.sort(key=lambda r: (r.onderdeel != "Regelkast",))
    devices.sort(key=lambda r: r.sort_key)
    # Make sections contiguous (real lists keep each group together). A section is
    # ranked by the smallest sort_key it contains, so process-code order drives the
    # sections and input order drives the rows inside them. Ranking by first
    # appearance instead could reorder devices sharing a procescode.
    rank = {}
    for row in devices:
        k = rank.get(row.section)
        if k is None or row.sort_key < k:
            rank[row.section] = row.sort_key
    devices.sort(key=lambda row: (rank[row.section], row.sort_key))

    # totals per rules v3: derden counts every feed cable Erco must terminate,
    # wherever the termination happens (Boerhaave: WPzijde counts; 'Werkzaamheden
    # derden' and 'reeds aangesloten' do not)
    derden_rk = sum(1 for r in voedingen if "Erco" in str(r.kabel))
    ws_total = sum(1 for r in devices + voedingen if str(r.ws).strip() == "1")

    onderstation = list(onderstation_extra)
    for row in onderstation:
        row.section = "Onderstation algemeen"
    if str(cfg.parameters.get("brandmelding_standaard", "ja")).lower() != "nee":
        onderstation.append(CableRow("Onderstation algemeen", "Brandmelding", "", "",
                                     cfg.texts["BRANDMELDING"], ""))
    return {"voedingen": voedingen, "devices": devices, "onderstation": onderstation,
            "tot_derden": derden_rk, "tot_ws": ws_total}, eng.flags


def run_per_rk(classified, cfg):
    """Multi-RK: group classified rows by their rk field and run each panel
    separately. Returns {rk_name: result_dict}, flags."""
    by_rk, order = {}, []
    for cr in classified:
        rk = cr.norm.rk or "RK"
        if rk not in by_rk:
            by_rk[rk] = []
            order.append(rk)
        by_rk[rk].append(cr)
    results, flags = {}, []
    for rk in order:
        res, fl = run(by_rk[rk], cfg)
        results[rk] = res
        flags.extend(fl)
    return results, flags