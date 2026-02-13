
Security Highlights:

- IAM-based authentication
- No service account keys stored
- Retention-safe unique filenames
- CSV sanitization
- Explicit firewall rule

---

# Troubleshooting Guide

## 403 Provided scope(s) are not authorized

Cause:
VM created without proper API scope.

Solution:
Recreate VM with:
Allow full access to all Cloud APIs

---

## 403 Forbidden

Cause:
Missing Storage Object Admin role.

Solution:
Assign IAM role to VM service account.

---

## Port 3000 Not Accessible

Cause:
Missing firewall rule.

Solution:
Allow TCP 3000 ingress.

---

# Key Learning Outcomes

- IAM roles vs OAuth scopes
- Cloud-native backend design
- Secure file upload architecture
- Express async route handling
- Debugging 403 authorization errors
- VM firewall and port management

---

# Author

Arjun Yadav  
B.Tech Information Technology  
Cloud and Backend Development
