# RTO Reverse Kinematics Documentation

## Overview

The **RTO (Real-Time Operations) Reverse Kinematics** script provides inverse kinematics calculations for Project Eragon's bipedal robot. It calculates the required joint angles (servo positions) to achieve desired foot positions in 2D space.

## What is Reverse/Inverse Kinematics?

**Inverse kinematics** (IK) solves the problem: "Given a desired position for the robot's foot, what angles should the joints be at?"

This is the reverse of **forward kinematics** (FK), which answers: "Given joint angles, where is the foot?"

### Why is IK Important?

When programming a walking robot, you typically think in terms of where you want the feet to be, not what angles the joints should be. IK allows you to:
- Plan foot trajectories for walking
- Maintain balance by positioning feet
- Respond to terrain changes
- Execute smooth, coordinated movements

## System Architecture

### Hardware Components
- **ESP32**: Main microcontroller
- **PCA9685**: 16-channel PWM driver for servo control
- **MG996R Servos**: 4 metal-gear servos (2 per leg)
  - Hip servo: Controls forward/backward leg swing
  - Knee servo: Controls leg extension/flexion

### 2-DOF Leg Configuration
Each leg has 2 degrees of freedom (DOF):
1. **Hip joint**: Rotates in sagittal plane (forward/backward)
2. **Knee joint**: Rotates in sagittal plane (extension/flexion)

## Mathematical Foundation

### Coordinate System
- **Origin**: At the hip joint
- **X-axis**: Positive forward (robot's front)
- **Y-axis**: Positive upward, negative downward (toward ground)
- **Units**: Centimeters (cm)

### IK Solution Method

The script uses the **geometric method** (law of cosines) for 2-DOF planar IK:

#### Step 1: Check Reachability
The target must be within the workspace:
```
min_reach < distance < max_reach
where:
  min_reach = |L1 - L2|
  max_reach = L1 + L2
  distance = sqrt(x² + y²)
```

#### Step 2: Calculate Knee Angle
Using the law of cosines:
```
cos(θ_knee) = (L1² + L2² - distance²) / (2 × L1 × L2)
θ_knee = acos(cos(θ_knee))
```

#### Step 3: Calculate Hip Angle
```
α = atan2(-y, x)  # Angle to target
β = asin((L2 × sin(θ_knee)) / distance)  # Law of sines
θ_hip = α - β
```

### Joint Limits
Physical constraints prevent joints from rotating freely:
- **Hip**: -90° to +90° (from vertical)
- **Knee**: 0° to 180° (0° = fully bent backward, 180° = straight)

## File Structure

```
03_Code/
├── rto_reverse_kinematics.py   # Main kinematics solver
├── robot_config.ini             # Robot parameters
├── example_usage.py             # Usage examples
└── RTO_Documentation.md         # This file
```

## Usage Guide

### Basic Usage

```python
from rto_reverse_kinematics import RTOKinematics

# Initialize solver with default configuration
rto = RTOKinematics()

# Calculate joint angles for a target position
x, y = 6.0, -12.0  # Target: 6 cm forward, 12 cm down
hip_angle, knee_angle, success = rto.inverse_kinematics_2d(x, y)

if success:
    print(f"Hip: {hip_angle:.2f}°, Knee: {knee_angle:.2f}°")
else:
    print("Target position is not reachable")
```

### Custom Configuration

```python
from rto_reverse_kinematics import RTOKinematics, RobotConfig

# Create custom configuration
config = RobotConfig(
    thigh_length=10.0,
    shin_length=10.0,
    hip_min=-120.0,
    hip_max=120.0
)

rto = RTOKinematics(config=config)
```

### Trajectory Planning

```python
# Generate linear trajectory between two points
start = (0.0, -14.0)
end = (6.0, -10.0)
trajectory = rto.calculate_trajectory(start, end, num_steps=10)

for x, y, hip, knee, valid in trajectory:
    if valid:
        # Send joint commands to servos
        control_servo(hip, knee)
```

### Servo Control Integration

```python
# Convert angles to PWM values for PCA9685
hip_pwm = rto.angle_to_pwm(hip_angle + 90)  # +90 for servo zero offset
knee_pwm = rto.angle_to_pwm(knee_angle)

# Send to PCA9685 (requires Adafruit_PCA9685 library)
# pwm.set_pwm(channel, 0, pwm_value)
```

## Class Reference

### `RobotConfig` (dataclass)
Configuration parameters for the robot.

**Attributes:**
- `thigh_length` (float): Thigh segment length in cm
- `shin_length` (float): Shin segment length in cm
- `foot_offset` (float): Foot length offset in cm
- `hip_min/max` (float): Hip joint angle limits in degrees
- `knee_min/max` (float): Knee joint angle limits in degrees
- `servo_min/max_pulse` (int): PWM pulse width limits
- `servo_frequency` (int): PWM frequency in Hz

### `RTOKinematics` Class

#### `__init__(config: Optional[RobotConfig] = None)`
Initialize the kinematics solver.

#### `inverse_kinematics_2d(x: float, y: float, leg: str = "right") -> Tuple[float, float, bool]`
Calculate inverse kinematics for a target position.

**Parameters:**
- `x`: Target x-coordinate (cm)
- `y`: Target y-coordinate (cm)
- `leg`: Which leg ("left" or "right")

**Returns:**
- `hip_angle`: Hip joint angle (degrees)
- `knee_angle`: Knee joint angle (degrees)
- `success`: True if solution is valid

#### `forward_kinematics_2d(hip_angle: float, knee_angle: float) -> Tuple[float, float]`
Calculate forward kinematics for verification.

**Parameters:**
- `hip_angle`: Hip joint angle (degrees)
- `knee_angle`: Knee joint angle (degrees)

**Returns:**
- `x`: Foot x-coordinate (cm)
- `y`: Foot y-coordinate (cm)

#### `angle_to_pwm(angle: float) -> int`
Convert servo angle to PWM pulse width.

**Parameters:**
- `angle`: Angle in degrees (0-180)

**Returns:**
- PWM pulse width value for PCA9685

#### `calculate_trajectory(start_pos, end_pos, num_steps=10) -> list`
Calculate linear trajectory between positions.

**Parameters:**
- `start_pos`: Starting (x, y) tuple
- `end_pos`: Ending (x, y) tuple
- `num_steps`: Number of interpolation steps

**Returns:**
- List of (x, y, hip, knee, valid) tuples

## Examples

See `example_usage.py` for complete working examples:

1. **Standing Pose**: Basic standing position calculation
2. **Step Trajectory**: Generate a walking step motion
3. **Circular Motion**: Create circular foot trajectory
4. **Workspace Mapping**: Visualize reachable positions
5. **Custom Configuration**: Use different robot dimensions

### Running Examples

```bash
cd 03_Code
python3 example_usage.py
```

Or run the main kinematics script:

```bash
python3 rto_reverse_kinematics.py
```

## Integration with ESP32

To use this on the ESP32:

1. **Option 1**: Use MicroPython
   - Port the Python script to MicroPython
   - Run directly on ESP32

2. **Option 2**: Convert to C++
   - Translate the mathematical formulas to C++/Arduino
   - Compile and upload to ESP32

3. **Option 3**: Host on Raspberry Pi
   - Run Python script on Raspberry Pi
   - Send servo commands to ESP32 via serial/WiFi

### Example C++ Integration Pseudocode

```cpp
float calculate_knee_angle(float x, float y, float L1, float L2) {
    float distance = sqrt(x*x + y*y);
    float cos_knee = (L1*L1 + L2*L2 - distance*distance) / (2*L1*L2);
    cos_knee = constrain(cos_knee, -1.0, 1.0);
    return acos(cos_knee) * 180.0 / PI;
}

void move_foot_to(float x, float y) {
    float hip = calculate_hip_angle(x, y);
    float knee = calculate_knee_angle(x, y);
    
    servo_hip.write(hip + 90);
    servo_knee.write(knee);
}
```

## Workspace Characteristics

### Default Configuration (8cm + 8cm links)
- **Minimum reach**: 0.5 cm (fully bent)
- **Maximum reach**: 16.0 cm (fully extended)
- **Optimal range**: 10-14 cm (best joint angles)

### Standing Height
With legs extended straight down:
- Maximum: ~16 cm (unstable)
- Recommended: ~14 cm (slightly bent for stability)
- Minimum: ~4 cm (fully crouched)

## Gait Planning Considerations

### Walking Gait Parameters
- **Step length**: 6 cm (configurable)
- **Step height**: 4 cm (foot lift during swing)
- **Cycle time**: 2 seconds per complete step
- **Stance width**: 6 cm (hip separation)

### Trajectory Phases
1. **Lift**: Raise foot from ground
2. **Swing**: Move foot forward/backward
3. **Place**: Lower foot to ground
4. **Push**: Support body weight and propel forward

## Troubleshooting

### Position Not Reachable
**Symptom**: Function returns `success=False`

**Solutions**:
- Check if target is within min/max reach
- Verify x, y coordinates are reasonable
- Consider adjusting link lengths in config

### Joint Limits Exceeded
**Symptom**: Warning about joint limits

**Solutions**:
- Adjust target position closer to robot
- Modify joint limit parameters if physically safe
- Use trajectory planning to avoid extreme positions

### Servo Not Moving
**Symptom**: PWM values calculated but servo doesn't respond

**Solutions**:
- Verify PCA9685 connections and I2C address
- Check servo power supply (7.4V LiPo)
- Confirm PWM pulse width range matches servo specs
- Test servos individually with known good values

### Inaccurate Positioning
**Symptom**: Robot foot doesn't reach intended position

**Solutions**:
- Measure actual link lengths accurately
- Update `thigh_length` and `shin_length` in config
- Verify servo mounting angles
- Calibrate servo zero positions

## Performance Considerations

- **Computation time**: < 1ms per IK calculation on modern CPU
- **Update rate**: 50 Hz recommended for smooth motion
- **Trajectory resolution**: 10-20 steps per motion segment
- **Memory usage**: Minimal (~2KB for class instance)

## Future Enhancements

Potential improvements for future versions:

1. **3D Kinematics**: Add hip abduction/adduction (roll) joint
2. **Dynamics**: Include velocity and acceleration constraints
3. **Balance Control**: Integrate IMU feedback for stability
4. **Gait Library**: Pre-programmed walking patterns
5. **Obstacle Avoidance**: Adaptive foot placement
6. **Energy Optimization**: Minimize servo power consumption

## References

- Inverse Kinematics: https://en.wikipedia.org/wiki/Inverse_kinematics
- Bipedal Locomotion: MIT Leg Laboratory research
- Servo Control: PCA9685 datasheet
- Robot Kinematics: "Introduction to Robotics" by John J. Craig

## License

MIT License - See LICENSE file in repository root

## Support

For questions or issues:
- Check this documentation first
- Review example_usage.py for working code
- Test with smaller, safer movements first
- Verify hardware connections before running

---

**Project Eragon** - Because even short robots can be mighty!
