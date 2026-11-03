"""
Example usage of Cutaneous Venous Refilling Time (VRT) & Venous Pump Power (VPP).
Demonstrates normal venous valvular competence vs superficial saphenous vein reflux.
"""

from client import VenousRefillingTimeClient

def main():
    client = VenousRefillingTimeClient()

    print("=== Case 1: Healthy Competent Venous Valves ===")
    normal_case = client.evaluate_venous_hemodynamics(
        venous_refilling_time_seconds=29.5,
        baseline_signal_mv=1000.0,
        post_exercise_nadir_mv=935.0,
        limb_examined="Right Leg"
    )
    print("Hemodynamics:")
    print(f"  VRT:        {normal_case['hemodynamic_metrics']['venous_refilling_time_vrt_seconds']} s")
    print(f"  Pump Power: {normal_case['hemodynamic_metrics']['venous_pump_power_vpp_pct']} %")
    print(f"  Valves:     {normal_case['clinical_assessment']['valvular_competence']}")
    print(f"  Muscle Pump:{normal_case['clinical_assessment']['calf_pump_status']}")

    print("\n=== Case 2: Great Saphenous Reflux (Tourniquet Tested) ===")
    reflux_case = client.evaluate_venous_hemodynamics(
        venous_refilling_time_seconds=12.0,
        baseline_signal_mv=1000.0,
        post_exercise_nadir_mv=955.0,
        limb_examined="Left Leg",
        tourniquet_applied=True,
        tourniquet_refilling_time_seconds=28.0
    )
    print("Hemodynamics:")
    print(f"  VRT (Baseline):   {reflux_case['hemodynamic_metrics']['venous_refilling_time_vrt_seconds']} s (Rapid retrograde reflux)")
    print(f"  Pump Power:       {reflux_case['hemodynamic_metrics']['venous_pump_power_vpp_pct']} %")
    print(f"  Valves:           {reflux_case['clinical_assessment']['valvular_competence']}")
    print(f"  Tourniquet Result:{reflux_case['clinical_assessment']['tourniquet_localization']}")
    print(f"  Pathophysiology:  {reflux_case['clinical_assessment']['pathophysiology_summary']}")

if __name__ == "__main__":
    main()
