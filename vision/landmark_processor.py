import numpy as np

class LandmarkProcessor:
    def extract_features(self, hand_landmarks):
        """
        Extract normalized features from mediapipe hand landmarks.
        Returns a flattened vector of 42 values (21 points * 2 coords).
        """
        x_coords = []
        y_coords = []
        
        for lm in hand_landmarks.landmark:
            x_coords.append(lm.x)
            y_coords.append(lm.y)
            
        # Normalize relative to wrist (landmark 0)
        wrist_x = x_coords[0]
        wrist_y = y_coords[0]
        
        normalized_x = [x - wrist_x for x in x_coords]
        normalized_y = [y - wrist_y for y in y_coords]
        
        # Find max absolute distance to normalize between -1 and 1
        max_dist = max(max(abs(x) for x in normalized_x), max(abs(y) for y in normalized_y))
        
        if max_dist > 0:
            normalized_x = [x / max_dist for x in normalized_x]
            normalized_y = [y / max_dist for y in normalized_y]
        
        # Flatten into [x0, y0, x1, y1, ...]
        features = []
        for x, y in zip(normalized_x, normalized_y):
            features.extend([x, y])
            
        return np.array(features, dtype=np.float32)
        
    def get_key_points(self, hand_landmarks, frame_width, frame_height):
        """
        Helper to get screen pixel coordinates of key points.
        Returns dict containing index tip, thumb tip, wrist, etc.
        """
        lm = hand_landmarks.landmark
        
        def to_pixel(landmark):
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
            
        return {
            'index_tip': to_pixel(lm[8]),
            'thumb_tip': to_pixel(lm[4]),
            'middle_tip': to_pixel(lm[12]),
            'wrist': to_pixel(lm[0])
        }
