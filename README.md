# Project Gimli

**A compact, mostly 3D-printed bipedal walking robot (~30 cm tall / 1 ft)** built as a hands-on robotics learning project.

Gimli is a small-scale biped designed to teach servo control, basic gait generation, balance feedback with IMU, and real-world mechanical/electrical integration — all while keeping the build affordable, beginner-friendly, and expandable.

## Features
- 4 degrees of freedom (hip + knee per leg) using MG996R metal-gear digital servos
- Controlled via Arduino Uno + PCA9685 16-channel PWM driver
- MPU6050 6-axis IMU for future tilt/balance feedback
- Powered by a compact 7.4V 1200mAh 2S LiPo with PH2.0 connector and inline switch
- Mostly 3D-printed structure (PLA prototypes, PETG for durability)
- Open-loop sequenced walking (weight shift → step cycle) as starting point
- Designed for easy expansion: add ankles, more DoF, ESP32 upgrade, dynamic gaits

## 3D Printing
- First prints: servo mounting clamps (verify fit with actual MG996R)
- Planned design: simple 4-servo static walker 
- Material: PLA for prototypes, PETG for final
- Settings: 0.2 mm layer height, 30–40% infill, 4–5 perimeters

## Software
- Arduino IDE & C++
- Libraries: Adafruit_PWMServoDriver, Wire (I2C), MPU6050 (future)
- Initial code: open-loop sequenced poses → weight shift → step cycle
- Future goals: add IMU tilt correction, smooth interpolation, basic turning

## License
MIT License — feel free to fork, modify, and build your own version!

Stay tuned — updates coming soon!

---
Project Gimli – because even short robots can be mighty.