"""
Ultrasonic sensor module for PiCar-X
Handles distance measurement for obstacle detection
"""

import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    # Mock GPIO for development/testing
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        IN = 'IN'
        
        @staticmethod
        def setmode(mode):
            pass
        
        @staticmethod
        def setup(pin, mode):
            pass
        
        @staticmethod
        def output(pin, state):
            pass
        
        @staticmethod
        def input(pin):
            return 0
        
        @staticmethod
        def cleanup():
            pass
        
        HIGH = 1
        LOW = 0
    
    GPIO = MockGPIO()


class Ultrasonic:
    """Controls ultrasonic sensor for distance measurement"""
    
    # Default ultrasonic sensor pins
    TRIG_PIN = 24
    ECHO_PIN = 25
    
    def __init__(self, trig_pin=TRIG_PIN, echo_pin=ECHO_PIN):
        """
        Initialize ultrasonic sensor
        
        Args:
            trig_pin: GPIO pin for trigger signal
            echo_pin: GPIO pin for echo signal
        """
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
    
    def get_distance(self, timeout=0.5):
        """
        Measure distance to nearest object
        
        Args:
            timeout: Maximum time to wait for echo (seconds)
        
        Returns:
            float: Distance in centimeters, or -1 if timeout
        """
        # Send trigger pulse
        GPIO.output(self.trig_pin, GPIO.HIGH)
        time.sleep(0.00001)  # 10 microseconds
        GPIO.output(self.trig_pin, GPIO.LOW)
        
        # Wait for echo start
        start_time = time.time()
        pulse_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()
            if pulse_start - start_time > timeout:
                return -1
        
        # Wait for echo end
        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()
            if pulse_end - pulse_start > timeout:
                return -1
        
        # Calculate distance
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound = 343 m/s
        distance = round(distance, 2)
        
        return distance
    
    def cleanup(self):
        """Clean up GPIO resources"""
        GPIO.cleanup()
