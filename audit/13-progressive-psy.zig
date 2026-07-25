// Artikel 11 — Progressive Psy
// تدريجي | प्रगतिशील
// Music = Progressive Psytrance | Muziek = Progressive Psytrance

const std = @import("std");
const testing = std.testing;
const math = std.math;

// CPU: lange spanningsbogen, zachte kick, diepe groove
const BPM_MIN: f64 = 136.0;
const BPM_MAX: f64 = 142.0;
const LAYERS_MIN: f64 = 3.0;
const LAYERS_MAX: f64 = 6.0;
const DONKER_BOS: bool = false;

// pad → horizontaal → atmosfeer
const PAD_FREQ: f64 = 73.0;
const PAD_DELAY_MS: f64 = 500.0;

// pluck → punt → melodie
const PLUCK_FREQ: f64 = 146.0;
const PLUCK_DELAY_MS: f64 = 250.0;

// bass → lijn → diep
const BASS_FREQ: f64 = 36.5;
const BASS_DELAY_MS: f64 = 125.0;

const C_INVARIANT: f64 = 299_792_458.0;

// === Synth Geometrie ===

pub fn padHorizontaal() struct { freq: f64, hoek: f64, vertraging_ms: f64 } {
    return .{
        .freq = PAD_FREQ,
        .hoek = 0.0, // horizontaal = 0°
        .vertraging_ms = PAD_DELAY_MS,
    };
}

pub fn pluckPunt() struct { freq: f64, vertraging_ms: f64, melodie: bool } {
    return .{
        .freq = PLUCK_FREQ,
        .vertraging_ms = PLUCK_DELAY_MS,
        .melodie = true,
    };
}

pub fn bassLijn() struct { freq: f64, vertraging_ms: f64, diep: bool } {
    return .{
        .freq = BASS_FREQ,
        .vertraging_ms = BASS_DELAY_MS,
        .diep = true,
    };
}

// === CPU/GPU Splitsing ===

pub fn cpuBpmRange() struct { min: f64, max: f64 } {
    return .{ .min = BPM_MIN, .max = BPM_MAX };
}

pub fn gpuLayerRange() struct { min: f64, max: f64 } {
    return .{ .min = LAYERS_MIN, .max = LAYERS_MAX };
}

pub fn isDonkerBosProgressive() bool {
    return DONKER_BOS;
}

// === Progressive Psy = Interface-Taal ===

pub fn progressiveInterface() struct {
    command: []const u8,
    synth: []const u8,
    geometrie: []const u8,
} {
    return .{
        .command = "build",
        .synth = "pad",
        .geometrie = "horizontaal",
    };
}

// === Donker Bos Regio ===

pub fn donkerBosRegioProgressive() struct {
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

test "progressive padHorizontaal = 0°" {
    const pad = padHorizontaal();
    try std.testing.expectEqual(PAD_FREQ, pad.freq);
    try std.testing.expect(math.approxEqAbs(f64, 0.0, pad.hoek, 1e-6));
    try std.testing.expectEqual(PAD_DELAY_MS, pad.vertraging_ms);
}

test "progressive pluckPunt = melodie" {
    const pluck = pluckPunt();
    try std.testing.expect(pluck.melodie);
    try std.testing.expectEqual(PLUCK_DELAY_MS, pluck.vertraging_ms);
}

test "progressive bassLijn = diep" {
    const bass = bassLijn();
    try std.testing.expect(bass.diep);
    try std.testing.expectEqual(BASS_DELAY_MS, bass.vertraging_ms);
}

test "progressive cpuBpmRange = 136-142" {
    const r = cpuBpmRange();
    try std.testing.expectEqual(BPM_MIN, r.min);
    try std.testing.expectEqual(BPM_MAX, r.max);
}

test "progressive gpuLayerRange = 3-6" {
    const r = gpuLayerRange();
    try std.testing.expectEqual(LAYERS_MIN, r.min);
    try std.testing.expectEqual(LAYERS_MAX, r.max);
}

test "progressive donker bos = false" {
    try std.testing.expect(!isDonkerBosProgressive());
}

test "progressive interface = build→pad→horizontaal" {
    const iface = progressiveInterface();
    try std.testing.expectEqualStrings("build", iface.command);
    try std.testing.expectEqualStrings("pad", iface.synth);
    try std.testing.expectEqualStrings("horizontaal", iface.geometrie);
}

test "progressive donkerBosRegio compleet" {
    const reg = donkerBosRegioProgressive();
    try std.testing.expectEqual(BPM_MIN, reg.cpu_bpm_min);
    try std.testing.expectEqual(BPM_MAX, reg.cpu_bpm_max);
    try std.testing.expectEqual(LAYERS_MIN, reg.gpu_layers_min);
    try std.testing.expectEqual(LAYERS_MAX, reg.gpu_layers_max);
    try std.testing.expect(!reg.donker_bos);
}
