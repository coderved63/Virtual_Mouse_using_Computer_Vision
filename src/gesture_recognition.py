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
            
        # 2. Moving Mode (Only Index up)
        elif fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
            gesture = "Move"
            
        # 3. Scrolling (Index + Middle up)
        elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            gesture = "Scroll"
        
        # 4. Zoom (Thumb + Index pinch, others down or irrelevant?)
        # Spec: Thumb + Index pinch -> Zoom
        # Usually checking if distance is small
        elif fingers[1] and fingers[0] and pinch_dist < 40:
             # This might overlap with Move if Thumb is considered "up".
             # We prioritize Pinch over Move if distance is small.
             gesture = "Zoom"
             
        # 5. Click (Fist - All fingers down)
        elif not any(fingers):
            gesture = "Click"
            
        # Refinement for Zoom vs Move:
        # If in "Move" state but thumb is close to index, it might be a pinch.
        if gesture == "Move" and pinch_dist < 40:
            gesture = "Zoom"

        return gesture, pinch_dist
