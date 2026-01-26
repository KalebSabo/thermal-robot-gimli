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

## Hardware (BOM – partial)
| Component                  | Quantity | Notes / Model                              |
|----------------------------|----------|--------------------------------------------|
| Arduino Uno                | 1        | REV3 or compatible                         |
| PCA9685 16-ch PWM driver   | 2        | HiLetgo, I2C control                       |
| MG996R metal-gear servos   | 4        | Deegoo, ~10–13 kg·cm                       |
| MPU6050 IMU module         | 1–3      | HiLetgo GY-521                             |
| 7.4V 1200mAh 2S LiPo       | 1        | VICMILE SCX24 style, PH2.0 connector       |
| XL4015 5A buck converters  | 2        | HiLetgo, adjustable (5V & 6V rails)        |
| 2200µF 25V Rubycon caps    | 2+       | Low-ESR, on each buck output               |
| M3 heat-set brass inserts  | 100+     | HANGLIFE, for strong printed joints        |
| 25T aluminum servo horns   | 4        | Acekeeps                                   |
| 5mm M3 ball heads          | 10       | Tamiya DF-02                               |
| M3 screw/nut assortment    | ~2200 pcs| Fgruh / similar                            |
| Bondhus ball-end hex keys  | 9-pc set | Sizes 1.5–10 mm                            |
| Pinecil smart soldering iron | 1      | For heat-set inserts                       |
| Quicko M2–M8 insert tips   | 1 set    | For Pinecil                                |
| Dupont jumper wires        | 120 pcs  | ELEGOO multicolored                        |
| PH2.0 on/off switch        | 1        | Adafruit JST PH2.0 extension with switch   |
| 45W USB-C PD charger       | 1        | Anker Nano                                 |

## 3D Printing
- First prints: servo mounting clamps (verify fit with actual MG996R)
- Planned design: simple 4-servo static walker 
- Material: PLA for prototypes, PETG for final
- Settings: 0.2 mm layer height, 30–40% infill, 4–5 perimeters

## Software
- Arduino IDE + C++
- Libraries: Adafruit_PWMServoDriver, Wire (I2C), MPU6050 (future)
- Initial code: open-loop sequenced poses → weight shift → step cycle
- Future goals: add IMU tilt correction, smooth interpolation, basic turning

## License
MIT License — feel free to fork, modify, and build your own version!

## Next Milestones
1. Parts arrival & unboxing photos
2. First servo centering & pulse range test
3. Breadboard wiring & single-leg movement test
4. Print & assemble first leg prototype
5. Full standing pose & weight-shift demo

Stay tuned — updates coming soon!

---
Project Gimli – because even short robots can be mighty.