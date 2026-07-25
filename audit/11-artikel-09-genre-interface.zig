const std = @import("std");
const testing = std.testing;
const math = std.math;

// === Artikel 09: Genre als Interface-Taal ===
// Muziek = code = taal = computationele potentie audit

// === 1. Synth Geometrie ===
// Elke synth = geometrisch ontwerp dat vertraagt tot geluid

const Synth = struct {
    naam: []const u8,
    geometrie: []const u8,
    vertraging_min_ms: f64,
    vertraging_max_ms: f64,
    uitgang: []const u8,
};

const SYNTHS = [_]Synth{
    .{ .naam = "Moog", .geometrie = "filterhoek", .vertraging_min_ms = 40, .vertraging_max_ms = 200, .uitgang = "warme bas" },
    .{ .naam = "ARP", .geometrie = "LFO", .vertraging_min_ms = 100, .vertraging_max_ms = 500, .uitgang = "modulatiediepte" },
    .{ .naam = "Buchla", .geometrie = "mesh", .vertraging_min_ms = 200, .vertraging_max_ms = 1000, .uitgang = "organische textuur" },
    .{ .naam = "Oberheim", .geometrie = "osc_stack", .vertraging_min_ms = 50, .vertraging_max_ms = 300, .uitgang = "supersaw breedte" },
    .{ .naam = "Roland", .geometrie = "PWM", .vertraging_min_ms = 10, .vertraging_max_ms = 100, .uitgang = "timbre shift" },
};

// CPU: ritme controleren
pub fn cpuRitmeControleren(bpm: f64) f64 {
    // Retourneer beat duur in seconden
    return 60.0 / bpm;
}

// GPU: synth geometrie berekenen
pub fn gpuSynthGeometrie(synth: *const Synth, t_ms: f64) f64 {
    // Normaliseer tijd binnen vertraging-range
    const range = synth.vertraging_max_ms - synth.vertraging_min_ms;
    const t_norm = std.math.clamp(t_ms - synth.vertraging_min_ms, 0.0, range);
    const progress = t_norm / range;
    return progress;
}

test "synth geometrie: vertraging binnen range" {
    const moog = &SYNTHS[0];
    try testing.expectEqualStrings("Moog", moog.naam);
    try testing.expect(moog.vertraging_min_ms > 0);
    try testing.expect(moog.vertraging_max_ms > moog.vertraging_min_ms);
}

test "cpu ritme: 140 BPM = 0.429s beat" {
    const beat_dur = cpuRitmeControleren(140.0);
    try testing.expect(math.approxEqAbs(f64, beat_dur, 60.0 / 140.0, 0.001));
}

test "gpu synth geometrie: progress 0→1 binnen range" {
    const moog = &SYNTHS[0];
    const p_min = gpuSynthGeometrie(moog, moog.vertraging_min_ms);
    const p_max = gpuSynthGeometrie(moog, moog.vertraging_max_ms);

    try testing.expect(math.approxEqAbs(f64, p_min, 0.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, p_max, 1.0, 0.01));
}

// === 2. Psytrance = Interface-Taal ===
// Ritme + geometrie = genre

const Genre = struct {
    naam: []const u8,
    cpu_bpm: f64,
    gpu_layers: u8,
    synth_set: []const []const u8,
};

const GENRES = [_]Genre{
    .{ .naam = "Psytrance", .cpu_bpm = 140.0, .gpu_layers = 16, .synth_set = &[_][]const u8{ "Moog", "Buchla", "Oberheim" } },
    .{ .naam = "Techno", .cpu_bpm = 128.0, .gpu_layers = 8, .synth_set = &[_][]const u8{ "Roland" } },
    .{ .naam = "Ambient", .cpu_bpm = 0.0, .gpu_layers = 24, .synth_set = &[_][]const u8{ "Buchla" } },
    .{ .naam = "IDM", .cpu_bpm = 160.0, .gpu_layers = 20, .synth_set = &[_][]const u8{ "Moog", "ARP", "Buchla" } },
};

// CPU: genre = ritme + synth-keuze
pub fn cpuGenreRitme(g: *const Genre) f64 {
    return cpuRitmeControleren(g.cpu_bpm);
}

// GPU: genre = veld + laagtel
pub fn gpuGenreVeld(g: *const Genre) usize {
    return g.synth_set.len;
}

test "psytrance = CPU 140 + GPU 16 layers" {
    const psy = &GENRES[0];
    try testing.expectEqualStrings("Psytrance", psy.naam);
    try testing.expect(math.approxEqAbs(f64, psy.cpu_bpm, 140.0, 0.1));
    try testing.expect(psy.gpu_layers == 16);
}

test "ambient = geen CPU ritme, maximaal GPU veld" {
    const amb = &GENRES[2];
    try testing.expect(math.approxEqAbs(f64, amb.cpu_bpm, 0.0, 0.1));
    try testing.expect(amb.gpu_layers >= 20);
}

test "genre: CPU bepaalt tempo, GPU bepaalt complexiteit" {
    const techno = &GENRES[1];
    const beat_dur = cpuGenreRitme(techno);
    const synth_count = gpuGenreVeld(techno);

    try testing.expect(beat_dur > 0);
    try testing.expect(synth_count > 0);
}

// === 3. Hz = Veld, Hoek = Geometrie ===

const Band = struct {
    hz: f64,
    hoek: f64, // radiaan
    amp: f64,
};

pub fn gpuVeldPerBand(t: f64, band: *const Band) f64 {
    // Hz = veldsterkte, hoek = fase-shift (geometrie van delay)
    return band.amp * @sin(2 * std.math.pi * band.hz * t + band.hoek);
}

test "hz = veld, hoek = geometrie" {
    const band = Band{ .hz = 440, .hoek = 0.0, .amp = 1.0 };
    const veld = gpuVeldPerBand(0.0, &band);

    // Bij t=0, hoek=0: sin(0) = 0
    try testing.expect(math.approxEqAbs(f64, veld, 0.0, 0.01));
}

test "hoek verschuift fase" {
    const pi = std.math.pi;
    const band0 = Band{ .hz = 440, .hoek = 0, .amp = 1.0 };
    const band1 = Band{ .hz = 440, .hoek = pi / 2.0, .amp = 1.0 }; // 90°

    // Bij t=0: band0 = sin(0) = 0, band1 = sin(π/2) = 1
    const v0 = gpuVeldPerBand(0.0, &band0);
    const v1 = gpuVeldPerBand(0.0, &band1);

    try testing.expect(math.approxEqAbs(f64, v0, 0.0, 0.01));
    try testing.expect(math.approxEqAbs(f64, v1, 1.0, 0.01));
}

// === 4. Viveka = Self-Organizing ===
// Genre vormt zich door onderscheid, niet door autoriteit

const VivekaField = struct {
    onderscheid: f64, // 0-1
    vorming: bool,
};

pub fn vivekaOnderscheid(s1: f64, s2: f64, threshold: f64) VivekaField {
    const diff = @abs(s1 - s2);
    return .{
        .onderscheid = diff,
        .vorming = diff > threshold,
    };
}

test "viveka: onderscheid boven threshold = vorming" {
    const r = vivekaOnderscheid(140.0, 128.0, 5.0);
    try testing.expect(r.vorming); // verschil 12 > 5
    try testing.expect(r.onderscheid == 12.0);
}

test "viveka: onderscheid onder threshold = geen vorming" {
    const r = vivekaOnderscheid(140.0, 139.0, 5.0);
    try testing.expect(!r.vorming); // verschil 1 < 5
}

// === 5. Terminal Interface ===
// CPU terminal spreekt → GPU synths uitvoeren

const TerminalCommand = struct {
    bpm: f64,
    synth_naam: []const u8,
    parameter: f64,
};

const TerminalOutput = struct {
    beat_dur: f64,
    synth_progress: f64,
};

pub fn terminalUitvoeren(cmd: TerminalCommand, t_ms: f64) TerminalOutput {
    // CPU: ritme controleren
    const beat_dur = cpuRitmeControleren(cmd.bpm);

    // GPU: vind synth en bereken geometrie
    var synth_progress: f64 = 0.0;
    for (SYNTHS) |s| {
        if (std.mem.eql(u8, s.naam, cmd.synth_naam)) {
            const syn = &s;
            synth_progress = gpuSynthGeometrie(syn, t_ms);
            break;
        }
    }

    return .{ .beat_dur = beat_dur, .synth_progress = synth_progress };
}

test "terminal: command → uitvoeren" {
    const cmd = TerminalCommand{
        .bpm = 140.0,
        .synth_naam = "Moog",
        .parameter = 0.5,
    };

    const out = terminalUitvoeren(cmd, 120.0);
    try testing.expect(math.approxEqAbs(f64, out.beat_dur, 60.0 / 140.0, 0.001));
    // Moog: vertraging 40-200ms, t=120ms → progress = (120-40)/(200-40) = 80/160 = 0.5
    try testing.expect(math.approxEqAbs(f64, out.synth_progress, 0.5, 0.01));
}

// === 6. Muziek = Code = Taal ===

test "muziek = code = taal: computationele potentie audit" {
    // Psytrance = audit van computationele potentie
    const psy = &GENRES[0];
    const cpu_ritme = cpuGenreRitme(psy);
    const gpu_veld = gpuGenreVeld(psy);

    // CPU bepaalt ritme (wanneer)
    try testing.expect(cpu_ritme > 0);
    // GPU bepaalt veld (wat)
    try testing.expect(gpu_veld >= 2);
    // Samen = genre
    _ = psy.naam; // naam = resultaat van CPU + GPU audit
}

// === 7. Dark Forest = Donker Bos ===
// Donker = computationele potentie zonder interface
// Donker bos is vol leven, niet leeg

const DarkForestRegion = struct {
    cpu_range: [2]f64, // BPM range
    gpu_range: [2]f64, // layer range
    leven: bool,        // is er potentie?
    naam: []const u8,   // benoemd?
};

pub fn donkerBosRegio(cpu_min: f64, cpu_max: f64, gpu_min: f64, gpu_max: f64) DarkForestRegion {
    // Donker bos = ruimte tussen genres
    // Vol leven (computationele potentie) maar nog niet benoemd
    return .{
        .cpu_range = .{ cpu_min, cpu_max },
        .gpu_range = .{ gpu_min, gpu_max },
        .leven = true, // altijd leven in donker bos
        .naam = "",     // nog niet benoemd
    };
}

test "dark forest: donker = potentie zonder naam" {
    const regio = donkerBosRegio(80, 100, 40, 60);
    try testing.expect(regio.leven); // donker bos is vol leven
    try testing.expect(std.mem.eql(u8, regio.naam, "")); // nog niet benoemd
    try testing.expect(regio.cpu_range[0] < regio.cpu_range[1]);
    try testing.expect(regio.gpu_range[0] < regio.gpu_range[1]);
}

test "natuur = muziek: donker bos = donker veld" {
    // Vergelijking:
    // Natuur: donker bos vol leven (schimmels, zaden, mycelium)
    // Muziek: donker veld vol potentie (onbenoemde combinaties)

    const bos = donkerBosRegio(50, 70, 20, 40);

    // Leven was al aanwezig, alleen niet benoemd
    try testing.expect(bos.leven);
    // Benoemen = vormt zichtbaar maken
    _ = bos.cpu_range;
    _ = bos.gpu_range;
}
