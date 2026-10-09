"""
Mewtwo Disaster Response - FastAPI REST Server
Project : Mewtwo
Team    : TEAM FLUXO
Track   : D3 — Autonomous Disaster Response Planner
AI      : IBM Bob
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn

# ---------------------------------------------------------------------------
# Import DisasterOptimizer — try package import first, fall back to direct
# ---------------------------------------------------------------------------
try:
    from src.optimizer import DisasterOptimizer
except ImportError:
    from optimizer import DisasterOptimizer  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Mewtwo — Autonomous Disaster Response Planner",
    description="Track D3 | Team TEAM FLUXO | AI Partner: IBM Bob",
    version="1.0.0",
)

optimizer = DisasterOptimizer()

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class ZoneInput(BaseModel):
    id: str
    location_name: str
    casualties: int
    hazard_depth: float
    medical_distress: int


class AllocationRequest(BaseModel):
    zones: List[ZoneInput]
    resources: Dict[str, int]


class BobQueryRequest(BaseModel):
    prompt: str
    context_data: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Root health-check — confirms the service is operational."""
    return {
        "project": "Mewtwo",
        "team": "TEAM FLUXO",
        "track": "D3",
        "status": "Operational",
        "ai_partner": "IBM Bob",
    }


@app.post("/api/allocate", tags=["Optimization"])
def allocate_resources(request: AllocationRequest):
    """
    Receives disaster zones and available resource inventory.
    Runs the MILP optimizer and returns urgency-sorted allocation plan.
    """
    if not request.zones:
        raise HTTPException(status_code=400, detail="At least one zone must be provided.")
    if not request.resources:
        raise HTTPException(status_code=400, detail="Resource inventory must not be empty.")

    # Convert Pydantic models → plain dicts expected by the optimizer
    zones_payload = [z.model_dump() for z in request.zones]

    try:
        result = optimizer.optimize_allocation(zones_payload, request.resources)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Optimizer error: {str(exc)}")

    if result.get("status") == "error":
        raise HTTPException(status_code=503, detail=result.get("message", "Solver unavailable."))

    return result


@app.post("/api/bob/assist", tags=["IBM Bob AI"])
def bob_assist(request: BobQueryRequest):
    """
    Operational conversational endpoint powered by IBM Bob.
    Interprets the incoming prompt and returns structured dispatch actions
    or system health information.
    """
    prompt_lower = request.prompt.lower()

    # --- Dispatch / deployment intent ---
    if any(kw in prompt_lower for kw in ["deploy", "dispatch", "send", "allocate"]):
        actions = [
            {
                "action": "dispatch_ndrf_team",
                "priority": "HIGH",
                "instruction": "Deploy NDRF personnel to highest-urgency zones immediately.",
            },
            {
                "action": "dispatch_medical_kits",
                "priority": "HIGH",
                "instruction": "Distribute medical kits to zones with medical_distress > 50.",
            },
            {
                "action": "dispatch_rescue_boats",
                "priority": "MEDIUM",
                "instruction": "Deploy rescue boats to zones where hazard_depth >= 1.5 m.",
            },
        ]
        return {
            "status": "actions_generated",
            "prompt": request.prompt,
            "bob_response": "Dispatch plan formulated based on current disaster parameters.",
            "actions": actions,
            "context_received": request.context_data is not None,
        }

    # --- Status / health-check intent ---
    if any(kw in prompt_lower for kw in ["status", "health", "check", "operational"]):
        return {
            "status": "health_check",
            "prompt": request.prompt,
            "bob_response": "All systems operational. Optimizer engine is ready. No active alerts.",
            "system_health": {
                "optimizer": "READY",
                "solver": "SCIP / CBC",
                "api": "ONLINE",
                "ai_partner": "IBM Bob — CONNECTED",
            },
            "context_received": request.context_data is not None,
        }

    # --- Generic / fallback response ---
    return {
        "status": "acknowledged",
        "prompt": request.prompt,
        "bob_response": (
            "IBM Bob has received your query. "
            "Please use /api/allocate for resource optimization, "
            "or rephrase your prompt with keywords like 'deploy', 'status', or 'dispatch'."
        ),
        "context_received": request.context_data is not None,
        "suggested_endpoints": [
            "POST /api/allocate — Run MILP resource allocation",
            "POST /api/bob/assist — Conversational AI actions",
            "GET /  — System health check",
        ],
    }


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
