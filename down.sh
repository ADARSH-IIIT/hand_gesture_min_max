# s1 moving active window to bottom of stack ==> minimizing it




#!/bin/bash
# sleep 3
# Get the window ID of the currently focused window
window_id=$(xdotool getactivewindow)

# Use xwininfo to get window geometry including decorations
window_info=$(xwininfo -id $window_id)

# Extract the actual width and height of the window
actual_width=$(echo "$window_info" | awk '/Width:/ {print $2}')
actual_height=$(echo "$window_info" | awk '/Height:/ {print $2}')

# Extract the position (top-left corner of the window including decorations)
x_pos=$(echo "$window_info" | awk '/Absolute upper-left X:/ {print $4}')
y_pos=$(echo "$window_info" | awk '/Absolute upper-left Y:/ {print $4}')

# Calculate the midpoint X position
mid_x=$(( x_pos + (actual_width / 2) ))

# Print the results
echo "Window Geometry:"
echo "Position: X=$x_pos, Y=$y_pos"
echo "Width: $actual_width"
echo "Height: $actual_height"
echo "Midpoint X: $mid_x"

# Simulate a middle-click at the calculated midpoint on the title bar

xdotool mousemove $mid_x $((y_pos - 30)) click 2

xdotool windowminimize "$window_id"

# Get screen dimensions
screen_width=$(xdotool getdisplaygeometry | awk '{print $1}')
screen_height=$(xdotool getdisplaygeometry | awk '{print $2}')

# Calculate the center of the screen
center_x=$((screen_width / 2))
center_y=$((screen_height / 2))

# Move the mouse back to the center of the screen
xdotool mousemove $center_x $center_y

echo "Middle-click simulated on the title bar, and mouse returned to the center."
