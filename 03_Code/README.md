# Project Eragon - Code

This directory contains the software code for Project Eragon, a bipedal walking robot.

## RTO Reverse Kinematics

The **RTO (Real-Time Operations) Reverse Kinematics** system provides inverse kinematics calculations for Eragon's legs.

### Quick Start

1. **Run the main script** to see demonstrations:
```bash
python3 rto_reverse_kinematics.py
```

2. **Run the examples** to see various usage patterns:
```bash
python3 example_usage.py
```

3. **Use in your own code**:
```python
from rto_reverse_kinematics import RTOKinematics

# Initialize the solver
rto = RTOKinematics()

# Calculate joint angles for a target foot position
x, y = 6.0, -12.0  # 6 cm forward, 12 cm down
hip_angle, knee_angle, success = rto.inverse_kinematics_2d(x, y)

if success:
    print(f"Hip: {hip_angle:.2f}°, Knee: {knee_angle:.2f}°")
```

### Files

- **`rto_reverse_kinematics.py`** - Main kinematics solver module
  - `RTOKinematics` class with inverse and forward kinematics
  - Servo PWM conversion utilities
  - Trajectory planning functions
  
- **`example_usage.py`** - Comprehensive usage examples
  - Standing pose calculation
  - Stepping motion trajectory
  - Circular foot motion
  - Workspace mapping
  - Custom robot configuration
  
- **`robot_config.ini`** - Robot configuration parameters
  - Link lengths and dimensions
  - Joint angle limits
  - Servo PWM settings
  - Gait parameters
  
- **`RTO_Documentation.md`** - Complete documentation
  - Mathematical foundations
  - API reference
  - Integration guide
  - Troubleshooting

### Features

✅ **2-DOF Inverse Kinematics** - Calculate joint angles for desired foot positions  
✅ **Forward Kinematics** - Verify solutions (validated with 0.0000 cm error)  
✅ **Trajectory Planning** - Generate smooth motion paths  
✅ **Workspace Validation** - Check reachability and joint limits  
✅ **Servo Integration** - Convert angles to PWM values for PCA9685  
✅ **Configurable** - Easy to adjust for different robot dimensions  

### Hardware Compatibility

- **Microcontroller**: ESP32
- **Servo Driver**: PCA9685 (16-channel PWM)
- **Servos**: MG996R Metal-Gear (4 total, 2 per leg)
- **Power**: 7.4V 2S LiPo battery

### Coordinate System

- **Origin**: At hip joint
- **X-axis**: Forward (positive) / Backward (negative)
- **Y-axis**: Up (positive) / Down (negative)
- **Units**: Centimeters

### Default Configuration

- **Thigh length**: 8.0 cm
- **Shin length**: 8.0 cm
- **Workspace**: 0 to 16 cm reach
- **Hip range**: -90° to +90°
- **Knee range**: 0° to 180°

### Next Steps

1. Review the documentation: `RTO_Documentation.md`
2. Run the examples: `example_usage.py`
3. Customize parameters in `robot_config.ini`
4. Integrate with your robot control code
5. Test on hardware with actual servos

### Future Development

- 3D kinematics (add hip abduction/adduction)
- Dynamic gait generation
- IMU-based balance control
- Terrain adaptation
- Energy-efficient motion planning

### Support

For detailed information, see:
- Full documentation: `RTO_Documentation.md`
- Project README: `../README.md`
- Hardware details: `../01_Hardware/02_BOM.md`

---

**Project Eragon** - Learning robotics through hands-on building!
