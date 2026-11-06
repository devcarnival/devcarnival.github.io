---
title: "BioPay: Next-Generation Biometric Contactless Payment Infrastructure"
date: 2026-11-06T10:10:00+05:30
draft: false
summary: "A smartphone-independent biometric payment ecosystem authorizing purchases with multi-modal fingerprint and live face verification against an encrypted prepaid virtual wallet."
demo_url: "https://drive.google.com/file/d/1WyEGMYiY8-TBFks9t8uw9RT16iQmRWnm/view?usp=drive_link"
project_type: "Student Innovation"
booth_number: "TP-06"
institution: "Kristu Jayanti University"
participant_type: "Students"

business_domains:
  - "Banking"
  - "FinTech"

tech_domains:
  - "IoT"
  - "Embedded Systems"

tags:
  - "Biometric Payments"
  - "Fingerprint Authentication"
  - "Face Verification"
  - "FinTech"
  - "IoT"
  - "ESP8266"
  - "Machine Learning"
  - "Fraud Detection"
  - "Cybersecurity"
  - "React Native"
  - "Flask"
  - "Encrypted Database"

participants:
  - name: "A. Benedict Paul"
    role: "Student Innovator"
    email: "26mcac01@kristujayanti.com"
    linkedin: "https://www.linkedin.com/in/benedictpaultech"
    github: "https://github.com/benedictpaul321-del"
  - name: "Mervyn Rithik Shanu A"
    role: "Student Innovator"
    email: "26mcac31@kristujayanti.com"
    linkedin: "https://www.linkedin.com/in/mervyntech"
    github: "https://github.com/MervynRithik"
---

## Overview

Modern digital transaction rails such as UPI and contactless NFC require an active smartphone, mobile battery, and continuous cellular data connectivity. In busy retail settings, rural regions, or among elderly citizens, these dependencies frequently cause checkout friction and payment failures.

**BioPay** introduces an autonomous, smartphone-independent point-of-sale payment architecture. Using multi-modal biometric authentication combining optical fingerprint recognition with real-time facial verification, BioPay allows customers to authorize transactions against a secure prepaid virtual wallet without needing a physical card or mobile device, supporting **SDG 8 (Decent Work and Economic Growth)** and **SDG 9 (Industry, Innovation, and Infrastructure)**.

### Dual-Biometric Authentication & Transaction Flow

- **Dual-Factor Biometrics:** Integrates an optical fingerprint scanner and high-resolution camera relay. The system demands unanimous agreement between fingerprint template matching and facial verification before releasing funds.
- **Microcontroller Edge Terminal:** Built on an ESP8266 microcontroller coordinating the R307 fingerprint sensor module and visual camera capture relay to communicate securely with central payment services.
- **Embedded Machine Learning:** Incorporates computer vision preprocessing to suppress noise from imperfect fingerprint scans and uses a trained scoring model that fuses facial landmarks and minutiae scores into a unified trust metric.
- **Anomaly Detection:** Real-time heuristic and machine learning anomaly detection monitors transaction frequency, velocity, and amounts to prevent fraudulent checkout patterns.
- **Encrypted Local & Remote Stores:** All biometric templates, user identities, and transactions are stored using AES-encrypted databases with strict session revocation and cryptographic tokenization.

### Architecture & Technology Stack

- **Hardware & Microcontroller:** ESP8266 Wi-Fi module paired with an R307 optical fingerprint reader and local camera peripheral.
- **Mobile Application:** React Native (Expo) consumer portal for balance top-ups, transaction ledger auditing, and biometric enrollment.
- **Backend Services:** Python Flask server implementing RESTful endpoints, scanner session authentication, rate limiting, and business validation.
- **Security & Database:** Encrypted SQLite / relational datastore holding salted credential hashes and biometric templates with zero raw image persistence.
- **ML & Computer Vision:** OpenCV for image contrast enhancement, minutiae extraction, and deep face-matching feature extraction.
