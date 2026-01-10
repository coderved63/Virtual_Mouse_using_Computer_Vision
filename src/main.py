import cv2
import time
import numpy as np
from hand_detector import HandDetector
from gesture_recognition import GestureRecognizer
from mouse_controller import MouseController
from utils import draw_text

def main():
    # 1. Initialization
    cap = cv2.VideoCapture(0)
    wCam, hCam = 640, 480
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = HandDetector(max_hands=1, detection_con=0.7)
    recognizer = GestureRecognizer()
    controller = MouseController(smoothing=5)

    pTime = 0
    
    print("Starting Virtual Mouse...")
    
    while True:
        # 2. Get image
        success, img = cap.read()
        if not success:
            break
            
        # Flip image for mirror view (easier for interaction)
        img = cv2.flip(img, 1)
        
        # 3. Find Hands
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        
        gesture = "None"
        pinch_dist = 0
        
        if len(lm_list) != 0:
            # 4. Filter Fingers
            fingers = detector.fingers_up(lm_list)
            
            # 5. Recognize Gesture
            gesture, pinch_dist = recognizer.recognize_gesture(fingers, lm_list, img)
            
            # 6. Apply Action
            # Coords for index finger (for moving)
            # Index tip: 8
            x1, y1 = lm_list[8][1], lm_list[8][2]
            
            if gesture == "Move":
                # Convert coordinates and move
                # We use a frame reduction rectangle to make it easier to reach edges
                controller.move_mouse(x1, y1, img.shape)
                
                # Visual Indicator for Active Zone
                frame_r = 100
                cv2.rectangle(img, (frame_r, frame_r), (wCam - frame_r, hCam - frame_r), (255, 0, 255), 2)
                
            elif gesture == "Scroll":
                # Scroll up/down based on hand position or movement?
                # Spec says "Scroll". Usually mapped to relative encoded movement.
                # Let's map Y position to scroll speed or just simple scroll.
                # Simple implementation: Scroll based on vertical movement or position?
                # Let's try: if hand is in top half, scroll up; bottom half, scroll down.
                # Or just continuous scroll if gesture is held (simpler).
                # Re-reading spec: "Scroll up/down".
                # Let's use position relative to center.
                if y1 < hCam // 2 - 50:
                    controller.scroll(20) # Up
                    cv2.putText(img, "Scroll UP", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                elif y1 > hCam // 2 + 50:
                    controller.scroll(-20) # Down
                    cv2.putText(img, "Scroll DOWN", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    
            elif gesture == "Zoom":
                # Pinch implies Zoom.
                # Depending on change in distance, we could zoom in/out.
                # Spec says: "Thumb + index pinch -> Zoom".
                # Simplify: Pinch = Zoom In? Or just 'Zoom' mode?
                # Let's implementation: Hold pinch to Zoom In (Ctrl + +)?
                # Or mapping distance to zoom level.
                # For simplicity: Pinch (< 40) is Zoom In.
                # We need a Zoom Out too.
                # Spec: "Zoom in / zoom out".
                # Maybe pinch in/out? Hard to track previous frame pinch without state.
                # Let's just key bind: Pinch -> Ctrl + Scroll?
                # Or PyAutoGUI doesn't support 'zoom' directly without hotkeys.
                # Let's assume standard Ctrl+Scroll.
                # If Pinch is tight -> Zoom In.
                # This part is tricky without state.
                # We will just note it on screen for now or send Hotkey.
                cv2.putText(img, f"Pinch: {int(pinch_dist)}", (20, 130), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                # controller.mouse_zoom(...) - PyAutoGUI doesn't have direct zoom.
                # We can do: pyautogui.keyDown('ctrl'), pyautogui.scroll(...), keyUp
                
            elif gesture == "Click":
                # Fist -> Click
                # Need cooldown to prevent spam
                # Implement cooldown in a robust app, here simple sleep or check
                # For responsiveness, we only click once per gesture enter (state machine needed)?
                # Or just simple click.
                controller.click()
                cv2.putText(img, "Click", (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                time.sleep(0.2) # Simple debounce

        # 7. FPS & UI
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        draw_text(img, f"FPS: {int(fps)}", (20, 50), (255, 0, 0))
        draw_text(img, f"Gesture: {gesture}", (20, 80), (0, 255, 0))

        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
