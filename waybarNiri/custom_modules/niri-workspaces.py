#!/usr/bin/env python3
"""Emit niri workspace state for waybar via event-stream."""

import json
import os
import subprocess
import sys

THEMES = {
    "nord": {
        "focused": "#88c0d0",
        "active": "#8fbcbb",
        "urgent": "#ebcb8b",
        "idle": "#4c566a",
    },
    "tokyonight": {
        "focused": "#7aa2f7",
        "active": "#7dcfff",
        "urgent": "#e0af68",
        "idle": "#414868",
    },
}

_theme_path = os.path.expanduser("~/.config/waybar/.current_theme")
try:
    with open(_theme_path) as f:
        _theme = f.read().strip()
except OSError:
    _theme = "nord"
_colors = THEMES.get(_theme, THEMES["nord"])

C_FOCUSED = _colors["focused"]
C_ACTIVE = _colors["active"]
C_URGENT = _colors["urgent"]
C_IDLE = _colors["idle"]


def render(workspaces, focused_output):
    ws = [w for w in workspaces.values() if w.get("output") == focused_output]
    ws.sort(key=lambda w: w["idx"])
    if ws:
        ws = ws[:-1]
    parts = []
    for w in ws:
        if w.get("is_focused"):
            parts.append(f'<span color="{C_FOCUSED}"><b>●</b></span>')
        elif w.get("is_urgent"):
            parts.append(f'<span color="{C_URGENT}">●</span>')
        elif w.get("is_active"):
            parts.append(f'<span color="{C_ACTIVE}">●</span>')
        else:
            parts.append(f'<span color="{C_IDLE}">●</span>')
    sys.stdout.write(json.dumps({"text": " ".join(parts), "tooltip": ""}) + "\n")
    sys.stdout.flush()


def main():
    workspaces = {}
    focused_output = None

    proc = subprocess.Popen(
        ["niri", "msg", "-j", "event-stream"],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        changed = False

        if "WorkspacesChanged" in event:
            workspaces = {w["id"]: w for w in event["WorkspacesChanged"]["workspaces"]}
            for w in workspaces.values():
                if w.get("is_focused"):
                    focused_output = w.get("output")
                    break
            changed = True

        elif "WorkspaceActivated" in event:
            data = event["WorkspaceActivated"]
            wid = data["id"]
            focused = data.get("focused", False)
            if wid in workspaces:
                target = workspaces[wid]
                out = target.get("output")
                for w in workspaces.values():
                    if w.get("output") == out:
                        w["is_active"] = False
                        if focused:
                            w["is_focused"] = False
                target["is_active"] = True
                if focused:
                    target["is_focused"] = True
                    focused_output = out
                changed = True

        elif "WorkspaceUrgencyChanged" in event:
            data = event["WorkspaceUrgencyChanged"]
            wid = data["id"]
            if wid in workspaces:
                workspaces[wid]["is_urgent"] = data.get("urgent", False)
                changed = True

        if changed:
            render(workspaces, focused_output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
