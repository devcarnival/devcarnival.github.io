---
title: "Whisper Shield: Offline-First AI Personal Safety Platform"
date: 2026-11-06T10:15:00+05:30
draft: false
summary: "An offline-first AI personal safety platform triggered by secret voice keywords, gestures, or SOS buttons to capture encrypted audio and broadcast GPS alerts without internet."
demo_url: "https://drive.google.com/file/d/1nlBOh3foBmkJ-bT1bTsHSDpOaSExrP4p/view?usp=drivesdk"
project_type: "Student Innovation"
booth_number: "TP-07"
institution: "Kristu Jayanti University"
participant_type: "Students"

business_domains:
  - "Government"
  - "Public Safety"

tech_domains:
  - "AI"
  - "Mobile Systems"

tags:
  - "Women Safety"
  - "Personal Safety"
  - "AI"
  - "Offline-First"
  - "Flutter"
  - "Node.js"
  - "Government Tech"
  - "Emergency SOS"
  - "GPS Tracking"
  - "Voice Activation"

participants:
  - name: "Shristi Singh"
    role: "Student Innovator"
    email: "26bcac27@kristujayanti.com"
    linkedin: "https://www.linkedin.com/in/shri-singh-0414b0426"
    github: "https://github.com/SHRI-26-arc"
  - name: "V Harshini"
    role: "Student Innovator"
    email: "26bcac32@kristujayanti.com"
    linkedin: "https://www.linkedin.com/in/harshini-venkatesh-b07410448"
    github: "https://github.com/26bcac32-crypto"
---

## Overview

Over 80% of standard emergency SOS applications fail when the victim’s phone is locked, cellular internet coverage is lost, or when an attacker prevents direct access to the handset screen.

**Whisper Shield** is an offline-first, discreet personal safety ecosystem engineered to function reliably in adverse, high-stress environments. Developed for campus security, enterprise personnel protection, and municipal safety initiatives, the application guarantees emergency activation without cellular internet connectivity, contributing directly to **SDG 5 (Gender Equality)**, **SDG 11 (Sustainable Cities and Communities)**, and **SDG 16 (Peace, Justice, and Strong Institutions)**.

### Multi-Modal Trigger & Offline Defense Mechanisms

- **Secret Acoustic Keyword Wakeup:** Low-power acoustic inference scans audio every 30 seconds for the secret keyword phrase *"Whisper Shield"* across multiple regional accents and languages, bypassing device lock states.
- **Physical Shake Gesture Detection:** Continuous accelerometer telemetry detects calibrated dual-shake motions to trigger discreet emergency protocols while keeping the phone concealed in a bag or pocket.
- **Manual Hardware & UI Override:** Dedicated SOS activation button featuring a 5-second cancel buffer to prevent false alarms.
- **Hybrid Vault Evidence Recording:** Captures high-accuracy GPS coordinates, timestamps, and encrypted ambient audio evidence stored securely in a tamper-resistant local vault.
- **Zero-Network Alert Transmission:** Dispatches encrypted SMS emergency telemetry and offline Google Maps location vectors to designated guardians and emergency responders without requiring mobile data.

### Architecture & Technology Stack

- **Frontend Mobile App:** Flutter and Dart cross-platform mobile client featuring native background services and low-power hardware sensor listeners.
- **Backend Infrastructure:** Node.js with Socket.io for real-time dispatch synchronizations when network connectivity is re-established.
- **Audio Processing & AI:** On-device acoustic keyword spotting with roadmap models for vocal distress emotion detection and scream anomaly classification.
- **Security & Storage:** AES-256 encrypted local data vault protecting audio recordings and telemetric evidence against unauthorized extraction.
- **Integration Protocols:** Telephony SMS API relays and WebSockets for low-latency emergency dispatch synchronization.
