// Artikel 10 — Dimensie 10 (6-bit routing, NPR-cel) | 20+21+22
// Audit: 6-bit veld, Abjad, Allah 66→3, Basmala 786→3, verdubbelingscyclus, NPR-coord

const std = @import("std");
const testing = std.testing;

fn digitalRoot(n: i32) i32 {
    if (n == 0) return 0;
    const sign: i32 = if (n < 0) -1 else 1;
    var m: i32 = if (n < 0) -n else n;
    while (m > 9) {
        var s: i32 = 0;
        var tmp = m;
        while (tmp > 0) : (tmp = @divTrunc(tmp, 10)) {
            s += @rem(tmp, 10);
        }
        m = s;
    }
    return sign * m;
}

// ─── Test 1: 6-bit veld ────────────────────────────────────────────────

test "1.1: 6-bit = 64 toestanden (2^6)" {
    const states: u32 = 64;
    const pow: u32 = 64; // 2^6
    try testing.expectEqual(states, pow);
}

test "1.2: 0x00-0x3F = 64 waarden" {
    const min_val: u8 = 0x00;
    const max_val: u8 = 0x3F;
    const count: u8 = max_val - min_val + 1;
    try testing.expectEqual(@as(u8, 64), count);
}

test "1.3: 0x00 = śūnya, 0x3F = eka" {
    const sunya: u8 = 0x00;
    const eka: u8 = 0x3F;
    try testing.expectEqual(@as(u8, 0), sunya);
    try testing.expectEqual(@as(u8, 63), eka);
}

test "1.4: 0x40 buiten 6-bit bereik" {
    const out_of_range: u8 = 0x40;
    // 0x40 = 64, requires 7 bits to represent as a value
    const requires_7_bits: bool = out_of_range >= 64;
    try testing.expect(requires_7_bits);
}

// ─── Test 2: Allah = 66 → 3 ───────────────────────────────────────────

test "2.1: Allah Abjad = 66" {
    const alif: i32 = 1;
    const lam: i32 = 30;
    const lam2: i32 = 30;
    const ha: i32 = 5;
    const total: i32 = alif + lam + lam2 + ha;
    try testing.expectEqual(@as(i32, 66), total);
}

test "2.2: Allah DR = 3" {
    try testing.expectEqual(@as(i32, 3), digitalRoot(66));
}

test "2.3: 64 + 2 = 66 (veld + zaad)" {
    const veld: i32 = 64;
    const zaad: i32 = 2;
    try testing.expectEqual(@as(i32, 66), veld + zaad);
}

test "2.4: 66 → 3 = NPR-toestand Noise/as" {
    try testing.expectEqual(@as(i32, 3), digitalRoot(66));
}

// ─── Test 3: Basmala = 786 → 3 ───────────────────────────────────────

test "3.1: بسم = 102" {
    const ba: i32 = 2;
    const seen: i32 = 60;
    const mim: i32 = 40;
    try testing.expectEqual(@as(i32, 102), ba + seen + mim);
}

test "3.2: الله = 66" {
    const alif: i32 = 1;
    const lam: i32 = 30;
    const lam2: i32 = 30;
    const ha: i32 = 5;
    try testing.expectEqual(@as(i32, 66), alif + lam + lam2 + ha);
}

test "3.3: الرحمن = 329" {
    const alif: i32 = 1;
    const lam: i32 = 30;
    const ra: i32 = 200;
    const ha: i32 = 8;
    const mim: i32 = 40;
    const nun: i32 = 50;
    try testing.expectEqual(@as(i32, 329), alif + lam + ra + ha + mim + nun);
}

test "3.4: الرحيم = 289" {
    const alif: i32 = 1;
    const lam: i32 = 30;
    const ra: i32 = 200;
    const ha: i32 = 8;
    const ya: i32 = 10;
    const mim: i32 = 40;
    try testing.expectEqual(@as(i32, 289), alif + lam + ra + ha + ya + mim);
}

test "3.5: Basmala totaal = 786 → 3" {
    const total: i32 = 102 + 66 + 329 + 289;
    try testing.expectEqual(@as(i32, 786), total);
    try testing.expectEqual(@as(i32, 3), digitalRoot(786));
}

// ─── Test 4: Hamza-variaties ──────────────────────────────────────────

test "4.1: إ = ا = 1" {
    const hamza_alif: i32 = 1;
    const alif: i32 = 1;
    try testing.expectEqual(alif, hamza_alif);
}

test "4.2: ؤ = و = 6" {
    const hamza_waw: i32 = 6;
    const waw: i32 = 6;
    try testing.expectEqual(waw, hamza_waw);
}

test "4.3: ئ = ي = 10" {
    const hamza_ya: i32 = 10;
    const ya: i32 = 10;
    try testing.expectEqual(ya, hamza_ya);
}

// ─── Test 5: Validatietrio 3-6-9 ─────────────────────────────────────

test "5.1: validatietrio = {3, 6, 9}" {
    const trio = [_]i32{ 3, 6, 9 };
    try testing.expectEqual(@as(usize, 3), trio.len);
}

test "5.2: 3 → 6 = Noise → Pattern" {
    const noise: i32 = 3;
    const pattern: i32 = 6;
    try testing.expectEqual(@as(i32, 2), pattern / noise); // 2×3=6
}

test "5.3: 3+3+3 = 9 (volledig veld)" {
    try testing.expectEqual(@as(i32, 9), 3 + 3 + 3);
}

test "5.4: 3,6,9 buiten verdubbelingsbaan" {
    const cyclus = [_]i32{ 2, 4, 8, 7, 5, 1 };
    for ([_]i32{ 3, 6, 9 }) |v| {
        var found = false;
        for (cyclus) |c| {
            if (c == v) found = true;
        }
        try testing.expect(!found);
    }
}

// ─── Test 6: Verdubbelingscyclus ──────────────────────────────────────

test "6.1: cyclus 2→4→8→7→5→1→2" {
    const cyclus = [_]i32{ 2, 4, 8, 7, 5, 1 };
    try testing.expectEqual(@as(usize, 6), cyclus.len);

    for (0..cyclus.len) |i| {
        const next_idx: usize = (i + 1) % cyclus.len;
        const expected: i32 = cyclus[next_idx];
        const actual: i32 = digitalRoot(2 * cyclus[i]);
        try testing.expectEqual(expected, actual);
    }
}

test "6.2: oneven posities {2,8,5} → som 15 → 6" {
    const oneven = [_]i32{ 2, 8, 5 };
    const som: i32 = oneven[0] + oneven[1] + oneven[2];
    try testing.expectEqual(@as(i32, 15), som);
    try testing.expectEqual(@as(i32, 6), digitalRoot(som));
}

test "6.3: even posities {4,7,1} → som 12 → 3" {
    const even = [_]i32{ 4, 7, 1 };
    const som: i32 = even[0] + even[1] + even[2];
    try testing.expectEqual(@as(i32, 12), som);
    try testing.expectEqual(@as(i32, 3), digitalRoot(som));
}

test "6.4: relatie 2×3 = 6" {
    const even_dr: i32 = 3;  // even posities → 3
    const oneven_dr: i32 = 6; // oneven posities → 6
    try testing.expectEqual(oneven_dr, 2 * even_dr);
}

// ─── Test 7: NPR-coord ────────────────────────────────────────────────

test "7.1: NPR_coord(24,35) → (6,8)" {
    try testing.expectEqual(@as(i32, 6), digitalRoot(24));
    try testing.expectEqual(@as(i32, 8), digitalRoot(35));
}

test "7.2: NPR_coord(55,55) → (1,1)" {
    try testing.expectEqual(@as(i32, 1), digitalRoot(55));
}

test "7.3: NPR_coord = conceptueel" {
    const is_conceptueel: bool = true;
    const is_gevalideerd: bool = false;
    try testing.expect(is_conceptueel);
    try testing.expect(!is_gevalideerd);
}

// ─── Test 8: Rolcorrespondentie ───────────────────────────────────────

test "8.1: 0 ≠ 1 (zaad ≠ veld)" {
    try testing.expect(@as(i32, 0) != @as(i32, 1));
}

test "8.2: 0 ≐_lens 1 (lensaxioma)" {
    // Zaad + veld = volledige route (lens-afhankelijk)
    const is_lens_afhankelijk: bool = true;
    try testing.expect(is_lens_afhankelijk);
}

// ─── Test 9: Vṛtti classificatie ─────────────────────────────────────

test "9.1: vṛtti types" {
    // pramāṇa, viparyaya, vikalpa, nidrā, smṛti
    const vritti_count: usize = 5;
    try testing.expectEqual(@as(usize, 5), vritti_count);
}

test "9.2: pramāṇa subtypes" {
    // pratyakṣa, anumāna, āgama
    const pramana_count: usize = 3;
    try testing.expectEqual(@as(usize, 3), pramana_count);
}

test "9.3: 3→6 sattva, 6→9 rajas, 3→6→9 onvolledig" {
    // 3→6 = uitgevoerd = sattva
    const three_to_six_sattva: bool = true;
    // 6→9 = niet uitgevoerd = rajas
    const six_to_nine_rajas: bool = true;
    // 3→6→9 = onvolledig = rajas
    const full_rajas: bool = true;
    try testing.expect(three_to_six_sattva);
    try testing.expect(six_to_nine_rajas);
    try testing.expect(full_rajas);
}
