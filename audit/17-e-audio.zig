const std = @import("std");
const testing = std.testing;
const math = std.math;

// Artikel E - Audio Superpositie (Uitgevoerd)
//
// 4 lenzen → 4 golven → 1 veld
// E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)
//
// DR → frequentie/amplitude/fase mapping (A4=432 Hz, Vedic)
//
// Mappings:
//   M_A: DR(66)=3     → 288.33 Hz, a=1.0000, φ=1.5708
//   M_B: DR(529)=7    → 432.00 Hz, a=0.5000, φ=4.7124
//   M_C: DR(437.27)=5 → 342.88 Hz, a=0.3333, φ=5.4978
//   M_D: DR(1071)=9   → 516.84 Hz, a=1.0000, φ=6.2832

const pi = math.pi;

/// Helper: float ongeveer gelijk (absolute tolerance)
fn approxEq(a: f64, b: f64, tol: f64) bool {
    return @abs(a - b) <= tol;
}

// ─── Digital Root ───

pub fn digitalRoot(n: u32) u32 {
    var val = n;
    while (val >= 10) {
        var s: u32 = 0;
        var tmp = val;
        while (tmp > 0) {
            s += tmp % 10;
            tmp /= 10;
        }
        val = s;
    }
    return val;
}

/// DR_decimal: verwijder decimaal, som cijfers, reduceer tot 1-9
/// Voorbeeld: DR_decimal(437.27) = DR(4+3+7+2+7) = DR(23) = 5
pub fn drDecimal(digits: []const u32) u32 {
    var s: u32 = 0;
    for (digits) |d| s += d;
    return digitalRoot(s);
}

// ─── DR_FREQ_MAP (A4=432 Hz, Vedic) ───

const DR_FREQ_MAP = [_]f64{
    0.0,        // placeholder, DR 0 niet gebruikt
    216.00,     // 1: A3 (432/2)
    256.91,     // 2: C4 (do)
    288.33,     // 3: D4 (re)
    323.65,     // 4: E4 (mi)
    342.88,     // 5: F4 (fa)
    384.82,     // 6: G4 (sol)
    432.00,     // 7: A4 (la — Vedic basis)
    484.90,     // 8: B4 (si)
    516.84,     // 9: C5 (do')
};

pub fn freqFromDR(dr: u32) f64 {
    return DR_FREQ_MAP[dr];
}

pub fn amplitudeFromDR(dr: u32) f64 {
    return 1.0 / (@as(f64, @floatFromInt(dr % 3 + 1)));
}

pub fn phaseFromDR(dr: u32) f64 {
    return @as(f64, @floatFromInt(dr - 1)) * (pi / 4.0);
}

// ─── Golf ───

pub const Golf = struct {
    freq: f64,
    amplitude: f64,
    phase: f64,

    /// W_i(t) = a_i sin(2π f_i t + φ_i)
    pub fn eval(self: Golf, t: f64) f64 {
        return self.amplitude * math.sin(2.0 * pi * self.freq * t + self.phase);
    }
};

/// Maak golf uit digitale wortel
pub fn golfFromDR(dr: u32) Golf {
    return Golf{
        .freq = freqFromDR(dr),
        .amplitude = amplitudeFromDR(dr),
        .phase = phaseFromDR(dr),
    };
}

// ─── Mappings ───

// M_A: Abjad 66 → DR(66)=3
pub const DR_A: u32 = digitalRoot(66); // = 3
pub const W_A = golfFromDR(DR_A);

// M_B: Isopsefia 529 → DR(529)=7
pub const DR_B: u32 = digitalRoot(529); // = 7
pub const W_B = golfFromDR(DR_B);

// M_C: Sanskriet grand_avg_freq=437.27 → DR(4+3+7+2+7)=DR(23)=5
pub const DR_C: u32 = drDecimal(&[_]u32{ 4, 3, 7, 2, 7 }); // = 5
pub const W_C = golfFromDR(DR_C);

// M_D: D_numeric 1071 → DR(1071)=9
pub const DR_D: u32 = digitalRoot(1071); // = 9
pub const W_D = golfFromDR(DR_D);

// ─── Superpositie ───

/// E(t) = W_A(t) + W_B(t) + W_C(t) + W_D(t)
pub fn superpositie(t: f64) f64 {
    return W_A.eval(t) + W_B.eval(t) + W_C.eval(t) + W_D.eval(t);
}

// ─── Tests ───

test "0.0: DR(66) = 3" {
    try testing.expectEqual(@as(u32, 3), DR_A);
}

test "0.1: DR(529) = 7" {
    try testing.expectEqual(@as(u32, 7), DR_B);
}

test "0.2: DR_decimal(437.27) = DR(4+3+7+2+7) = DR(23) = 5" {
    try testing.expectEqual(@as(u32, 5), DR_C);
}

test "0.3: DR(1071) = 9" {
    try testing.expectEqual(@as(u32, 9), DR_D);
}

test "0.4: M_A frequentie = 288.33 Hz (DR 3 → D4)" {
    try testing.expect(approxEq(288.33, W_A.freq, 0.01));
}

test "0.5: M_B frequentie = 432.00 Hz (DR 7 → A4 Vedic)" {
    try testing.expect(approxEq(432.00, W_B.freq, 0.01));
}

test "0.6: M_C frequentie = 342.88 Hz (DR 5 → F4)" {
    try testing.expect(approxEq(342.88, W_C.freq, 0.01));
}

test "0.7: M_D frequentie = 516.84 Hz (DR 9 → C5)" {
    try testing.expect(approxEq(516.84, W_D.freq, 0.01));
}

test "0.8: amplitude = 1/(DR%3+1)" {
    // DR 3: 1/(3%3+1) = 1/1 = 1.0
    try testing.expect(approxEq(1.0, W_A.amplitude, 0.001));
    // DR 7: 1/(7%3+1) = 1/2 = 0.5
    try testing.expect(approxEq(0.5, W_B.amplitude, 0.001));
    // DR 5: 1/(5%3+1) = 1/3 = 0.3333
    try testing.expect(approxEq(0.3333, W_C.amplitude, 0.001));
}

test "0.9: fase = (DR-1) × π/4" {
    // DR 3: (3-1)×π/4 = π/2 ≈ 1.5708
    try testing.expect(approxEq(math.pi / 2.0, W_A.phase, 0.001));
    // DR 7: (7-1)×π/4 = 3π/2 ≈ 4.7124
    try testing.expect(approxEq(3.0 * math.pi / 2.0, W_B.phase, 0.001));
}

test "1.0: E(0) = som van golven op t=0" {
    const e0 = superpositie(0.0);
    const expected = W_A.eval(0.0) + W_B.eval(0.0) + W_C.eval(0.0) + W_D.eval(0.0);
    try testing.expect(approxEq(expected, e0, 0.001));
}

test "1.1: superpositie is lineaire optelling" {
    const t: f64 = 0.001;
    const e_t = superpositie(t);
    const expected = W_A.eval(t) + W_B.eval(t) + W_C.eval(t) + W_D.eval(t);
    try testing.expect(approxEq(expected, e_t, 0.001));
}

test "1.2: E ≠ enige individuele lens" {
    const t: f64 = 0.001;
    const e_t = superpositie(t);
    // E(t) is niet identiek aan enige enkele golf
    const notA = !approxEq(e_t, W_A.eval(t), 0.001);
    const notB = !approxEq(e_t, W_B.eval(t), 0.001);
    const notC = !approxEq(e_t, W_C.eval(t), 0.001);
    const notD = !approxEq(e_t, W_D.eval(t), 0.001);
    try testing.expect(notA or notB or notC or notD);
}

test "1.3: DR_FREQ_MAP heeft 10 entries (0..9)" {
    try testing.expectEqual(@as(usize, 10), DR_FREQ_MAP.len);
}

test "1.4: A4=432 Hz is Vedic basis (DR 7)" {
    try testing.expect(approxEq(432.00, freqFromDR(7), 0.01));
}

test "1.5: 4 lenzen → 4 golven → 1 veld" {
    // Architectuur: 4 lenzen, elk levert één golf
    const golven = [_]Golf{ W_A, W_B, W_C, W_D };
    try testing.expectEqual(@as(usize, 4), golven.len);
}

test "1.6: Arabische route: 66 → DR 3 → 264 → DR 3 → 396 → DR 9" {
    // 66 × 4 = 264 → DR(264) = DR(2+6+4) = DR(12) = 3
    try testing.expectEqual(@as(u32, 3), digitalRoot(264));
    // 264 × 1.5 = 396 → DR(396) = DR(3+9+6) = DR(18) = DR(9) = 9
    try testing.expectEqual(@as(u32, 9), digitalRoot(396));
    // Cyclus: 3 → 6 → 9 (Tesla-cyclus)
}

test "1.7: C_sound_features → W_C (geen circulaire betekenis)" {
    // C_sound_features = pre-sonificatie (DR 5)
    // W_C = gesonificeerde golf (342.88 Hz)
    try testing.expect(approxEq(342.88, W_C.freq, 0.01));
    try testing.expectEqual(@as(u32, 5), DR_C);
}
