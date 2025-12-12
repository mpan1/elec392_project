"""
Object detection module using TensorFlow Lite and Coral USB Accelerator
"""

try:
    import numpy as np
except ImportError:
    class MockNumpy:
        @staticmethod
        def array(data):
            return data
    np = MockNumpy()

try:
    import cv2
except ImportError:
    class MockCV2:
        @staticmethod
        def resize(image, size):
            return image
        
        @staticmethod
        def rectangle(img, pt1, pt2, color, thickness):
            pass
        
        @staticmethod
        def putText(img, text, org, font, scale, color, thickness):
            pass
        
        FONT_HERSHEY_SIMPLEX = 0
    
    cv2 = MockCV2()

try:
    from pycoral.utils import edgetpu
    from pycoral.utils import dataset
    from pycoral.adapters import common
    from pycoral.adapters import detect
except ImportError:
    # Mock implementations for development/testing
    class MockEdgeTPU:
        @staticmethod
        def make_interpreter(model_path):
            class MockInterpreter:
                def allocate_tensors(self):
                    pass
                
                def set_tensor(self, index, data):
                    pass
                
                def invoke(self):
                    pass
                
                def get_tensor(self, index):
                    return np.array([])
            
            return MockInterpreter()
    
    class MockDetect:
        class BBox:
            def __init__(self, xmin, ymin, xmax, ymax):
                self.xmin = xmin
                self.ymin = ymin
                self.xmax = xmax
                self.ymax = ymax
        
        class Object:
            def __init__(self, id, score, bbox):
                self.id = id
                self.score = score
                self.bbox = bbox
        
        @staticmethod
        def get_objects(interpreter, score_threshold=0.5):
            return []
    
    class MockCommon:
        @staticmethod
        def set_input(interpreter, image):
            pass
        
        @staticmethod
        def input_size(interpreter):
            return (300, 300)
    
    edgetpu = MockEdgeTPU()
    detect = MockDetect()
    common = MockCommon()


class ObjectDetector:
    """Object detection using Coral USB Accelerator"""
    
    def __init__(self, model_path='models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite',
                 labels_path='models/coco_labels.txt',
                 threshold=0.5):
        """
        Initialize object detector
        
        Args:
            model_path: Path to TFLite model for Edge TPU
            labels_path: Path to labels file
            threshold: Confidence threshold for detections
        """
        self.threshold = threshold
        self.labels = self._load_labels(labels_path)
        
        try:
            self.interpreter = edgetpu.make_interpreter(model_path)
            self.interpreter.allocate_tensors()
            self.input_size = common.input_size(self.interpreter)
        except Exception as e:
            print(f"Failed to initialize Edge TPU: {e}")
            print("Running in mock mode")
            self.interpreter = None
            self.input_size = (300, 300)
    
    def _load_labels(self, labels_path):
        """Load labels from file"""
        try:
            with open(labels_path, 'r') as f:
                labels = [line.strip() for line in f.readlines()]
            return labels
        except FileNotFoundError:
            # Return common COCO labels if file not found
            return ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
                   'train', 'truck', 'boat', 'traffic light', 'fire hydrant',
                   'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog']
    
    def detect_objects(self, image):
        """
        Detect objects in image
        
        Args:
            image: Input image (numpy array)
        
        Returns:
            list: List of detected objects with format:
                  [{'label': str, 'score': float, 'bbox': (xmin, ymin, xmax, ymax)}]
        """
        if self.interpreter is None:
            return []
        
        # Resize image to input size
        resized = cv2.resize(image, self.input_size)
        
        # Set input tensor
        common.set_input(self.interpreter, resized)
        
        # Run inference
        self.interpreter.invoke()
        
        # Get results
        objects = detect.get_objects(self.interpreter, self.threshold)
        
        # Format results
        detections = []
        height, width = image.shape[:2]
        
        for obj in objects:
            bbox = obj.bbox
            detection = {
                'label': self.labels[obj.id] if obj.id < len(self.labels) else 'unknown',
                'score': obj.score,
                'bbox': (
                    int(bbox.xmin * width),
                    int(bbox.ymin * height),
                    int(bbox.xmax * width),
                    int(bbox.ymax * height)
                )
            }
            detections.append(detection)
        
        return detections
    
    def draw_detections(self, image, detections):
        """
        Draw bounding boxes on image
        
        Args:
            image: Input image
            detections: List of detections
        
        Returns:
            numpy array: Image with drawn bounding boxes
        """
        output = image.copy()
        
        for det in detections:
            xmin, ymin, xmax, ymax = det['bbox']
            label = det['label']
            score = det['score']
            
            # Draw bounding box
            cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            
            # Draw label
            text = f"{label}: {score:.2f}"
            cv2.putText(output, text, (xmin, ymin - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return output
