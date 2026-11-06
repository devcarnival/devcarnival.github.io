---
title: "Rakshak-AI: Autonomous Road-Accident Detection and Emergency Triage Platform"
date: 2026-11-06T10:00:00+05:30
draft: false
summary: "A pan-India, edge-powered ecosystem that autonomously detects severe road accidents using smartphone telemetry, dispatching GPS coords to ambulances and activating traffic preemption."
demo_url: "https://drive.google.com/file/d/1oQV7xgLip5IBGfmeP-dw7vEsNE57Zv8H/view?usp=drivesdk"
project_type: "Student Innovation"
booth_number: "TP-04"
institution: "Kristu Jayanti University"
participant_type: "Students"

business_domains:
  - "Government"
  - "Public Safety"

tech_domains:
  - "AI"
  - "Mobile Systems"

tags:
  - "AI"
  - "HealthTech"
  - "Emergency Services"
  - "Crash Detection"
  - "Public Safety"
  - "Smart Mobility"
  - "Telematics"
  - "Flutter"
  - "Kotlin"
  - "PostGIS"
  - "Redis"
  - "WebSockets"
  - "Socket.io"
  - "TensorFlow Lite"
  - "GovTech"

participants:
  - name: "Stevin Joseph B"
    role: "Student Innovator"
    email: "stevinjoseph2003@gmail.com"
    linkedin: "https://www.linkedin.com/in/itsmestevinjosephb"
    github: "https://github.com/StevinJoseph22"
  - name: "Tania T M"
    role: "Student Innovator"
    email: "taniatm99@gmail.com"
    linkedin: "https://www.linkedin.com/in/taniatm99"
    github: "https://github.com/Tania-T-M"
---

## Overview

India faces severe casualties and loss of life during road incidents due to delayed emergency responses and missed "Golden Hours" caused by urban gridlock and bystander reliance. 

**Rakshak-AI** is a pan-India, edge-powered accident detection and emergency triage platform designed to address these bottlenecks. By eliminating human reporting delays, Rakshak-AI dynamically engineers rescue routes, coordinates emergency services, and works to reduce nationwide traffic mortalities, directly aligning with **SDG 3 (Good Health and Well-Being)** and **SDG 9 (Industry, Innovation, and Infrastructure)**.

### Edge Telemetry & Intelligent Triage

The system operates directly on mobile edge devices using real-time sensor processing:
- **Autonomous Crash Detection:** Samples smartphone IMU telemetry at 50Hz, processing accelerometer and gyroscope vectors through an edge-optimized TensorFlow Lite model trained to distinguish actual high-impact collisions from potholes and sudden stops.
- **Instant Dispatch & Geolocation:** Automatically captures and streams precise GPS coordinates to the nearest emergency dispatch center and active ambulance fleet.
- **C-V2X "Green Wave" Preemption:** Interfaces with smart traffic management systems to orchestrate green corridors for approaching emergency vehicles.
- **Trauma Center Triage Integration:** Pre-alerts receiving trauma centers with ABHA-linked patient vitals and incoming injury telemetry to prepare critical care units before arrival.
- **Privacy & Compliance:** Adheres to DPDP standards with zero persistent storage of non-incident telemetry.

### Architecture & Technology Stack

- **Mobile Client:** Flutter and native Kotlin modules for low-power background telemetry processing, hardware sensor listener relays, and lock-screen override.
- **Edge AI:** TensorFlow Lite neural model evaluating IMU telemetry windows at 50Hz for immediate crash classification.
- **Backend & Ingestion:** Node.js backend with Socket.io and WebSockets for low-latency dispatch streaming and real-time fleet synchronization.
- **Spatial Data & Caching:** Redis for fast real-time coordinate caching and spatial queuing, paired with PostgreSQL/PostGIS for geographic radius search and route analysis.
- **Emergency Protocols:** C-V2X protocol emulation for signal preemption and webhook integrations with trauma medical portals.
