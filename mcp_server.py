"""
MCP Server for Cutaneous Venous Refilling Time (VRT) & Venous Pump Power (VPP).
Exposes tools for chronic venous insufficiency and calf pump assessment.
"""

import json
from typing import Dict, Any, Optional
from client import VenousRefillingTimeClient


def handle_evaluate_venous(params: Dict[str, Any]) -> Dict[str, Any]:
    venous_refilling_time_seconds = float(params.get("venous_refilling_time_seconds", 26.0))
    baseline_signal_mv = float(params.get("baseline_signal_mv", 1000.0))
    post_exercise_nadir_mv = float(params.get("post_exercise_nadir_mv", 940.0))
    limb_examined = str(params.get("limb_examined", "Right Leg"))
    tourniquet_applied = bool(params.get("tourniquet_applied", False))
    tourniquet_refilling_time_seconds = params.get("tourniquet_refilling_time_seconds")
    if tourniquet_refilling_time_seconds is not None:
        tourniquet_refilling_time_seconds = float(tourniquet_refilling_time_seconds)

    client = VenousRefillingTimeClient()
    return client.evaluate_venous_hemodynamics(
        venous_refilling_time_seconds=venous_refilling_time_seconds,
        baseline_signal_mv=baseline_signal_mv,
        post_exercise_nadir_mv=post_exercise_nadir_mv,
        limb_examined=limb_examined,
        tourniquet_applied=tourniquet_applied,
        tourniquet_refilling_time_seconds=tourniquet_refilling_time_seconds
    )


TOOLS = {
    "evaluate_venous_hemodynamics": {
        "description": "Calculates Digital Photoplethysmography (D-PPG) Venous Refilling Time (VRT), Venous Pump Power (VPP), and CEAP chronic venous insufficiency staging.",
        "parameters": {
            "type": "object",
            "properties": {
                "venous_refilling_time_seconds": {
                    "type": "number",
                    "description": "Refilling time in seconds after 10 active dorsiflexions (e.g. 26.0 s)."
                },
                "baseline_signal_mv": {
                    "type": "number",
                    "description": "Resting pre-exercise baseline PPG voltage in mV (e.g. 1000.0 mV)."
                },
                "post_exercise_nadir_mv": {
                    "type": "number",
                    "description": "Minimum post-exercise PPG voltage in mV (e.g. 940.0 mV)."
                },
                "limb_examined": {
                    "type": "string",
                    "description": "Limb tested (e.g. 'Right Leg' or 'Left Leg'), default 'Right Leg'."
                },
                "tourniquet_applied": {
                    "type": "boolean",
                    "description": "Whether superficial tourniquet compression was applied, default false."
                },
                "tourniquet_refilling_time_seconds": {
                    "type": "number",
                    "description": "Refilling time with tourniquet applied (seconds), optional."
                }
            },
            "required": ["venous_refilling_time_seconds", "baseline_signal_mv", "post_exercise_nadir_mv"]
        },
        "handler": handle_evaluate_venous
    }
}


def process_request(request_str: str) -> str:
    try:
        req = json.loads(request_str)
        method = req.get("method")
        req_id = req.get("id")

        if method == "tools/list":
            tools_list = [
                {
                    "name": name,
                    "description": spec["description"],
                    "inputSchema": spec["parameters"]
                }
                for name, spec in TOOLS.items()
            ]
            return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            if tool_name not in TOOLS:
                return json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}
                })

            result = TOOLS[tool_name]["handler"](args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })

        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": f"Unsupported method '{method}'"}
            })

    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        if line.strip():
            print(process_request(line))
            sys.stdout.flush()
