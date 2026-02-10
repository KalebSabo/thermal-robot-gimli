#!/usr/bin/env python3
"""
Example Usage Script for RTO Reverse Kinematics

This script demonstrates how to use the RTO kinematics solver
for practical robot control applications.
"""

from rto_reverse_kinematics import RTOKinematics, RobotConfig
import math


def example_standing_pose():
    """Example: Calculate joint angles for standing pose"""
    print("\n" + "="*60)
    print("Example 1: Standing Pose")
    print("="*60)
    
    rto = RTOKinematics()
    
    # Standing with legs extended straight down
    x, y = 0.0, -14.0  # 14 cm down (thigh + shin = 16 cm, slightly bent)
    
    hip_angle, knee_angle, success = rto.inverse_kinematics_2d(x, y)
    
    if success:
        print(f"\nTarget foot position: ({x}, {y}) cm")
        print(f"Required joint angles:")
        print(f"  Hip:  {hip_angle:.2f}°")
        print(f"  Knee: {knee_angle:.2f}°")
        print(f"\nServo PWM values:")
        print(f"  Hip:  {rto.angle_to_pwm(hip_angle + 90)} (pulse width)")
        print(f"  Knee: {rto.angle_to_pwm(knee_angle)} (pulse width)")
    else:
        print("Position not reachable!")


def example_step_trajectory():
    """Example: Generate a stepping motion trajectory"""
    print("\n" + "="*60)
    print("Example 2: Stepping Motion Trajectory")
    print("="*60)
    
    rto = RTOKinematics()
    
    # Define step motion: lift, forward, down
    # Start position: on ground, center
    start_pos = (0.0, -14.0)
    
    # Lift position: same x, lifted up
    lift_pos = (0.0, -10.0)
    
    # Forward position: moved forward, still up
    forward_pos = (6.0, -10.0)
    
    # End position: forward, back on ground
    end_pos = (6.0, -14.0)
    
    print("\nStep trajectory points:")
    positions = [start_pos, lift_pos, forward_pos, end_pos]
    
    for i, (x, y) in enumerate(positions):
        hip, knee, success = rto.inverse_kinematics_2d(x, y)
        status = "✓" if success else "✗"
        print(f"  Point {i+1}: ({x:>5.1f}, {y:>5.1f}) cm -> "
              f"Hip: {hip:>6.2f}°, Knee: {knee:>6.2f}° {status}")


def example_circular_motion():
    """Example: Generate circular foot trajectory"""
    print("\n" + "="*60)
    print("Example 3: Circular Foot Motion")
    print("="*60)
    
    rto = RTOKinematics()
    
    # Circle parameters
    center_x, center_y = 3.0, -12.0
    radius = 2.0
    num_points = 8
    
    print(f"\nCircular path: center=({center_x}, {center_y}), radius={radius} cm")
    print(f"{'Angle':<10} {'X (cm)':<10} {'Y (cm)':<10} {'Hip (°)':<10} {'Knee (°)':<10} {'Valid':<6}")
    print("-" * 60)
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        hip, knee, success = rto.inverse_kinematics_2d(x, y)
        status = "✓" if success else "✗"
        
        print(f"{math.degrees(angle):<10.1f} {x:<10.2f} {y:<10.2f} "
              f"{hip:<10.2f} {knee:<10.2f} {status:<6}")


def example_workspace_mapping():
    """Example: Map the reachable workspace"""
    print("\n" + "="*60)
    print("Example 4: Workspace Mapping")
    print("="*60)
    
    rto = RTOKinematics()
    
    print("\nScanning workspace (this may take a moment)...")
    
    # Test grid of positions
    x_range = range(-8, 13, 2)
    y_range = range(-18, -2, 2)
    
    reachable = []
    unreachable = []
    
    for x in x_range:
        for y in y_range:
            _, _, success = rto.inverse_kinematics_2d(float(x), float(y))
            if success:
                reachable.append((x, y))
            else:
                unreachable.append((x, y))
    
    print(f"\nWorkspace analysis:")
    print(f"  Total points tested: {len(reachable) + len(unreachable)}")
    print(f"  Reachable points: {len(reachable)}")
    print(f"  Unreachable points: {len(unreachable)}")
    print(f"  Workspace coverage: {100 * len(reachable) / (len(reachable) + len(unreachable)):.1f}%")
    
    # Simple ASCII visualization
    print("\nWorkspace visualization (top view):")
    print("  ✓ = reachable, ✗ = unreachable\n")
    
    for y in sorted(set(p[1] for p in reachable + unreachable), reverse=True):
        line = f"  y={y:>3} |"
        for x in sorted(set(p[0] for p in reachable + unreachable)):
            if (x, y) in reachable:
                line += " ✓"
            else:
                line += " ✗"
        print(line)
    
    x_labels = "       |"
    for x in sorted(set(p[0] for p in reachable + unreachable)):
        x_labels += f"{x:>2}"
    print(x_labels)
    print("        " + "-" * (len(x_labels) - 8))
    print("        x-axis (cm)")


def example_custom_config():
    """Example: Use custom robot configuration"""
    print("\n" + "="*60)
    print("Example 5: Custom Robot Configuration")
    print("="*60)
    
    # Create custom configuration for a different robot size
    custom_config = RobotConfig(
        thigh_length=10.0,  # Longer thigh
        shin_length=10.0,   # Longer shin
        hip_min=-120.0,     # More flexible hip
        hip_max=120.0,
        knee_min=0.0,
        knee_max=180.0
    )
    
    rto = RTOKinematics(config=custom_config)
    
    print(f"\nCustom robot configuration:")
    print(f"  Thigh: {custom_config.thigh_length} cm")
    print(f"  Shin: {custom_config.shin_length} cm")
    print(f"  Max reach: {custom_config.thigh_length + custom_config.shin_length} cm")
    
    # Test with larger workspace
    x, y = 0.0, -18.0
    hip, knee, success = rto.inverse_kinematics_2d(x, y)
    
    if success:
        print(f"\nTesting position ({x}, {y}) cm:")
        print(f"  Hip:  {hip:.2f}°")
        print(f"  Knee: {knee:.2f}°")
        print(f"  Status: Reachable ✓")
    else:
        print(f"\nPosition ({x}, {y}) cm is not reachable with custom config")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  RTO Reverse Kinematics - Usage Examples".center(58) + "║")
    print("║" + "  Project Eragon Bipedal Robot".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    try:
        example_standing_pose()
        example_step_trajectory()
        example_circular_motion()
        example_workspace_mapping()
        example_custom_config()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
