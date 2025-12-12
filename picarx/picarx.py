"""
Main PiCar-X class
Integrates all hardware components for easy control
"""

from .motor import Motor
from .servo import Servo
from .camera import Camera
from .ultrasonic import Ultrasonic
from .grayscale import Grayscale


class PiCarX:
    """Main controller class for PiCar-X robot"""
    
    def __init__(self):
        """Initialize all PiCar-X components"""
        # Initialize motors
        self.left_motor = Motor(Motor.LEFT_MOTOR_DIR, Motor.LEFT_MOTOR_PWM)
        self.right_motor = Motor(Motor.RIGHT_MOTOR_DIR, Motor.RIGHT_MOTOR_PWM)
        
        # Initialize servos
        self.steering_servo = Servo(Servo.STEERING_CHANNEL, 
                                    min_angle=45, max_angle=135, default_angle=90)
        self.camera_pan_servo = Servo(Servo.CAMERA_PAN_CHANNEL,
                                      min_angle=0, max_angle=180, default_angle=90)
        self.camera_tilt_servo = Servo(Servo.CAMERA_TILT_CHANNEL,
                                       min_angle=30, max_angle=150, default_angle=90)
        
        # Initialize sensors
        self.camera = Camera()
        self.ultrasonic = Ultrasonic()
        self.grayscale = Grayscale()
    
    def set_motor_speed(self, left_speed, right_speed):
        """
        Set speed for both motors
        
        Args:
            left_speed: Speed for left motor (-100 to 100)
            right_speed: Speed for right motor (-100 to 100)
        """
        self.left_motor.set_speed(left_speed)
        self.right_motor.set_speed(right_speed)
    
    def forward(self, speed=50):
        """
        Move forward at specified speed
        
        Args:
            speed: Speed value (0 to 100)
        """
        self.set_motor_speed(speed, speed)
    
    def backward(self, speed=50):
        """
        Move backward at specified speed
        
        Args:
            speed: Speed value (0 to 100)
        """
        self.set_motor_speed(-speed, -speed)
    
    def turn_left(self, speed=50):
        """
        Turn left by differential drive
        
        Args:
            speed: Speed value (0 to 100)
        """
        self.set_motor_speed(speed // 2, speed)
    
    def turn_right(self, speed=50):
        """
        Turn right by differential drive
        
        Args:
            speed: Speed value (0 to 100)
        """
        self.set_motor_speed(speed, speed // 2)
    
    def stop(self):
        """Stop all motors"""
        self.left_motor.stop()
        self.right_motor.stop()
    
    def set_steering_angle(self, angle):
        """
        Set steering servo angle
        
        Args:
            angle: Steering angle (45-135, 90 is center)
        """
        self.steering_servo.set_angle(angle)
    
    def center_steering(self):
        """Center the steering servo"""
        self.steering_servo.center()
    
    def set_camera_pan(self, angle):
        """
        Set camera pan angle
        
        Args:
            angle: Pan angle (0-180, 90 is center)
        """
        self.camera_pan_servo.set_angle(angle)
    
    def set_camera_tilt(self, angle):
        """
        Set camera tilt angle
        
        Args:
            angle: Tilt angle (30-150, 90 is center)
        """
        self.camera_tilt_servo.set_angle(angle)
    
    def center_camera(self):
        """Center the camera servos"""
        self.camera_pan_servo.center()
        self.camera_tilt_servo.center()
    
    def get_distance(self):
        """
        Get distance from ultrasonic sensor
        
        Returns:
            float: Distance in centimeters
        """
        return self.ultrasonic.get_distance()
    
    def get_line_position(self):
        """
        Get line position from grayscale sensors
        
        Returns:
            int: Line position (-1, 0, 1, or None)
        """
        return self.grayscale.get_line_position()
    
    def capture_frame(self):
        """
        Capture frame from camera
        
        Returns:
            numpy array: RGB image
        """
        return self.camera.capture_frame()
    
    def cleanup(self):
        """Clean up all resources"""
        self.stop()
        self.center_steering()
        self.center_camera()
        self.left_motor.cleanup()
        self.right_motor.cleanup()
        self.ultrasonic.cleanup()
        self.grayscale.cleanup()
        self.camera.close()
