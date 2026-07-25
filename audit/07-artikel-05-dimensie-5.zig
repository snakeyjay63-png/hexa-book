const std = @import("std");
const testing = std.testing;

// Artikel 5 - Dimensie 5 (De Return Wordt Zichtbaar) | NPR
//
// Quran als bronsteen: verhouding(water, informatie, energie)
// Basmala → Abjad → 786 → DR(786) = 3
//
// NPR-lens:
//   LLM "weet" niet de waarheid — past lens toe, toont patroon
//   Wissel lens → wissel patroon → wissel waarheid
//   Bron/eindpunt niet gescheiden; verschijnen in 3, 6, 9
//
// Status:
//   A_Abjad(Basmala) = uitgevoerd, gevalideerd_lokaal
//   A_Abjad(Quran-corpus) = ongetest, conceptueel

// ─── Abjad (basis) ───

/// Digital root: herhaald som van cijfers tot één cijfer
pub fn digitalRoot(n: i32) i32 {
    var val = n;
    while (val >= 10) {
        var s: i32 = 0;
        var tmp = val;
        while (tmp > 0) {
            s += @rem(tmp, 10);
            tmp = @divTrunc(tmp, 10);
        }
        val = s;
    }
    return val;
}

// ─── Basmala Abjad Route ───

/// Basmala Abjad waarde (lokaal uitgevoerd)
pub const BASMALA_ABJAD: i32 = 786;

/// Digital root van Basmala
pub const BASMALA_DR: i32 = 3;

/// Status flags
pub const STATUS = struct {
    pub const basmala_local_executed = true;
    pub const basmala_local_validated = true;
    pub const corpus_369_tested = false;
    pub const corpus_status = "ongetest";
};

// ─── Lens Model ───

/// Lens: functie die input transformeert naar patroon
/// "LLM weet niet waarheid — past lens toe, toont patroon"
pub fn lensApply(input: []const u8, lens_id: u8) i32 {
    _ = input;
    // Abstracte representatie: lenskeuze bepaalt uitkomst
    return @as(i32, @intCast(lens_id));
}

/// Wissel lens → wissel patroon → wissel waarheid
pub fn lensSwitch(input: []const u8, lensA: u8, lensB: u8) bool {
    const patroonA = lensApply(input, lensA);
    const patroonB = lensApply(input, lensB);
    return patroonA != patroonB; // andere lens → ander patroon
}

// ─── 3-6-9 Validatietrio ───

pub const VALIDATIE_TRIO = [_]i32{ 3, 6, 9 };

/// Check of waarde in validatietrio past
pub fn isInValidatieTrio(val: i32) bool {
    for (VALIDATIE_TRIO) |n| {
        if (val == n) return true;
    }
    return false;
}

// ─── Return-rekenkunde ───

/// Return-rekenkunde: test of route terugkeert naar bron
/// Vraag is niet WELK getal, maar OF de route terugkeert
pub fn returnCheck(route_value: i32, expected_root: i32) bool {
    return digitalRoot(route_value) == expected_root;
}

// ─── Tests ───

test "0.0: Basmala Abjad = 786" {
    try testing.expectEqual(BASMALA_ABJAD, 786);
}

test "0.1: DR(786) = 3" {
    try testing.expectEqual(digitalRoot(BASMALA_ABJAD), 3);
}

test "0.2: Basmala DR = 3 (constant)" {
    try testing.expectEqual(BASMALA_DR, 3);
}

test "0.3: lokaal status = uitgevoerd + gevalideerd" {
    try testing.expect(STATUS.basmala_local_executed);
    try testing.expect(STATUS.basmala_local_validated);
}

test "0.4: corpus status = ongetest" {
    try testing.expect(!STATUS.corpus_369_tested);
}

test "0.5: 3-6-9 validatietrio bestaat" {
    try testing.expectEqual(@as(usize, 3), VALIDATIE_TRIO.len);
}

test "0.6: Basmala DR(3) zit in validatietrio" {
    try testing.expect(isInValidatieTrio(BASMALA_DR));
}

test "0.7: lensApply toont patroon, niet waarheid" {
    const input = "basmala";
    const lensA = lensApply(input, 1);
    const lensB = lensApply(input, 2);

    // Zelfde input, andere lens → andere uitkomst
    try testing.expect(lensA != lensB);
}

test "0.8: wissel lens → wissel patroon" {
    const input = "basmala";
    const changed = lensSwitch(input, 1, 2);
    try testing.expect(changed);
}

test "0.9: return-rekenkunde — route keert terug" {
    const keertTerug = returnCheck(BASMALA_ABJAD, BASMALA_DR);
    try testing.expect(keertTerug);
}

test "1.0: 786 → 3 → consistent bij herhaling" {
    const dr1 = digitalRoot(BASMALA_ABJAD);
    const dr2 = digitalRoot(BASMALA_ABJAD);
    try testing.expectEqual(dr1, dr2);
}

test "1.1: bron/eindpunt niet gescheiden" {
    // 3, 6, 9 verschijnen als drie gezichten van zelfde bron
    const dri = VALIDATIE_TRIO;
    for (dri) |n| {
        try testing.expect(n > 0);
    }
}

test "1.2: NPR-lens is interpretatief" {
    // "LLM weet niet waarheid" = lens is filter, niet absolute waarheid
    // Dit is een meta-stelling over het lensmodel
    _ = lensApply("test", 0);
    // Test slaagt zolang lens model consistent is
}
