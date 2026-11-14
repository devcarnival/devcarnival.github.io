---
title: "TiltScan 2.5D: Rust-Based Foveated LiDAR Scanning and Height Mapping System"
date: 2026-10-14T09:36:57+05:30
draft: false
summary: "A Rust-based robotics sensing platform that mechanically tilts a 2D LiDAR to generate height-aware 2.5D environmental maps and foveated spatial obstacle representations."
demo_url: "https://drive.google.com/drive/folders/1YJ8ofulcDgaPR5YuR88sdiO2MB4jxeJn?usp=sharing"
github_url: "https://github.com/ATITYARAM/J-Bot-RoVer"
project_type: "Student Innovation"
booth_number: "TP-11"
institution: "Kongu Engineering College"
participant_type: "Students"

business_domains:
  - "Enterprise Infrastructure"

tech_domains:
  - "IoT"
  - "Embedded Systems"

tags:
  - "Rust"
  - "LiDAR"
  - "ROS 2"
  - "Robotics"
  - "2.5D Mapping"
  - "SLAM"
  - "ESP32"
  - "Raspberry Pi"
  - "Autonomous Navigation"
  - "Foveated Perception"

participants:
  - name: "Keerthana R"
    role: "Student Innovator"
    email: "keerthana.rajvanitha@gmail.com"
    linkedin: "https://www.linkedin.com/in/keerthana-rajendran357"
    github: "https://github.com/keerthana2k7"
  - name: "Atitya Ram S"
    role: "Student Innovator"
    email: "atityaramsureshmanickam@gmail.com"
    linkedin: "https://www.linkedin.com/in/atityaram/"
    github: "https://github.com/ATITYARAM"
---

## Overview

Autonomous mobile robots operating in unstructured or indoor environments frequently rely on planar 2D LiDARs for SLAM and obstacle detection. However, standard horizontal 2D laser scans remain blind to obstacles located above or below the single scanning plane—such as table overhangs, ascending stairs, drop-offs, and ground debris—unless expensive, power-heavy 3D multi-beam LiDAR sensors are utilized.

**TiltScan 2.5D** overcomes this limitation by pairing an affordable 2D LiDAR with a precision servo-actuated mechanical tilting mechanism and memory-safe Rust firmware. By coordinating laser sweeps across multiple calibrated elevation angles and synthesizing returns into a unified 3D/2.5D coordinate grid, the system provides full-height obstacle perception at a fraction of the cost and weight of commercial 3D scanning arrays. Aligned with **UN SDG 9 (Industry, Innovation, and Infrastructure)** and **SDG 11 (Sustainable Cities and Communities)**, TiltScan enables safer navigation for robotics research, warehouse AGVs, industrial inspections, and field rovers.

### Multi-Angle Tilt Coordination & 2.5D Perception Engine

- **Servo-Coordinated Tilt Scanning:** A precision servo mechanism tilts the 2D LiDAR across continuous pitch angles, transforming flat 2D range slices into rich 3D spatial slices.
- **Unified 2.5D Elevation Mapping:** Laser measurement pulses across varying tilt orientations are dynamically transformed into a common Cartesian reference frame to construct a height-aware elevation and occupancy map.
- **Foveated Spatial Perception:** Employs foveated spatial sampling algorithms that concentrate high-density angular resolution on critical near-field navigation sectors while relaxing scan density for distant, non-critical background regions to reduce computational overhead.
- **Embedded Real-Time Safety with Rust:** Core actuation and sensor polling routines are authored in native Rust, preventing data races, pointer corruption, and timing jitter during high-speed UART telemetry exchange.
- **ROS 2 SLAM Pipeline:** Formats synchronized point clouds and odometry transforms for seamless consumption by ROS 2 Nav2 stacks and Cartographer SLAM.

### Architecture & Technology Stack

- **Firmware & Core Control:** Pure **Rust** (`esp-hal`, `no_std` bare-metal routines) executing on a **Waveshare ESP32-S3** microcontroller to govern servo pitch trajectories, limit switches, and sensor serial telemetry with deterministic timing.
- **Companion Compute Unit:** **Raspberry Pi 5** handling coordinate frame transformations, point-cloud accumulation, and high-level ROS 2 node communication.
- **Mechanical Platform:** Integrated into the **J-Bot Rover**, an autonomous field robot featuring a rocker-bogie suspension system designed to navigate rugged, uneven ground.
- **Communication & Protocols:** High-speed UART between ESP32 and LiDAR, USB-Serial interface between ESP32 and companion compute, and ROS 2 middleware publishing sensor topics.

### Future Roadmap

The DarcARK team is advancing active IMU-based motion compensation to filter out chassis vibrations while the rover traverses steep terrain, implementing dynamic tilt frequency modulation triggered by robot velocity, and testing the system for industrial pipe inspection and perimeter surveillance.
