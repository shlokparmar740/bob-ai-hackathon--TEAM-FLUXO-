# Architecture Overview - Mewtwo (Autonomous Disaster Response Planner)

## 1. System Architecture
Mewtwo is designed as a robust, modular disaster response planning system that bridges the gap between raw emergency data and optimal resource allocation during the critical first 72 hours of a disaster.
+-----------------------------------------------------------------+
|                       Coordinator Frontend                      |
|                  (React / Dashboards / Maps)                    |
+--------------------------------+--------------------------------+
| REST APIs / WebSockets
+--------------------------------v--------------------------------+
|                         FastAPI Backend                         |
+--------------------------------+--------------------------------+
|
+------------------------+------------------------+
|                                                 |
v                                                 v
+-----------------------+                         +-----------------------+
|   Core Engine (Python)|                         |      Database         |
|  - Pandas & NumPy     |                         |     (MongoDB)         |
|  - Google OR-Tools    |                         +-----------------------+
|  - Scikit-learn (ML)  |                                    ^
+-----------------------+                                    |
|                                                 |
+------------------------+------------------------+
|
v
+-------------------------------+
|        IBM Bob Integration    |
| (Conversational & Automation) |
+-------------------------------+
## 2. Component Breakdown

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Core Engine** | Python | Main decision logic and execution flow. |
| **Data Processing** | Pandas + NumPy | Processing incoming disaster reports and constraints. |
| **Priority Scoring** | Rule-based weighted scoring | Determine urgency and severity across affected zones. |
| **Optimization** | Google OR-Tools | Allocate limited rescue teams and medical units efficiently. |
| **Optimization Method** | MILP / Integer Programming | Mathematical modeling for team and resource distribution. |
| **Database** | MongoDB | Store and retrieve rapidly changing incident data. |
| **Backend** | FastAPI | Connect core engine to frontend interfaces via REST/WebSockets. |
| **Real-time Updates** | WebSockets | Live status synchronization for emergency coordinators. |
| **Maps & Routing** | Leaflet + OpenStreetMap & OSRM | Visualize affected zones and estimate travel distance/time. |
| **Frontend** | React | Coordinator dashboard interface. |
| **Optional ML** | Scikit-learn | Future demand prediction and pattern analysis. |

## 3. Workflow & Data Flow
1. **Data Ingestion:** Incoming field reports, distress calls, and sensor data are captured and stored in MongoDB.
2. **Prioritization:** The core engine processes inputs using Pandas and rule-based weighted scoring to calculate zone criticality.
3. **Optimization & Allocation:** Google OR-Tools applies Mixed-Integer Linear Programming (MILP) to map available medical units and rescue teams to high-priority zones.
4. **Coordination Interface:** FastAPI serves the computed plans to the React frontend and enables natural language workflow management via IBM Bob integration.