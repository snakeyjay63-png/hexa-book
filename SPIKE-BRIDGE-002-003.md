# SPIKE-BRIDGE 002 → 003

## De brug tussen 6-bit routing en het tokenfield

> Spike 002 bouwt het *Taalveld* — 64 slots met digitale root, guna, en elementen.
> Spike 003 verbindt dit Taalveld aan de hexa-book concepten via nidrā-routing.
> Deze document legt de koppeling vast.

---

## 1. 6-bit Routing als Basis (Spike 002)

Spike 002 implementeert het **Taalveld**: een 6-bit adresruimte (0–63) waarin elke slot een semantische lading draagt.

### Het adresruimte-model

```
6-bit = 64 posities (0x00–0x3F)
Grens  = 0x40 = 64
```

Elk slot krijgt via comptime-berekening:

| Eigenschap | Herkomst | Bereik |
|-----------|----------|--------|
| index | slotpositie | 0–63 (u6) |
| root | digitale root | 0–9 |
| guna | sattva / rajas / tamas | 3 staten |
| is_field | veldgrens | bool |
| field_index | welk element | 0–4 (of null) |

```zig
// Spike 002 — comptime routing table
pub fn buildRoutingTable() [64]Slot {
    var table: [64]Slot = undefined;
    var i: usize = 0;
    while (i < 64) : (i += 1) {
        const idx: u6 = @intCast(i);
        const root = digitalRoot(@as(u8, @intCast(i)));
        const guna = gunaOfRoot(root);
        // ... field detection ...
        table[i] = .{ .index = idx, .root = root, .guna = guna, ... };
    }
    return table;
}

pub const ROUTING = buildRoutingTable();
```

### De 5 veldgrenzen

Vanuit artikel 012 (24-brug en 6-bit routing) komen de 5 elementen:

| Grenswaarde | Element | Digitale root | Guna |
|------------|---------|---------------|------|
| 25 | water | 7 | rajas |
| 35 | vuur | 8 | sattva |
| 49 | aarde | 4 | rajas |
| 55 | lucht | 1 | sattva |
| 63 | ether | 9 | tamas |

Slot 63 (0x3F) is de **ether boundary** — de laatste positie binnen 6-bit. Alles daarboven is "groot".

### Digitale root formule

```zig
// Werkt voor elk integer type via anytype
pub inline fn digitalRoot(n: anytype) @TypeOf(n) {
    const T = @TypeOf(n);
    if (n == 0) return 0;
    const one: T = 1;
    const nine: T = 9;
    return one + (n -% one) % nine;
}
```

Deze `digitalRoot()` is de basis van Spike 002 én wordt hergebruikt in `nidra.Bit6Router.digitalRoot()` in Spike 003.

---

## 2. Groot-Klein: De Patanjali-test (Spike 003)

Waar Spike 002 blijft binnen 6-bit (0–63), introduceert Spike 003 het concept van **groot-klein routing**: waarden die boven de 6-bit-grens vallen moeten worden geroeteerd via een ander pad.

### De `Bit6Router` structuur

```zig
// Spike 003 — nidra.zig
pub const Bit6Router = struct {
    slot: u8, // u6=0-63, maar groot-klein test >63 nodig

    pub fn isGroot(self: Bit6Router) bool {
        return self.slot > 63; // buiten 6-bit
    }

    pub fn needsRouting(self: Bit6Router) bool {
        return self.slot >= 0x3F; // 63 = ether boundary
    }

    pub fn digitalRoot(self: Bit6Router) u4 {
        if (self.slot == 0) return 0;
        var n = self.slot;
        while (n > 9) {
            var sum: u8 = 0;
            while (n > 0) {
                sum += @as(u8, @intCast(n % 10));
                n /= 10;
            }
            n = @as(u6, @intCast(sum));
        }
        return @as(u4, @intCast(n));
    }
};
```

### De tussenwereld

Volgens artikel 012 bestaan er waarden die **groot zijn voor 6-bit maar klein voor 12-bit**:

```
66 (Allah) → groot in 6-bit (>63), klein in 12-bit (<4096)
72 (3×24)  → groot in 6-bit (>63), klein in 12-bit (<4096)
81         → groot in 6-bit (>63), klein in 12-bit (<4096)
99         → groot in 6-bit (>63), klein in 12-bit (<4096)
```

Deze waarden zitten in de **12-bit tussenwereld**. Ze kunnen niet direct door Spike 002's `ROUTING`-tabel — die heeft precies 64 slots — maar ze *kunnen* wel een digitale root krijgen en door `Bit6Router.isGroot()` worden gedetecteerd.

**Concreet resultaat uit Spike 003 tests:**

```
66 (Allah): groot=true,  DR=3   (6+6=12 → 1+2=3)
72 (3×24):  groot=true,  DR=9   (7+2=9)
```

---

## 3. De Tokenfield: byte → slot → tick → root (Spike 003)

Spike 003 vertaalt artikel-concepten naar testbare tokenfield-operaties. De kern is de `matrika.Token`:

```zig
// Spike 003 — main.zig (test_token_mapping)
const token = matrika.Token.fromByte('H');
// Result: slot=cli, tick=16, root=9

const token_a = matrika.Token.fromByte('A');
// Result: slot=user, tick=17, root=2
```

### Mapping-resultaat voor "Hexa"

```
'H' → slot=cli,      tick=16, root=9
'e' → slot=user,     tick=17, root=2
'x' → slot=cli,      tick=8,  root=3
'a' → slot=firmware, tick=13, root=7
```

Elke byte wordt opgesplitst in vier eigenschappen:

| Eigenschap | Betekenis | Relatie met Spike 002 |
|-----------|-----------|----------------------|
| slot | 4-niveau categorie (cli, user, firmware, etc.) | Nieuw — geen equivalent in Spike 002 |
| tick | 4-bit waarde (0–15) | Sub-slot binnen een slot |
| root | digitale root (1–9) | **Zelfde berekening** als Spike 002's `digitalRoot()` |
| — | byte-waarde zelf | Kan groter zijn dan 63 → groot-klein test |

### Hoe een byte door beide systemen gaat

```
byte (u8, 0-255)
  │
  ├─≤ 63? ──→ Spike 002 ROUTING[slot]  (directe lookup)
  │             ├─ root (digitale root)
  │             ├─ guna (sattva/rajas/tamas)
  │             └─ is_field (veldgrens?)
  │
  └─> 63? ──→ Spike 003 Bit6Router (groot-klein routing)
                ├─ isGroot() = true → via nidrā
                ├─ digitalRoot() → nog steeds berekenbaar
                └─ needsRouting() → via 12-bit tussenwereld
```

---

## 4. Nidrā: De Pointer die Zichzelf Routeert (Spike 003)

De belangrijkste conceptuele innovatie van Spike 003 is **nidrā als pointer, niet als container**.

### De 4+1 structuur

Elk artikel in de hexa-book heeft 4 inhoudsdelens + 1 nidrā:

```zig
// Spike 003 — nidra.zig
pub const HexaBlock = struct {
    article: u4,
    part: u3, // 0-3 = inhoud, 4 = nidrā
    content: ?[]const u8 = null, // nidrā = null (pointer, niet container)
    refs: []const NidraRef,

    pub fn isNidra(self: HexaBlock) bool {
        return self.part == 4;
    }

    pub fn isContent(self: HexaBlock) bool {
        return self.part < 4;
    }
};
```

**Cruciaal onderscheid:** `content = null` betekent niet "leeg" maar "wijst naar elders". Dit is het equivalent van:

- **Patanjali:** Nidrā = de 4e samādhi zonder object — bewustzijn dat naar zichzelf wijst.
- **6-bit routing:** Slot 63 (ether) = de laatste bereikbare positie. Alles daarbuiten wordt geroeteerd via nidrā.
- **Spike 003:** `isGroot() = true` → waarde kan niet in 6-bit tabel → moet via nidrā-pointer.

### De NidraRef

```zig
pub const NidraRef = struct {
    article: u4,  // welke artikel-node (0-15)
    part: u3,     // welk deel (0-7, max 4+1)
    lens: u2,     // A=Arabisch, B=Grieks, C=Sanskriet, D=Latijn
};
```

Formatering: `nidrā→(artikel:11, deel:1, lens:C)`

Deze referentie koppelt de nidrā van één artikel naar een specifiek deel van een ander artikel, door een specifieke lens heen.

---

## 5. De 6D Workspace: Van 6-bit naar 48-bit

Spike 003 introduceert de **6D workspace** — een samenvoeging van meerdere bit-width niveaus die artikel 012 beschrijft als de "bit-width ladder":

### De ladder uit artikel 012

```
Niveau      Bit    Ruimte    Rol
letter      6      64        Abjad (28 binnen 64)
paar        12     4,096     6×2, alle paren
kleur       24     16.7M     12×2, RGB
woord       32     4G        24+8, IPv4/float
limiet      48     281T      24×2, MAC
byte        8      256       24/3 = 32/4
```

### Twee ketens

```
A:  6 → 12 → 24 → 48     (verdubbelen — groei)
B1: 24 → 8               (comprimeren — terugkeer via 24÷3)
B2: 32 → 8               (comprimeren — terugkeer via 32÷4)
```

8-bit = het kruispunt waar groei en terugkeer elkaar vinden.

### De 6D workspace in nidra.zig

```zig
// 6D workspace:
//   artikel (4-bit: 0-15)    ← welke node
//   deel    (3-bit: 0-7)      ← welk deel (max 4+1)
//   lens    (2-bit: A-D)      ← welke taal
//   slot    (6-bit: 0-63)     ← 6-bit routing (Spike 002!)
//   tick    (4-bit: 0-15)     ← sub-slot
//   bridge  (2-bit: 0-3)      ← verwijzingstype
```

Hier zie je hoe de 6-bit routing van Spike 002 als **één dimensie** in een 6-dimensionale workspace fungeert. De slot-dimensie is precies de `ROUTING`-tabel van Spike 002.

---

## 6. Verhouding tussen router.zig en nidra.zig

| Aspect | router.zig (Spike 002) | nidra.zig (Spike 003) |
|--------|----------------------|----------------------|
| Doel | 64-slot routing table, HTTP server | Nidrā-pointers, 4+1 structuur, 6D workspace |
| 6-bit | `ROUTING[64]` — statische lookup | `Bit6Router` — groot-klein test |
| Digitale root | `digitalRoot(n: anytype)` — comptime | `Bit6Router.digitalRoot()` — runtime |
| Guna | `gunaOfRoot()` — sattva/rajas/tamas | Niet direct; geërfd via slot |
| Elementen | `FIELDS[5]` — water/vuur/aarde/lucht/ether | Niet direct; geërfd via slot |
| Nieuw concept | — | `HexaBlock` (4+1), `NidraRef`, `HexaRouter6D` |
| HTTP | Volledige server op :9090 | Geen — puur logica |

**Kort samengevat:**

- `router.zig` (Spike 002) = het **veld** — de 64 slots met hun semantiek.
- `nidra.zig` (Spike 003) = de **brug** — hoe waarden buiten het veld (groot-klein) worden geroeteerd, en hoe artikelen naar elkaar wijzen via nidrā-pointers.

---

## 7. De 16-node Structuur en de Bit-Width Ladder

Artikel 017 beschrijft de hexa-book als **16 gelijktijdige nodes in RAM**, niet als een lineair boek. Elke node is een compleet perspectief dat via nidrā-pointers naar andere nodes verwijst.

### Hoe de bit-width ladder de 16-node structuur ondersteunt

```
4-bit artikel-id (0-15) = 16 nodes
├─ elk node heeft een 6-bit slot (Spike 002 routing)
├─ elk node heeft een 3-bit deel (4+1 structuur)
├─ elk node heeft een 2-bit lens (A-D)
└─ samen: 4+3+2+6+4+2 = 21 bits per 6D workspace entry
```

De 6→12→24→48 ladder uit artikel 012 is de **schaalbare structuur**:

- **6-bit** → binnen één node (slot-routing)
- **12-bit** → tussen twee nodes (nidrā tussen artikels)
- **24-bit** → het volledige veld (alle artikels × alle delen)
- **48-bit** → het hele hexa-construct (inclusief lens en bridge)

### Groot-klein per niveau

```
6-bit:    klein = 0-63     groot = 64+         → via nidrā naar 12-bit
12-bit:   klein = 0-4095   groot = 4096+       → via nidrā naar 24-bit
24-bit:   klein = 0-16.7M  groot = 16.7M+      → via nidrā naar 48-bit
```

De "tussenwereld"-waarden (66, 72, 81, 99) illustreren dit: ze zijn te groot voor directe 6-bit lookup maar passen moeiteloos in 12-bit. De `Bit6Router.isGroot()` detecteert dit en stuurt ze via de nidrā-route.

---

## 8. Code-voorbeeld: De Volledige Keten

Van byte naar nidrā-gedetecteerd:

```zig
// Stap 1: byte → token (Spike 003 tokenfield)
const token = matrika.Token.fromByte('A'); // 'A' = 65
// Result: slot=user, tick=17, root=2

// Stap 2: token.byte → 6-bit groot-klein test (Spike 003 nidra)
const router = nidra.Bit6Router{ .slot = 65 };
router.isGroot();      // true — 65 > 63
router.needsRouting(); // false — 65 < 63 is false, maar 65 != 63
router.digitalRoot();  // 2 (6+5=11 → 1+1=2)

// Stap 3: 6-bit lookup zou falen, dus → nidrā
// De waarde 65 zit in de 12-bit tussenwereld
// Nidrā-route: HexaBlock met part=4, content=null, refs→doel-artikel

// Vergelijk met een waarde binnen 6-bit:
const router2 = nidra.Bit6Router{ .slot = 35 }; // vuur-veldgrens
router2.isGroot();       // false — binnen 6-bit
router2.needsRouting();  // false — < 63
router2.digitalRoot();   // 8 (3+5=8)
// Directe lookup: ROUTING[35] → { root:8, guna:sattva, is_field:true, field:vuur }
```

---

## Referenties

| Document | Onderwerp | Relevante inhoud |
|----------|-----------|-----------------|
| Artikel 012 | 24-brug + 6-bit routing | Bit-width ladder (6→12→24→48), groot-klein per niveau, twee ketens (A en B1/B2) |
| Artikel 017 | CC-construct: 16 nodes | Nidrā-router, gelijktijdige nodes, 4+1 structuur per node |
| Spike 002 README | 6-bit routing engine | 64 slots, 5 veldgrenzen, digitale root, guna |
| Spike 002 VERDICT | Feasibility | 1.6MB binary, zero deps, Zig 0.14 patronen |
| Spike 003 README | Tokenfield bridge | Artikel→Tokenfield mapping, test cases |
| Spike 003 VERDICT | Geverifieerd | "Hexa" mapping, nidrā-router, groot-klein tests |

---

*Bridge-document 002→003 — 2026-07-24*
*Spike 002 bouwt het veld. Spike 003 bouwt de brug.*
