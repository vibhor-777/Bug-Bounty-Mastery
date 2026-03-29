# 🔍 Module 02: Information Gathering

> **Level:** 🟢 Beginner | **Time:** ~3 hours | **Prerequisites:** Module 01

---

## 📖 Overview

Information gathering (reconnaissance) is the foundation of every successful bug bounty hunt. The more you know about a target, the more likely you are to find unique, impactful vulnerabilities. This module covers both passive (OSINT) and active reconnaissance techniques used by professional researchers.

---

## ❓ Why It Matters

90% of successful bug bounty hunters spend more time on recon than on actual exploitation. Understanding the full attack surface — subdomains, technologies, exposed endpoints, leaked credentials — directly translates to finding bugs others miss.

---

## 🌍 Real-World Example

A researcher targeting a Fortune 500 company used `subfinder` to enumerate subdomains and discovered `dev-api.company.com` — a development API endpoint left exposed to the internet. The endpoint had no authentication and exposed full customer records. This earned a **$15,000 critical bounty**.

---

## 📋 Step-by-Step Methodology

### Phase 1: Passive Reconnaissance

```
Target: example.com
    ↓
WHOIS lookup → registrant, nameservers
    ↓
DNS enumeration → subdomains, records
    ↓
Google Dorking → exposed files, login panels
    ↓
Shodan/Censys → internet-facing services
    ↓
GitHub search → leaked keys, internal code
```

### Phase 2: Active Reconnaissance

```
Subdomain enumeration (subfinder, amass)
    ↓
Port scanning (nmap, masscan)
    ↓
Web server fingerprinting (whatweb, wappalyzer)
    ↓
Directory/file fuzzing (ffuf, gobuster)
    ↓
Technology stack identification
    ↓
JS file analysis for endpoints and secrets
```

### Phase 3: Attack Surface Mapping

- List all live hosts and services
- Identify login portals and admin panels
- Map API endpoints from JS files
- Note technology versions for CVE lookup
- Document all findings in structured notes

---

## 🛠️ Tools Used

| Tool | Type | Command |
|------|------|---------|
| **subfinder** | Passive subdomain enum | `subfinder -d target.com` |
| **amass** | Active/passive enum | `amass enum -d target.com` |
| **httpx** | HTTP probing | `httpx -l subdomains.txt` |
| **nmap** | Port scanning | `nmap -sV target.com` |
| **ffuf** | Directory fuzzing | `ffuf -u URL/FUZZ -w wordlist.txt` |
| **waybackurls** | Historical URLs | `waybackurls target.com` |
| **gau** | Get All URLs | `gau target.com` |
| **nuclei** | Vulnerability scanning | `nuclei -u target.com` |
| **shodan** | Internet-wide scanning | [shodan.io](https://shodan.io) |

---

## 💡 Payload Examples

### Subdomain Enumeration

```bash
# Passive subdomain enumeration
subfinder -d target.com -o subdomains.txt

# Active enumeration with amass
amass enum -d target.com -o amass_output.txt

# Combine and deduplicate results
cat subdomains.txt amass_output.txt | sort -u > all_subdomains.txt

# Find live hosts
httpx -l all_subdomains.txt -o live_hosts.txt -status-code -title
```

### Google Dorking

```
site:target.com ext:php inurl:admin
site:target.com filetype:sql
site:target.com inurl:config
site:target.com "index of /"
site:target.com ext:env OR ext:yml OR ext:yaml
inurl:target.com "api_key" OR "secret" site:github.com
```

### JavaScript Analysis

```bash
# Download and analyze JS files
cat live_hosts.txt | waybackurls | grep "\.js$" | sort -u > js_files.txt

# Extract endpoints from JS files
cat js_files.txt | while read url; do
    curl -s "$url" | grep -oP '(?<=["'"'"'])/[a-zA-Z0-9_/-]+' 
done | sort -u > endpoints.txt

# Look for secrets in JS
cat js_files.txt | while read url; do
    curl -s "$url" | grep -iE "(api_key|secret|password|token|auth)" 
done
```

### Shodan Queries

```
hostname:target.com
org:"Target Company" port:8080
ssl.cert.subject.cn:target.com
```

---

## 🛡️ Prevention

- **For defenders**: Regularly audit your external attack surface
- Use tools like `subfinder` on your own domains periodically
- Monitor for exposed credentials on GitHub
- Implement security headers and restrict admin panels

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger | [portswigger.net](https://portswigger.net/web-security) | Information disclosure labs |
| TryHackMe | [tryhackme.com](https://tryhackme.com) | "Passive Recon" room |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | Enumeration challenges |
| Bugcrowd University | [bugcrowd.com/university](https://bugcrowd.com/university) | Recon methodologies |

---

## 📚 Additional Reading

- [Recon Techniques](./recon-techniques.md) — Deep dive into each technique
- [OSINT Tools Guide](./osint-tools.md) — Comprehensive tool reference

---

<div align="center">

[← Module 01: Introduction](../01.%20Introduction%20to%20Bug%20Bounty/README.md) | [Next Module: Setting Up Labs →](../03.%20Setting%20Up%20Labs/README.md)

</div>
