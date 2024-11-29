#!/bin/bash

window_id=$(xdotool getactivewindow)

if [ -z "$window_id" ] || [ "$window_id" == "0" ]; then
    exit 1
fi

window_name=$(xdotool getwindowname "$window_id")

if [ "$window_name" == "Desktop" ]; then
    exit 1
fi

window_info=$(xwininfo -id $window_id)
x_pos=$(echo "$window_info" | awk '/Absolute upper-left X:/ {print $4}')
y_pos=$(echo "$window_info" | awk '/Absolute upper-left Y:/ {print $4}')
actual_width=$(echo "$window_info" | awk '/Width:/ {print $2}')
mid_x=$(( x_pos + (actual_width / 2) ))

xdotool mousemove $mid_x $((y_pos - 30)) click 2
xdotool windowminimize "$window_id"