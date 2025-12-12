"""
Autonomous driving controller
Integrates lane following, object detection, and obstacle avoidance
"""

import time
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from picarx import PiCarX
from utils.lane_following import LaneFollower
from utils.object_detection import ObjectDetector
from utils.obstacle_avoidance import ObstacleAvoider


class AutonomousTaxi:
    """Main autonomous driving controller for robotic taxi"""
    
    def __init__(self, use_camera_vision=True, use_object_detection=True):
        """
        Initialize autonomous taxi controller
        
        Args:
            use_camera_vision: Use camera for lane detection
            use_object_detection: Use Coral accelerator for object detection
        """
        # Initialize hardware
        self.car = PiCarX()
        
        # Initialize vision systems
        self.lane_follower = LaneFollower(use_sensors=True)
        self.obstacle_avoider = ObstacleAvoider(safe_distance=30.0, critical_distance=15.0)
        
        self.use_camera_vision = use_camera_vision
        self.use_object_detection = use_object_detection
        
        if use_object_detection:
            try:
                self.object_detector = ObjectDetector()
            except Exception as e:
                print(f"Object detection initialization failed: {e}")
                self.object_detector = None
        else:
            self.object_detector = None
        
        # Control parameters
        self.base_speed = 40
        self.running = False
        
        # Center camera and steering
        self.car.center_camera()
        self.car.center_steering()
    
    def run(self, duration=None):
        """
        Run autonomous driving
        
        Args:
            duration: How long to run (seconds), None for indefinite
        """
        print("Starting autonomous taxi...")
        self.running = True
        start_time = time.time()
        
        try:
            while self.running:
                # Check duration
                if duration and (time.time() - start_time) > duration:
                    break
                
                # Get sensor data
                distance = self.car.get_distance()
                frame = self.car.capture_frame()
                
                # Obstacle detection
                detections = []
                if self.object_detector and self.use_object_detection:
                    try:
                        detections = self.object_detector.detect_objects(frame)
                    except Exception as e:
                        print(f"Object detection error: {e}")
                
                obstacle_status = self.obstacle_avoider.check_obstacles(distance, detections)
                
                # Lane following
                steering_offset = 0
                
                if self.use_camera_vision:
                    # Use camera-based lane detection
                    steering_offset, lane_image = self.lane_follower.detect_lane(frame)
                else:
                    # Use line tracking sensors
                    line_position = self.car.get_line_position()
                    steering_offset = self.lane_follower.follow_line_sensors(line_position)
                
                # Calculate steering angle (90 is center)
                steering_angle = 90 + steering_offset
                steering_angle = max(45, min(135, steering_angle))
                
                # Determine speed based on obstacles
                speed = int(self.base_speed * obstacle_status['speed_factor'])
                
                # Apply obstacle avoidance if needed
                if obstacle_status['action'] == 'stop':
                    self.car.stop()
                    self.car.set_steering_angle(steering_angle)
                    print(f"STOPPED: {obstacle_status['reason']}")
                    time.sleep(0.5)
                elif obstacle_status['action'] == 'slow':
                    self.car.forward(speed)
                    self.car.set_steering_angle(steering_angle)
                    print(f"SLOW: {obstacle_status['reason']} - Speed: {speed}")
                else:
                    self.car.forward(speed)
                    self.car.set_steering_angle(steering_angle)
                    print(f"DRIVING - Steering: {steering_angle}, Speed: {speed}")
                
                # Print detections
                if detections:
                    det_str = ["{} ({:.2f})".format(d['label'], d['score']) for d in detections]
                    print(f"Detected: {det_str}")
                
                time.sleep(0.1)  # Control loop frequency
        
        except KeyboardInterrupt:
            print("\nStopping autonomous taxi...")
        finally:
            self.stop()
    
    def stop(self):
        """Stop autonomous driving and clean up"""
        self.running = False
        self.car.stop()
        self.car.center_steering()
        print("Autonomous taxi stopped")
    
    def cleanup(self):
        """Clean up all resources"""
        self.stop()
        self.car.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    # Run autonomous taxi
    taxi = AutonomousTaxi(use_camera_vision=True, use_object_detection=True)
    
    try:
        taxi.run()
    finally:
        taxi.cleanup()
