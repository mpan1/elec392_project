"""
Object detection example
Demonstrates object detection using Coral USB Accelerator
"""

import sys
import os
import time
import cv2

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from picarx import PiCarX
from utils.object_detection import ObjectDetector


def main():
    """Demonstrate object detection"""
    print("PiCar-X Object Detection Example")
    print("=" * 40)
    
    # Initialize car and object detector
    car = PiCarX()
    detector = ObjectDetector(
        model_path='models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite',
        labels_path='models/coco_labels.txt',
        threshold=0.5
    )
    
    try:
        car.center_camera()
        
        print("Starting object detection...")
        print("Press Ctrl+C to stop")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            # Capture frame
            frame = car.capture_frame()
            frame_count += 1
            
            # Detect objects
            detections = detector.detect_objects(frame)
            
            # Draw detections
            output_frame = detector.draw_detections(frame, detections)
            
            # Print detections
            if detections:
                print(f"\nFrame {frame_count}:")
                for det in detections:
                    print(f"  {det['label']}: {det['score']:.2f} at {det['bbox']}")
            
            # Calculate FPS
            elapsed = time.time() - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"FPS: {fps:.1f}", end='\r')
            
            # Optional: Save detection images
            # cv2.imwrite(f'detection_{frame_count}.jpg', output_frame)
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nObject detection stopped by user")
        elapsed = time.time() - start_time
        avg_fps = frame_count / elapsed if elapsed > 0 else 0
        print(f"Average FPS: {avg_fps:.1f}")
    finally:
        car.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()
