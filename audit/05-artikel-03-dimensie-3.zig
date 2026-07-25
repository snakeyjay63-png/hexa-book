// Artikel 3 - Dimensie 3 (de as, 3-6-9 veld)
// الفصل الثالث - الحلقة 3-6-9 | तृतीय अध्यायः - वलयः ३-६-९

const std = @import("std");
const testing = std.testing;
const math = std.math;

// === Digitale Wortel ===

pub fn digitaleWortel(n: u32) u32 {
    if (n == 0) return 0;
    var r: u32 = n % 9;
    if (r == 0) r = 9;
    return r;
}

// === Verdubbelingscyclus (modulo-9) ===

const U_9 = [_]u32{ 1, 2, 4, 8, 7, 5 }; // eenhedencyclus

pub fn verdubbelingscyclus() [6]u32 {
    return .{ 1, 2, 4, 8, 7, 5 };
}

pub fn verdubbeling(x: u32) u32 {
    return digitaleWortel(x * 2);
}

// === 3-6-9 Veld ===

const NPR_3_AS: u32 = 3;
const NPR_6_PATTERN: u32 = 6;
const NPR_9_RETURN: u32 = 9;

pub fn nprVeld() struct { as: u32, pattern: u32, return_: u32 } {
    return .{
        .as = NPR_3_AS,
        .pattern = NPR_6_PATTERN,
        .return_ = NPR_9_RETURN,
    };
}

// === Even/Oneven Split ===

pub fn onevenPositiesSom() u32 {
    // Posities 1,3,5 van cyclus (0-indexed: 0,2,4) → waarden 2,8,5
    return digitaleWortel(2 + 8 + 5); // → 6
}

pub fn evenPositiesSom() u32 {
    // Posities 2,4,6 van cyclus (0-indexed: 1,3,5) → waarden 4,7,1
    return digitaleWortel(4 + 7 + 1); // → 3
}

// === NPR Koppelregel J(r_even, n_groups) ===

pub fn koppelregelJ(r_even: u32, n_groups: u32) u32 {
    return digitaleWortel(n_groups * r_even);
}

// === Allah = 66 → 3 ===

pub fn allahDr() u32 {
    return digitaleWortel(66); // → 3
}

// === Tests ===

test "digitaleWortel basis" {
    try std.testing.expectEqual(@as(u32, 1), digitaleWortel(1));
    try std.testing.expectEqual(@as(u32, 2), digitaleWortel(2));
    try std.testing.expectEqual(@as(u32, 9), digitaleWortel(9));
    try std.testing.expectEqual(@as(u32, 9), digitaleWortel(18));
    try std.testing.expectEqual(@as(u32, 1), digitaleWortel(10));
}

test "digitaleWortel modulo9" {
    try std.testing.expectEqual(@as(u32, 3), digitaleWortel(66)); // Allah = 6+6=12=1+2=3
    try std.testing.expectEqual(@as(u32, 3), digitaleWortel(12));
    try std.testing.expectEqual(@as(u32, 6), digitaleWortel(15));
}

test "verdubbelingscyclus = 1→2→4→8→7→5" {
    const cyc = verdubbelingscyclus();
    const expected = [_]u32{ 1, 2, 4, 8, 7, 5 };
    for (expected, 0..) |exp, i| {
        try std.testing.expectEqual(exp, cyc[i]);
    }
}

test "verdubbeling operator" {
    try std.testing.expectEqual(@as(u32, 2), verdubbeling(1));
    try std.testing.expectEqual(@as(u32, 4), verdubbeling(2));
    try std.testing.expectEqual(@as(u32, 8), verdubbeling(4));
    try std.testing.expectEqual(@as(u32, 7), verdubbeling(8));
    try std.testing.expectEqual(@as(u32, 5), verdubbeling(7));
    try std.testing.expectEqual(@as(u32, 1), verdubbeling(5));
}

test "verdubbeling 3↔6" {
    try std.testing.expectEqual(@as(u32, 6), verdubbeling(3));
    try std.testing.expectEqual(@as(u32, 3), verdubbeling(6));
}

test "verdubbeling 9 = vast punt" {
    try std.testing.expectEqual(@as(u32, 9), verdubbeling(9));
}

test "nprVeld = 3-as, 6-pattern, 9-return" {
    const v = nprVeld();
    try std.testing.expectEqual(@as(u32, 3), v.as);
    try std.testing.expectEqual(@as(u32, 6), v.pattern);
    try std.testing.expectEqual(@as(u32, 9), v.return_);
}

test "onevenPositiesSom = 2+8+5 → 6" {
    try std.testing.expectEqual(@as(u32, 6), onevenPositiesSom());
}

test "evenPositiesSom = 4+7+1 → 3" {
    try std.testing.expectEqual(@as(u32, 3), evenPositiesSom());
}

test "koppelregel J(3, 2) = 6" {
    // J(r_even, n_groups) = DR(n_groups · r_even) = DR(2 · 3) = 6
    try std.testing.expectEqual(@as(u32, 6), koppelregelJ(3, 2));
}

test "koppelregel J = r_odd" {
    // Uitkomst valt samen met r_odd
    const j_result = koppelregelJ(3, 2);
    const r_odd = onevenPositiesSom();
    try std.testing.expectEqual(r_odd, j_result);
}

test "Allah = 66 → 3 (de as)" {
    try std.testing.expectEqual(@as(u32, 3), allahDr());
    try std.testing.expectEqual(@as(u32, 3), allahDr());
}
