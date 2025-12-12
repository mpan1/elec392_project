"""
Simple tests to verify code structure and imports
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test picarx imports
        from picarx import PiCarX, Motor, Servo, Camera, Ultrasonic, Grayscale
        print("✓ PiCar-X modules imported successfully")
        
        # Test utils imports
        from utils import LaneFollower, ObjectDetector, ObstacleAvoider, AutonomousTaxi
        print("✓ Utility modules imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_picarx_initialization():
    """Test PiCar-X initialization"""
    print("\nTesting PiCar-X initialization...")
    
    try:
        from picarx import PiCarX
        car = PiCarX()
        print("✓ PiCar-X initialized successfully")
        
        # Test basic methods
        car.center_steering()
        car.center_camera()
        car.stop()
        print("✓ Basic methods work")
        
        car.cleanup()
        print("✓ Cleanup successful")
        
        return True
    except Exception as e:
        print(f"✗ Initialization error: {e}")
        return False


def test_lane_follower():
    """Test lane follower"""
    print("\nTesting lane follower...")
    
    try:
        from utils.lane_following import LaneFollower
        import numpy as np
        
        follower = LaneFollower(use_sensors=True)
        
        # Test with dummy image
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        steering_offset, lane_image = follower.detect_lane(dummy_image)
        
        print(f"✓ Lane detection works (offset: {steering_offset})")
        
        # Test sensor-based following
        steering = follower.follow_line_sensors(0)
        print(f"✓ Sensor-based following works (steering: {steering})")
        
        return True
    except Exception as e:
        print(f"✗ Lane follower error: {e}")
        return False


def test_obstacle_avoider():
    """Test obstacle avoider"""
    print("\nTesting obstacle avoider...")
    
    try:
        from utils.obstacle_avoidance import ObstacleAvoider
        
        avoider = ObstacleAvoider(safe_distance=30.0, critical_distance=15.0)
        
        # Test with different distances
        status1 = avoider.check_obstacles(50)
        print(f"✓ Safe distance: {status1['action']}")
        
        status2 = avoider.check_obstacles(20)
        print(f"✓ Slow distance: {status2['action']}")
        
        status3 = avoider.check_obstacles(10)
        print(f"✓ Critical distance: {status3['action']}")
        
        return True
    except Exception as e:
        print(f"✗ Obstacle avoider error: {e}")
        return False


def test_object_detector():
    """Test object detector"""
    print("\nTesting object detector...")
    
    try:
        from utils.object_detection import ObjectDetector
        import numpy as np
        
        detector = ObjectDetector(threshold=0.5)
        print("✓ Object detector initialized")
        
        # Test with dummy image
        dummy_image = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = detector.detect_objects(dummy_image)
        
        print(f"✓ Object detection works (found {len(detections)} objects)")
        
        return True
    except Exception as e:
        print(f"✗ Object detector error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("ELEC 392 PiCar-X Code Structure Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_imports,
        test_picarx_initialization,
        test_lane_follower,
        test_obstacle_avoider,
        test_object_detector
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
