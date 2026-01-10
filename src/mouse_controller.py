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
        Move the mouse to a position mapped from frame coordinates to screen coordinates.
        x, y: Coordinates in the frame (usually normalized or pixel).
        frame_shape: (height, width) of the webcame frame.
        """
        h, w = frame_shape[:2]
        
        # Frame reduction to avoid reaching the very edge (which is hard)
        frame_r = 100 
        
        # Map coordinates
        # Invert X because camera is mirrored
        # But we will handle mirroring in main loop usually. 
        # If camera is mirrored, x=0 is right side of screen.
        # Let's map directly:
        
        x_mapped = np.interp(x, (frame_r, w - frame_r), (0, self.screen_width))
        y_mapped = np.interp(y, (frame_r, h - frame_r), (0, self.screen_height))
        
        # Smoothing
        self.clocX = self.plocX + (x_mapped - self.plocX) / self.smoothing
        self.clocY = self.plocY + (y_mapped - self.plocY) / self.smoothing
        
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
        
    def drag(self, x, y, frame_shape):
        """
        Drag operation.
        """
        # Similar logic to move but using dragTo
        # For simplicity in this version, we might just hold click.
        pass # To be implemented if complex drag is needed, else just click loop.
