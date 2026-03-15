class CameraRotation:
    def __init__(self, speed=0.6):
        self.speed = speed
        self.angle_x = 0.0
        self.angle_y = 0.0
        self.current_z = -15.0
        self.target_z = -15.0
        
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.friction = 0.90

    def update(self, dx, dy):
        """
        Takes active hand movement delta and applies it as velocity.
        """
        # Vertical movement (dy) applies to rotation over X axis
        self.velocity_x += dy * self.speed * 2.5
        # Horizontal movement (dx) applies to rotation over Y axis
        self.velocity_y += dx * self.speed * 2.5
        
    def apply_momentum(self):
        """
        Continuously called every frame to apply rotation and degrade velocity.
        """
        self.angle_x += self.velocity_x
        self.angle_y += self.velocity_y
        
        # Apply friction to slowly stop
        self.velocity_x *= self.friction
        self.velocity_y *= self.friction
        
        # Clamp velocity to 0 if very small to prevent micro-drifting
        if abs(self.velocity_x) < 0.01: self.velocity_x = 0.0
        if abs(self.velocity_y) < 0.01: self.velocity_y = 0.0
        
    def update_zoom(self, zoom_delta):
        """
        Updates target zoom depth. 
        zoom_delta > 0 zooms in, zoom_delta < 0 zooms out.
        """
        self.target_z += zoom_delta * 0.5
        # Clamp zoom to reasonable min/max depths
        self.target_z = max(-40.0, min(-3.0, self.target_z))
        
    def interpolate_zoom(self):
        """Smoothly lerps the current z depth towards the target z depth"""
        self.current_z += (self.target_z - self.current_z) * 0.1

    def get_angles(self):
        return self.angle_x, self.angle_y
        
    def get_z(self):
        return self.current_z
