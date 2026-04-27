#!/bin/bash
# Wait for xwayland-satellite to set up the X11 socket, then propagate
# DISPLAY into the D-Bus activation environment for apps like Steam.
for i in $(seq 120); do
    for sock in /tmp/.X11-unix/X*; do
        [ -S "$sock" ] || continue
        num="${sock##*/X}"
        dbus-update-activation-environment "DISPLAY=:${num}" WAYLAND_DISPLAY XDG_SESSION_TYPE XDG_CURRENT_DESKTOP
        exit 0
    done
    sleep 0.5
done
