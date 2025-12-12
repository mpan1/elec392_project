"""
Obstacle avoidance module
Implements obstacle detection and avoidance logic
"""

try:
    import time
except ImportError:
    pass


class ObstacleAvoider:
    """Obstacle detection and avoidance using ultrasonic sensor and object detection"""
    
    def __init__(self, safe_distance=30.0, critical_distance=15.0):
        """
        Initialize obstacle avoider
        
        Args:
            safe_distance: Distance (cm) to start slowing down
            critical_distance: Distance (cm) to stop completely
        """
        self.safe_distance = safe_distance
        self.critical_distance = critical_distance
    
    def check_obstacles(self, distance, detections=None):
        """
        Check for obstacles and determine action
        
        Args:
            distance: Distance from ultrasonic sensor (cm)
            detections: Optional list of object detections from camera
        
        Returns:
            dict: Action to take with keys:
                  'action': 'stop', 'slow', 'clear'
                  'reason': Description of obstacle
                  'speed_factor': Speed multiplier (0.0 to 1.0)
        """
        # Check ultrasonic distance
        if distance > 0:  # Valid reading
            if distance < self.critical_distance:
                return {
                    'action': 'stop',
                    'reason': f'Obstacle at {distance:.1f}cm',
                    'speed_factor': 0.0
                }
            elif distance < self.safe_distance:
                # Slow down proportionally
                speed_factor = (distance - self.critical_distance) / (self.safe_distance - self.critical_distance)
                return {
                    'action': 'slow',
                    'reason': f'Approaching obstacle at {distance:.1f}cm',
                    'speed_factor': max(0.3, speed_factor)
                }
        
        # Check camera detections for obstacles
        if detections:
            for det in detections:
                label = det['label']
                score = det['score']
                bbox = det['bbox']
                
                # Check if obstacle is in path (center of image)
                xmin, ymin, xmax, ymax = bbox
                center_x = (xmin + xmax) / 2
                
                # If object is in center 50% of image and has high confidence
                if score > 0.6 and 0.25 < center_x / 640 < 0.75:
                    if label in ['person', 'car', 'bicycle', 'motorcycle', 'dog', 'cat']:
                        return {
                            'action': 'slow',
                            'reason': f'{label} detected in path',
                            'speed_factor': 0.5
                        }
        
        return {
            'action': 'clear',
            'reason': 'No obstacles',
            'speed_factor': 1.0
        }
    
    def plan_avoidance(self, distance, steering_angle):
        """
        Plan avoidance maneuver
        
        Args:
            distance: Current obstacle distance
            steering_angle: Current steering angle
        
        Returns:
            dict: Avoidance plan with 'steer' and 'speed'
        """
        if distance < self.critical_distance:
            # Try to turn away from obstacle
            avoidance_steer = 45 if steering_angle >= 0 else -45
            return {
                'steer': avoidance_steer,
                'speed': 0
            }
        elif distance < self.safe_distance:
            # Gentle avoidance
            avoidance_steer = min(30, max(-30, steering_angle + 15))
            return {
                'steer': avoidance_steer,
                'speed': 30
            }
        else:
            # Normal operation
            return {
                'steer': steering_angle,
                'speed': 50
            }
