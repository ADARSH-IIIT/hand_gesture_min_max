#!/bin/bash
# Check if xdotool and xprop are installed
if ! command -v xdotool &> /dev/null || ! command -v xprop &> /dev/null; then
    echo "xdotool or xprop is not installed. Please install them using your package manager."
    exit 1
fi

# Get visible window IDs
window_ids=$(xdotool search --onlyvisible --all "")

# Filter valid windows
declare -a window_array
for window_id in $window_ids; do
    window_name=$(xdotool getwindowname "$window_id" 2>/dev/null)
    if [[ -z "$window_name" ]] || [[ "$window_name" =~ [Cc]innamon ]] || [[ "$window_name" == "Desktop" ]]; then
        continue
    fi
    window_type=$(xprop -id "$window_id" | grep "_NET_WM_WINDOW_TYPE" | awk -F'=' '{print $2}')
    if [[ "$window_type" =~ "_NET_WM_WINDOW_TYPE_NORMAL" ]]; then
        window_array+=("$window_id")
    fi
done

# Exit if no valid windows are found
if [[ ${#window_array[@]} -eq 0 ]]; then
    exit 1
fi

# Target window for animation
window_id="${window_array[0]}"

# Minimize and restore the window
xdotool windowminimize "$window_id"
sleep 0.2
xdotool windowactivate "$window_id"

# Screen dimensions
screen_width=$(xdotool getdisplaygeometry | awk '{print $1}')
screen_height=$(xdotool getdisplaygeometry | awk '{print $2}')

# Animation parameters
end_width=$((screen_width * 9 / 10))   # 90% of screen width
end_height=$((screen_height * 9 / 10)) # 90% of screen height
steps=2                                # Minimal animation steps for fast popup

# Quick animation loop
for ((i=1; i<=steps; i++)); do
    new_width=$((50 + (end_width - 50) * i / steps))
    new_height=$((50 + (end_height - 50) * i / steps))
    xdotool windowsize "$window_id" "$new_width" "$new_height"
    sleep 0.01
done

# Final size adjustment
xdotool windowsize "$window_id" "$end_width" "$end_height"
