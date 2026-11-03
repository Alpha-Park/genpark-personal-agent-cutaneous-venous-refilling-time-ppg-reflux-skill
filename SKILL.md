---
name: genpark-personal-agent-cutaneous-venous-refilling-time-ppg-reflux-skill
version: 1.0.0
description: Calculates Digital Photoplethysmography (D-PPG) Venous Refilling Time (VRT), Venous Pump Power (VPP), and CEAP chronic venous insufficiency staging.
license: Apache-2.0
compatibility:
  python: ">=3.9"
  openclaw: ">=1.0.0"
  mcp: ">=1.0.0"
---

# Cutaneous Venous Refilling Time (VRT) & Venous Pump Power (VPP) Skill

A zero-dependency personal agent skill for evaluating lower-extremity chronic venous insufficiency (CVI), valvular reflux kinetics, and calf muscle pump ejection power using Digital Photoplethysmography (D-PPG).

## Features
- **Venous Refilling Time ($VRT$)**: Quantifies venous blood re-accumulation time following active calf muscle pump emptying.
- **Venous Pump Power ($VPP\%$)**: Measures percentage optical volume drop to assess calf muscle pump ejection fraction ($\ge 4\%$ normal).
- **Valvular Competence Stratification**: Differentiates competent valves ($\ge 25\text{ s}$) from mild ($20-25\text{ s}$), moderate ($10-20\text{ s}$), and severe reflux ($< 10\text{ s}$).
- **Tourniquet Localization**: Distinguishes isolated superficial saphenous vein reflux from deep venous insufficiency.

## MCP Server Integration
Exposes `evaluate_venous_hemodynamics` for autonomous vascular wellness screening, edema prevention, and occupational standing ergonomics.
