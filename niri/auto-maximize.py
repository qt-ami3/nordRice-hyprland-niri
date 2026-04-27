#!/usr/bin/env python3
"""Auto-arrange new tiled windows into repeating 2x2 grids, column-first.

Decision is based on the CURRENT column layout of the workspace rather
than a raw window count, so the script keeps doing the right thing when
you close windows mid-grid or start from an arbitrary shape (e.g. two
single-window columns already sitting side-by-side).

Rules applied to each new tiled window:
  - No existing cols         -> new col, maximized (W1 case).
  - Any col has < 2 windows  -> stack new into the leftmost such col.
  - Else (all cols full, N)  -> N is even: new col, maximized (new grid).
                             -> N is odd:  new col, shrink prev col to 50%.

Widths: a column sitting at 100% (start of a grid) keeps its width when
stacked into; the shrink branch explicitly sets both cols of the
forming pair to 50% so the grid ends up side-by-side.
"""
import json
import subprocess


def msg_json(*args):
    r = subprocess.run(["niri", "msg", "-j", *args],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def action(*args):
    subprocess.run(["niri", "msg", "action", *args],
                   capture_output=True)


def columns(workspace_id, exclude_wid):
    """Return {col_idx: [win_ids]} for tiled wins on workspace, excluding one id."""
    cols = {}
    for w in msg_json("windows"):
        if w["workspace_id"] != workspace_id or w["is_floating"]:
            continue
        if w["id"] == exclude_wid:
            continue
        pos = w.get("layout", {}).get("pos_in_scrolling_layout")
        if not pos:
            continue
        cols.setdefault(pos[0], []).append(w["id"])
    return cols


def arrange(new_wid, workspace_id):
    cols = columns(workspace_id, new_wid)
    col_indexes = sorted(cols.keys())

    # Always put focus on the new window first so subsequent column ops
    # act on the correct workspace and on the new window's column.
    action("focus-window", "--id", str(new_wid))

    if not col_indexes:
        action("maximize-column")
        return

    hole = next((i for i in col_indexes if len(cols[i]) < 2), None)

    if hole is not None:
        # Stack new into the leftmost incomplete column. Move new adjacent
        # to the hole (in case it didn't land at the rightmost slot), then
        # consume the right neighbor (the new win) into the hole column.
        action("move-column-to-index", str(hole + 1))
        action("focus-column", str(hole))
        action("consume-window-into-column")
        return

    # No holes; all existing cols are full stacks.
    num_full = len(col_indexes)
    action("move-column-to-index", str(num_full + 1))

    if num_full % 2 == 0:
        # Even count of full cols -> last grid is complete. Start a new
        # grid by maximizing the new column.
        action("maximize-column")
        return

    # Odd count of full cols -> the last grid is mid-pair. Shrink the
    # trailing full col (currently maximized) back to 50% so the pair
    # sits side-by-side at 50/50.
    action("focus-column", str(col_indexes[-1]))
    action("set-column-width", "50%")
    action("focus-window", "--id", str(new_wid))


def main():
    known = set()
    for w in msg_json("windows"):
        known.add(w["id"])

    proc = subprocess.Popen(["niri", "msg", "-j", "event-stream"],
                            stdout=subprocess.PIPE, text=True)

    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if "WindowOpenedOrChanged" in event:
            win = event["WindowOpenedOrChanged"]["window"]
            wid = win["id"]
            if wid in known:
                continue
            known.add(wid)
            ws = win.get("workspace_id")
            if ws is None or win.get("is_floating"):
                continue
            arrange(wid, ws)

        elif "WindowClosed" in event:
            known.discard(event["WindowClosed"]["id"])


if __name__ == "__main__":
    main()
