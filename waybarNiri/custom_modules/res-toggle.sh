#!/bin/bash

OUTPUT="eDP-1"
SCALE=$(niri msg focused-output 2>/dev/null | awk '/Scale:/ {print $2; exit}')

case "$1" in
    toggle)
        if [ "$SCALE" = "1.6" ]; then
            niri msg output "$OUTPUT" scale 2.0
        else
            niri msg output "$OUTPUT" scale 1.6
        fi
        ;;
    *)
        if [ "$SCALE" = "1.6" ]; then
            echo "4K"
        else
            echo "FHD"
        fi
        ;;
esac
