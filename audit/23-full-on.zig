// Artikel 10 — Full-On
// کامل | पूर्ण
// Music = Full-On Psytrance | Muziek = Full-On Psytrance

const std = @import("std");
const testing = std.testing;
const math = std.math;

// CPU: ononderbroken rolling bass met kick op elke beat
const BPM_MIN: f64 = 144.0;
const BPM_MAX: f64 = 150.0;
const LAYERS_MIN: f64 = 4.0;
const LAYERS_MAX: f64 = 7.0;
const DONKER_BOS: bool = false;

// 303-acid → spiraal → lead
const ACID_FREQ: f64 = 93.0;
const ACID_DELAY_MS: f64 = 187.0;

// supersaw → golf → pad
const SAW_FREQ: f64 = 186.0;
const SAW_DELAY_MS: f64 = 375.0;

// arpeggio → ladder → klimmend
const ARP_FREQ: f64 = 372.0;
const ARP_DELAY_MS: f64 = 93.0;

const C_INVARIANT: f64 = 299_792_458.0;

// === Synth Geometrie ===

pub fn synthGeometrieFullOn() struct { freq: f64, hoek: f64, vertraging_ms: f64 } {
    return .{
        .freq = ACID_FREQ,
        .hoek = std.math.pi / 4.0, // spiraal = 45°
        .vertraging_ms = ACID_DELAY_MS,
    };
}

pub fn supersawGolf() struct { freq: f64, golflengte: f64, vertraging_ms: f64 } {
    return .{
        .freq = SAW_FREQ,
        .golflengte = C_INVARIANT / SAW_FREQ,
        .vertraging_ms = SAW_DELAY_MS,
    };
}

pub fn arpeggioLadder() struct { freq: f64, stappen: usize, vertraging_ms: f64 } {
    return .{
        .freq = ARP_FREQ,
        .stappen = 8,
        .vertraging_ms = ARP_DELAY_MS,
    };
}

// === CPU/GPU Splitsing ===

pub fn cpuBpmRange() struct { min: f64, max: f64 } {
    return .{ .min = BPM_MIN, .max = BPM_MAX };
}

pub fn gpuLayerRange() struct { min: f64, max: f64 } {
    return .{ .min = LAYERS_MIN, .max = LAYERS_MAX };
}

pub fn isDonkerBosFullOn() bool {
    return DONKER_BOS;
}

// === Full-On = Interface-Taal ===

pub fn fullOnInterface() struct {
    command: []const u8,
    synth: []const u8,
    geometrie: []const u8,
} {
    return .{
        .command = "roll",
        .synth = "303-acid",
        .geometrie = "spiraal",
    };
}

// === Donker Bos Regio ===

pub fn donkerBosRegioFullOn() struct {
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

test "fullOn synthGeometrie = spiraal 45°" {
    const geo = synthGeometrieFullOn();
    try std.testing.expectEqual(ACID_FREQ, geo.freq);
    try std.testing.expect(math.approxEqAbs(f64, std.math.pi / 4.0, geo.hoek, 1e-6));
    try std.testing.expectEqual(ACID_DELAY_MS, geo.vertraging_ms);
}

test "fullOn supersawGolf = C/f" {
    const golf = supersawGolf();
    try std.testing.expect(math.approxEqAbs(f64, C_INVARIANT / SAW_FREQ, golf.golflengte, 1e-6));
    try std.testing.expectEqual(SAW_DELAY_MS, golf.vertraging_ms);
}

test "fullOn arpeggioLadder = 8 stappen" {
    const ladder = arpeggioLadder();
    try std.testing.expectEqual(8, ladder.stappen);
    try std.testing.expectEqual(ARP_DELAY_MS, ladder.vertraging_ms);
}

test "fullOn cpuBpmRange = 144-150" {
    const r = cpuBpmRange();
    try std.testing.expectEqual(BPM_MIN, r.min);
    try std.testing.expectEqual(BPM_MAX, r.max);
}

test "fullOn gpuLayerRange = 4-7" {
    const r = gpuLayerRange();
    try std.testing.expectEqual(LAYERS_MIN, r.min);
    try std.testing.expectEqual(LAYERS_MAX, r.max);
}

test "fullOn donker bos = false" {
    try std.testing.expect(!isDonkerBosFullOn());
}

test "fullOn interface = roll→303→spiraal" {
    const iface = fullOnInterface();
    try std.testing.expectEqualStrings("roll", iface.command);
    try std.testing.expectEqualStrings("303-acid", iface.synth);
    try std.testing.expectEqualStrings("spiraal", iface.geometrie);
}

test "fullOn donkerBosRegio compleet" {
    const reg = donkerBosRegioFullOn();
    try std.testing.expectEqual(BPM_MIN, reg.cpu_bpm_min);
    try std.testing.expectEqual(BPM_MAX, reg.cpu_bpm_max);
    try std.testing.expectEqual(LAYERS_MIN, reg.gpu_layers_min);
    try std.testing.expectEqual(LAYERS_MAX, reg.gpu_layers_max);
    try std.testing.expect(!reg.donker_bos);
}
