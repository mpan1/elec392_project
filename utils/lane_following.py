"""
Lane following module
Implements computer vision-based lane detection and following
"""

try:
    import cv2
except ImportError:
    class MockCV2:
        @staticmethod
        def cvtColor(image, code):
            return image
        
        @staticmethod
        def GaussianBlur(image, ksize, sigma):
            return image
        
        @staticmethod
        def Canny(image, threshold1, threshold2):
            return image
        
        @staticmethod
        def fillPoly(image, pts, color):
            pass
        
        @staticmethod
        def bitwise_and(src1, src2):
            return src1
        
        @staticmethod
        def HoughLinesP(image, rho, theta, threshold, minLineLength, maxLineGap):
            return None
        
        @staticmethod
        def line(img, pt1, pt2, color, thickness):
            pass
        
        COLOR_BGR2GRAY = 0
    
    cv2 = MockCV2()

try:
    import numpy as np
except ImportError:
    class MockNumpy:
        @staticmethod
        def zeros_like(arr):
            return arr
        
        @staticmethod
        def array(data):
            return data
        
        @staticmethod
        def polyfit(x, y, deg):
            return [1, 0]
        
        @staticmethod
        def concatenate(arrays):
            return sum(arrays, [])
        
        int32 = 'int32'
        pi = 3.14159
    
    np = MockNumpy()


class LaneFollower:
    """Lane detection and following using computer vision"""
    
    def __init__(self, use_sensors=True):
        """
        Initialize lane follower
        
        Args:
            use_sensors: Whether to use grayscale sensors in addition to vision
        """
        self.use_sensors = use_sensors
    
    def detect_lane(self, image):
        """
        Detect lane lines in image
        
        Args:
            image: Input image (BGR format)
        
        Returns:
            tuple: (steering_angle, lane_image)
                   steering_angle: Recommended steering angle
                   lane_image: Image with lane lines drawn
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blur, 50, 150)
        
        # Define region of interest (lower portion of image)
        height, width = edges.shape
        mask = np.zeros_like(edges)
        polygon = np.array([[
            (0, height),
            (0, height * 2 // 3),
            (width, height * 2 // 3),
            (width, height)
        ]], np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_edges = cv2.bitwise_and(edges, mask)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            masked_edges,
            rho=2,
            theta=np.pi/180,
            threshold=50,
            minLineLength=40,
            maxLineGap=100
        )
        
        # Create output image
        lane_image = image.copy()
        
        if lines is None:
            return 0, lane_image  # No steering correction
        
        # Separate left and right lane lines
        left_lines = []
        right_lines = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 == x1:
                continue
            
            slope = (y2 - y1) / (x2 - x1)
            
            # Filter by slope to identify left/right lanes
            if slope < -0.5:  # Left lane (negative slope)
                left_lines.append(line[0])
            elif slope > 0.5:  # Right lane (positive slope)
                right_lines.append(line[0])
        
        # Average the lines
        left_line = self._average_lines(left_lines, height)
        right_line = self._average_lines(right_lines, height)
        
        # Draw lanes
        if left_line is not None:
            x1, y1, x2, y2 = left_line
            cv2.line(lane_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
        
        if right_line is not None:
            x1, y1, x2, y2 = right_line
            cv2.line(lane_image, (x1, y1), (x2, y2), (0, 0, 255), 5)
        
        # Calculate steering angle
        steering_angle = self._calculate_steering_angle(left_line, right_line, width)
        
        return steering_angle, lane_image
    
    def _average_lines(self, lines, height):
        """Average multiple line segments into one line"""
        if not lines:
            return None
        
        lines_array = np.array(lines)
        x1s = lines_array[:, 0]
        y1s = lines_array[:, 1]
        x2s = lines_array[:, 2]
        y2s = lines_array[:, 3]
        
        # Fit line using least squares
        try:
            coeffs = np.polyfit(
                np.concatenate([y1s, y2s]),
                np.concatenate([x1s, x2s]),
                1
            )
            
            # Calculate endpoints
            y1 = height
            y2 = int(height * 2 / 3)
            x1 = int(coeffs[0] * y1 + coeffs[1])
            x2 = int(coeffs[0] * y2 + coeffs[1])
            
            return (x1, y1, x2, y2)
        except (TypeError, ValueError, IndexError):
            return None
    
    def _calculate_steering_angle(self, left_line, right_line, width):
        """
        Calculate steering angle based on lane lines
        
        Returns:
            int: Steering angle offset from center (-45 to 45)
        """
        if left_line is None and right_line is None:
            return 0
        
        # Calculate lane center
        mid_x = width // 2
        
        if left_line is not None and right_line is not None:
            # Both lanes detected - steer between them
            left_x = left_line[0]
            right_x = right_line[0]
            lane_center = (left_x + right_x) // 2
        elif left_line is not None:
            # Only left lane - estimate right lane
            left_x = left_line[0]
            lane_center = left_x + width // 4
        else:
            # Only right lane - estimate left lane
            right_x = right_line[0]
            lane_center = right_x - width // 4
        
        # Calculate steering offset
        offset = lane_center - mid_x
        
        # Convert to steering angle (-45 to 45 degrees)
        steering_angle = int(offset / width * 90)
        steering_angle = max(-45, min(45, steering_angle))
        
        return steering_angle
    
    def follow_line_sensors(self, sensor_reading):
        """
        Calculate steering based on line tracking sensors
        
        Args:
            sensor_reading: Line position from grayscale sensors (-1, 0, 1, None)
        
        Returns:
            int: Steering angle offset (-30, 0, 30)
        """
        if sensor_reading == -1:
            return -30  # Turn left
        elif sensor_reading == 1:
            return 30  # Turn right
        elif sensor_reading == 0:
            return 0  # Go straight
        else:
            return 0  # No line detected, maintain course
