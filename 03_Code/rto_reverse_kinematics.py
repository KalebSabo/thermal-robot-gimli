#!/usr/bin/env python3
"""
RTO Reverse Kinematics Script for Project Eragon
Real-Time Operations (RTO) - Inverse Kinematics Solver for Bipedal Robot

This script provides inverse kinematics calculations for Eragon's bipedal legs.
It calculates the required joint angles (servo positions) to achieve a desired
end-effector (foot) position in 2D space.

Hardware Configuration:
- 4 MG996R Metal-Gear Digital Servos
- 2 servos per leg (hip and knee joints)
- ESP32 microcontroller
- PCA9685 PWM driver for servo control

Author: Project Eragon Team
License: MIT
"""

import math
from typing import Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class RobotConfig:
    """Configuration parameters for Eragon bipedal robot"""
    # Link lengths (in cm) - adjust based on actual robot dimensions
    thigh_length: float = 8.0      # Length of thigh segment
    shin_length: float = 8.0       # Length of shin segment
    foot_offset: float = 2.0       # Foot length offset
    
    # Joint angle limits (in degrees)
    hip_min: float = -90.0         # Minimum hip angle
    hip_max: float = 90.0          # Maximum hip angle
    knee_min: float = 0.0          # Minimum knee angle
    knee_max: float = 180.0        # Maximum knee angle
    
    # Servo PWM configuration (for PCA9685)
    servo_min_pulse: int = 150     # Minimum pulse length (0 degrees)
    servo_max_pulse: int = 600     # Maximum pulse length (180 degrees)
    servo_frequency: int = 50      # PWM frequency in Hz


class RTOKinematics:
    """
    Real-Time Operations Kinematics Solver
    Implements inverse kinematics for a 2-DOF planar leg
    """
    
    def __init__(self, config: Optional[RobotConfig] = None):
        """
        Initialize the RTO kinematics solver
        
        Args:
            config: Robot configuration parameters. Uses default if None.
        """
        self.config = config if config else RobotConfig()
        
    def inverse_kinematics_2d(self, x: float, y: float, 
                              leg: str = "right") -> Tuple[float, float, bool]:
        """
        Calculate inverse kinematics for a 2-DOF leg in 2D plane
        
        Uses geometric/analytic method for planar 2-link manipulator.
        Convention: 
        - Hip angle: angle of thigh from horizontal (positive = counterclockwise)
        - Knee angle: interior angle at knee joint (180° = straight, 0° = fully bent)
        
        Args:
            x: Target x-coordinate (forward/backward) in cm
            y: Target y-coordinate (up/down) in cm, negative is down
            leg: Which leg ("left" or "right")
            
        Returns:
            Tuple of (hip_angle, knee_angle, success)
            - hip_angle: Hip joint angle in degrees
            - knee_angle: Knee joint angle in degrees  
            - success: Boolean indicating if solution is valid
        """
        # Get link lengths
        L1 = self.config.thigh_length
        L2 = self.config.shin_length
        
        # Calculate distance to target
        distance = math.sqrt(x**2 + y**2)
        
        # Check if target is reachable
        if distance > (L1 + L2) or distance < abs(L1 - L2):
            print(f"Warning: Target ({x}, {y}) is out of reach!")
            print(f"Reachable range: {abs(L1 - L2):.2f} to {L1 + L2:.2f} cm")
            return (0.0, 0.0, False)
        
        # Calculate knee angle using law of cosines
        # cos(knee_angle) = (L1^2 + L2^2 - distance^2) / (2 * L1 * L2)
        # This gives the interior angle at the knee
        cos_knee = (L1**2 + L2**2 - distance**2) / (2 * L1 * L2)
        
        # Clamp to valid range to avoid numerical errors
        cos_knee = max(-1.0, min(1.0, cos_knee))
        
        # Knee angle (interior angle)
        knee_angle = math.degrees(math.acos(cos_knee))
        
        # Calculate hip angle using law of cosines for the angle at the hip
        # First, find the angle from horizontal to the target
        # Using standard atan2(y, x) where y-axis is positive up, negative down
        angle_to_target = math.atan2(y, x)
        
        # Then find the angle correction using law of cosines
        # cos(angle_correction) = (L1^2 + distance^2 - L2^2) / (2 * L1 * distance)
        cos_correction = (L1**2 + distance**2 - L2**2) / (2 * L1 * distance)
        cos_correction = max(-1.0, min(1.0, cos_correction))
        angle_correction = math.acos(cos_correction)
        
        # Hip angle is angle to target plus correction
        # (correction accounts for the bent knee)
        hip_angle = math.degrees(angle_to_target + angle_correction)
        
        # Validate joint limits
        hip_valid = self.config.hip_min <= hip_angle <= self.config.hip_max
        knee_valid = self.config.knee_min <= knee_angle <= self.config.knee_max
        
        if not (hip_valid and knee_valid):
            print(f"Warning: Joint limits exceeded!")
            if not hip_valid:
                print(f"  Hip angle {hip_angle:.2f}° out of range "
                      f"[{self.config.hip_min}, {self.config.hip_max}]")
            if not knee_valid:
                print(f"  Knee angle {knee_angle:.2f}° out of range "
                      f"[{self.config.knee_min}, {self.config.knee_max}]")
            return (hip_angle, knee_angle, False)
        
        return (hip_angle, knee_angle, True)
    
    def forward_kinematics_2d(self, hip_angle: float, knee_angle: float) -> Tuple[float, float]:
        """
        Calculate forward kinematics for verification
        
        Args:
            hip_angle: Hip joint angle in degrees (angle from horizontal, positive = CCW)
            knee_angle: Knee joint angle in degrees (interior angle at knee, 180° = straight)
            
        Returns:
            Tuple of (x, y) coordinates in cm
        """
        L1 = self.config.thigh_length
        L2 = self.config.shin_length
        
        # Convert to radians
        hip_rad = math.radians(hip_angle)
        knee_rad = math.radians(knee_angle)
        
        # Calculate knee position (end of thigh)
        knee_x = L1 * math.cos(hip_rad)
        knee_y = L1 * math.sin(hip_rad)
        
        # Calculate shin angle
        # Interior knee angle of 180° means shin continues in same direction as thigh
        # Interior knee angle of 90° means shin is perpendicular
        shin_angle = hip_rad - (math.pi - knee_rad)
        
        # Calculate foot position
        x = knee_x + L2 * math.cos(shin_angle)
        y = knee_y + L2 * math.sin(shin_angle)
        
        return (x, y)
    
    def angle_to_pwm(self, angle: float) -> int:
        """
        Convert servo angle to PWM pulse width
        
        Args:
            angle: Angle in degrees (0-180)
            
        Returns:
            PWM pulse width value for PCA9685
        """
        # Clamp angle to valid range
        angle = max(0, min(180, angle))
        
        # Linear interpolation between min and max pulse
        pulse_range = self.config.servo_max_pulse - self.config.servo_min_pulse
        pwm = self.config.servo_min_pulse + (angle / 180.0) * pulse_range
        
        return int(pwm)
    
    def calculate_trajectory(self, start_pos: Tuple[float, float], 
                           end_pos: Tuple[float, float], 
                           num_steps: int = 10) -> list:
        """
        Calculate a linear trajectory between two positions
        
        Args:
            start_pos: Starting (x, y) position in cm
            end_pos: Ending (x, y) position in cm
            num_steps: Number of interpolation steps
            
        Returns:
            List of (x, y, hip_angle, knee_angle, valid) tuples
        """
        trajectory = []
        
        for i in range(num_steps + 1):
            t = i / num_steps
            x = start_pos[0] + t * (end_pos[0] - start_pos[0])
            y = start_pos[1] + t * (end_pos[1] - start_pos[1])
            
            hip, knee, valid = self.inverse_kinematics_2d(x, y)
            trajectory.append((x, y, hip, knee, valid))
        
        return trajectory


def print_banner():
    """Print RTO script banner"""
    print("=" * 60)
    print("  RTO Reverse Kinematics - Project Eragon")
    print("  Real-Time Operations Inverse Kinematics Solver")
    print("=" * 60)
    print()


def main():
    """Main demonstration function"""
    print_banner()
    
    # Initialize kinematics solver with default configuration
    rto = RTOKinematics()
    
    print("Robot Configuration:")
    print(f"  Thigh length: {rto.config.thigh_length} cm")
    print(f"  Shin length: {rto.config.shin_length} cm")
    print(f"  Workspace: {abs(rto.config.thigh_length - rto.config.shin_length):.1f} "
          f"to {rto.config.thigh_length + rto.config.shin_length:.1f} cm")
    print()
    
    # Example 1: Standing position
    print("Example 1: Standing Position")
    print("-" * 60)
    x, y = 0.0, -14.0  # Straight down, legs extended
    hip, knee, success = rto.inverse_kinematics_2d(x, y)
    
    if success:
        print(f"Target: ({x:.2f}, {y:.2f}) cm")
        print(f"Hip angle: {hip:.2f}°")
        print(f"Knee angle: {knee:.2f}°")
        print(f"Hip PWM: {rto.angle_to_pwm(hip + 90)}")  # +90 for servo offset
        print(f"Knee PWM: {rto.angle_to_pwm(knee)}")
        
        # Verify with forward kinematics
        check_x, check_y = rto.forward_kinematics_2d(hip, knee)
        print(f"Verification: ({check_x:.2f}, {check_y:.2f}) cm")
        print(f"Error: {math.sqrt((x - check_x)**2 + (y - check_y)**2):.4f} cm")
    print()
    
    # Example 2: Forward step
    print("Example 2: Forward Step Position")
    print("-" * 60)
    x, y = 6.0, -12.0  # Forward and slightly up
    hip, knee, success = rto.inverse_kinematics_2d(x, y)
    
    if success:
        print(f"Target: ({x:.2f}, {y:.2f}) cm")
        print(f"Hip angle: {hip:.2f}°")
        print(f"Knee angle: {knee:.2f}°")
        print(f"Hip PWM: {rto.angle_to_pwm(hip + 90)}")
        print(f"Knee PWM: {rto.angle_to_pwm(knee)}")
    print()
    
    # Example 3: Trajectory planning
    print("Example 3: Linear Trajectory")
    print("-" * 60)
    start = (0.0, -14.0)
    end = (6.0, -10.0)
    trajectory = rto.calculate_trajectory(start, end, num_steps=5)
    
    print(f"Trajectory from {start} to {end}:")
    print(f"{'Step':<6} {'X (cm)':<10} {'Y (cm)':<10} {'Hip (°)':<10} {'Knee (°)':<10} {'Valid':<6}")
    print("-" * 60)
    
    for i, (x, y, hip, knee, valid) in enumerate(trajectory):
        status = "✓" if valid else "✗"
        print(f"{i:<6} {x:<10.2f} {y:<10.2f} {hip:<10.2f} {knee:<10.2f} {status:<6}")
    print()
    
    # Example 4: Workspace visualization data
    print("Example 4: Workspace Boundary Points")
    print("-" * 60)
    print("Testing reachability at different positions:")
    
    test_points = [
        (0, -16),    # Maximum reach down
        (8, -12),    # Forward diagonal
        (0, -4),     # Minimum reach (bent)
        (10, -10),   # Near edge
        (0, -20),    # Out of reach
    ]
    
    for x, y in test_points:
        hip, knee, success = rto.inverse_kinematics_2d(x, y)
        status = "✓ Reachable" if success else "✗ Out of reach"
        print(f"  ({x:>4.1f}, {y:>5.1f}) cm: {status}")
    print()
    
    print("=" * 60)
    print("RTO Kinematics solver ready for integration!")
    print("Import this module to use in your robot control code.")
    print("=" * 60)


if __name__ == "__main__":
    main()
