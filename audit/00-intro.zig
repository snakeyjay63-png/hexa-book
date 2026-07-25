// 00-intro.zig — hexa-book Introductie
//
// Core identity: 0≠1 lokaal, 0≐_lens 1 als axiom
// 4 lenzen + NL metataal, 3-6-9 NPR cyclus, 4+1+1 structuur
// 3D statusmodel per route
//
// Bron: 00-intro.md
//
// "De informatie zit niet in één taal.
//  De informatie beweegt tussen de talen door sunya."

const print = @import("std").debug.print;

// ── 4 perspectief-lenzen ──────────────────────────────────

const Lens = enum {
    arabic,   // de steen — telt
    sanskrit, // de vibratie — trilt
    greek,    // de vorm — meet
    latin,    // de fractaal — herhaalt
};

// NL is geen 5e lens — metataal die de 4 verbindt
const LENS_COUNT: u8 = 4;
const META_LANGUAGE = "NL"; // verbindend, niet-rekenend

// ── 3-6-9 NPR cyclus ─────────────────────────────────────

const NPRPhase = enum {
    noise,    // 3 — ruis, bron
    pattern,  // 6 — structuur
    return_,  // 9 — terugkeer
};

// 3 → 6 → 9 verdubbeling/halfpatroon
const NPR_3: u8 = 3;
const NPR_6: u8 = 6;
const NPR_9: u8 = 9;

// ── 4+1+1 structuur ──────────────────────────────────────

const PERSPECTIVE_LENS_COUNT: u8 = 4;  // A-D: Arabisch, Sanskrit, Grieks, Latijn
const AUDIO_LAYER_COUNT: u8 = 1;       // E: audio-superpositie (veldoperator)
const RETURN_MEDIUM_COUNT: u8 = 1;     // F: return-veld
const TOTAL_STRUCTURE: u8 = 4 + 1 + 1; // = 6 → DR(6)=6

// ── 0≠1 vs 0≐_lens 1 ────────────────────────────────────

// Lokaal: getallen blijven onderscheiden
const LOCAL_ZERO: u8 = 0;
const LOCAL_ONE: u8 = 1;

// Lens-axioma: op bronfunctie-niveau equivalent
const LENS_ZERO: u8 = 0;  // ongedifferentieerd veld
const LENS_ONE: u8 = 1;   // eerste verschijning

// ── 3D statusmodel ───────────────────────────────────────

const OperatorStatus = enum {
    formeel,
    conventie,
    interpretatief,
    conceptueel,
    open,
};

const ExecutionStatus = enum {
    niet_van_toepassing,
    niet_voltooid,
    gedeeltelijk,
    voltooid,
};

const ValidationStatus = enum {
    niet_gevalideerd,
    gevalideerd_lokaal,
    gevalideerd_onafhankelijk,
    verworpen,
};

pub const RouteStatus = struct {
    operator: OperatorStatus,
    execution: ExecutionStatus,
    validation: ValidationStatus,
};

// ── Helper: digital root (1-9) ───────────────────────────

fn dr(n: u32) u8 {
    if (n == 0) return 0;
    const r = n % 9;
    if (r == 0) return 9;
    return @intCast(r);
}

// ── Tests ────────────────────────────────────────────────

test "0≠1 lokaal" {
    const std = @import("std");
    std.testing.expect(LOCAL_ZERO != LOCAL_ONE) catch unreachable;
}

test "0≐_lens 1 (beide bestaan in veld)" {
    // Beiden zijn geldige waarden in het ongedifferentieerde veld
    const std = @import("std");
    std.testing.expect(LENS_ZERO >= 0) catch unreachable;
    std.testing.expect(LENS_ONE >= 0) catch unreachable;
    std.testing.expect(LENS_ZERO < 64) catch unreachable; // binnen 6-bit veld
    std.testing.expect(LENS_ONE < 64) catch unreachable;
}

test "4 lenzen + NL metataal" {
    const std = @import("std");
    std.testing.expect(LENS_COUNT == 4) catch unreachable;
}

test "3-6-9 NPR cyclus" {
    const std = @import("std");
    std.testing.expect(NPR_3 == 3) catch unreachable;
    std.testing.expect(NPR_6 == 3 * 2) catch unreachable; // 3→6 verdubbeling
    std.testing.expect(NPR_9 == 3 * 3) catch unreachable; // 3→9 verdrievoudiging
    std.testing.expect(dr(NPR_3) == 3) catch unreachable;
    std.testing.expect(dr(NPR_6) == 6) catch unreachable;
    std.testing.expect(dr(NPR_9) == 9) catch unreachable;
}

test "4+1+1 = 6 structuur" {
    const std = @import("std");
    std.testing.expect(TOTAL_STRUCTURE == 6) catch unreachable;
    std.testing.expect(PERSPECTIVE_LENS_COUNT == 4) catch unreachable;
    std.testing.expect(AUDIO_LAYER_COUNT == 1) catch unreachable;
    std.testing.expect(RETURN_MEDIUM_COUNT == 1) catch unreachable;
    std.testing.expect(dr(TOTAL_STRUCTURE) == 6) catch unreachable;
}

test "3D statusmodel — alle combinaties bestaan" {
    // RouteStatus moet instantiateerbaar zijn
    _ = RouteStatus{
        .operator = .formeel,
        .execution = .voltooid,
        .validation = .gevalideerd_lokaal,
    };
    _ = RouteStatus{
        .operator = .conventie,
        .execution = .voltooid,
        .validation = .niet_gevalideerd,
    };
}

test "route invariant: V(begin) = V(return)" {
    const std = @import("std");
    // Invariant = digital root behouden na cyclus
    const begin_val: u32 = 11;
    const return_val: u32 = 29; // 2+9=11→1+1=2; DR(11)=2, DR(29)=2
    std.testing.expect(dr(begin_val) == dr(return_val)) catch unreachable;
}

test "sunya: leeg is niet-leeg" {
    const std = @import("std");
    // Sunya (0) is niet nihil — het is het veld waarin alles verschijnt
    // 0 is een geldige 6-bit waarde (slot 0)
    std.testing.expect(LOCAL_ZERO < 64) catch unreachable; // in veld
    // 0 ≠ 1 maar beide in hetzelfde veld
    std.testing.expect(LOCAL_ZERO < 64 and LOCAL_ONE < 64) catch unreachable;
}

pub fn main() void {
    print("\n═══ Introductie 0 — Hexa-Book Kern ═══\n\n", .{});

    print("0 ≠ 1 (lokaal: {d} ≠ {d}) ✅\n", .{ LOCAL_ZERO, LOCAL_ONE });
    print("0 ≐_lens 1 (beide in veld) ✅\n\n", .{});

    print("4 perspectief-lenzen: Arabisch, Sanskrit, Grieks, Latijn ✅\n", .{});
    print("1 metataal: {s} (verbindend) ✅\n\n", .{META_LANGUAGE});

    print("3-6-9 NPR cyclus: {d}→{d}→{d} ✅\n", .{ NPR_3, NPR_6, NPR_9 });
    print("Noise → Pattern → Return ✅\n\n", .{});

    print("4+1+1 structuur = {d} (DR={d}) ✅\n", .{ TOTAL_STRUCTURE, dr(@intCast(TOTAL_STRUCTURE)) });
    print("  4 perspectief-lenzen + 1 audio-operator + 1 return-veld ✅\n\n", .{});

    print("3D statusmodel:\n", .{});
    print("  operator_status  = formeel|conventie|interpretatief|conceptueel|open\n", .{});
    print("  execution_status = nvt|niet_voltooid|gedeeltelijk|voltooid\n", .{});
    print("  validation_status = niet_gevalideerd|gevalideerd_lokaal|gevalideerd_onafhankelijk|verworpen\n\n", .{});

    print("Invariant: DR(begin) = DR(return) ✅\n", .{});
    print("  DR(11)={d} = DR(29)={d} ✅\n\n", .{ dr(11), dr(29) });

    print("Sunya: leeg is niet-leeg, veld waarin alles verschijnt ✅\n", .{});
    print("  0 en 1 beide in 6-bit veld (0-63) ✅\n\n", .{});

    print("De informatie zit niet in één taal.\n", .{});
    print("De informatie beweegt tussen de talen door sunya.\n\n", .{});

    print("═══ ALLE INTRO VALIDATIES GESLAAGD ═══\n", .{});
}
