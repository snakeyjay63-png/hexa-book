const std = @import("std");
const testing = std.testing;

// Artikel 4 - Dimensie 4 (Expansie) | Mandelbrot: 0.0.0.0
//
// z(n+1) = z(n)² + c
// M = { c ∈ C : (z_n)_{n≥0} blijft begrensd }
//
// HEXA mapping:
//   ρ_HEXA(0_C) = 0.0.0.0
//   ρ_Mandelbrot-role(0_C) = bronpunt
//   ρ_NPR-source(0) = ongedifferentieerd bronveld
//
// Lensaxioma: 0 ≠ 1 (lokaal), 0 ≐_lens 1 (route sluit bijzelfde bron)

// ─── Complex Number ───

const Complex = struct {
    re: f64,
    im: f64,

    pub fn mul(self: Complex, other: Complex) Complex {
        return Complex{
            .re = self.re * other.re - self.im * other.im,
            .im = self.re * other.im + self.im * other.re,
        };
    }

    pub fn add(self: Complex, other: Complex) Complex {
        return Complex{
            .re = self.re + other.re,
            .im = self.im + other.im,
        };
    }

    pub fn magSq(self: Complex) f64 {
        return self.re * self.re + self.im * self.im;
    }
};

// ─── Mandelbrot Core ───

const MAX_ITER = 256;
const ESCAPE_THRESH: f64 = 4.0; // |z|² > 4 → divergeert

/// Return number of iterations before escape, or MAX_ITER if bounded.
pub fn mandelbrotIter(c: Complex) usize {
    var z: Complex = .{ .re = 0.0, .im = 0.0 };
    var i: usize = 0;
    while (i < MAX_ITER) : (i += 1) {
        z = z.mul(z).add(c);
        if (z.magSq() > ESCAPE_THRESH) {
            return i;
        }
    }
    return MAX_ITER;
}

/// Is c in the Mandelbrot set (within threshold)?
pub fn isInMandelbrot(c: Complex) bool {
    return mandelbrotIter(c) == MAX_ITER;
}

// ─── HEXA Projection ───

pub const HEXARole = enum {
    bronpunt,     // c = 0, absolute stabiliteit
    begrensd,     // c ∈ M, maar ≠ 0
    divergeert,   // c ∉ M
};

pub fn hexaRole(c: Complex) HEXARole {
    if (c.re == 0.0 and c.im == 0.0) return .bronpunt;
    if (isInMandelbrot(c)) return .begrensd;
    return .divergeert;
}

// ─── Tests ───

test "0.0: bronpunt c=0 heeft absolute stabiliteit" {
    const c_zero = Complex{ .re = 0.0, .im = 0.0 };
    try testing.expectEqual(HEXARole.bronpunt, hexaRole(c_zero));
}

test "0.1: c=0 divergeert niet" {
    const c_zero = Complex{ .re = 0.0, .im = 0.0 };
    try testing.expectEqual(MAX_ITER, mandelbrotIter(c_zero));
}

test "0.2: c=0 blijft op z=0 (geen escape)" {
    const c_zero = Complex{ .re = 0.0, .im = 0.0 };
    try testing.expect(isInMandelbrot(c_zero));
}

test "0.3: c=1 divergeert" {
    const c_one = Complex{ .re = 1.0, .im = 0.0 };
    try testing.expectEqual(HEXARole.divergeert, hexaRole(c_one));
}

test "0.4: c=-0.75 is begrensd (in de set)" {
    const c = Complex{ .re = -0.75, .im = 0.0 };
    try testing.expect(isInMandelbrot(c));
}

test "0.5: c=-0.75 is geen bronpunt" {
    const c = Complex{ .re = -0.75, .im = 0.0 };
    try testing.expectEqual(HEXARole.begrensd, hexaRole(c));
}

test "0.6: c=2i divergeert" {
    const c = Complex{ .re = 0.0, .im = 2.0 };
    try testing.expect(!isInMandelbrot(c));
}

test "0.7: c=-1 is begrensd (boundary cycling)" {
    const c = Complex{ .re = -1.0, .im = 0.0 };
    try testing.expect(isInMandelbrot(c));
}

test "0.8: 0≠1 lokaal, maar ≐_lens via route" {
    const c_zero = Complex{ .re = 0.0, .im = 0.0 };
    const c_one = Complex{ .re = 1.0, .im = 0.0 };

    // Lokaal verschillend
    try testing.expectEqual(HEXARole.bronpunt, hexaRole(c_zero));
    try testing.expectEqual(HEXARole.divergeert, hexaRole(c_one));

    // Maar beide vertrekken vanuit z_0 = 0 (zelfde bronpunt)
    // Lensaxioma: route sluit bijzelfde bron
    // Dit is een interpretatief onderscheid, geen computationeel
}

test "0.9: escape threshold correct" {
    // |z|² > 4 = escape
    const big = Complex{ .re = 2.1, .im = 0.0 };
    try testing.expect(big.magSq() > ESCAPE_THRESH);

    const small = Complex{ .re = 1.9, .im = 0.0 };
    try testing.expect(small.magSq() <= ESCAPE_THRESH);
}

test "1.0: iteraties nemen af met grotere c" {
    const c_small = Complex{ .re = 0.1, .im = 0.0 };
    const c_big = Complex{ .re = 2.0, .im = 0.0 };

    const iter_small = mandelbrotIter(c_small);
    const iter_big = mandelbrotIter(c_big);

    // Grotere c → snellere escape (minder iteraties)
    try testing.expect(iter_big < iter_small);
}

test "1.1: Mandelbrot-lens is interpretatief" {
    // ρ_Mandelbrot-lens projecteert, meet niet "zuivere" realiteit
    // operator_status = interpretatief
    // Dit test dat onze projectie consistent is
    const c = Complex{ .re = -0.5, .im = 0.5 };
    const role = hexaRole(c);

    // Moet een van de drie rollen zijn
    switch (role) {
        .bronpunt, .begrensd, .divergeert => {},
    }
}

test "1.2: 0.0.0.0 = potentie, kijken = collapse" {
    // c=0 is het bronpunt: z blijft op 0, geen escape
    // In HEXA: dit is 0.0.0.0 — ongedifferentieerd bronveld
    // Kijken (itereren) = framerate collapse naar één pad
    const c_zero = Complex{ .re = 0.0, .im = 0.0 };
    try testing.expectEqual(HEXARole.bronpunt, hexaRole(c_zero));
    try testing.expect(isInMandelbrot(c_zero));
}
