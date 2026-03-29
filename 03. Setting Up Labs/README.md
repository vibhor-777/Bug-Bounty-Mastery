# 🧪 Module 03: Setting Up Labs

> **Level:** 🟢 Beginner | **Time:** ~2 hours | **Prerequisites:** Module 01-02

---

## 📖 Overview

Before hunting on real targets, you need a safe practice environment. This module walks you through setting up multiple vulnerable-by-design applications so you can practice every technique in this course legally and safely.

---

## ❓ Why It Matters

Practicing on intentionally vulnerable apps is the fastest way to learn. You can break things, try payloads, and understand how vulnerabilities work without legal risk. Every professional security tester has a local lab.

---

## 🌍 Real-World Example

Many top bug bounty hunters start by solving every PortSwigger Academy lab before touching real targets. This builds the muscle memory needed to recognize vulnerable patterns quickly in production applications.

---

## 📋 Step-by-Step Methodology

### Lab Environment Overview

```
Your Machine
    ├── Burp Suite (Proxy & Testing Tool)
    ├── DVWA (Docker or XAMPP)
    ├── OWASP Juice Shop (Docker or Node.js)
    ├── Browser (Firefox with FoxyProxy)
    └── VPN (optional, for TryHackMe/HackTheBox)
```

---

## 🛠️ Tools Used

| Tool | Purpose | Install |
|------|---------|---------|
| **Burp Suite Community** | HTTP proxy and testing | [portswigger.net/burp](https://portswigger.net/burp) |
| **Docker** | Run lab apps in containers | [docker.com](https://docker.com) |
| **DVWA** | Damn Vulnerable Web App | Docker or XAMPP |
| **OWASP Juice Shop** | Modern vulnerable app | Docker or npm |
| **Firefox** | Testing browser | [firefox.com](https://firefox.com) |
| **FoxyProxy** | Proxy switcher extension | Firefox Add-ons |

---

## 💡 Setup Instructions

### 1. Install Burp Suite Community

```bash
# Download from official site
# https://portswigger.net/burp/communitydownload

# On Linux (after download)
chmod +x burpsuite_community_linux_*.sh
./burpsuite_community_linux_*.sh

# Verify Java is installed
java -version
```

### 2. Set Up DVWA with Docker

```bash
# Pull and run DVWA
docker pull vulnerables/web-dvwa

docker run -d \
  --name dvwa \
  -p 80:80 \
  vulnerables/web-dvwa

# Access at: http://localhost/
# Default login: admin / password
```

### 3. Set Up OWASP Juice Shop

```bash
# Method 1: Docker (recommended)
docker pull bkimminich/juice-shop
docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop

# Method 2: Node.js
git clone https://github.com/juice-shop/juice-shop.git
cd juice-shop
npm install
npm start

# Access at: http://localhost:3000
```

### 4. Configure Burp Suite Proxy

```
Burp Suite → Proxy → Options → Add Listener
    Interface: 127.0.0.1
    Port: 8080

Firefox → Settings → Network Settings → Manual proxy
    HTTP Proxy: 127.0.0.1
    Port: 8080
```

### 5. Install Burp CA Certificate

```
1. With Burp running, go to http://burp in Firefox
2. Click "CA Certificate" to download
3. Firefox → Settings → Privacy → Certificates → Import
4. Trust for websites
```

### 6. Set Up FoxyProxy

```
1. Install FoxyProxy extension in Firefox
2. Add proxy: 127.0.0.1:8080 (Burp)
3. Toggle easily between direct and proxied connections
```

---

## 🧪 Lab Verification

### Test DVWA

```
1. Navigate to http://localhost
2. Click "Setup / Reset DB"
3. Login: admin / password
4. Set security to "Low"
5. Explore vulnerabilities menu
```

### Test Juice Shop

```
1. Navigate to http://localhost:3000
2. Register an account
3. Check the Score Board (hidden challenge)
4. Start solving challenges
```

### Test Burp Suite Proxy

```
1. Enable FoxyProxy → Burp profile
2. Browse to http://localhost:3000
3. Intercept should show requests in Burp
4. Forward requests to continue browsing
```

---

## 🛡️ Lab Security Notes

- Run labs on a dedicated VM or isolated network
- Never connect lab machines to production networks
- Use snapshots to easily restore lab state
- Keep Docker images updated for security

---

## 🎯 Recommended Lab Schedule

| Day | Activity |
|-----|---------|
| Day 1 | Install all tools, verify they work |
| Day 2 | Complete DVWA at Low security |
| Day 3-5 | PortSwigger Academy beginner labs |
| Day 6-7 | Juice Shop basic challenges |

---

## 📚 Additional Reading

- [Lab Setup Guide](./lab-setup.md) — Detailed installation walkthrough
- [Burp Suite Basics](./burp-basics.md) — Getting the most from Burp

---

<div align="center">

[← Module 02: Information Gathering](../02.%20Information%20Gathering/README.md) | [Next Module: Introduction to Web →](../04.%20Introduction%20to%20Web/README.md)

</div>
