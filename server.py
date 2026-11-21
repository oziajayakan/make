"""Muse AI MCP server - a simple task & note tracker (e.g. for bounty work)."""
import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

DATA = Path(os.environ.get("DATA_FILE", "data.json"))
mcp = FastMCP(
    "Muse AI",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "8000")),
    stateless_http=True,
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

def _load():
    try:
        return json.loads(DATA.read_text())
    except Exception:
        return []

def _save(items):
    DATA.write_text(json.dumps(items, indent=2, ensure_ascii=False))

@mcp.tool()
def add_task(title: str, notes: str = "", due: str = "") -> dict:
    """Add a new task. `due` is optional free text such as 2026-12-01."""
    items = _load()
    t = {"id": uuid.uuid4().hex[:8], "title": title, "notes": notes, "due": due,
         "status": "todo", "created": datetime.now(timezone.utc).isoformat()}
    items.append(t); _save(items)
    return t

@mcp.tool()
def list_tasks(status: str = "") -> list:
    """List tasks. Optionally filter by status: todo, doing, or done."""
    items = _load()
    return [t for t in items if not status or t["status"] == status]

@mcp.tool()
def update_task(id: str, status: str = "", title: str = "", notes: str = "") -> dict:
    """Update a task's status (todo/doing/done), title, or notes by its id."""
    if status and status not in ("todo", "doing", "done"):
        return {"error": "status must be todo, doing or done"}
    items = _load()
    for t in items:
        if t["id"] == id:
            if status: t["status"] = status
            if title: t["title"] = title
            if notes: t["notes"] = notes
            _save(items); return t
    return {"error": "task not found"}

@mcp.tool()
def delete_task(id: str) -> dict:
    """Delete a task by its id."""
    items = _load()
    new = [t for t in items if t["id"] != id]
    _save(new)
    return {"deleted": len(items) - len(new)}

@mcp.tool()
def summary() -> dict:
    """Return counts of tasks per status."""
    out = {"todo": 0, "doing": 0, "done": 0}
    for t in _load(): out[t["status"]] = out.get(t["status"], 0) + 1
    return out

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
