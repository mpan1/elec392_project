"""
Servo control module for PiCar-X
Handles servo motors for steering and camera pan/tilt
"""

try:
    from adafruit_servokit import ServoKit
except ImportError:
    # Mock ServoKit for development/testing
    class MockServoKit:
        class MockServo:
            def __init__(self):
                self.angle = 90
        
        def __init__(self, channels=16):
            self._servos = [self.MockServo() for _ in range(channels)]
        
        @property
        def servo(self):
            return self._servos
    
    ServoKit = MockServoKit


class Servo:
    """Controls servo motors for steering and camera positioning"""
    
    # Default servo channels
    STEERING_CHANNEL = 0
    CAMERA_PAN_CHANNEL = 1
    CAMERA_TILT_CHANNEL = 2
    
    def __init__(self, channel, min_angle=0, max_angle=180, default_angle=90):
        """
        Initialize servo controller
        
        Args:
            channel: Servo channel number (0-15)
            min_angle: Minimum servo angle
            max_angle: Maximum servo angle
            default_angle: Default/center position
        """
        self.channel = channel
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.default_angle = default_angle
        self.current_angle = default_angle
        
        try:
            self.kit = ServoKit(channels=16)
            self.set_angle(default_angle)
        except Exception:
            self.kit = None
    
    def set_angle(self, angle):
        """
        Set servo to specific angle
        
        Args:
            angle: Target angle (will be clamped to min/max range)
        """
        self.current_angle = max(self.min_angle, min(self.max_angle, angle))
        
        if self.kit:
            try:
                self.kit.servo[self.channel].angle = self.current_angle
            except Exception:
                pass
    
    def center(self):
        """Move servo to center/default position"""
        self.set_angle(self.default_angle)
    
    def get_angle(self):
        """Get current servo angle"""
        return self.current_angle
