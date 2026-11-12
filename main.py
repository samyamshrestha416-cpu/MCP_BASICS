
import os
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("ai-sticky-notes")


NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE,"w") as f:
            f.write("")

@mcp.tool()
def add_note(message: str) -> str:
    """Add a note to the notes file."""
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note added."

@mcp.tool()
def read_notes() -> str:
    """Read all notes from the notes file."""
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.read()
    return notes if notes else "No notes found."

@mcp.resource("notes://latest")
def latest_note() -> str:
    """Get the latest note from the notes file."""
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes found."

@mcp.prompt()
def notes_summary() -> str:
    """Summarize the notes."""
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.read().strip()
    if not notes:
        return "No notes to summarize."
    return f"Summary of notes:\n{notes}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")