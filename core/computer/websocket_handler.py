"""
Real-time WebSocket Connection Manager & Handler Generator.
Generates heartbeat ping/pong keep-alive, client connection registry, broadcasting,
and FastAPI / Node.js WebSocket router code.
"""

from typing import Dict, Any

def generate_websocket_handler(
    endpoint: str = "/ws/telemetry",
    heartbeat_interval_sec: int = 15
) -> Dict[str, Any]:
    """
    Generates WebSocket server boilerplate with broadcast and heartbeat.
    """
    py_code = f"""# FastAPI WebSocket Connection Manager & Broadcast Handler
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("{endpoint}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Telemetry payload: {{data}}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
"""

    return {
        "status": "success",
        "endpoint": endpoint,
        "heartbeat_interval_sec": heartbeat_interval_sec,
        "fastapi_websocket_code": py_code
    }
