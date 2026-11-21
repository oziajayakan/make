# Muse AI MCP

A small MCP (Model Context Protocol) server that works as a task and notes tracker. It is useful for keeping track of work items such as competition or bounty tasks.

## Tools

| Tool | Description |
|------|-------------|
| `add_task(title, notes?, due?)` | Create a task |
| `list_tasks(status?)` | List tasks, optionally filtered by `todo`, `doing`, `done` |
| `update_task(id, status?, title?, notes?)` | Change a task |
| `delete_task(id)` | Remove a task |
| `summary()` | Count of tasks per status |

## Example prompts

- "Add a task: finish the news-image kit, due 2026-12-01"
- "Show me everything that is still in progress"
- "Mark task 3f9a1c2d as done"
- "Give me a summary of my tasks"

## Endpoint

Transport: Streamable HTTP (stateless). The MCP endpoint is `https://<your-host>/mcp`.

## Access requirements

- No account or paid plan required.
- Authentication: none.
- Available worldwide.
- Data is stored per server instance in `data.json`.

## Run locally

```bash
pip install -r requirements.txt
python server.py        # listens on port 8000, or $PORT
```

## Deploy (Render)

1. Push this folder to a GitHub repo.
2. On render.com create a **Web Service** from the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python server.py`
5. Your endpoint is `https://<service-name>.onrender.com/mcp`.

## Privacy and terms

See the Privacy Policy and Terms of Service linked in the connector submission. Contact: kyosvwrn@gmail.com
