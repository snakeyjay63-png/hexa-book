const std = @import("std");
const testing = std.testing;
const math = std.math;

// === Artikel ##: [Genre Naam] ===

// === 1. Terminal Command ===

const TerminalCommand = struct {
    bpm: f64,
    synth_naam: []const u8,
    parameter: f64,
};

pub fn cpuRitmeControleren(bpm: f64) f64 {
    return 60.0 / bpm;
}

pub fn terminalUitvoeren(cmd: TerminalCommand) f64 {
    return cpuRitmeControleren(cmd.bpm);
}

test "[genre]: CPU ritme" {
    // TODO: vul in
}

// === 2. Synth Geometrie ===

const Synth = struct {
    naam: []const u8,
    geometrie: []const u8,
    vertraging_min_ms: f64,
    vertraging_max_ms: f64,
    uitgang: []const u8,
};

pub fn gpuSynthGeometrie(synth: *const Synth, t_ms: f64) f64 {
    const range = synth.vertraging_max_ms - synth.vertraging_min_ms;
    const t_norm = std.math.clamp(t_ms - synth.vertraging_min_ms, 0.0, range);
    return t_norm / range;
}

test "[genre]: GPU synth geometrie" {
    // TODO: vul in
}

// === 3. Genre Veld ===

pub fn donkerBosRegio(cpu_min: f64, cpu_max: f64, gpu_min: f64, gpu_max: f64) struct {
    cpu_range: [2]f64,
    gpu_range: [2]f64,
    leven: bool,
} {
    return .{
        .cpu_range = .{ cpu_min, cpu_max },
        .gpu_range = .{ gpu_min, gpu_max },
        .leven = true,
    };
}

test "[genre]: donker bos regio" {
    // TODO: vul in
}

// === 4. Nidrā ===

// TODO: verwijzing naar parallel artikels
