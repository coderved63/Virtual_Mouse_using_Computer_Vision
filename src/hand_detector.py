import cv2
import mediapipe as mp
import time
import os

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        """
        Initialize the MediaPipe Hand Detector using Tasks API.
        """
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        
        # Load the model
        model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
        
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=self.max_hands,
            min_hand_detection_confidence=self.detection_con,
            min_hand_presence_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        
        self.landmarker = HandLandmarker.create_from_options(options)
        self.results = None
        self.mp_draw = mp.solutions.drawing_utils if hasattr(mp, 'solutions') else None
        # If mp.solutions is missing, we can't use mp_draw directly easily. 
        # We will implement custom drawing or try to import it if available.
        # But we know solutions is missing. 
        # So we will implement a simple custom drawer.

    def find_hands(self, img, draw=True):
        """
        Process the image and find hands.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Use current time in ms
        timestamp_ms = int(time.time() * 1000)
        
        self.results = self.landmarker.detect_for_video(mp_image, timestamp_ms)

        if self.results.hand_landmarks:
            if draw:
                for hand_lms in self.results.hand_landmarks:
                    # manual drawing since mp.solutions.drawing_utils might be missing
                    self.draw_landmarks_manual(img, hand_lms)
        return img

    def draw_landmarks_manual(self, img, landmarks):
        """
        Draw landmarks manually using OpenCV.
        """
        h, w, c = img.shape
        # Connections for hand (standard MediaPipe logic)
        connections = [
            (0,1), (1,2), (2,3), (3,4), # Thumb
            (0,5), (5,6), (6,7), (7,8), # Index
            (0,9), (9,10), (10,11), (11,12), # Middle
            (0,13), (13,14), (14,15), (15,16), # Ring
            (0,17), (17,18), (18,19), (19,20), # Pinky
            (5,9), (9,13), (13,17) # Knuckles
        ]
        
        # Draw connections
        points = []
        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            points.append((cx, cy))
            
        for p1_id, p2_id in connections:
             if p1_id < len(points) and p2_id < len(points):
                cv2.line(img, points[p1_id], points[p2_id], (0, 255, 0), 2)
        
        # Draw points
        for cx, cy in points:
            cv2.circle(img, (cx, cy), 4, (255, 0, 0), cv2.FILLED)

    def find_position(self, img, hand_no=0):
        """
        Get the position of landmarks for a specific hand.
        """
        lm_list = []
        if self.results and self.results.hand_landmarks:
            try:
                my_hand = self.results.hand_landmarks[hand_no]
                h, w, c = img.shape
                for id, lm in enumerate(my_hand):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy])
            except IndexError:
                pass
        return lm_list

    def fingers_up(self, lm_list):
        """
        Check which fingers are up.
        """
        fingers = []
        if not lm_list:
            return fingers

        tip_ids = [4, 8, 12, 16, 20]

        # Thumb (Simple Logic)
        if lm_list[tip_ids[0]][1] < lm_list[tip_ids[0] - 1][1]: 
             fingers.append(1) 
        else:
             fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
