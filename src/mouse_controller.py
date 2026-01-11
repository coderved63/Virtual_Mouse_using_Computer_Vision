import pyautogui
import numpy as np
import time

class MouseController:
    def __init__(self, smoothing=5):
        """
        Initialize Mouse Controller.
        smoothing: Factor for exponential moving average (higher = smoother but more lag).
        """
        self.screen_width, self.screen_height = pyautogui.size()
        self.smoothing = smoothing
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        
        # Disable fail-safe if needed, but safer to keep it enabled or handle gracefully.
        # pyautogui.FAILSAFE = False 

    def move_mouse(self, x, y, frame_shape):
        """
        Move the mouse with adaptive smoothing and deadzone.
        """
        h, w = frame_shape[:2]
        frame_r = 100 
        
        # Map coordinates
        x_mapped = np.interp(x, (frame_r, w - frame_r), (0, self.screen_width))
        y_mapped = np.interp(y, (frame_r, h - frame_r), (0, self.screen_height))
        
        # Calculate distance from previous location
        dist = np.sqrt((x_mapped - self.plocX)**2 + (y_mapped - self.plocY)**2)

        # Deadzone: Ignore very small movements (jitter)
        # If movement is < 2 pixels, don't update
        if dist < 2:
            return 

        # Adaptive Smoothing
        # If moving fast (large dist), lower smoothing (more responsive)
        # If moving slow (small dist), higher smoothing (more precision)
        # Base smoothing is self.smoothing (e.g., 5)
        
        current_smoothing = self.smoothing
        if dist > 100:
            current_smoothing = max(1, self.smoothing / 2) # Faster response
        elif dist < 20: 
            current_smoothing = self.smoothing * 1.5 # More precision
            
        self.clocX = self.plocX + (x_mapped - self.plocX) / current_smoothing
        self.clocY = self.plocY + (y_mapped - self.plocY) / current_smoothing
        
        try:
            pyautogui.moveTo(self.clocX, self.clocY)
        except pyautogui.FailSafeException:
            pass
            
        self.plocX, self.plocY = self.clocX, self.clocY

    def scroll(self, steps):
        """
        Scroll up or down.
        """
        pyautogui.scroll(steps)

    def click(self, button='left'):
        """
        Perform a mouse click.
        """
        pyautogui.click(button=button)
        
    def zoom(self, steps):
        """
        Zoom in or out using Ctrl + Scroll.
        steps: Positive for Zoom In, Negative for Zoom Out.
        """
        pyautogui.keyDown('ctrl')
        pyautogui.scroll(steps)
        pyautogui.keyUp('ctrl')

    def drag(self, x, y, frame_shape):
        """
        Drag operation.
        """
        # Similar logic to move but using dragTo
        # For simplicity in this version, we might just hold click.
        pass # To be implemented if complex drag is needed, else just click loop.
