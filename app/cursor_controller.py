import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.smoothing import ExponentialSmoothing

class CursorController:
    def __init__(self, screen_w, screen_h, alpha=0.75):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.smoother = ExponentialSmoothing(alpha)
        
    def update(self, index_tip_norm):
        if not index_tip_norm:
            return None
            
        raw_x = int(index_tip_norm[0] * self.screen_w)
        raw_y = int(index_tip_norm[1] * self.screen_h)
        
        # Mirror X because camera is mirrored
        raw_x = self.screen_w - raw_x
        
        smoothed = self.smoother.update((raw_x, raw_y))
        return (int(smoothed[0]), int(smoothed[1]))
