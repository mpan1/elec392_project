"""
Motor control module for PiCar-X
Handles DC motor control for forward/backward movement
"""

try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for development/testing on non-Raspberry Pi systems
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        
        @staticmethod
        def setmode(mode):
            pass
        
        @staticmethod
        def setup(pin, mode):
            pass
        
        @staticmethod
        def PWM(pin, frequency):
            class MockPWM:
                def start(self, duty_cycle):
                    pass
                
                def ChangeDutyCycle(self, duty_cycle):
                    pass
                
                def stop(self):
                    pass
            return MockPWM()
        
        @staticmethod
        def cleanup():
            pass
    
    GPIO = MockGPIO()


class Motor:
    """Controls the DC motors for the PiCar-X"""
    
    # Default motor pins
    LEFT_MOTOR_DIR = 17
    LEFT_MOTOR_PWM = 27
    RIGHT_MOTOR_DIR = 22
    RIGHT_MOTOR_PWM = 23
    
    def __init__(self, dir_pin=None, pwm_pin=None):
        """
        Initialize motor controller
        
        Args:
            dir_pin: GPIO pin for direction control
            pwm_pin: GPIO pin for PWM speed control
        """
        self.dir_pin = dir_pin
        self.pwm_pin = pwm_pin
        self.speed = 0
        self.pwm = None
        
        if dir_pin and pwm_pin:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.dir_pin, GPIO.OUT)
            GPIO.setup(self.pwm_pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.pwm_pin, 1000)  # 1kHz frequency
            self.pwm.start(0)
    
    def set_speed(self, speed):
        """
        Set motor speed
        
        Args:
            speed: Speed value from -100 to 100
                   Positive values for forward, negative for backward
        """
        self.speed = max(-100, min(100, speed))
        
        if self.pwm:
            # Set direction
            direction = GPIO.HIGH if self.speed >= 0 else GPIO.LOW
            GPIO.output(self.dir_pin, direction)
            
            # Set PWM duty cycle
            self.pwm.ChangeDutyCycle(abs(self.speed))
    
    def stop(self):
        """Stop the motor"""
        self.set_speed(0)
    
    def cleanup(self):
        """Clean up GPIO resources"""
        if self.pwm:
            self.pwm.stop()
