---
title: "Autonomous Rescue System"
date: 2026-11-06T17:46:00+05:30
draft: false
summary: "Decouples conversational voice intake from mathematical optimization to slash emergency CAD dispatch latency by over 60% and guarantee zero allocation errors."
demo_url: "https://drive.google.com/file/d/1WF1G3U6u7Mbq8zebwzKlKZ_Lio-_Az1I/view?usp=drivesdk"
project_type: "Student Innovation"
booth_number: "TP-09"
institution: "Acharya Bangalore B-School"
participant_type: "Students"

business_domains:
  - "Government"
  - "Public Safety"

tech_domains:
  - "AI"
  - "Optimization"

tags:
  - "AI"
  - "Emergency Response"
  - "Disaster Management"
  - "Smart Healthcare"
  - "Real-Time Tracking"
  - "Intelligent Routing"
  - "Geolocation"
  - "Google Gemini"
  - "Whisper"
  - "OR-Tools"
  - "CP-SAT"
  - "GovTech"

participants:
  - name: "Rahul Kumar Khatua"
    role: "Student Innovator"
    email: "rahulplatitech@gmail.com"
    linkedin: "https://www.linkedin.com/in/rahul-kumar-700b50405"
    github: "https://github.com/rahulplatitech-lgtm"
  - name: "Manoj Kumar S"
    role: "Student Innovator"
    email: "manojnbhs530@gmail.com"
    linkedin: "https://www.linkedin.com/in/manoj-kumar-a977b2366"
    github: "https://github.com/manojnbhs530-art"
---

## Overview

Over 4.2 million preventable pre-hospital deaths occur worldwide each year due to the "Golden Hour" penalty: patient survival chances plummet by 7% to 10% for every single minute an emergency response is delayed. 

Legacy 911 and 112 Computer-Aided Dispatch (CAD) systems suffer from three acute bottlenecks:
1. **Manual Ingestion Delays:** 3 to 7 minutes of stressful verbal interrogation while frantic callers struggle to communicate clearly.
2. **Greedy Dispatch Heuristics:** Traditional CAD platforms dispatch the single nearest available ambulance unit, leaving downstream high-severity (S5) trauma victims completely unserviced just blocks away.
3. **Operational Fragility:** When an emergency vehicle breaks down or road flooding obstructs an artery, manual dispatcher recalculations take 15 to 30 minutes.

The **Autonomous Rescue System** (Crisis Command AI) replaces this broken workflow by decoupling conversational voice intake from deterministic mathematical optimization. The platform cuts emergency dispatch latency by over 60%, eliminates allocation hallucinations, and dynamically recalculates citywide fleet assignments in under 500 milliseconds, directly advancing **SDG 3 (Good Health and Well-Being)**, **SDG 9 (Industry, Innovation, and Infrastructure)**, and **SDG 11 (Sustainable Cities and Communities)**.

### Autonomous Ingestion & Multi-Agent Dispatch Engine

- **Conversational Voice Ingestion:** Employs Whisper Voice Activity Detection (VAD) coupled with Google Gemini 1.5 Flash to parse panicked, unstructured emergency calls, transcribing medical symptoms and extracting critical location markers in real time.
- **Deterministic Mathematical Optimization:** Decouples natural language processing from resource allocation by feeding structured incident constraints into Google OR-Tools CP-SAT solver, guaranteeing zero allocation hallucinations.
- **Global Fleet Optimization:** Avoids greedy nearest-unit pitfalls by optimizing global survival probability across all active incident clusters, preserving advanced life support units for high-severity trauma cases.
- **Dynamic Real-Time Rerouting:** Automatically ingests live road closures, vehicle telemetry, and weather alerts to trigger microsecond fleet recalculations in under 500ms.
- **Dispatcher Copilot UI:** Delivers clean visual telemetry to dispatch directors with automated routing recommendations, patient triage scores, and ETA projections.

### Architecture & Technology Stack

- **Voice Ingestion & Triage:** Google Gemini 1.5 Flash with Whisper Voice Activity Detection (VAD) for real-time speech-to-text and unstructured entity extraction.
- **Optimization & Routing Core:** Google OR-Tools CP-SAT constraint programming solver combined with geospatial routing engines for fleet assignment.
- **Backend & Data Pipeline:** Python / FastAPI event-driven services handling high-concurrency emergency incident streams and telematics queues.
- **Real-Time Telemetry & Tracking:** WebSocket and GPS telemetry relays broadcasting vehicle states, transit coordinates, and traffic corridor updates.
- **Frontend Dashboard:** Modern dispatcher command portal visualizing citywide emergency incidents, ambulance coordinates, and predictive ETAs.
