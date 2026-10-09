"""
Mewtwo Disaster Response - Core Optimization Engine
Track D3: Autonomous Disaster Response Planner
Uses Google OR-Tools (Mixed-Integer Linear Programming - MILP / SCIP Solver)
"""
from ortools.linear_solver import pywraplp
from typing import List, Dict, Any


class DisasterOptimizer:
    def __init__(self):
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        if not self.solver:
            self.solver = pywraplp.Solver.CreateSolver('CBC')

    def calculate_urgency_score(
        self,
        casualties: int,
        hazard_depth: float,
        medical_distress: int
    ) -> float:
        """
        Composite Urgency Formula:
          - Casualties:      40% weight
          - Hazard depth:    30% weight  (scaled 0-100 via *10, capped at 100)
          - Medical distress:30% weight
        Returns a score in [0, 100].
        """
        scaled_hazard = min(hazard_depth * 10, 100.0)
        urgency = (casualties * 0.40) + (scaled_hazard * 0.30) + (medical_distress * 0.30)
        return round(min(urgency, 100.0), 2)

    def optimize_allocation(
        self,
        zones: List[Dict[str, Any]],
        available_resources: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        MILP optimization over all zones.

        Constraints:
          1. Total allocation of each resource <= inventory limit.
          2. rescue_boats allocation = 0 for zones where hazard_depth < 1.5 m.

        Objective:
          Maximize weighted urgency across all (zone, resource) pairs.
          medical_kits and ndrf_personnel get 2x coefficient multiplier.
        """
        if not self.solver:
            return {"status": "error", "message": "Solver could not be initialized"}

        self.solver.Clear()

        resource_types = list(available_resources.keys())

        # Decision variables: integer units allocated per (zone, resource)
        allocations: Dict[str, Dict[str, pywraplp.Variable]] = {}
        for z in zones:
            z_id = z["id"]
            allocations[z_id] = {}
            for r in resource_types:
                allocations[z_id][r] = self.solver.IntVar(
                    0, available_resources[r], f"alloc_{z_id}_{r}"
                )

        # Constraint 1: Inventory limits
        for r in resource_types:
            self.solver.Add(
                self.solver.Sum([allocations[z["id"]][r] for z in zones]) <= available_resources[r]
            )

        # Constraint 2: Terrain-aware — no rescue_boats where hazard_depth < 1.5 m
        for z in zones:
            z_id = z["id"]
            if z.get("hazard_depth", 0) < 1.5 and "rescue_boats" in allocations[z_id]:
                self.solver.Add(allocations[z_id]["rescue_boats"] == 0)

        # Pre-compute urgency scores and attach to zone dicts
        for z in zones:
            z["calculated_urgency"] = self.calculate_urgency_score(
                z.get("casualties", 0),
                z.get("hazard_depth", 0.0),
                z.get("medical_distress", 0)
            )

        # Objective: Maximize lives saved / urgency addressed
        objective = self.solver.Objective()
        for z in zones:
            urgency = z["calculated_urgency"]
            for r in resource_types:
                # Give higher-impact resources a 2x coefficient boost
                weight = urgency * (2.0 if r in ["medical_kits", "ndrf_personnel"] else 1.0)
                objective.SetCoefficient(allocations[z["id"]][r], weight)
        objective.SetMaximization()

        status = self.solver.Solve()

        if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
            results = []
            for z in zones:
                z_id = z["id"]
                assigned = {
                    r: int(allocations[z_id][r].solution_value())
                    for r in resource_types
                }
                results.append({
                    "zone_id": z_id,
                    "location_name": z["location_name"],
                    "urgency_score": z["calculated_urgency"],
                    "allocated_resources": assigned,
                    "recommended_action": (
                        "Deploy Immediately" if z["calculated_urgency"] > 50 else "Standby / Queue"
                    )
                })

            return {
                "status": "success",
                "solution_type": "OPTIMAL" if status == pywraplp.Solver.OPTIMAL else "FEASIBLE",
                "allocations": sorted(results, key=lambda x: x["urgency_score"], reverse=True)
            }
        else:
            return {
                "status": "failed",
                "message": "No feasible allocation found with current constraints."
            }
