// digital_root.zig — Digital root (mod 9) veld
//
// DR is geen berekening — het is positie in het veld.

const std = @import("std");

/// Digital root 1-9 (0 voor 0)
pub fn digitalRoot(n: u64) u4 {
    if (n == 0) return 0;
    return @as(u4, @intCast(@rem(n - 1, 9) + 1));
}

/// Mod 9 omkeersfactoren
/// a / b = a × (b⁻¹ mod 9)
const MOD9_INV = [_]u4{ 0, 1, 5, 3, 7, 2, 8, 4, 6 };

/// /divisor in mod 9
pub fn mod9Div(n: u64, divisor: u4) u4 {
    const idx: usize = @as(usize, @intCast(divisor));
    return digitalRoot(n) * MOD9_INV[idx];
}

test "dr basis" {
    try std.testing.expectEqual(@as(u4, 2), digitalRoot(11));
    try std.testing.expectEqual(@as(u4, 4), digitalRoot(13));
    try std.testing.expectEqual(@as(u4, 8), digitalRoot(17));
    try std.testing.expectEqual(@as(u4, 1), digitalRoot(19));
    try std.testing.expectEqual(@as(u4, 9), digitalRoot(396));
}

test "mod9Div /2 = ×5" {
    try std.testing.expectEqual(@as(u4, 5), mod9Div(1, 2));
    try std.testing.expectEqual(@as(u4, 5), mod9Div(289, 2));
}
