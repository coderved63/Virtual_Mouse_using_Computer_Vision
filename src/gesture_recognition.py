from utils import calculate_distance

class GestureRecognizer:
    def __init__(self):
        pass

    def recognize_gesture(self, fingers, landmarks, img):
        """
        Determine the gesture based on finger states and landmarks.
        fingers: List of 5 booleans [Thumb, Index, Middle, Ring, Pinky]
        landmarks: List of [id, x, y]
        """
        gesture = "None"
        
        if not landmarks:
            return gesture

        # Coordinates
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        
        # Calculate distances
        pinch_dist = calculate_distance((thumb_tip[1], thumb_tip[2]), (index_tip[1], index_tip[2]))
        
        # Logic
        # 1. Open Palm (All fingers up) -> Pause
        if all(fingers):
            gesture = "Pause"
            
        # 2. Moving Mode (Index UP + Thumb DOWN)
        elif fingers[1] and not fingers[0] and not fingers[2] and not fingers[3] and not fingers[4]:
            gesture = "Move"
            
        # 3. Scroll Down (Index + Middle + Ring up)
        elif fingers[1] and fingers[2] and fingers[3] and not fingers[4]:
            gesture = "Scroll Down"

        # 4. Scroll Up (Index + Middle up)
        elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            gesture = "Scroll Up"
        
        # 5. Zoom Out (Pinky + Thumb UP - "Shaka")
        elif fingers[4] and fingers[0] and not fingers[1] and not fingers[2] and not fingers[3]:
             gesture = "Zoom Out"

        # 6. Zoom In (Pinky UP only)
        elif fingers[4] and not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3]:
             gesture = "Zoom In"
             
        # 7. Click (Fist - All fingers down)
        elif not any(fingers):
            gesture = "Click"
            
        return gesture, pinch_dist

        return gesture, pinch_dist
