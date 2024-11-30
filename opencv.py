import cv2
import mediapipe as mp
import subprocess
import os

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Path to the scripts
down_script = './down.sh'
up_script = './up.sh'
max_script = './max.sh'

# Function to run a shell script
def run_script(script_path):
    if os.path.exists(script_path):
        subprocess.run([script_path], shell=True)
    else:
        print(f"Script {script_path} not found!")

# Function to check for "duck mouth" (V-shaped or curled fingers) gesture
def is_duck_mouth(hand_landmarks):
    # Get the coordinates of the landmarks of each finger
    thumb = hand_landmarks.landmark[4]  # Tip of the thumb
    index = hand_landmarks.landmark[8]  # Tip of the index finger
    middle = hand_landmarks.landmark[12]  # Tip of the middle finger
    ring = hand_landmarks.landmark[16]  # Tip of the ring finger
    pinky = hand_landmarks.landmark[20]  # Tip of the pinky finger
    
    # Check if the index and middle fingers are pointing close to each other
    # and the other fingers are curled inwards (towards palm), forming a "V" shape
    duck_mouth = index.y > thumb.y and middle.y > thumb.y and ring.y < thumb.y and pinky.y < thumb.y
    return duck_mouth

# Function to check for "open palm" gesture
def is_open_palm(hand_landmarks):
    # Get the coordinates of the landmarks of each finger
    fingers = [hand_landmarks.landmark[i] for i in [4, 8, 12, 16, 20]]  # Tip of fingers
    # Check if all the finger tips are above the base of the palm (landmark 0)
    open_palm = all(finger.y < hand_landmarks.landmark[0].y for finger in fingers)
    return open_palm

# Function to maximize the window by running max.sh script
def maximize_window():
    run_script(max_script)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Previous positions of the index and middle fingers
prev_pos = None

# Threshold for movement detection (adjust this value as needed)
movement_threshold = 100  # Increase this value to reduce sensitivity

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)

    # Convert the image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the frame and get hand landmarks
    results = hands.process(rgb_image)

    # If hands are detected
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Draw the hand landmarks
            mp_draw.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates for the index and middle fingers (landmark 8 for index, 12 for middle)
            index_finger = landmarks.landmark[8]
            middle_finger = landmarks.landmark[12]

            # Convert to pixel values
            index_pos = (int(index_finger.x * image.shape[1]), int(index_finger.y * image.shape[0]))
            middle_pos = (int(middle_finger.x * image.shape[1]), int(middle_finger.y * image.shape[0]))

            # Draw circles at the positions of index and middle fingers
            cv2.circle(image, index_pos, 5, (0, 255, 0), -1)
            cv2.circle(image, middle_pos, 5, (255, 0, 0), -1)

            # Detect the direction of movement (up or down) based on vertical movement (y-coordinate)
            if prev_pos:
                prev_index, prev_middle = prev_pos

                # Calculate the change in y positions of both fingers
                delta_index_y = index_pos[1] - prev_index[1]
                delta_middle_y = middle_pos[1] - prev_middle[1]

                # Check if the movement is significant enough (above the threshold)
                if abs(delta_index_y) > movement_threshold and abs(delta_middle_y) > movement_threshold:
                    if delta_index_y > 0 and delta_middle_y > 0:
                        cv2.putText(image, "Moving Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        run_script(down_script)  # Run down.sh if moving down
                    elif delta_index_y < 0 and delta_middle_y < 0:
                        cv2.putText(image, "Moving Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        run_script(up_script)  # Run up.sh if moving up

            # Update previous positions
            prev_pos = (index_pos, middle_pos)

            # Check if the gesture matches "duck mouth" (fingers in a V shape)
            if is_duck_mouth(landmarks):
                cv2.putText(image, 'Duck Mouth Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Check if the gesture matches "open palm"
            if not is_open_palm(landmarks):
                cv2.putText(image, 'Open Palm Detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                maximize_window()  # Maximize window when open palm is detected
    
    # Display the resulting image
    # cv2.imshow("Hand Gesture Detection", image)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
