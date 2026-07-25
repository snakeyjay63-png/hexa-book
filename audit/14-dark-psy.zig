// Artikel 12 — Dark Psy
// ظلام | अंधकार
// Music = Dark Psytrance | Muziek = Dark Psytrance

const std = @import("std");
const testing = std.testing;
const math = std.math;

// CPU: zware, verstoorde kick, lage frequenties dominant
const BPM_MIN: f64 = 148.0;
const BPM_MAX: f64 = 155.0;
const LAYERS_MIN: f64 = 6.0;
const LAYERS_MAX: f64 = 10.0;
const DONKER_BOS: bool = true;

// scream → scherpe driehoek → lead
const SCREAM_FREQ: f64 = 294.0;
const SCREAM_DELAY_MS: f64 = 140.0;

// noise → chaos → textuur
const NOISE_FREQ: f64 = 588.0;
const NOISE_DELAY_MS: f64 = 70.0;

// sub → verticale as → drukkend
const SUB_FREQ: f64 = 29.4;
const SUB_DELAY_MS: f64 = 280.0;

const C_INVARIANT: f64 = 299_792_458.0;

// === Synth Geometrie ===

pub fn screamDriehoek() struct { freq: f64, hoek: f64, vertraging_ms: f64 } {
    return .{
        .freq = SCREAM_FREQ,
        .hoek = std.math.pi / 3.0, // scherpe driehoek = 60°
        .vertraging_ms = SCREAM_DELAY_MS,
    };
}

pub fn noiseChaos() struct { freq: f64, vertraging_ms: f64, chaos: bool } {
    return .{
        .freq = NOISE_FREQ,
        .vertraging_ms = NOISE_DELAY_MS,
        .chaos = true,
    };
}

pub fn subVerticaleAs() struct { freq: f64, vertraging_ms: f64, drukkend: bool } {
    return .{
        .freq = SUB_FREQ,
        .vertraging_ms = SUB_DELAY_MS,
        .drukkend = true,
    };
}

// === CPU/GPU Splitsing ===

pub fn cpuBpmRange() struct { min: f64, max: f64 } {
    return .{ .min = BPM_MIN, .max = BPM_MAX };
}

pub fn gpuLayerRange() struct { min: f64, max: f64 } {
    return .{ .min = LAYERS_MIN, .max = LAYERS_MAX };
}

pub fn isDonkerBosDark() bool {
    return DONKER_BOS;
}

// === Dark Psy = Interface-Taal ===

pub fn darkPsyInterface() struct {
    command: []const u8,
    synth: []const u8,
    geometrie: []const u8,
} {
    return .{
        .command = "crush",
        .synth = "scream",
        .geometrie = "driehoek",
    };
}

// === Donker Bos Regio ===

pub fn donkerBosRegioDark() struct {
    cpu_bpm_min: f64,
    cpu_bpm_max: f64,
    gpu_layers_min: f64,
    gpu_layers_max: f64,
    donker_bos: bool,
} {
    return .{
        .cpu_bpm_min = BPM_MIN,
        .cpu_bpm_max = BPM_MAX,
        .gpu_layers_min = LAYERS_MIN,
        .gpu_layers_max = LAYERS_MAX,
        .donker_bos = DONKER_BOS,
    };
}

// === Tests ===

test "darkPsy screamDriehoek = 60°" {
    const geo = screamDriehoek();
    try std.testing.expectEqual(SCREAM_FREQ, geo.freq);
    try std.testing.expect(math.approxEqAbs(f64, std.math.pi / 3.0, geo.hoek, 1e-6));
    try std.testing.expectEqual(SCREAM_DELAY_MS, geo.vertraging_ms);
}

test "darkPsy noiseChaos = chaos" {
    const noise = noiseChaos();
    try std.testing.expect(noise.chaos);
    try std.testing.expectEqual(NOISE_DELAY_MS, noise.vertraging_ms);
}

test "darkPsy subVerticaleAs = drukkend" {
    const sub = subVerticaleAs();
    try std.testing.expect(sub.drukkend);
    try std.testing.expectEqual(SUB_DELAY_MS, sub.vertraging_ms);
}

test "darkPsy cpuBpmRange = 148-155" {
    const r = cpuBpmRange();
    try std.testing.expectEqual(BPM_MIN, r.min);
    try std.testing.expectEqual(BPM_MAX, r.max);
}

test "darkPsy gpuLayerRange = 6-10" {
    const r = gpuLayerRange();
    try std.testing.expectEqual(LAYERS_MIN, r.min);
    try std.testing.expectEqual(LAYERS_MAX, r.max);
}

test "darkPsy donker bos = true" {
    try std.testing.expect(isDonkerBosDark());
}

test "darkPsy interface = crush→scream→driehoek" {
    const iface = darkPsyInterface();
    try std.testing.expectEqualStrings("crush", iface.command);
    try std.testing.expectEqualStrings("scream", iface.synth);
    try std.testing.expectEqualStrings("driehoek", iface.geometrie);
}

test "darkPsy donkerBosRegio compleet" {
    const reg = donkerBosRegioDark();
    try std.testing.expectEqual(BPM_MIN, reg.cpu_bpm_min);
    try std.testing.expectEqual(BPM_MAX, reg.cpu_bpm_max);
    try std.testing.expectEqual(LAYERS_MIN, reg.gpu_layers_min);
    try std.testing.expectEqual(LAYERS_MAX, reg.gpu_layers_max);
    try std.testing.expect(reg.donker_bos);
}
