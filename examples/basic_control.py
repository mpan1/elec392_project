"""
Basic vehicle control example
Demonstrates how to control the PiCar-X manually
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from picarx import PiCarX


def main():
    """Demonstrate basic vehicle control"""
    print("PiCar-X Basic Control Example")
    print("=" * 40)
    
    # Initialize car
    car = PiCarX()
    
    try:
        # Center steering and camera
        print("Centering steering and camera...")
        car.center_steering()
        car.center_camera()
        time.sleep(1)
        
        # Move forward
        print("Moving forward...")
        car.forward(speed=50)
        time.sleep(2)
        
        # Turn left
        print("Turning left...")
        car.set_steering_angle(60)  # Turn left
        time.sleep(1)
        
        # Center steering
        print("Centering steering...")
        car.set_steering_angle(90)
        time.sleep(1)
        
        # Turn right
        print("Turning right...")
        car.set_steering_angle(120)  # Turn right
        time.sleep(1)
        
        # Center steering
        print("Centering steering...")
        car.set_steering_angle(90)
        time.sleep(1)
        
        # Stop
        print("Stopping...")
        car.stop()
        time.sleep(1)
        
        # Move backward
        print("Moving backward...")
        car.backward(speed=40)
        time.sleep(2)
        
        # Stop
        print("Stopping...")
        car.stop()
        
        # Test camera pan/tilt
        print("\nTesting camera movement...")
        print("Pan left...")
        car.set_camera_pan(60)
        time.sleep(1)
        
        print("Pan right...")
        car.set_camera_pan(120)
        time.sleep(1)
        
        print("Center camera...")
        car.center_camera()
        time.sleep(1)
        
        print("\nBasic control test complete!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    finally:
        car.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()
