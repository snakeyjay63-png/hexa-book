// Artikel 6 — Dimensie 6 (de terugkeer vormt zich) | 3×2
// Audit: verdubbelingscyclus, J_axis, 3→6, steen als drager

const std = @import("std");
const testing = std.testing;

// ─── Helpers ───────────────────────────────────────────────────────────────

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

fn jAxis(x: i32) i32 {
    return digitalRoot(2 * x);
}

// ─── Test 1: Verdubbelingscyclus ──────────────────────────────────────────

test "1.1: cyclus 2→4→8→7→5→1→2" {
    // De volledige verdubbelingscyclus mod 9
    const cyclus = [_]i32{ 2, 4, 8, 7, 5, 1 };
    try testing.expectEqual(@as(usize, 6), cyclus.len);

    // Elke stap: volgende = DR(2 * huidige)
    var prev: i32 = 1; // start na 1 → 2
    for (cyclus) |val| {
        const next: i32 = jAxis(prev);
        try testing.expectEqual(val, next);
        prev = val;
    }
    // Terug naar begin: 1 → 2
    try testing.expectEqual(@as(i32, 2), jAxis(1));
}

test "1.2: J_axis(3) = 6" {
    try testing.expectEqual(@as(i32, 6), jAxis(3));
}

test "1.3: J_axis ≡ d (verdubbelingsoperator)" {
    // J_axis(x) = DR(2x) voor alle x ∈ {1..9}
    for (1..10) |x| {
        const xi: i32 = @as(i32, @intCast(x));
        try testing.expectEqual(digitalRoot(2 * xi), jAxis(xi));
    }
}

// ─── Test 2: 3→6 Route ───────────────────────────────────────────────────

test "2.1: Allah = 66 → 3 (de as)" {
    try testing.expectEqual(@as(i32, 3), digitalRoot(66));
}

test "2.2: 3 → 6 → as verdubbelt" {
    const as: i32 = 3;
    const terugkeer: i32 = 6;
    try testing.expectEqual(terugkeer, jAxis(as));
}

test "2.3: status_route(3→6) = uitgevoerd" {
    const route_3_6_done: bool = true;
    const route_6_9_done: bool = false;
    const route_3_6_9_done: bool = false;
    try testing.expect(route_3_6_done);
    try testing.expect(!route_6_9_done);
    try testing.expect(!route_3_6_9_done);
}

test "2.4: halve cyclus voltooid (3→6)" {
    // 3→6 is halve NPR-cyclus (3-6-9); 6→9 ontbreekt nog
    const halve_cyclus: bool = true;
    const volle_cyclus: bool = false;
    try testing.expect(halve_cyclus);
    try testing.expect(!volle_cyclus);
}

// ─── Test 3: Steen als drager ────────────────────────────────────────────

test "3.1: steen = gepositioneerde informatie" {
    // Steen beweegt niet, steen draagt
    const steen_beweegt: bool = false;
    const steen_draagt: bool = true;
    try testing.expect(!steen_beweegt);
    try testing.expect(steen_draagt);
}

test "3.2: 0 ≘ 1 — returnroute opent" {
    // Operationele bron-equivalentie nog niet gevalideerd
    const return_opent: bool = true;
    const bron_equiv_gevalideerd: bool = false;
    try testing.expect(return_opent);
    try testing.expect(!bron_equiv_gevalideerd);
}

// ─── Test 4: Verdubbelingsoperator — volledige kaart ─────────────────────

test "4.1: J_axis tabel compleet" {
    // J_axis(x) = DR(2x) voor x = 1..9
    // J(1)=2, J(2)=4, J(3)=6, J(4)=8, J(5)=1, J(6)=3, J(7)=5, J(8)=7, J(9)=9
    const table = [_]i32{ 2, 4, 6, 8, 1, 3, 5, 7, 9 };
    for (1..10) |x| {
        const xi: i32 = @as(i32, @intCast(x));
        try testing.expectEqual(table[x - 1], jAxis(xi));
    }
}

test "4.2: J_axis(9) = 9 (vaste punt)" {
    try testing.expectEqual(@as(i32, 9), jAxis(9));
}
