import math

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points (2D or 3D)."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

def calculate_angle(point1, point2, point3):
    """Calculate the angle between three points (2D). Center is point2."""
    p1 = (point1[0] - point2[0], point1[1] - point2[1])
    p3 = (point3[0] - point2[0], point3[1] - point2[1])
    
    dot_product = p1[0] * p3[0] + p1[1] * p3[1]
    mag_p1 = math.sqrt(p1[0]**2 + p1[1]**2)
    mag_p3 = math.sqrt(p3[0]**2 + p3[1]**2)
    
    if mag_p1 * mag_p3 == 0:
        return 0
        
    cos_angle = dot_product / (mag_p1 * mag_p3)
    cos_angle = max(-1.0, min(1.0, cos_angle)) # clamp
    return math.degrees(math.acos(cos_angle))
