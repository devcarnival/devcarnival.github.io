---
title: "Alumnex Connect"
date: 2026-08-01T10:00:00+05:30
draft: false
summary: "A verified, college-exclusive alumni mentorship platform connecting students, alumni, and college administration for mentorship, job referrals, and coding profile tracking."
demo_url: "https://alumnex-connect.onrender.com"
project_type: "Friendly Coders"
booth_number: "TP-02"
community: "Friendly Coders"
institution: "Kongu Engineering College"
participant_type: "Students"

business_domains:
  - "Education"

tech_domains:
  - "Web Systems"

tags:
  - "React"
  - "Node.js"
  - "Express"
  - "Full-Stack Development"
  - "WebSystems"
  - "EdTech"
  - "Alumni Network"
  - "Mentorship"
  - "REST API"
  - "MongoDB"
  - "Community Portal"

participants:
  - name: "Sriman Kumar V"
    role: "Student Innovator"
    email: "srimankumar06@gmail.com"
    linkedin: "https://www.linkedin.com/in/sriman-vel-b89432383/"
    github: "https://github.com/SrimanKumarV"
  - name: "Srimathi D"
    role: "Student Innovator"
    email: "srimathi.dhinakaran2006@gmail.com"
    linkedin: "https://www.linkedin.com/in/srimathidhinakaran/"
    github: "https://github.com/srimathidhinakaran"
---

## Overview

Colleges today lack a centralized, secure platform that connects students with alumni for mentorship, career guidance, internships, job referrals, and coding profile tracking, leaving career opportunities scattered and difficult to access.

**Alumnex Connect** addresses this gap as a verified, college-exclusive alumni mentorship platform that brings students, alumni, and the college administration onto a single ecosystem. Aligned with **SDG 4 (Quality Education)** and contributing to **SDG 8 & SDG 9**, the platform strengthens ties between colleges, alumni, and students.

### Structured Onboarding & Verification

The system follows a structured onboarding and verification flow where users register by role. For alumni, employment proof must be uploaded and approved by the college administrator before access is granted.

Once verified:
- **Students** gain access to Smart Mentor Allocation, a Tech Hub, a Career Board for jobs and referrals, a Projects module to discover teammates, and **DevPulse** to track competitive programming profiles across LeetCode, Codeforces, CodeChef, HackerRank, and GitHub.
- **Alumni** can manage mentees, publish career opportunities, and analyze mentorship engagement through built-in analytics.
- **Shared Features:** Real-time chat & messaging, dynamic notifications, an AI-powered resume builder, gamification badges, learning resources, and an admin moderation panel.

### Architecture & Technology Stack

- **Frontend:** Built with React.js (v18), React Router, Tailwind CSS, and Framer Motion for responsive, role-based interfaces, paired with Lucide React icons and Recharts for data visualization.
- **Backend:** Node.js with Express.js, featuring Socket.io for real-time messaging and notifications, and Multer for secure file uploads.
- **Database:** MongoDB with Mongoose for user, mentorship, and project data persistence.
- **Authentication & Security:** JWT sessions, Google & GitHub OAuth, bcrypt password hashing, dynamic OTP-based two-factor authentication, and CORS with rate limiting.
- **AI & Integrations:** Google Gemini API for AI-assisted mentoring and resume critique, REST/GraphQL scrapers for LeetCode, Codeforces, and CodeChef profiles, and Brevo API for transactional email notifications.
