# Node.js Form Application with Google Cloud Storage Integration

## Overview

This project is a Node.js web application that collects user form submissions and stores them as CSV files in a Google Cloud Storage bucket.

The application runs on a Google Compute Engine virtual machine and uses IAM-based authentication for secure communication with Google Cloud services. Each submission creates a uniquely named CSV file to prevent overwriting and to remain compatible with bucket retention policies.

---

## Architecture

Client (Browser)
→ Express Server (Compute Engine VM)
→ Google Cloud Storage
→ CSV file stored in bucket

---

## Technologies Used

- Node.js
- Express.js
- Google Cloud Storage SDK
- Google Compute Engine
- Git and GitHub

---

## Project Structure

node-app/
│
├── index.js
├── package.json
├── package-lock.json
└── public/
    └── form.html

---

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/Carnage08/node-gcp.git
cd node-gcp

### 2. Install Dependencies

npm install

---

## Google Cloud Configuration

### VM Configuration

When creating the Compute Engine VM:

- Go to Identity and API access
- Select:
  Allow full access to all Cloud APIs

This is required to avoid OAuth scope authorization errors.

---

### IAM Role Requirement

Ensure the VM service account has the following role:

Storage Object Admin

You can verify or assign this role from:
IAM & Admin → IAM

---

### Cloud Storage Bucket

Verify bucket existence:

gsutil ls

If needed, update the bucket name inside index.js:

const BUCKET_NAME = "your-bucket-name";

---

## Firewall Configuration

Create an ingress firewall rule:

Direction: Ingress
Action: Allow
Source IP range: 0.0.0.0/0
Protocol: TCP
Port: 3000

---

## Running the Application

Start the server:

node index.js

Access the application:

http://<VM_EXTERNAL_IP>:3000

---

## API Endpoint

POST /submit

Accepts:

- name
- email
- contact
- branch
- position

Each submission generates a file:

gs://<bucket-name>/responses/form_<timestamp>.csv

---

## Troubleshooting

### 403 Provided scope(s) are not authorized

Cause:
VM was created without proper API access scope.

Solution:
Recreate VM with:
Allow full access to all Cloud APIs

---

### 403 Forbidden (Storage)

Cause:
Service account missing Storage Object Admin role.

Solution:
Assign required IAM role.

---

### Port Not Accessible

Cause:
Missing firewall rule.

Solution:
Create ingress rule allowing TCP port 3000.

---

## Key Concepts Demonstrated

- IAM roles vs OAuth scopes
- Secure Cloud Storage integration
- Express async route handling
- Retention-safe file creation
- Cloud firewall configuration

---

## Author

Arjun Yadav
B.Tech Information Technology
Cloud and Backend Development


#dumy
