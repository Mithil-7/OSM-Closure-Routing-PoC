from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import networkx as nx
import uvicorn

# Initialize the API
app = FastAPI(title="OSM Closures & Routing API PoC", version="1.0")

# 1. Initialize our "City Graph" (Acting as our routing database)
city_graph = nx.Graph()
roads = [
    ("Node_A", "Node_B", 5), ("Node_B", "Node_C", 5), ("Node_C", "Node_D", 5),
    ("Node_A", "Node_E", 8), ("Node_B", "Node_F", 4), ("Node_C", "Node_G", 6),
    ("Node_E", "Node_F", 4), ("Node_F", "Node_G", 4), ("Node_G", "Node_D", 7)
]
for u, v, w in roads:
    city_graph.add_edge(u, v, weight=w)

# 2. Define the JSON payload structure for closures
class ClosurePayload(BaseModel):
    node1: str
    node2: str
    reason: str

# --- API ENDPOINTS ---

@app.get("/api/route")
def calculate_route(start: str, end: str):
    """Calculates the fastest route between two nodes."""
    try:
        path = nx.shortest_path(city_graph, source=start, target=end, weight='weight')
        travel_time = nx.shortest_path_length(city_graph, source=start, target=end, weight='weight')
        return {
            "status": "success",
            "start": start,
            "end": end,
            "optimal_path": path,
            "estimated_time_minutes": travel_time
        }
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No valid route exists. Destination isolated.")
    except nx.NodeNotFound:
        raise HTTPException(status_code=400, detail="Start or End node does not exist in the graph.")

@app.post("/api/closures")
def apply_road_closure(closure: ClosurePayload):
    """Ingests a road closure and applies an infinite penalty to that edge."""
    if city_graph.has_edge(closure.node1, closure.node2):
        # Apply the penalty to force the routing algorithm to avoid this road
        city_graph[closure.node1][closure.node2]['weight'] = float('inf')
        return {
            "status": "success",
            "message": f"Closure successfully applied between {closure.node1} and {closure.node2}",
            "reason": closure.reason
        }
    raise HTTPException(status_code=404, detail="The specified road segment does not exist.")

if __name__ == "__main__":
    print("Starting OSM Routing API Simulator on http://127.0.0.1:8080/docs ...")
    uvicorn.run(app, host="127.0.0.1", port=8080)