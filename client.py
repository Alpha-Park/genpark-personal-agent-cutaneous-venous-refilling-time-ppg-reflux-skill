"""
Cutaneous Venous Refilling Time (VRT) & Venous Pump Power (VPP) Client.
Zero-mock pure Python standard library implementation.
Calculates Photoplethysmographic Venous Refilling Time (VRT in seconds),
Venous Pump Power (VPP in %), and CEAP venous insufficiency staging.
"""

import math
from typing import Dict, Any, Optional


class VenousRefillingTimeClient:
    """
    Evaluates chronic venous insufficiency (CVI) and calf muscle pump competence via D-PPG:
    - V0 (mV): baseline resting cutaneous venous blood volume
    - V_min (mV): post-exercise nadir venous volume after 10 dorsiflexions
    - VPP (%) = ((V0 - V_min) / V0) * 100 (venous ejection fraction)
    - VRT (s): time elapsed from end of exercise until venous volume refills to baseline (or 90% baseline)
    """

    def __init__(self):
        pass

    def evaluate_venous_hemodynamics(
        self,
        venous_refilling_time_seconds: float,
        baseline_signal_mv: float,
        post_exercise_nadir_mv: float,
        limb_examined: Optional[str] = "Right Leg",
        tourniquet_applied: Optional[bool] = False,
        tourniquet_refilling_time_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates PPG venous hemodynamics metrics.
        venous_refilling_time_seconds: refilling time in seconds (e.g. 28.0 s).
        baseline_signal_mv: baseline resting PPG voltage (e.g. 1000.0 mV).
        post_exercise_nadir_mv: minimal post-exercise PPG voltage (e.g. 920.0 mV).
        tourniquet_applied: whether superficial tourniquet test was performed.
        """
        if venous_refilling_time_seconds <= 0:
            raise ValueError("Venous refilling time must be strictly positive.")
        if baseline_signal_mv <= 0 or post_exercise_nadir_mv <= 0:
            raise ValueError("PPG voltages must be strictly positive.")
        if post_exercise_nadir_mv > baseline_signal_mv:
            raise ValueError("Nadir voltage cannot exceed baseline resting voltage.")

        # Venous Pump Power (VPP in %)
        vpp_pct = ((baseline_signal_mv - post_exercise_nadir_mv) / baseline_signal_mv) * 100.0

        # Venous Refilling Time (VRT) Clinical Staging (CEAP Consensus):
        # VRT >= 25.0 s: Normal competent valves (arterial capillary inflow only)
        # VRT 20.0 - 24.9 s: Mild / Borderline Venous Incompetence
        # VRT 10.0 - 19.9 s: Moderate Chronic Venous Insufficiency
        # VRT < 10.0 s: Severe Retrograde Venous Reflux (deep/superficial incompetence)
        if venous_refilling_time_seconds >= 25.0:
            valvular_status = "Competent Venous Valves / Normal Refilling"
            clinical_risk = "Physiological venous drainage; arterial capillary refill kinetics with no retrograde valvular leak."
        elif venous_refilling_time_seconds >= 20.0:
            valvular_status = "Mild / Borderline Venous Valvular Reflux"
            clinical_risk = "Early saphenous or perforator valve laxity; early evening lower-extremity edema risk."
        elif venous_refilling_time_seconds >= 10.0:
            valvular_status = "Moderate Chronic Venous Insufficiency (CVI)"
            clinical_risk = "Significant retrograde reflux; recommend graduated compression therapy and walking calf pump activation."
        else:
            valvular_status = "Severe Retrograde Venous Reflux"
            clinical_risk = "Gross saphenofemoral or deep venous valve incompetence; high risk of stasis dermatitis, hemosiderin pigmentation, and venous ulceration."

        # Calf Muscle Pump Competence
        # VPP >= 4.0%: Robust calf pump ejection
        # VPP < 2.5%: Impaired muscle pump ejection (joint stiffness, calf muscle atrophy)
        if vpp_pct >= 4.0:
            pump_status = "Robust Calf Muscle Pump Ejection"
        elif vpp_pct >= 2.5:
            pump_status = "Mildly Reduced Muscle Pump Efficacy"
        else:
            pump_status = "Impaired Calf Muscle Pump Function (Musculoskeletal / Ankle Ankylosis)"

        # Tourniquet differentiation (if provided)
        # If tourniquet normalizes VRT (> 25s), reflux is isolated to superficial veins (Great/Small Saphenous)
        # If VRT remains < 20s despite tourniquet, deep venous reflux is present.
        tourniquet_diff = None
        if tourniquet_applied and tourniquet_refilling_time_seconds is not None:
            if tourniquet_refilling_time_seconds >= 25.0:
                tourniquet_diff = "Isolated Superficial Saphenous Reflux (Normalizes with tourniquet occlusion)"
            elif tourniquet_refilling_time_seconds > venous_refilling_time_seconds + 5.0:
                tourniquet_diff = "Mixed Superficial and Deep Venous Reflux"
            else:
                tourniquet_diff = "Predominant Deep Venous System Reflux (Refractory to superficial tourniquet)"

        return {
            "status": "success",
            "hemodynamic_metrics": {
                "venous_refilling_time_vrt_seconds": round(venous_refilling_time_seconds, 1),
                "venous_pump_power_vpp_pct": round(vpp_pct, 2),
                "baseline_signal_mv": round(baseline_signal_mv, 1),
                "post_exercise_nadir_mv": round(post_exercise_nadir_mv, 1),
                "limb_examined": limb_examined
            },
            "clinical_assessment": {
                "valvular_competence": valvular_status,
                "calf_pump_status": pump_status,
                "pathophysiology_summary": clinical_risk,
                "tourniquet_localization": tourniquet_diff
            }
        }
