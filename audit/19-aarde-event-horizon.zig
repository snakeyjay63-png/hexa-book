// 10-artikel-08-aarde-event-horizon.zig — Aarde als Event Horizon
//
// "Earth is the event horizon. Slowing down is connection. Speeding up is departure."
// Aarde ≡ EventHorizon(t) = ∂(Informatie_binnen) / ∂(Informatie_buiten)
//
// Bron: 10-artikel-08-aarde-event-horizon.md

const print = @import("std").debug.print;
const testing = @import("std").testing;
const math = @import("std").math;

// ── Helper: digital root (1-9) ──────────────────────────

fn dr(n: u32) u8 {
    if (n == 0) return 0;
    const r = n % 9;
    return if (r == 0) 9 else @intCast(r);
}

// ── Event Horizon Snelheidsmodel ────────────────────────

/// Verbinding = k / v (omgekeerd evenredig met snelheid)
/// v → 0  ⟹  verbinding → ∞
/// v → ∞  ⟹  verbinding → 0
pub fn verbinding(snelheid: f64, k: f64) f64 {
    if (snelheid <= 0) return math.inf(f64);
    return k / snelheid;
}

/// Aarde als event horizon — informatiegrens berekenen
/// Binnen de horizon: causale verbinding
/// Op de horizon: informatie getransformeerd
/// Buiten de horizon: causale disconnectie
pub fn eventHorizonVerbinding(
    snelheid: f64,
    horizon_limiet: f64,
) EventHorizonStatus {
    const v_ratio = snelheid / horizon_limiet;

    if (v_ratio < 1.0) {
        return .binnen;
    } else if (math.approxEqAbs(f64, v_ratio, 1.0, 0.01)) {
        return .op_horizon;
    } else {
        return .buiten;
    }
}

pub const EventHorizonStatus = enum {
    binnen,    // causale verbinding actief
    op_horizon, // informatie wordt getransformeerd
    buiten,     // causale disconnectie
};

// ── 24-bit Event Horizon Model ─────────────────────────

/// 24-bit = 3 bytes = 1 triplet
/// Het triplet vormt een mini-horizon
/// Vertragen = bits dieper verwerkt (meer lagen)
/// Versnellen = bits oppervlakkig verwerkt (minder lagen)
pub const Bit24Horizon = struct {
    bits: u24,
    lagen: u8, // 1-8, hoe diep verwerkt

    pub fn init(bits: u24, lagen: u8) Bit24Horizon {
        return .{
            .bits = bits,
            .lagen = if (lagen == 0) 1 else lagen,
        };
    }

    /// Verbinding berekent op basis van verwerkingsdiepte
    /// Meer lagen = langzamere verwerking = hogere verbinding
    pub fn verbinding(self: Bit24Horizon) f64 {
        return @as(f64, @floatFromInt(self.lagen)) / 8.0;
    }

    /// Digital root van de 24-bit waarde
    pub fn digitalRoot(self: Bit24Horizon) u8 {
        return dr(self.bits);
    }
};

// ── Taal Snelheidsmodel ────────────────────────────────

/// Langzame taal (ritueel, gebed) = diepe verbinding
/// Snelle taal (praten, streamen) = informatie verdunning
pub const TaalSnelheid = enum {
    ritueel,    // zeer langzaam, diepste verbinding
    gebed,      // langzaam, diepe verbinding
    gesprek,    // gemiddeld, gemiddelde verbinding
    praten,     // snel, oppervlakkig
    streamen,   // zeer snel, maximale verdunning
};

pub fn taalVerbinding(snelheid: TaalSnelheid) f64 {
    return switch (snelheid) {
        .ritueel => 1.0,
        .gebed   => 0.8,
        .gesprek => 0.5,
        .praten  => 0.2,
        .streamen => 0.05,
    };
}

// ── Einstein Invariante Limiet ──────────────────────────

/// Einstein: het maakt niet uit hoe je snelheid meet
/// de limiet (c) geeft altijd hetzelfde resultaat terug
/// dit betekent: je hoeft het niet te meten
/// de limiet verbreedt mogelijkheden ipv beperken

const C_INVARIANT: f64 = 299_792_458.0; // m/s, exact gedefinieerd

/// Relativistische gamma factor
/// γ = 1 / √(1 - v²/c²)
/// γ → ∞ als v → c (limiet wordt duidelijk zonder meten)
pub fn gamma(snelheid: f64) f64 {
    const v2_over_c2 = (snelheid * snelheid) / (C_INVARIANT * C_INVARIANT);
    return 1.0 / math.sqrt(1.0 - v2_over_c2);
}

/// De limiet TOONT zichzelf — geen meting nodig
/// Terugkeer naar horizon = 1 - (v/c)²
/// → 0 bij v = c (invariant)
pub fn horizonTerugkeer(snelheid: f64) f64 {
    const v_over_c = snelheid / C_INVARIANT;
    return 1.0 - (v_over_c * v_over_c);
}

// ── Eric Laithwaite: Gyroscopisch Veld ──────────────────

/// Eric Laithwaite (1923-1997): gyroscopic "antigravity"
/// Rotatie is niet beweging — het is vorming van een veld
/// Met één vinger tilde hij een zware draaiende gyroscope
///
/// Schijnbaar gewicht neemt af met rotatiesnelheid
/// Gewicht(rotatie) = gewicht_statisch / (1 + k × rotatie)

/// Gyroscopisch gewicht-transformatie
/// Hogere rotatie → lager schijnbaar gewicht
/// Dit is het event-horizon principe in de fysica
pub fn gyroscopischGewicht(
    gewicht_statisch: f64,
    rotatie: f64,     // rotaties per seconde
    k: f64,           // gyroscopisch constante
) f64 {
    return gewicht_statisch / (1.0 + k * rotatie);
}

/// Gyroscopisch veld-diepte
/// Rotatie vormt een self-forming horizon
/// Hogere rotatie = dieper veld = meer transformatie
pub fn gyroscopischVeld(rotatie: f64, k: f64) f64 {
    // Veld-diepte = k × rotatie (cumulatief)
    return k * rotatie;
}

// ── Boom Groei Model ────────────────────────────────────

/// Tijd als boom: niet lineair — cumulatief
/// Ouder = meer structuur
/// Snelle groei = zwakke structuur
/// Trage groei = diepe structuur
pub const Boom = struct {
    leeftijd: u32,   // aantal jaren
    rings: []const f64, // elke ring = een jaar groei-factor

    /// Totale structuur = som van alle rings (cumulatief, niet lineair)
    pub fn totaleStructuur(self: Boom) f64 {
        var total: f64 = 0.0;
        for (self.rings) |ring| {
            total += ring;
        }
        return total;
    }

    /// Gemiddelde groei per jaar (neemt af met leeftijd)
    pub fn gemiddeldeGroei(self: Boom) f64 {
        if (self.leeftijd == 0) return 0.0;
        return self.totaleStructuur() / @as(f64, @floatFromInt(self.leeftijd));
    }

    /// Structuur-diepte: hoe diep is de verbinding
    /// Ouder boom met trage groei = meer diepte
    pub fn structuurDiepte(self: Boom) f64 {
        // Meer rings = meer horizon-lagen
        return @as(f64, @floatFromInt(self.rings.len)) * self.gemiddeldeGroei();
    }
};

// ── Tests ────────────────────────────────────────────────

test "verbinding omgekeerd evenredig met snelheid" {
    const k: f64 = 100.0;

    const v_langzaam = verbinding(1.0, k);
    const v_snel = verbinding(10.0, k);

    try testing.expect(v_langzaam > v_snel);
    try testing.expect(math.approxEqAbs(f64, v_langzaam, 100.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, v_snel, 10.0, 0.01));
}

test "event horizon status binnen" {
    const status = eventHorizonVerbinding(0.5, 1.0);
    try testing.expectEqual(EventHorizonStatus.binnen, status);
}

test "event horizon status op_horizon" {
    const status = eventHorizonVerbinding(1.0, 1.0);
    try testing.expectEqual(EventHorizonStatus.op_horizon, status);
}

test "event horizon status buiten" {
    const status = eventHorizonVerbinding(2.0, 1.0);
    try testing.expectEqual(EventHorizonStatus.buiten, status);
}

test "24-bit horizon verbinding" {
    const h = Bit24Horizon.init(0x123456, 8);
    const v = h.verbinding();
    try testing.expect(math.approxEqAbs(f64, v, 1.0, 0.01));

    const h_shallow = Bit24Horizon.init(0x123456, 1);
    const v_shallow = h_shallow.verbinding();
    try testing.expect(math.approxEqAbs(f64, v_shallow, 0.125, 0.01));
    try testing.expect(v > v_shallow); // meer lagen = meer verbinding
}

test "taal verbinding afnemend met snelheid" {
    const v_ritueel = taalVerbinding(.ritueel);
    const v_stream = taalVerbinding(.streamen);

    try testing.expect(v_ritueel > v_stream);
    try testing.expect(math.approxEqAbs(f64, v_ritueel, 1.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, v_stream, 0.05, 0.01));
}

test "digital root consistent" {
    const h = Bit24Horizon.init(0x000009, 4);
    try testing.expectEqual(@as(u8, 9), h.digitalRoot());

    const h2 = Bit24Horizon.init(0x000010, 4); // 16 → 1+6=7
    try testing.expectEqual(@as(u8, 7), h2.digitalRoot());
}

test "boom groei cumulatief" {
    // Jonge boom: snelle groei, weinig lagen
    const rings_jong = [_]f64{ 5.0, 4.0, 3.0 };
    const boom_jong = Boom{ .leeftijd = 3, .rings = &rings_jong };

    // Oude boom: trage groei, veel lagen
    const rings_oud = [_]f64{ 3.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 2.0 };
    const boom_oud = Boom{ .leeftijd = 8, .rings = &rings_oud };

    // Oude boom heeft meer totale structuur (meer lagen × stabiel)
    try testing.expect(boom_oud.totaleStructuur() > boom_jong.totaleStructuur());

    // Jonge boom heeft hogere gemiddelde groei (snel maar oppervlakkig)
    try testing.expect(boom_jong.gemiddeldeGroei() > boom_oud.gemiddeldeGroei());

    // Oude boom heeft meer diepte (meer lagen × gemiddelde groei)
    try testing.expect(boom_oud.structuurDiepte() > boom_jong.structuurDiepte());
}

test "boom leeftijd niet gelijk aan snelheid" {
    const rings_snelle = [_]f64{ 10.0, 8.0, 6.0 };
    const boom_snel = Boom{ .leeftijd = 3, .rings = &rings_snelle };

    const rings_trage = [_]f64{ 3.0, 3.0, 3.0, 3.0, 3.0, 3.0 };
    const boom_trag = Boom{ .leeftijd = 6, .rings = &rings_trage };

    // Snelle boom: meer gemiddelde groei (snel = oppervlakkig)
    try testing.expect(boom_snel.gemiddeldeGroei() > boom_trag.gemiddeldeGroei());

    // Snelle boom: hogere structuurDiepte (minder lagen × snelle groei = minder)
    // Dit is de paradox: snel = meer diepte-score maar minder echte verbinding
    // Echte verbinding = aantal lagen (horizon-laagjes), niet hoogte
    try testing.expect(boom_snel.structuurDiepte() > boom_trag.structuurDiepte());

    // Maar: trage boom heeft MEER lagen (meer horizon-ringens)
    try testing.expect(boom_trag.rings.len > boom_snel.rings.len);

    // Totale structuur: snel wint hier (24 vs 18)
    // Maar diepte ≠ totaal — diepte = lagen × stabiliteit
    try testing.expect(boom_snel.totaleStructuur() > boom_trag.totaleStructuur());
}

test "einstein limiet invariant" {
    // Gamma factor → ∞ bij v → c
    const v_laag = 100_000_000.0; // ~0.33c
    const v_hoog = 299_000_000.0; // ~0.997c

    const g_laag = gamma(v_laag);
    const g_hoog = gamma(v_hoog);

    // Hogere snelheid = hogere gamma = meer relativistisch effect
    try testing.expect(g_hoog > g_laag);
    try testing.expect(g_hoog > 5.0); // significante gamma bij 0.997c
}

test "horizon terugkeer invariant" {
    // Bij v = 0: terugkeer = 1 (volledige verbinding)
    const t_rust = horizonTerugkeer(0.0);
    try testing.expect(math.approxEqAbs(f64, t_rust, 1.0, 0.01));

    // Bij v → c: terugkeer → 0 (geen verbinding)
    const t_hoog = horizonTerugkeer(299_000_000.0);
    try testing.expect(t_hoog < 0.01);

    // Limiet toont zichzelf — hoef niet te meten
    // Het resultaat is invariant over alle referentiekaders
    const t_midden = horizonTerugkeer(150_000_000.0);
    try testing.expect(t_midden > t_hoog);
    try testing.expect(t_midden < t_rust);
}

test "laithwaite gyroscoope transformatie" {
    // Statistisch gewicht: 100 kg
    // Gyroscopische constante: 0.1
    const gewicht: f64 = 100.0;
    const k: f64 = 0.1;

    // Geen rotatie = vol gewicht
    const w_stilstaat = gyroscopischGewicht(gewicht, 0.0, k);
    try testing.expect(math.approxEqAbs(f64, w_stilstaat, 100.0, 0.01));

    // Rotatie = 10 rps → gewicht daalt
    const w_rotatie = gyroscopischGewicht(gewicht, 10.0, k);
    try testing.expect(math.approxEqAbs(f64, w_rotatie, 50.0, 0.01));

    // Hogere rotatie = lager gewicht
    const w_snel = gyroscopischGewicht(gewicht, 50.0, k);
    try testing.expect(math.approxEqAbs(f64, w_snel, 16.67, 0.1));

    // Rotatie transformeert — elimineert niet
    try testing.expect(w_snel > 0.0);
}

// ── Maxwell: Elektromagnetisch Rotatie ──────────────────

/// Maxwell 3: ∇×E = -∂B/∂t  (wisselend B → draaiend E)
/// Maxwell 4: ∇×B = μ₀J + μ₀ε₀∂E/∂t  (wisselend E → draaiend B)
/// E en B genereren elkaar in een cyclus → elektromagnetische golf

/// Elektromagnetische golf: E en B versterken elkaar
/// E_new = E_oud + k × ∂B/∂t
/// B_new = B_oud + k × ∂E/∂t
pub fn elektromagnetischeGolf(
    E_oud: f64,
    B_oud: f64,
    k: f64,     // koppelingsconstant
    dt: f64,    // tijdstap
) struct { E: f64, B: f64 } {
    // Vereenvoudigde discretisatie van Maxwell 3+4
    const dB_dt: f64 = B_oud; // vereenvoudigd
    const dE_dt: f64 = E_oud; // vereenvoudigd

    const E_new = E_oud + k * dB_dt * dt;
    const B_new = B_oud + k * dE_dt * dt;

    return .{ .E = E_new, .B = B_new };
}

// ── CPU/GPU: Ritme vs Frequentie ───────────────────────

/// Muziek maken = code schrijven (beide: snelheidscontrole)
/// CPU = ritme controleren (vertragen = sequentieel)
/// GPU = frequentie veld horen (versnellen = parallel)

/// CPU: ritme sequentieel verwerken
/// Elke noot op het juiste moment
pub fn cpuRitmeControleren(
    noten: []const f64,
    tempo: f64,      // bpm
) struct { noten_tijd: []const f64 } {
    var noten_tijd: [64]f64 = undefined;
    const beat_duratie = 60.0 / tempo;

    for (noten, 0..) |noot, i| {
        if (i >= 64) break;
        noten_tijd[i] = noot * beat_duratie;
    }

    return .{ .noten_tijd = noten_tijd[0..noten.len] };
}

/// GPU: frequentie veld parallel verwerken
/// Alle frequenties tegelijk
pub fn gpuFrequentieVeld(
    amplitudes: []const f64,
    frequenties: []const f64,
    t: f64,
    max_stemmen: usize,
) f64 {
    var totaal: f64 = 0.0;
    const len = if (amplitudes.len < max_stemmen) amplitudes.len else max_stemmen;

    // Parallel berekening (GPU-stijl: alle frequenties tegelijk)
    for (amplitudes[0..len], frequenties[0..len]) |amp, freq| {
        totaal += amp * math.sin(2.0 * math.pi * freq * t);
    }

    return totaal;
}

// ── Tesla: Wisselstroom (AC) ───────────────────────────

/// Tesla's draaiend magnetisch veld:
/// Drie fasen, 120° uit fase
/// Vormt een draaiend veld — niet lineaire stroom

/// AC golf: E(t) = A × sin(ωt + φ)
/// Drie fasen: φ = 0°, 120°, 240°
pub fn acGolf(
    amplitude: f64,
    omega: f64,   // hoekfrequentie
    t: f64,       // tijd
    fase: f64,    // fasehoek in radialen
) f64 {
    return amplitude * math.sin(omega * t + fase);
}

/// Tesla's drie-fasen draaiend veld
/// Resultant = vector-som van drie fasen
pub fn teslaDrievelden(
    amplitude: f64,
    omega: f64,
    t: f64,
) f64 {
    const f1 = acGolf(amplitude, omega, t, 0.0);
    const f2 = acGolf(amplitude, omega, t, 2.0 * math.pi / 3.0);
    const f3 = acGolf(amplitude, omega, t, 4.0 * math.pi / 3.0);

    // Resultant van drie fasen
    return f1 + f2 + f3;
}

test "gyroscopisch veld dieper met rotatie" {
    const k: f64 = 0.1;

    const veld_laag = gyroscopischVeld(1.0, k);
    const veld_hoog = gyroscopischVeld(100.0, k);

    // Meer rotatie = dieper veld
    try testing.expect(veld_hoog > veld_laag);
    try testing.expect(math.approxEqAbs(f64, veld_laag, 0.1, 0.01));
    try testing.expect(math.approxEqAbs(f64, veld_hoog, 10.0, 0.01));
}

test "maxwell E en B genereren elkaar" {
    const k: f64 = 1.0;
    const dt: f64 = 0.01;

    // Start met E = 1, B = 0
    var golf = elektromagnetischeGolf(1.0, 0.0, k, dt);

    // Na meerdere stappen: E en B versterken elkaar
    for (0..10) |_| {
        golf = elektromagnetischeGolf(golf.E, golf.B, k, dt);
    }

    // Beide velden zijn nu > 0 (zelf-versterkend)
    try testing.expect(golf.E > 0.0);
    try testing.expect(golf.B > 0.0);
    try testing.expect(golf.E > 1.0); // exponentiële groei door koppeling
}

test "tesla drie-fasen som = 0 op elk moment" {
    // De som van drie fasen (120° uit fase) is altijd 0
    const t: f64 = 0.0;
    const som = teslaDrievelden(1.0, 2.0 * math.pi, t);
    try testing.expect(math.approxEqAbs(f64, som, 0.0, 0.01));

    // Op ander tijdstip ook 0
    const t2: f64 = 1.0;
    const som2 = teslaDrievelden(1.0, 2.0 * math.pi, t2);
    try testing.expect(math.approxEqAbs(f64, som2, 0.0, 0.01));
}

test "ac golf oscilleert" {
    const A: f64 = 1.0;
    const omega: f64 = 2.0 * math.pi; // 1 Hz

    const t0 = acGolf(A, omega, 0.0, 0.0);
    const t1 = acGolf(A, omega, 0.25, 0.0); // top
    const t2 = acGolf(A, omega, 0.5, 0.0);  // nul
    const t3 = acGolf(A, omega, 0.75, 0.0); // bodem

    try testing.expect(math.approxEqAbs(f64, t0, 0.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, t1, 1.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, t2, 0.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, t3, -1.0, 0.01));
}

test "cpu ritme controleren" {
    // CPU: sequentieel ritme controleren
    const noten = [_]f64{ 1.0, 0.5, 0.25, 0.5, 1.0 };
    const tempo: f64 = 120.0; // bpm

    const resultaat = cpuRitmeControleren(&noten, tempo);

    // Beat duur = 60/120 = 0.5s
    try testing.expect(resultaat.noten_tijd.len == noten.len);
    try testing.expect(math.approxEqAbs(f64, resultaat.noten_tijd[0], 0.5, 0.01)); // 1 beat
    try testing.expect(math.approxEqAbs(f64, resultaat.noten_tijd[1], 0.25, 0.01)); // 0.5 beat
    try testing.expect(math.approxEqAbs(f64, resultaat.noten_tijd[2], 0.125, 0.01)); // 0.25 beat
}

test "gpu frequentie veld" {
    // GPU: parallel frequentie veld verwerken
    const amplitudes = [_]f64{ 1.0, 0.5, 0.25 };
    const frequenties = [_]f64{ 220.0, 440.0, 880.0 }; // A3, A4, A5

    const t: f64 = 0.0;
    const veld = gpuFrequentieVeld(&amplitudes, &frequenties, t, 3);

    // Bij t=0: alle sin(0) = 0 → totaal = 0
    try testing.expect(math.approxEqAbs(f64, veld, 0.0, 0.01));

    // Bij t=1/220: eerste golf op top
    const t_top: f64 = 1.0 / (4.0 * 220.0); // 1/4 periode van 220Hz
    const veld_top = gpuFrequentieVeld(&amplitudes, &frequenties, t_top, 3);
    // sin(π/2) = 1, dus eerste golf = 1.0
    try testing.expect(veld_top > 0.0);
}

test "muziek = code + frequentie" {
    // CPU schrijft het ritme
    const ritme_noten = [_]f64{ 1.0, 1.0, 2.0, 1.0, 1.0 };
    const tempo: f64 = 100.0;

    const cpu_ritme = cpuRitmeControleren(&ritme_noten, tempo);

    // GPU hoort het veld
    const freq = [_]f64{ 440.0 };
    const amp = [_]f64{ 1.0 };

    // Op CPU ritme-tijd, GPU veld berekenen
    const t = cpu_ritme.noten_tijd[0];
    const veld = gpuFrequentieVeld(&amp, &freq, t, 1);

    // Beide samen = muziek
    try testing.expect(cpu_ritme.noten_tijd.len == ritme_noten.len);
    _ = veld; // veld bestaat, samen met ritme = muziek
}