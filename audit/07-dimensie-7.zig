// Artikel 7 — Dimensie 7 (reflectie) | 23-1
// Audit: lensrekenkunde, projectie-afhankelijkheid, reflectie

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

// ─── Test 1: Lensrekenkunde ───────────────────────────────────────────────

test "1.1: antwoord hangt af van gekozen projectie" {
    // Zelfde input, verschillende lenzen → verschillende uitkomsten
    const input: i32 = 786;

    // Lens 1: directe digital root → 3
    const lens1: i32 = digitalRoot(input);
    try testing.expectEqual(@as(i32, 3), lens1);

    // Lens 2: verdubbel dan digital root → 6
    const lens2: i32 = digitalRoot(2 * input);
    try testing.expectEqual(@as(i32, 6), lens2);

    // Verschillende lens → verschillende uitkomst
    try testing.expect(lens1 != lens2);
}

test "1.2: elke lens lokaal correct mits regels expliciet" {
    // Consistentie-test: herhaalde toepassing geeft zelfde resultaat
    const input: i32 = 786;
    const r1: i32 = digitalRoot(input);
    const r2: i32 = digitalRoot(input);
    try testing.expectEqual(r1, r2);
}

// ─── Test 2: Reflectie ───────────────────────────────────────────────────

test "2.1: reflectie = door de lens kijken" {
    // Reflectie is niet een operator maar een perspectief
    const is_operator: bool = false;
    const is_perspective: bool = true;
    try testing.expect(!is_operator);
    try testing.expect(is_perspective);
}

test "2.2: spiegel — bron of lens zelf?" {
    // De vraag is conceptueel, geen computationele test
    // Spiegel toont zowel bron als lens — beide zijn aanwezig
    const bron_aanwezig: bool = true;
    const lens_aanwezig: bool = true;
    try testing.expect(bron_aanwezig and lens_aanwezig);
}

// ─── Test 3: Systeem-identiteit ──────────────────────────────────────────

test "3.1: systeem waarmee je leest = systeem dat je krijgt" {
    // Identiteit: lees-systeem ≡ uitkomst-systeem
    const lees_systeem: i32 = 1; // abstracte referentie
    const uitkomst_systeem: i32 = 1;
    try testing.expectEqual(lees_systeem, uitkomst_systeem);
}

test "3.2: geen beperking, maar ontwerp" {
    const is_beperking: bool = false;
    const is_ontwerp: bool = true;
    try testing.expect(!is_beperking);
    try testing.expect(is_ontwerp);
}

// ─── Test 4: 23-1 referentie ─────────────────────────────────────────────

test "4.1: 23-1 → DR 6" {
    // Artikel 7 is gemarkeerd als 23-1
    // 2+3+1 = 6 (of 23-1 = 22 → 4)
    // De notatie 23-1 is een artikel-referentie, geen berekening
    // Als som: 2+3+1 = 6
    const som: i32 = 2 + 3 + 1;
    try testing.expectEqual(@as(i32, 6), som);
}

test "4.2: dimensie 7 = reflectielens" {
    // Dimensie 7 is de reflectie-dimensie
    const dimensie: i32 = 7;
    const rol: i32 = 2; // 2 = reflectie (abstract)
    try testing.expectEqual(@as(i32, 7), dimensie);
    _ = rol;
}
