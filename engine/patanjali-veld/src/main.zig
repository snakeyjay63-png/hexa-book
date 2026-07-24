// Patanjali Router — veld, niet lineair
//
// Alles bestaat tegelijk. Keten = route door het veld.

const std = @import("std");
const dr = @import("digital_root.zig").digitalRoot;
const veld = @import("veld.zig");
const flower = @import("flower_of_life.zig");

pub fn main() void {
    // ── Veld ──
    std.debug.print("\n=== Patanjali-veld ===\n", .{});

    const p = veld.PatanjaliVeld{};
    std.debug.print("Entry: 11 (DR={})\n", .{p.entryDR()});

    const t = p.trillingDRs();
    std.debug.print("Trilling: 11²↔13² ({}↔{})\n", .{ t[0], t[1] });

    const s = p.stilteDRs();
    std.debug.print("Stilte: 17²=19² ({}={})\n", .{ s[0], s[1] });

    std.debug.print("Beide naar entry (DR=2): {}\n", .{p.beideNaarEntry()});

    // ── Richting ──
    std.debug.print("\n=== Richting (vanaf 1) ===\n", .{});
    std.debug.print("  ×2 (vooruit)  → DR({})\n", .{veld.richtingVanaf1(.vooruit)});
    std.debug.print("  /2 (achteruit) → DR({})\n", .{veld.richtingVanaf1(.achteruit)});

    // ── Keten ──
    std.debug.print("\n=== 11→396 Keten ===\n", .{});
    const chain = [_]u16{ 11, 44, 66, 264, 396 };
    const multipliers = [_][]const u8{ "start", "×4", "×1.5", "×4", "×1.5" };
    var dr_chain: [5]u4 = undefined;

    var i: usize = 0;
    while (i < chain.len) : (i += 1) {
        dr_chain[i] = dr(chain[i]);
        std.debug.print("  {d:3} ({s}) → DR={}\n", .{ chain[i], multipliers[i], dr_chain[i] });
    }
    std.debug.print("\nDR cyclus: ", .{});
    i = 0;
    while (i < dr_chain.len) : (i += 1) {
        if (i > 0) std.debug.print(" → ", .{});
        std.debug.print("{}", .{dr_chain[i]});
    }
    std.debug.print("\n", .{});

    // ── Flower of Life ──
    std.debug.print("\n=== Flower of Life ===\n", .{});
    const fol = flower.FlowerOfLife{};
    std.debug.print("Cirkels: {} (DR={})\n", .{ fol.cirkels, fol.drCirkels() });
    std.debug.print("Oogjes: {} (DR={})\n", .{ fol.oogjes_totaal, fol.drOogjes() });
    std.debug.print("Sattva: {}, Tamas: {}, Rajas: {}\n", .{
        flower.FlowerOfLife.gunaOogjes(.sattva),
        flower.FlowerOfLife.gunaOogjes(.tamas),
        flower.FlowerOfLife.gunaOogjes(.rajas),
    });

    std.debug.print("\n=== Veld compleet ===\n", .{});
}
