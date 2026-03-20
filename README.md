# OSM-Closure-Routing-PoC
# OpenStreetMap Dynamic Closure Routing PoC
**Author:** Mithilesh A | **Target:** GSoC 2026 `closures.osm.ch` Production Integration

### Overview
This is a lightweight FastAPI microservice designed as a Proof of Concept (PoC) for dynamic spatial routing. It demonstrates the backend logic required to ingest temporary road closure data (simulating `closures.osm.ch` JSON payloads) and immediately apply infinite edge-weight penalties to a graph network.

By dynamically manipulating edge weights on the fly, downstream routing algorithms (like Dijkstra's) are forced to recalculate optimal detours around closed nodes without requiring a full planetary re-indexing.

### Tech Stack
* **Framework:** FastAPI / Uvicorn (Asynchronous API serving)
* **Graph Logic:** NetworkX (Dijkstra's shortest path simulation)
* **Data Validation:** Pydantic

### Endpoints
* `GET /api/route`: Calculates the optimal path and travel time between two nodes in the graph.
* `POST /api/closures`: Ingests a JSON payload detailing a blocked road segment and dynamically updates the graph's edge weights to detour future queries.
