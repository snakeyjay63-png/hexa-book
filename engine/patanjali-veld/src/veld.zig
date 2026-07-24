// veld.zig — Het Patanjali-veld (niet-lineair)
//
// Alles bestaat tegelijk. De keten is de route, niet de structuur.

const std = @import("std");
const dr = @import("digital_root.zig").digitalRoot;

// ============================================================
// Richting: ×2 en /2 vanaf 1
// ============================================================
pub const Richting = enum {
    vooruit,  // ×2
    achteruit, // /2 (= ×5 in mod 9)
};

/// DR vanuit 1 met richting
/// ×2 = vooruit, /2 = achteruit
pub fn richtingVanaf1(r: Richting) u4 {
    return switch (r) {
        .vooruit => dr(1 * 2),   // → 2
        .achteruit => dr(1 * 5), // → 5 (mod 9: /2 = ×5)
    };
}

// ============================================================
// Kwadraat Paarspiegel
// ============================================================
pub const KwadraatPaar = struct {
    klein: u16,
    groot: u16,

    /// DR van beide kwadraten
    pub fn drKwadraten(self: KwadraatPaar) [2]u4 {
        return .{ dr(@as(u64, self.klein) * self.klein), dr(@as(u64, self.groot) * self.groot) };
    }

    /// Som kwadraten → DR (terug naar entry)
    pub fn somKwadratenDR(self: KwadraatPaar) u4 {
        const s = @as(u64, self.klein) * self.klein + @as(u64, self.groot) * self.groot;
        return dr(s);
    }
};

// ============================================================
// Het Veld — alle relaties tegelijk
// ============================================================
pub const PatanjaliVeld = struct {
    /// 11/13: trilling (spiegel)
    pub const trilling: KwadraatPaar = .{ .klein = 11, .groot = 13 };

    /// 17/19: stilte (samenvallen)
    pub const stilte: KwadraatPaar = .{ .klein = 17, .groot = 19 };

    /// Entry-point: 11 (default)
    entry: u8 = 11,

    /// Het veld is één structuur — keten is route erdoorheen
    pub fn entryDR(self: PatanjaliVeld) u4 {
        return dr(self.entry);
    }

    /// Beide paren sommen naar entry DR
    pub fn beideNaarEntry(self: PatanjaliVeld) bool {
        _ = self;
        return trilling.somKwadratenDR() == dr(11) and
               stilte.somKwadratenDR() == dr(11);
    }

    /// Trilling: 4 ↔ 7 (spiegel)
    pub fn trillingDRs(_: PatanjaliVeld) [2]u4 {
        return trilling.drKwadraten();
    }

    /// Stilte: 1 = 1 (samenvallen)
    pub fn stilteDRs(_: PatanjaliVeld) [2]u4 {
        return stilte.drKwadraten();
    }
};

test "veld structuur" {
    const veld = PatanjaliVeld{};

    // Entry
    try std.testing.expectEqual(@as(u4, 2), veld.entryDR());

    // Trilling: 4 ↔ 7
    const t = veld.trillingDRs();
    try std.testing.expectEqual(@as(u4, 4), t[0]);
    try std.testing.expectEqual(@as(u4, 7), t[1]);

    // Stilte: 1 = 1
    const s = veld.stilteDRs();
    try std.testing.expectEqual(@as(u4, 1), s[0]);
    try std.testing.expectEqual(@as(u4, 1), s[1]);

    // Beide sommen naar entry (DR=2)
    try std.testing.expect(veld.beideNaarEntry());
}
