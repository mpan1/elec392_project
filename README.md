# ELEC 392 - Autonomous Robotic Taxi

A repository for code used in Smith Engineering ELEC 392 design course. This project uses a **Sunfounder PiCar-X** and **Coral USB Accelerator** to develop a robotic taxi capable of operating autonomously in a miniature town populated with rubber duckies.

## Features

- **Hardware Control Libraries**: Complete interface for PiCar-X components including motors, servos, camera, ultrasonic sensor, and line tracking sensors
- **Autonomous Driving**: Lane following using computer vision and line tracking sensors
- **Object Detection**: Real-time object detection using Coral USB Accelerator for edge AI inference
- **Obstacle Avoidance**: Intelligent obstacle detection and avoidance using ultrasonic sensor and camera
- **Sample Code**: Ready-to-use examples demonstrating all key features

## Project Structure

```
elec392/
├── picarx/                      # PiCar-X hardware interface libraries
│   ├── __init__.py
│   ├── picarx.py                # Main PiCar-X controller class
│   ├── motor.py                 # DC motor control
│   ├── servo.py                 # Servo control (steering, camera)
│   ├── camera.py                # Camera interface
│   ├── ultrasonic.py            # Ultrasonic distance sensor
│   └── grayscale.py             # Line tracking sensors
├── utils/                       # Autonomous driving utilities
│   ├── autonomous_controller.py # Main autonomous driving controller
│   ├── lane_following.py        # Lane detection and following
│   ├── object_detection.py      # Object detection using Coral
│   └── obstacle_avoidance.py    # Obstacle detection and avoidance
├── examples/                    # Sample code and demonstrations
│   ├── basic_control.py         # Basic vehicle control example
│   ├── lane_following_demo.py   # Lane following demonstration
│   ├── object_detection_demo.py # Object detection demonstration
│   └── autonomous_taxi_demo.py  # Full autonomous taxi demo
├── models/                      # AI models for object detection
│   └── (Place TFLite models here)
├── tutorials/
│   ├──road_sign_detector        # Training Road Sign Detector (Colab)
│   └──salad_detector            # Training Salad Detector (Colab)
└── requirements.txt             # Python dependencies
```

## Hardware Requirements

- Sunfounder PiCar-X robot car
- Raspberry Pi 4B (recommended)
- Coral USB Accelerator
- Camera module (Pi Camera or compatible)
- Ultrasonic distance sensor
- Line tracking (grayscale) sensors

## Software Requirements

- Python 3.7+
- Raspberry Pi OS (Bullseye)
- See `requirements.txt` for Python dependencies

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mpan1/elec392.git
   cd elec392
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the object detection model for Coral USB Accelerator:
   ```bash
   mkdir -p models
   cd models
   wget https://github.com/google-coral/test_data/raw/master/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite
   wget https://github.com/google-coral/test_data/raw/master/coco_labels.txt
   cd ..
   ```

## Usage

### Basic Vehicle Control

Test basic motor and servo control:

```bash
python examples/basic_control.py
```

### Lane Following

Demonstrate lane following using camera vision or line tracking sensors:

```bash
python examples/lane_following_demo.py
```

### Object Detection

Test object detection with the Coral USB Accelerator:

```bash
python examples/object_detection_demo.py
```

### Full Autonomous Taxi

Run the complete autonomous driving system:

```bash
python examples/autonomous_taxi_demo.py
```

## Using the PiCar-X Library

```python
from picarx import PiCarX

# Initialize the car
car = PiCarX()

# Basic movement
car.forward(speed=50)
car.set_steering_angle(90)  # 90 is center, 45-135 range

# Get sensor data
distance = car.get_distance()  # Ultrasonic distance in cm
line_pos = car.get_line_position()  # -1 (left), 0 (center), 1 (right)
frame = car.capture_frame()  # Capture camera image

# Cleanup when done
car.cleanup()
```

## Autonomous Driving System

The autonomous taxi integrates multiple subsystems:

1. **Lane Following**: Uses camera-based computer vision to detect lane lines and calculate steering angles
2. **Object Detection**: Coral USB Accelerator runs MobileNet SSD for real-time object detection
3. **Obstacle Avoidance**: Combines ultrasonic sensor and camera detections to avoid obstacles
4. **Controller**: Main control loop that coordinates all systems

```python
from utils.autonomous_controller import AutonomousTaxi

taxi = AutonomousTaxi(use_camera_vision=True, use_object_detection=True)
taxi.run()  # Run indefinitely
taxi.cleanup()
```

## Development Notes

- All hardware libraries include mock implementations for development/testing on non-Pi systems
- The code is designed to work with or without actual hardware connected
- Adjust PID constants and thresholds in the controller for your specific environment

## Contributing

This is a course project repository. Contributions should follow the course guidelines and be coordinated with the instructor.

## License

See LICENSE file for details.

## Course Information

**Course**: ELEC 392 - Engineering Design and Development
**Institution**: Smith Engineering, Queen's University
**Project**: Autonomous Robotic Taxi with PiCar-X 
