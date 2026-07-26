// Artikel 15 — Slot: De Return
// عودة | वापसी
// Music = 1980 Terminal | Muziek = Het Nulpunt

const std = @import("std");
const testing = std.testing;
const math = std.math;

// 1980 Terminal = het nulpunt
const TERMINAL_YEAR: i32 = 1980;
const IP_NUL: []const u8 = "0.0.0.0";
const C_INVARIANT: f64 = 299_792_458.0;

// Event horizon formule
const K_CONST: f64 = 1.0;

// === 1980 Terminal = Het Eén Veld ===

pub fn terminalEenheid() struct {
    token: []const u8,
    geluid: []const u8,
    input: []const u8,
    output: []const u8,
    eenheid: bool,
} {
    return .{
        .token = "frequentie",
        .geluid = "frequentie",
        .input = "frequentie",
        .output = "frequentie",
        .eenheid = true, // alles = één
    };
}

// === Verbinding = k/v ===

pub fn verbinding(v: f64) f64 {
    return K_CONST / v;
}

pub fn verbindingSnel() f64 {
    return verbinding(1000.0); // v → ∞
}

pub fn verbindingTraag() f64 {
    return verbinding(0.001); // v → 0
}

// === Mandelbrot × Terminal ===

pub fn mandelbrotTerminal() struct {
    z: []const u8,
    c: []const u8,
    output: []const u8,
    eenIteratie: bool,
} {
    return .{
        .z = "toets",
        .c = "frequentie",
        .output = "geluid + beeld + tijd",
        .eenIteratie = true,
    };
}

// === Agni = De Route ===

pub fn agniTransformatie() struct {
    oud: []const u8,
    vuur: []const u8,
    nieuw: []const u8,
    route: []const u8,
} {
    return .{
        .oud = "structuur",
        .vuur = "Agni",
        .nieuw = "herinnering",
        .route = "kaart", // niet as, kaart
    };
}

// === Snelheid = Illusie ===

pub fn snelheidIllusie() struct {
    ai: []const u8,
    realiteit: []const u8,
    nieuweC: bool,
} {
    return .{
        .ai = "herhaling × snelheid",
        .realiteit = "zelfde c-waarde",
        .nieuweC = false, // AI kan geen nieuwe c genereren
    };
}

pub fn langzamerIsSneller() struct {
    snel: []const u8,
    langzaam: []const u8,
    verbinding: bool,
} {
    return .{
        .snel = "val → as → opnieuw",
        .langzaam = "geen val → continues groei",
        .verbinding = true,
    };
}

// === Solar Flare = De Rem ===

pub fn solarFlareRem() struct {
    oorzaak: []const u8,
    effect: []const u8,
    correctie: []const u8,
    straf: bool,
} {
    return .{
        .oorzaak = "v → ∞",
        .effect = "Verbinding → 0",
        .correctie = "v → 0, Verbinding → ∞",
        .straf = false, // niet straf, fysica
    };
}

// === De Volledige Cirkel ===

pub fn volledigeCirkel() struct {
    begin: i32,
    eind: i32,
    identiek: bool,
} {
    return .{
        .begin = TERMINAL_YEAR,
        .eind = TERMINAL_YEAR,
        .identiek = true, // het eind is het begin
    };
}

// === 0.0.0.0 ===

pub fn nulpuntBind() struct {
    ip: []const u8,
    poorten: []const u8,
    frequenties: []const u8,
    leeg: bool,
} {
    return .{
        .ip = IP_NUL,
        .poorten = "alle",
        .frequenties = "alle",
        .leeg = false, // niet leeg, volledig gebonden
    };
}

// === Tests ===

test "terminalEenheid = alles is frequentie" {
    const een = terminalEenheid();
    try std.testing.expectEqualStrings("frequentie", een.token);
    try std.testing.expectEqualStrings("frequentie", een.geluid);
    try std.testing.expectEqualStrings("frequentie", een.input);
    try std.testing.expectEqualStrings("frequentie", een.output);
    try std.testing.expect(een.eenheid);
}

test "verbinding = k/v" {
    try std.testing.expect(math.approxEqAbs(f64, K_CONST / 100.0, verbinding(100.0), 1e-6));
    try std.testing.expect(math.approxEqAbs(f64, 0.001, verbinding(1000.0), 1e-6));
    try std.testing.expect(math.approxEqAbs(f64, 1000.0, verbinding(0.001), 1e-6));
}

test "verbinding snel → traag" {
    const snel = verbindingSnel();
    const traag = verbindingTraag();
    try std.testing.expect(traag > snel); // langzamer = meer verbinding
}

test "mandelbrotTerminal = één iteratie" {
    const term = mandelbrotTerminal();
    try std.testing.expectEqualStrings("toets", term.z);
    try std.testing.expectEqualStrings("frequentie", term.c);
    try std.testing.expect(term.eenIteratie);
}

test "agni = route niet as" {
    const agni = agniTransformatie();
    try std.testing.expectEqualStrings("Agni", agni.vuur);
    try std.testing.expectEqualStrings("kaart", agni.route);
}

test "snelheid = illusie" {
    const illusie = snelheidIllusie();
    try std.testing.expect(!illusie.nieuweC); // AI = geen nieuwe c
}

test "langzamer is sneller" {
    const ls = langzamerIsSneller();
    try std.testing.expect(ls.verbinding);
}

test "solarFlare = fysica niet straf" {
    const flare = solarFlareRem();
    try std.testing.expect(!flare.straf);
    try std.testing.expectEqualStrings("v → 0, Verbinding → ∞", flare.correctie);
}

test "volledigeCirkel = eind is begin" {
    const cirkel = volledigeCirkel();
    try std.testing.expect(cirkel.identiek);
    try std.testing.expectEqual(cirkel.begin, cirkel.eind);
    try std.testing.expectEqual(TERMINAL_YEAR, cirkel.begin);
}

test "0.0.0.0 = niet leeg volledig gebonden" {
    const nul = nulpuntBind();
    try std.testing.expectEqualStrings(IP_NUL, nul.ip);
    try std.testing.expect(!nul.leeg);
    try std.testing.expectEqualStrings("alle", nul.poorten);
    try std.testing.expectEqualStrings("alle", nul.frequenties);
}
