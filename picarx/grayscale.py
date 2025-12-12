"""
Grayscale sensor module for PiCar-X
Handles line tracking sensors for lane following
"""

try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for development/testing
    class MockGPIO:
        BCM = 'BCM'
        IN = 'IN'
        
        @staticmethod
        def setmode(mode):
            pass
        
        @staticmethod
        def setup(pin, mode):
            pass
        
        @staticmethod
        def input(pin):
            return 1  # Default to high (no line detected)
        
        @staticmethod
        def cleanup():
            pass
    
    GPIO = MockGPIO()


class Grayscale:
    """Controls grayscale/line tracking sensors for lane following"""
    
    # Default grayscale sensor pins (3 sensors)
    LEFT_PIN = 18
    CENTER_PIN = 19
    RIGHT_PIN = 20
    
    def __init__(self, left_pin=LEFT_PIN, center_pin=CENTER_PIN, right_pin=RIGHT_PIN):
        """
        Initialize grayscale sensors
        
        Args:
            left_pin: GPIO pin for left sensor
            center_pin: GPIO pin for center sensor
            right_pin: GPIO pin for right sensor
        """
        self.left_pin = left_pin
        self.center_pin = center_pin
        self.right_pin = right_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_pin, GPIO.IN)
        GPIO.setup(self.center_pin, GPIO.IN)
        GPIO.setup(self.right_pin, GPIO.IN)
    
    def read_sensors(self):
        """
        Read all three grayscale sensors
        
        Returns:
            tuple: (left, center, right) sensor values
                   0 = dark/line detected, 1 = light/no line
        """
        left = GPIO.input(self.left_pin)
        center = GPIO.input(self.center_pin)
        right = GPIO.input(self.right_pin)
        
        return (left, center, right)
    
    def get_line_position(self):
        """
        Determine line position relative to sensors
        
        Returns:
            int: -1 (left), 0 (center), 1 (right), None (no line)
        """
        left, center, right = self.read_sensors()
        
        # 0 means dark/line detected
        if center == 0:
            return 0  # Line is centered
        elif left == 0:
            return -1  # Line is to the left
        elif right == 0:
            return 1  # Line is to the right
        else:
            return None  # No line detected
    
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()
