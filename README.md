# Node.js Form Application with Google Cloud Storage Integration

## Overview

This project is a Node.js web application that collects user form submissions and stores them as CSV files in a Google Cloud Storage bucket.

The application runs on a Google Compute Engine virtual machine and uses IAM-based authentication for secure communication with Google Cloud services.

Each form submission creates a uniquely named CSV file to prevent overwriting conflicts and to remain compatible with bucket retention policies.

---

# System Architecture

## High-Level Architecture Diagram

+-------------+        HTTP        +-------------------+        Google API        +----------------------+
|             |  POST /submit     |                   |   Upload CSV via SDK    |                      |
|   Browser   | --------------->  |  Express Server   | ----------------------> |  Cloud Storage Bucket|
|             |                   |  (Compute Engine) |                          |                      |
+-------------+                   +-------------------+                          +----------------------+

---

# Application Flow

## Sequence Diagram

User
 |
 | Fill Form
 v
Browser
 |
 | POST /submit
 v
Express Server
 |
 | Validate Data
 |
 | Convert to CSV
 |
 | Upload via GCS SDK
 v
Cloud Storage
 |
 | Store file: responses/form_<timestamp>.csv
 v
Return 200 OK

---

# Data Flow

[ User Input ]
      ↓
[ FormData Object ]
      ↓
[ Express req.body ]
      ↓
[ CSV Formatter ]
      ↓
[ Google Cloud Storage SDK ]
      ↓
[ Bucket → responses/ folder ]

---

# UI Wireframe

+--------------------------------------------------+
|                Get in Touch                      |
|--------------------------------------------------|
| Full Name       [__________________________]     |
|                                                  |
| Email Address   [__________________________]     |
|                                                  |
| Contact Number  [__________________________]     |
|                                                  |
| Branch          [ Select Branch ▼ ]              |
|                                                  |
| Position        [ Select Position ▼ ]            |
|                                                  |
|        [ Submit ]           [ Reset ]            |
+--------------------------------------------------+

---

# Technology Stack

- Node.js
- Express.js
- Google Cloud Storage SDK
- Google Compute Engine
- Git and GitHub

---

# Project Structure

node-app/
│
├── index.js
├── package.json
├── package-lock.json
└── public/
    └── form.html

---

# Installation

## 1. Clone Repository

git clone https://github.com/Carnage08/node-gcp.git
cd node-gcp

## 2. Install Dependencies

npm install

---

# Google Cloud Configuration

## VM Requirements

When creating the Compute Engine VM:

Identity and API access →  
Select:

Allow full access to all Cloud APIs

---

## IAM Role Requirement

Ensure VM service account has:

Storage Object Admin

Location:
IAM & Admin → IAM

---

## Bucket Verification

gsutil ls

If needed, update bucket name in index.js:

const BUCKET_NAME = "your-bucket-name";

---

# Firewall Configuration

Create ingress firewall rule:

Direction: Ingress  
Action: Allow  
Source IP: 0.0.0.0/0  
Protocol: TCP  
Port: 3000  

---

# Running the Application

node index.js

Access application:

http://<VM_EXTERNAL_IP>:3000

---

# API Endpoint

POST /submit

Fields:

- name
- email
- contact
- branch
- position

Each submission generates:

gs://<bucket-name>/responses/form_<timestamp>.csv

---

# Security Model

Compute Engine VM
        ↓ (OAuth Token with Scope)
Google Storage API
        ↓ (IAM Role Validation)
Cloud Storage Bucket

Security Features:

- IAM-based authentication
- No service account key files stored
- Unique timestamp-based file naming
- CSV value sanitization
- Explicit firewall configuration

---

# Troubleshooting

403 Provided scope(s) are not authorized  
Cause: VM created without proper API scope  
Solution: Recreate VM with "Allow full access to all Cloud APIs"

403 Forbidden  
Cause: Missing Storage Object Admin role  
Solution: Assign IAM role

Port 3000 not accessible  
Cause: Missing firewall rule  
Solution: Allow TCP port 3000

---

# Key Learning Outcomes

- IAM roles vs OAuth scopes
- Secure Cloud Storage integration
- Express async route handling
- Retention-safe file creation
- VM firewall and port configuration

---

# Author

Arjun Yadav  
B.Tech Information Technology  
Cloud and Backend Development
