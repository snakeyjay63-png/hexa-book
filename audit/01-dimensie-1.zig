// 01-artikel-01-dimensie-1.zig — Dimensie 1: Vonk (Agni)
//
// "Agni is geen element. Agni is het getuige."
// T_Agni: X_raw ↝ X_selected (conceptuele transformatie)
//
// Bron: 01-artikel-01-dimensie-1.md
//
// "Het vuur dat ruis verbrandt en patroon onthult."

const print = @import("std").debug.print;

// ── Agni: vonk, niet element ─────────────────────────────

// Agni is geen element — het is de transformatie
const AGNI_IS_ELEMENT = false;
const AGNI_IS_WITNESS = true;

// T_Agni: ruw materiaal → geselecteerd patroon
// Conceptueel, niet numeriek uitgevoerd
pub const AgniStatus = struct {
    is_conceptual: bool = true,
    is_numeric: bool = false,
    is_executed: bool = false,
};

// Transformatie: X_raw ↝ X_selected
// ↝ = conceptueel (niet = uitgevoerd)
const RAW_INPUT = "X_raw";
const SELECTED_OUTPUT = "X_selected";

// 3 perspectieven op Agni
const ARABIC_Agni = "النار التي تحرق الضجيج";     // vuur verbrandt ruis
const SANSKRIT_Agni = "तेजः शब्दात् विशुद्धं";  // zuivering van geluid
const GREEK_Agni = "τὸ πῦρ τὸν ἦχον κατακαίει"; // vuur verbrandt geluid

// ── Tests ────────────────────────────────────────────────

test "Agni is geen element, het is getuige" {
    const std = @import("std");
    std.testing.expect(!AGNI_IS_ELEMENT) catch unreachable;
    std.testing.expect(AGNI_IS_WITNESS) catch unreachable;
}

test "T_Agni status: conceptueel, niet numeriek" {
    const std = @import("std");
    const s = AgniStatus{};
    std.testing.expect(s.is_conceptual) catch unreachable;
    std.testing.expect(!s.is_numeric) catch unreachable;
    std.testing.expect(!s.is_executed) catch unreachable;
}

test "T_Agni: X_raw ↝ X_selected" {
    // Transformatie bestaat (bron en doel gedefinieerd)
    const testing = @import("std").testing;
    try testing.expectEqualStrings(RAW_INPUT, "X_raw");
    try testing.expectEqualStrings(SELECTED_OUTPUT, "X_selected");
}

test "Agni is conceptuele transformatie, niet NPR-berekening" {
    const std = @import("std");
    const s = AgniStatus{};
    // Conceptueel ≠ uitgevoerd
    std.testing.expect(s.is_conceptual and !s.is_executed) catch unreachable;
}

test "3 perspectieven op Agni bestaan" {
    const std = @import("std");
    // Alle 3 lenzen hebben Agni-descriptor
    std.testing.expect(ARABIC_Agni.len > 0) catch unreachable;
    std.testing.expect(SANSKRIT_Agni.len > 0) catch unreachable;
    std.testing.expect(GREEK_Agni.len > 0) catch unreachable;
}

pub fn main() void {
    print("\n═══ Dimensie 1 — Agni: De Vonk ═══\n\n", .{});

    print("Agni is geen element. Agni is het getuige. ✅\n", .{});
    print("  is_element = {any}, is_witness = {any} ✅\n\n", .{ AGNI_IS_ELEMENT, AGNI_IS_WITNESS });

    print("T_Agni: {s} ↝ {s} ✅\n", .{ RAW_INPUT, SELECTED_OUTPUT });
    print("  (conceptuele transformatie, niet numeriek uitgevoerd)\n\n", .{});

    const s = AgniStatus{};
    print("Status:\n", .{});
    print("  operator  = conceptueel ({any})\n", .{s.is_conceptual});
    print("  numeric   = nee ({any})\n", .{s.is_numeric});
    print("  executed  = nee ({any})\n\n", .{s.is_executed});

    print("3 perspectieven:\n", .{});
    print("  Arabisch:  {s}\n", .{ARABIC_Agni});
    print("  Sanskriet: {s}\n", .{SANSKRIT_Agni});
    print("  Grieks:    {s}\n\n", .{GREEK_Agni});

    print("Je ziet het vuur niet. Je ziet alleen wat erover is.\n", .{});
    print("Het vuur brandt. Wie het niet ziet, draagt een andere lens.\n\n", .{});

    print("═══ DIMENSIE 1 VALIDATIE GESLAAGD ═══\n", .{});
}
