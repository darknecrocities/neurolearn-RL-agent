import torch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.gesture_classifier import GestureClassifier

class GestureController:
    def __init__(self, model_path):
        self.model = GestureClassifier()
        if os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'), weights_only=True))
        else:
            print(f"Warning: Gesture model not found at {model_path}")
        self.model.eval()

    def predict(self, features):
        """Predict gesture from 42-length normalized feature list/array"""
        if features is None or len(features) == 0:
            return None
            
        # Convert to tensor shaped (1, 42)
        features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        prediction = self.model.predict(features_tensor)
        
        # Mapping definition based on prompt
        # 0 = move_cursor
        # 1 = pinch_select
        # 2 = open_hand_rotate
        # 3 = closed_fist_cancel
        # 4 = swipe_left
        # 5 = swipe_right
        return prediction
