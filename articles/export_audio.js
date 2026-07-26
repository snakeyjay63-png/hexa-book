#!/usr/bin/env node
/**
 * Export bit.html stages as WAV audio
 * Generates one continuous file with all 7 stages
 */

const fs = require('fs');
const path = require('path');

const SAMPLE_RATE = 44100;
const STAGE_DURATION = 4; // seconds per stage
const STAGES = 7;
const TOTAL_SAMPLES = SAMPLE_RATE * STAGE_DURATION * STAGES;

// ── WAV Writer ──
function writeWav(buf, filePath) {
  const out = Buffer.alloc(44 + buf.length);

  // RIFF header
  out.write('RIFF', 0);
  out.writeUInt32LE(36 + buf.length, 4);
  out.write('WAVE', 8);

  // fmt chunk
  out.write('fmt ', 12);
  out.writeUInt32LE(16, 16);
  out.writeUInt16LE(1, 20);  // PCM
  out.writeUInt16LE(1, 22);  // mono
  out.writeUInt32LE(SAMPLE_RATE, 24);
  out.writeUInt32LE(SAMPLE_RATE * 2, 28);
  out.writeUInt16LE(2, 32);  // block align
  out.writeUInt16LE(16, 34); // bits per sample

  // data chunk
  out.write('data', 36);
  out.writeUInt32LE(buf.length, 40);
  buf.copy(out, 44);

  fs.writeFileSync(filePath, out);
  console.log(`✓ Written: ${filePath} (${(buf.length / 1024 / 1024).toFixed(1)} MB)`);
}

// ── Audio Generation ──
function generateStage(stage, offset) {
  const samples = new Float32Array(SAMPLE_RATE * STAGE_DURATION);
  const fadeTime = 0.05; // 50ms fade in/out
  const fadeSamples = Math.floor(SAMPLE_RATE * fadeTime);

  for (let i = 0; i < samples.length; i++) {
    const t = i / SAMPLE_RATE;
    let val = 0;

    // Fade in/out
    const env = i < fadeSamples ? i / fadeSamples :
                i > samples.length - fadeSamples ? (samples.length - i) / fadeSamples : 1;

    switch (stage) {
      case 0: // 0=1: pure tone
        val = Math.sin(2 * Math.PI * 220 * t) * 0.3;
        break;

      case 1: // 1 WAVE: 2^0
        val = Math.sin(2 * Math.PI * 220 * t) * 0.3;
        break;

      case 2: // 2 WAVES: 2^1 (octave)
        val = Math.sin(2 * Math.PI * 110 * t) * 0.2 +
              Math.sin(2 * Math.PI * 220 * t) * 0.2;
        break;

      case 3: // 4 WAVES: 2^2 (harmonic series)
        val = Math.sin(2 * Math.PI * 110 * t) * 0.15 +
              Math.sin(2 * Math.PI * 165 * t) * 0.15 +
              Math.sin(2 * Math.PI * 220 * t) * 0.15 +
              Math.sin(2 * Math.PI * 330 * t) * 0.15;
        break;

      case 4: // 8 WAVES: 2^3 (full harmonic)
        [55, 82.5, 110, 137.5, 165, 220, 275, 330].forEach(f => {
          val += Math.sin(2 * Math.PI * f * t) * 0.1;
        });
        break;

      case 5: // CHAOS: white noise
        val = (Math.random() * 2 - 1) * 0.2;
        // Simple lowpass
        if (i > 0) val = samples[i - 1] * 0.8 + val * 0.2;
        break;

      case 6: // MANDELBROT: drone + LFO
        val = Math.sin(2 * Math.PI * 55 * t) * 0.2;
        const lfo = Math.sin(2 * Math.PI * 0.2 * t) * 10;
        val += Math.sin(2 * Math.PI * (110 + lfo) * t) * 0.15;
        break;
    }

    samples[i] = val * env;
  }

  // Interleave into output buffer
  const globalOffset = offset * SAMPLE_RATE * STAGE_DURATION;
  for (let i = 0; i < samples.length; i++) {
    const idx = globalOffset + i;
    if (idx < output.length) {
      output[idx] = samples[i];
    }
  }
}

// Generate all stages
const output = new Float32Array(TOTAL_SAMPLES);
const stageNames = [
  '0=1 (eenheid)',
  '2^0 (1 wave)',
  '2^1 (2 waves)',
  '2^2 (4 waves)',
  '2^3 (8 waves)',
  '>7 (chaos)',
  '∞→1 (mandelbrot)'
];

for (let s = 0; s < STAGES; s++) {
  console.log(`Generating stage ${s}: ${stageNames[s]}...`);
  generateStage(s, s);
}

// Convert to 16-bit PCM
const pcm = Buffer.alloc(output.length * 2);
for (let i = 0; i < output.length; i++) {
  const s = Math.max(-1, Math.min(1, output[i]));
  pcm.writeInt16LE(s < 0 ? s * 32768 : s * 32767, i * 2);
}

// Write
const outPath = path.join(__dirname, '..', 'audio', 'bit-loop.wav');
const outDir = path.dirname(outPath);
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
writeWav(pcm, outPath);

console.log(`\nTotal duration: ${(TOTAL_SAMPLES / SAMPLE_RATE).toFixed(1)}s`);
console.log(`Stages: ${stageNames.join(' → ')}`);
