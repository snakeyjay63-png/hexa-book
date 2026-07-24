// flower_of_life.zig — Flower of Life veld
//
// 19 cirkels = stilte (DR=1)
// 90 oogjes  = beweging (DR=9)
// 3 gunas    = structuur

const std = @import("std");
const dr = @import("digital_root.zig").digitalRoot;

pub const Guna = enum { sattva, tamas, rajas };

pub const FlowerOfLife = struct {
    cirkels: u8 = 1 + 6 + 12, // 19
    oogjes_binnenin: u8 = 3 * 24, // 72
    oogjes_rand: u8 = 18,
    oogjes_totaal: u8 = 72 + 18, // 90

    pub fn gunaOogjes(g: Guna) u8 {
        return switch (g) {
            .sattva => 24,
            .tamas => 24,
            .rajas => 24 + 18, // rand = overgang, niet buiten
        };
    }

    pub fn drCirkels(self: FlowerOfLife) u4 {
        return dr(self.cirkels);
    }

    pub fn drOogjes(self: FlowerOfLife) u4 {
        return dr(self.oogjes_totaal);
    }

    /// Guna totaal = oogjes totaal
    pub fn gunaTotaal() u8 {
        return gunaOogjes(.sattva) + gunaOogjes(.tamas) + gunaOogjes(.rajas);
    }
};

test "flower of life basis" {
    const fol = FlowerOfLife{};
    try std.testing.expectEqual(@as(u8, 19), fol.cirkels);
    try std.testing.expectEqual(@as(u8, 90), fol.oogjes_totaal);
    try std.testing.expectEqual(@as(u4, 1), fol.drCirkels());
    try std.testing.expectEqual(@as(u4, 9), fol.drOogjes());
}

test "guna mapping" {
    try std.testing.expectEqual(@as(u8, 24), FlowerOfLife.gunaOogjes(.sattva));
    try std.testing.expectEqual(@as(u8, 24), FlowerOfLife.gunaOogjes(.tamas));
    try std.testing.expectEqual(@as(u8, 42), FlowerOfLife.gunaOogjes(.rajas));
    try std.testing.expectEqual(@as(u8, 90), FlowerOfLife.gunaTotaal());
}
