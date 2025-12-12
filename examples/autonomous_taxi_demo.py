"""
Full autonomous taxi demonstration
Combines lane following, object detection, and obstacle avoidance
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.autonomous_controller import AutonomousTaxi


def main():
    """Run full autonomous taxi demonstration"""
    print("=" * 50)
    print("PiCar-X Autonomous Taxi Demonstration")
    print("=" * 50)
    print()
    print("This demo combines:")
    print("  - Lane following using camera vision")
    print("  - Object detection using Coral USB Accelerator")
    print("  - Obstacle avoidance using ultrasonic sensor")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 50)
    print()
    
    # Initialize autonomous taxi
    taxi = AutonomousTaxi(
        use_camera_vision=True,
        use_object_detection=True
    )
    
    try:
        # Run indefinitely until stopped
        taxi.run()
    except KeyboardInterrupt:
        print("\n\nAutonomous taxi stopped by user")
    finally:
        taxi.cleanup()
        print("\nThank you for using PiCar-X Autonomous Taxi!")


if __name__ == "__main__":
    main()
