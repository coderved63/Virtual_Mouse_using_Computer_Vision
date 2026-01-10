import math
import numpy as np
import cv2

def calculate_distance(p1, p2):
    """
    Calculate Euclidean distance between two points (x, y).
    """
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def get_angle(a, b, c):
    """
    Calculate angle between three points (a, b, c).
    b is the vertex.
    Returns angle in degrees.
    """
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def map_range(value, in_min, in_max, out_min, out_max):
    """
    Map a value from one range to another.
    """
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def draw_text(image, text, position=(20, 50), color=(255, 0, 0), scale=1, thickness=2):
    """
    Draw text on the image with a background for better visibility.
    """
    cv2.putText(image, text, position, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)
