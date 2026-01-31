# Notes on the Code for Gimli
- This file will contain the notes for developing the codebase to   Gimli.

## Arduino Core
- Primary microcontroller, handles the servo, sensor and locomotion control
    - c++/Python hybrid programming
    - .ino extension

### Python
- Easier but inefficient
- Main programming used in AI 
    - Computer Vision
    - Data Processing
    - UI 

#### Practical Application TBA
- Could implement on a host, where commands are sent from a Raspberry Pi. 

### C++
- Difficult but efficient
- 10-100x faster than Python
    - Look at boolean byte sizes?
