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
                
            elif gesture == "Scroll Up":
                # 2 Fingers UP -> Scroll Page UP
                controller.scroll(30)
                cv2.putText(img, "Scroll UP", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                
            elif gesture == "Scroll Down":
                # 3 Fingers UP -> Scroll Page DOWN
                controller.scroll(-30)
                cv2.putText(img, "Scroll DOWN", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    
            elif gesture == "Zoom In":
                # Pinky UP only -> Zoom In
                controller.zoom(20)
                cv2.putText(img, "Zoom IN", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                
            elif gesture == "Zoom Out":
                # Pinky + Thumb UP -> Zoom Out
                controller.zoom(-20)
                cv2.putText(img, "Zoom OUT", (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

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
