"""
Lane following example
Demonstrates lane following using camera vision and line tracking sensors
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from picarx import PiCarX
from utils.lane_following import LaneFollower


def main():
    """Demonstrate lane following"""
    print("PiCar-X Lane Following Example")
    print("=" * 40)
    
    # Initialize car and lane follower
    car = PiCarX()
    lane_follower = LaneFollower(use_sensors=True)
    
    use_camera = True  # Set to False to use line tracking sensors only
    
    try:
        car.center_steering()
        car.center_camera()
        
        print(f"Starting lane following (Camera: {use_camera})...")
        print("Press Ctrl+C to stop")
        
        base_speed = 40
        running = True
        
        while running:
            if use_camera:
                # Camera-based lane detection
                frame = car.capture_frame()
                steering_offset, lane_image = lane_follower.detect_lane(frame)
                
                # Calculate steering angle
                steering_angle = 90 + steering_offset
                steering_angle = max(45, min(135, steering_angle))
                
                print(f"Steering offset: {steering_offset:+3d}, Angle: {steering_angle}")
            else:
                # Sensor-based line following
                line_position = car.get_line_position()
                steering_offset = lane_follower.follow_line_sensors(line_position)
                steering_angle = 90 + steering_offset
                
                print(f"Line position: {line_position}, Steering: {steering_angle}")
            
            # Apply steering and speed
            car.set_steering_angle(steering_angle)
            car.forward(base_speed)
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nLane following stopped by user")
    finally:
        car.stop()
        car.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()
