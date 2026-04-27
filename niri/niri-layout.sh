#!/usr/bin/env bash
set -euo pipefail
 
# --- (Master & Stack 70/30) ---
layout_master_stack() {
    echo "Applying Master-Stack Layout..."
    
    WINDOW_DATA=$(niri msg --json windows | jq -r '.[] | select(.is_focused == true)')
    COLUMN_WIDTH=$(echo "$WINDOW_DATA" | jq -r '.layout.tile_size[0]')
    SCREEN_WIDTH=$(niri msg --json outputs | jq -r 'to_entries | .[0].value.logical.width')
 
    if [[ -n "$SCREEN_WIDTH" && "$SCREEN_WIDTH" != "null" ]]; then
        PERCENTAGE=$(echo "scale=2; ($COLUMN_WIDTH / $SCREEN_WIDTH) * 100" | bc -l)
        PERCENTAGE_INT=$(printf "%.0f" "$PERCENTAGE")
        
        if [ "$PERCENTAGE_INT" -le 35 ]; then
            niri msg action consume-or-expel-window-right
            sleep 0.2
        fi
    fi
 
    niri msg action move-column-to-first
    sleep 0.1
    niri msg action set-column-width "70%"
    sleep 0.1
 
    niri msg action focus-column-right
    sleep 0.1
    for i in {1..15}; do
        niri msg action consume-window-into-column
        sleep 0.05
    done
    
    niri msg action set-column-width "30%"
    niri msg action focus-column-left
}
 
# ---  (2x2 Grid) ---
layout_grid_2x2() {
    echo "Applying 2x2 Grid Layout..."
    WINDOWS_PER_COLUMN=2
    TOTAL_COLUMNS=4
 
    niri msg action focus-column-first
    sleep 0.1
 
    for ((c=0; c<TOTAL_COLUMNS; c++)); do
        niri msg action set-column-width "50%"
        sleep 0.05
        niri msg action consume-window-into-column
        sleep 0.05
        niri msg action focus-column-right
        sleep 0.1
    done
    niri msg action focus-column-first
}
 
# --- (50/50 Split) ---
layout_split_50() {
    echo "Applying 50/50 Split..."
    niri msg action set-column-width "50%"
    sleep 0.1
    niri msg action focus-column-left
    niri msg action set-column-width "50%"
    sleep 0.1
    niri msg action focus-column-right
}
 
# ---  ---
case "${1:-}" in
    master)
        layout_master_stack
        ;;
    grid)
        layout_grid_2x2
        ;;
    split)
        layout_split_50
        ;;
    *)
        echo "Usage: $0 {master|grid|split}"
        exit 1
        ;;
esac
