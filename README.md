# Cutaneous Venous Refilling Time (VRT) & Venous Pump Power (VPP) Skill

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](requirements.txt)
[![Status: Production-Ready](https://img.shields.io/badge/status-production--ready-success.svg)](https://github.com/alphaparkinc)

A zero-dependency, mathematically rigorous personal agent skill that evaluates lower-extremity chronic venous insufficiency (CVI), valvular competence, and calf muscle pump ejection power via Digital Photoplethysmography (D-PPG).

## Architecture

```mermaid
flowchart TD
    A[Cutaneous Infrared PPG Probe] --> B[Continuous Optical Density Sampling]
    B --> C[10 Active Dorsiflexions Calf Pump Ejection]
    C --> D[Compute Venous Pump Power VPP = Delta V / V0]
    D --> E[Track Refilling Time VRT to Baseline]
    E --> F[CEAP Reflux Grading & Tourniquet Localization]
```

## Quick Start

```python
from client import VenousRefillingTimeClient

client = VenousRefillingTimeClient()
result = client.evaluate_venous_hemodynamics(
    venous_refilling_time_seconds=28.5,
    baseline_signal_mv=1000.0,
    post_exercise_nadir_mv=930.0,
    limb_examined="Right Leg"
)
print("VRT (s):", result["hemodynamic_metrics"]["venous_refilling_time_vrt_seconds"])
print("Venous Pump Power (%):", result["hemodynamic_metrics"]["venous_pump_power_vpp_pct"])
print("Valvular Status:", result["clinical_assessment"]["valvular_competence"])
```

## License
Apache-2.0
