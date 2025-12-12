"""
Camera module for PiCar-X
Handles camera capture for vision-based features
"""

import time

try:
    import numpy as np
except ImportError:
    # Mock numpy for development/testing
    class MockNumpy:
        @staticmethod
        def zeros(shape, dtype=None):
            return [[0] * shape[1] for _ in range(shape[0])]
        
        uint8 = 'uint8'
    
    np = MockNumpy()

try:
    from picamera2 import Picamera2
except ImportError:
    # Mock camera for development/testing
    class MockPicamera2:
        def __init__(self):
            self.started = False
        
        def configure(self, config):
            pass
        
        def create_preview_configuration(self, main=None):
            return {}
        
        def start(self):
            self.started = True
        
        def capture_array(self):
            # Return a dummy image (black 640x480 RGB image)
            return np.zeros((480, 640, 3), dtype=np.uint8)
        
        def stop(self):
            self.started = False
        
        def close(self):
            self.started = False
    
    Picamera2 = MockPicamera2


class Camera:
    """Controls the camera for vision-based navigation and detection"""
    
    def __init__(self, resolution=(640, 480), framerate=30):
        """
        Initialize camera
        
        Args:
            resolution: Tuple of (width, height)
            framerate: Frames per second
        """
        self.resolution = resolution
        self.framerate = framerate
        self.camera = None
        
        try:
            self.camera = Picamera2()
            config = self.camera.create_preview_configuration(
                main={"size": resolution, "format": "RGB888"}
            )
            self.camera.configure(config)
            self.camera.start()
            time.sleep(0.5)  # Allow camera to warm up
        except Exception as e:
            print(f"Camera initialization failed: {e}")
            self.camera = Picamera2()  # Use mock camera
    
    def capture_frame(self):
        """
        Capture a single frame from the camera
        
        Returns:
            numpy array: RGB image array
        """
        if self.camera:
            try:
                return self.camera.capture_array()
            except Exception:
                return np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
        return np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
    
    def stop(self):
        """Stop the camera"""
        if self.camera:
            try:
                self.camera.stop()
            except Exception:
                pass
    
    def close(self):
        """Close and release camera resources"""
        if self.camera:
            try:
                self.camera.close()
            except Exception:
                pass
