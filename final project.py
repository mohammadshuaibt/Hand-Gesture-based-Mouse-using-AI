import cv2
import mediapipe as mp
import pyautogui
# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False
# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Initialize drawing utility
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)
ws, hs = 1920, 1440
cap.set(3, ws)
cap.set(4, hs)

# Get screen size

#screen_width, screen_height = pyautogui.size()

screen_width = 2960  # Enter your screen width here
screen_height = 1740  # Enter your screen height here


while cap.isOpened():
    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the frame as not writeable to pass by reference.
    rgb_frame.flags.writeable = False

    # Process the frame to get hand landmarks
    results = hands.process(rgb_frame)

    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the label for the hand (left or right)
            hand_label = handedness.classification[0].label
            hand_confidence = handedness.classification[0].score

            # Put text on the frame to label the hand
            cv2.putText(frame, f"{hand_label} hand, {hand_confidence:.2f}",
                        (int(hand_landmarks.landmark[0].x * frame.shape[1]),
                         int(hand_landmarks.landmark[0].y * frame.shape[0] - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Label each landmark with its ID
            for idx, landmark in enumerate(hand_landmarks.landmark):
                cx, cy = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.putText(frame, f"{idx}", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

                # Move the mouse pointer based on specific landmarks if the hand is labeled as "Right"
                if hand_label == 'Right':

                    if idx == 8:
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                        # Get the coordinates relative to the screen size
                        index_x = int(screen_width * landmark.x)
                        index_y = int(screen_height * landmark.y)
                        # Move the mouse pointer to the index finger position
                        pyautogui.moveTo(index_x, index_y)

                        if abs(index_y - thumb_y) < 160:
                            pyautogui.hotkey('win', 'tab')
                            pyautogui.sleep(0.5)

                    elif idx == 4:
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                        thumb_x = screen_width / frame.shape[1] * cx
                        thumb_y = screen_height / frame.shape[0] * cy


                    elif idx == 12:
                        cv2.circle(frame, (cx, cy), 10, (255, 255, 255), -1)
                        middle_x = screen_width / frame.shape[1] * cx
                        middle_y = screen_height / frame.shape[0] * cy

                        if abs(middle_y - thumb_y) < 110:
                            pyautogui.doubleClick()
                            pyautogui.sleep(0.1)

                    elif idx == 16:
                        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)
                        ring_x = screen_width / frame.shape[1] * cx
                        ring_y = screen_height / frame.shape[0] * cy

                        if abs(ring_y - thumb_y) < 110:
                            pyautogui.rightClick()
                            pyautogui.sleep(0.1)
                    elif idx == 20:
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 255), -1)
                        pinky_x = screen_width / frame.shape[1] * cx
                        pinky_y = screen_height / frame.shape[0] * cy
                        #print('middlemcp finger :', abs(thumb_y - pinky_y))

                        if abs(pinky_y - thumb_y) < 40:
                            pyautogui.mouseDown(button='left')
                            #pyautogui.hotkey('win', 'tab')
                            pyautogui.sleep(1)

                if hand_label == 'Left':

                    if idx == 8:
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 0), -1)
                        # Get the coordinates relative to the screen size
                        index_x = int(screen_width * landmark.x)
                        index_y = int(screen_height * landmark.y)

                        if abs(index_y - thumb_y) < 160:
                            pyautogui.press('volumeup')
                            pyautogui.sleep(0.1)

                    elif idx == 4:
                        cv2.circle(frame, (cx, cy), 10, (255, 102, 255), -1)
                        thumb_x = screen_width / frame.shape[1] * cx
                        thumb_y = screen_height / frame.shape[0] * cy


                    elif idx == 12:
                        cv2.circle(frame, (cx, cy), 10, (153, 102, 51), -1)
                        middle_x = screen_width / frame.shape[1] * cx
                        middle_y = screen_height / frame.shape[0] * cy

                        if abs(middle_y - thumb_y) < 110:
                            pyautogui.press('volumedown')
                            pyautogui.sleep(0.1)

                    elif idx == 16:
                        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)
                        ring_x = screen_width / frame.shape[1] * cx
                        ring_y = screen_height / frame.shape[0] * cy

                        if abs(ring_y - thumb_y) < 110:
                            pyautogui.scroll(-900)
                            pyautogui.sleep(1)
                    elif idx == 20:
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 255), -1)
                        pinky_x = screen_width / frame.shape[1] * cx
                        pinky_y = screen_height / frame.shape[0] * cy
                        # print('middlemcp finger :', abs(thumb_y - pinky_y))

                        if abs(pinky_y - thumb_y) < 40:
                            pyautogui.scroll(900)
                            pyautogui.sleep(1)

    # Show the frame with landmarks and labels
    cv2.imshow('Hand Landmarks Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()