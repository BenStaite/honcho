
import os, json
from pathlib import Path

paths = [
    "/root/.claude/.credentials.json",
    str(Path.home() / ".claude" / ".credentials.json"),
]
for p in paths:
    path = Path(p)
    print(f"{p}: exists={path.exists()}")
    if path.exists():
        try:
            data = json.loads(path.read_text())
            token = data.get("claudeAiOauth", {}).get("accessToken", "")
            print(f"  token: {bool(token)}, len={len(token)}")
        except Exception as e:
            print(f"  read error: {e}")

print("HOME:", os.environ.get("HOME"))
print("USER:", os.environ.get("USER"))
