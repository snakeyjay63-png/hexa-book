// Artikel 13 — Forest Psy
// غابة | वन
// Music = Forest Psytrance | Muziek = Forest Psytrance

const std = @import("std");
const testing = std.testing;
const math = std.math;

// CPU: organische, hobbelige ritmes met tribal elementen
const BPM_MIN: f64 = 148.0;
const BPM_MAX: f64 = 158.0;
const LAYERS_MIN: f64 = 7.0;
const LAYERS_MAX: f64 = 12.0;
const DONKER_BOS: bool = true;

// frog → organisch → sample
const FROG_FREQ: f64 = 147.0;
const FROG_DELAY_MS: f64 = 160.0;

// root → wortel → bass
const ROOT_FREQ: f64 = 36.75;
const ROOT_DELAY_MS: f64 = 320.0;

// insect → cluster → zoemend
const INSECT_FREQ: f64 = 588.0;
const INSECT_DELAY_MS: f64 = 80.0;

const C_INVARIANT: f64 = 299_792_458.0;

// === Synth Geometrie ===

pub fn frogOrganisch() struct { freq: f64, vertraging_ms: f64, nat: bool } {
    return .{
        .freq = FROG_FREQ,
        .vertraging_ms = FROG_DELAY_MS,
        .nat = true,
    };
}

pub fn rootWortel() struct { freq: f64, vertraging_ms: f64, diep: bool } {
    return .{
        .freq = ROOT_FREQ,
        .vertraging_ms = ROOT_DELAY_MS,
        .diep = true,
    };
}

pub fn insectCluster() struct { freq: f64, vertraging_ms: f64, zoemend: bool } {
    return .{
        .freq = INSECT_FREQ,
        .vertraging_ms = INSECT_DELAY_MS,
        .zoemend = true,
    };
}

// === CPU/GPU Splitsing ===

pub fn cpuBpmRange() struct { min: f64, max: f64 } {
    return .{ .min = BPM_MIN, .max = BPM_MAX };
}

pub fn gpuLayerRange() struct { min: f64, max: f64 } {
    return .{ .min = LAYERS_MIN, .max = LAYERS_MAX };
}

pub fn isDonkerBosForest() bool {
    return DONKER_BOS;
}

// === Forest Psy = Interface-Taal ===

pub fn forestInterface() struct {
    command: []const u8,
    synth: []const u8,
    geometrie: []const u8,
} {
    return .{
        .command = "pulse",
        .synth = "frog",
        .geometrie = "organisch",
    };
}

// === Donker Bos Regio ===

pub fn donkerBosRegioForest() struct {
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

test "forestPsy frogOrganisch = nat" {
    const frog = frogOrganisch();
    try std.testing.expect(frog.nat);
    try std.testing.expectEqual(FROG_DELAY_MS, frog.vertraging_ms);
}

test "forestPsy rootWortel = diep" {
    const root = rootWortel();
    try std.testing.expect(root.diep);
    try std.testing.expectEqual(ROOT_DELAY_MS, root.vertraging_ms);
}

test "forestPsy insectCluster = zoemend" {
    const insect = insectCluster();
    try std.testing.expect(insect.zoemend);
    try std.testing.expectEqual(INSECT_DELAY_MS, insect.vertraging_ms);
}

test "forestPsy cpuBpmRange = 148-158" {
    const r = cpuBpmRange();
    try std.testing.expectEqual(BPM_MIN, r.min);
    try std.testing.expectEqual(BPM_MAX, r.max);
}

test "forestPsy gpuLayerRange = 7-12" {
    const r = gpuLayerRange();
    try std.testing.expectEqual(LAYERS_MIN, r.min);
    try std.testing.expectEqual(LAYERS_MAX, r.max);
}

test "forestPsy donker bos = true" {
    try std.testing.expect(isDonkerBosForest());
}

test "forestPsy interface = pulse→frog→organisch" {
    const iface = forestInterface();
    try std.testing.expectEqualStrings("pulse", iface.command);
    try std.testing.expectEqualStrings("frog", iface.synth);
    try std.testing.expectEqualStrings("organisch", iface.geometrie);
}

test "forestPsy donkerBosRegio compleet" {
    const reg = donkerBosRegioForest();
    try std.testing.expectEqual(BPM_MIN, reg.cpu_bpm_min);
    try std.testing.expectEqual(BPM_MAX, reg.cpu_bpm_max);
    try std.testing.expectEqual(LAYERS_MIN, reg.gpu_layers_min);
    try std.testing.expectEqual(LAYERS_MAX, reg.gpu_layers_max);
    try std.testing.expect(reg.donker_bos);
}
