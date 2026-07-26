// Artikel 14 — Hi-Tech
// تقنية عالية | उच्च तकनीक
// Music = Hi-Tech Psytrance | Muziek = Hi-Tech Psytrance

const std = @import("std");
const testing = std.testing;
const math = std.math;

// CPU: extreem snelle, gefragmenteerde ritmes, broken beats
const BPM_MIN: f64 = 160.0;
const BPM_MAX: f64 = 180.0;
const LAYERS_MIN: f64 = 8.0;
const LAYERS_MAX: f64 = 14.0;
const DONKER_BOS: bool = false;

// digital → pixel → lead
const DIGITAL_FREQ: f64 = 1176.0;
const DIGITAL_DELAY_MS: f64 = 50.0;

// glitch → breuk → textuur
const GLITCH_FREQ: f64 = 2352.0;
const GLITCH_DELAY_MS: f64 = 25.0;

// laser → lijn → snijdend
const LASER_FREQ: f64 = 588.0;
const LASER_DELAY_MS: f64 = 100.0;

const C_INVARIANT: f64 = 299_792_458.0;

// === Synth Geometrie ===

pub fn digitalPixel() struct { freq: f64, vertraging_ms: f64, scherp: bool } {
    return .{
        .freq = DIGITAL_FREQ,
        .vertraging_ms = DIGITAL_DELAY_MS,
        .scherp = true,
    };
}

pub fn glitchBreuk() struct { freq: f64, vertraging_ms: f64, kapot: bool } {
    return .{
        .freq = GLITCH_FREQ,
        .vertraging_ms = GLITCH_DELAY_MS,
        .kapot = true,
    };
}

pub fn laserLijn() struct { freq: f64, vertraging_ms: f64, snijdend: bool } {
    return .{
        .freq = LASER_FREQ,
        .vertraging_ms = LASER_DELAY_MS,
        .snijdend = true,
    };
}

// === CPU/GPU Splitsing ===

pub fn cpuBpmRange() struct { min: f64, max: f64 } {
    return .{ .min = BPM_MIN, .max = BPM_MAX };
}

pub fn gpuLayerRange() struct { min: f64, max: f64 } {
    return .{ .min = LAYERS_MIN, .max = LAYERS_MAX };
}

pub fn isDonkerBosHiTech() bool {
    return DONKER_BOS;
}

// === Hi-Tech = Interface-Taal ===

pub fn hiTechInterface() struct {
    command: []const u8,
    synth: []const u8,
    geometrie: []const u8,
} {
    return .{
        .command = "rush",
        .synth = "digital",
        .geometrie = "pixel",
    };
}

// === Donker Bos Regio ===

pub fn donkerBosRegioHiTech() struct {
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

test "hiTech digitalPixel = scherp" {
    const digital = digitalPixel();
    try std.testing.expect(digital.scherp);
    try std.testing.expectEqual(DIGITAL_DELAY_MS, digital.vertraging_ms);
}

test "hiTech glitchBreuk = kapot" {
    const glitch = glitchBreuk();
    try std.testing.expect(glitch.kapot);
    try std.testing.expectEqual(GLITCH_DELAY_MS, glitch.vertraging_ms);
}

test "hiTech laserLijn = snijdend" {
    const laser = laserLijn();
    try std.testing.expect(laser.snijdend);
    try std.testing.expectEqual(LASER_DELAY_MS, laser.vertraging_ms);
}

test "hiTech cpuBpmRange = 160-180" {
    const r = cpuBpmRange();
    try std.testing.expectEqual(BPM_MIN, r.min);
    try std.testing.expectEqual(BPM_MAX, r.max);
}

test "hiTech gpuLayerRange = 8-14" {
    const r = gpuLayerRange();
    try std.testing.expectEqual(LAYERS_MIN, r.min);
    try std.testing.expectEqual(LAYERS_MAX, r.max);
}

test "hiTech donker bos = false (digitale nacht)" {
    try std.testing.expect(!isDonkerBosHiTech());
}

test "hiTech interface = rush→digital→pixel" {
    const iface = hiTechInterface();
    try std.testing.expectEqualStrings("rush", iface.command);
    try std.testing.expectEqualStrings("digital", iface.synth);
    try std.testing.expectEqualStrings("pixel", iface.geometrie);
}

test "hiTech donkerBosRegio compleet" {
    const reg = donkerBosRegioHiTech();
    try std.testing.expectEqual(BPM_MIN, reg.cpu_bpm_min);
    try std.testing.expectEqual(BPM_MAX, reg.cpu_bpm_max);
    try std.testing.expectEqual(LAYERS_MIN, reg.gpu_layers_min);
    try std.testing.expectEqual(LAYERS_MAX, reg.gpu_layers_max);
    try std.testing.expect(!reg.donker_bos);
}
