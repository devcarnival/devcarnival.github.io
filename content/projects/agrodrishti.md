---
title: "AgroDrishti: Turning Satellite Data into Farm Intelligence"
date: 2026-11-06T10:05:00+05:30
draft: false
summary: "Replaces physical field inspections with satellite evidence using Sentinel-2 and Google Earth Engine to rapidly detect and verify crop loss for insurance and relief claims."
demo_url: "https://drive.google.com/file/d/1gmAPeR-oT-z2LwKGeF9nUWtCEmLnFDZq/view?usp=drive_link"
project_type: "Student Innovation"
booth_number: "TP-05"
institution: "Kristu Jayanti University"
participant_type: "Students"

business_domains:
  - "AgriTech"
  - "Insurance"

tech_domains:
  - "Remote Sensing"
  - "AI"

tags:
  - "AgriTech"
  - "Remote Sensing"
  - "Crop Insurance"
  - "Crop Damage Assessment"
  - "NDVI"
  - "Sentinel-2"
  - "Google Earth Engine"
  - "Evidence Certificate"
  - "QR Verification"
  - "Sentinel-1"
  - "Multilingual"

participants:
  - name: "Prajwalitha Bojanam"
    role: "Student Innovator"
    email: "prazuh.7@gmail.com"
    linkedin: "https://www.linkedin.com/in/prajwalitha-bojanam-496081431/"
    github: "https://github.com/prazuh-75"
  - name: "Abhinav Athreya R"
    role: "Student Innovator"
    email: "abhinavathreya6@gmail.com"
    linkedin: "https://www.linkedin.com/in/abhinav-athreya-r-7a3357220"
    github: "https://github.com/SixShooter-glitch"
---

## Overview

Following climate shocks such as floods or severe droughts, smallholder farmers face long delays before crop insurance or relief claims can be processed, as manual field inspections take weeks and vary widely between inspectors.

**AgroDrishti** replaces subjective manual initial visits with objective satellite evidence. By tracking multi-temporal earth observation data, AgroDrishti automates damage assessment to accelerate claim settlements for farmers, aligning with **SDG 1 (No Poverty)**, **SDG 2 (Zero Hunger)**, and **SDG 13 (Climate Action)**.

### Satellite Telemetry & Verification Pipeline

- **Automated Crop Health Monitoring:** Uses free Sentinel-2 multispectral imagery via Google Earth Engine to compute Normalized Difference Vegetation Index (NDVI) values per farm polygon on a weekly basis, benchmarked against multi-year baseline averages.
- **Algorithmic Loss Detection:** Automatically flags an incident when NDVI drops by more than 20% over three consecutive weeks. When losses hit or exceed the statutory 33% crop-loss threshold, the platform auto-generates a verified damage claim.
- **Meteorological Causality Analysis:** Fuses ERA5-Land reanalysis weather data to correlate crop distress with extreme heat, drought, or precipitation anomalies, routing ambiguous cases for targeted on-ground audit.
- **Cryptographic Evidence Certificates:** Compiles an immutable evidence docket for each case featuring time-series NDVI imagery, historical baselines, and a SHA-256 hash verifiable via QR code.
- **Role-Based Applications:** Includes dedicated mobile interfaces for farmers (offering multilingual voice and SMS alerts) and dashboard tools for agricultural officers and insurance adjusters.

### Architecture & Technology Stack

- **Earth Observation & Analytics:** Google Earth Engine (GEE) Python API with ESA Sentinel-2 MSI and Sentinel-1 SAR radar imagery pipelines.
- **Weather Telemetry:** ECMWF ERA5-Land dataset integration for temperature and precipitation anomaly mapping.
- **Backend & Validation:** Python-based microservice architecture managing polygon extraction, NDVI delta computations, and cryptographic SHA-256 evidence generation.
- **Client Applications:** Multilingual Farmer App supporting Kannada, Hindi, and Telugu alongside an administrative portal for claims inspection.
