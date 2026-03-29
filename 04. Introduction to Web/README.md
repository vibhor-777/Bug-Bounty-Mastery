# 🌐 Module 04: Introduction to Web

> **Level:** 🟢 Beginner | **Time:** ~3 hours | **Prerequisites:** Module 01-03

---

## 📖 Overview

Understanding how the web works is essential for finding web vulnerabilities. This module covers HTTP, the protocol powering the web, along with cookies, sessions, authentication, and how modern web applications are structured.

---

## ❓ Why It Matters

You cannot find vulnerabilities in something you don't understand. Every web vulnerability — XSS, SQLi, CSRF, SSRF — exploits how the web works. Mastering HTTP fundamentals makes you a better and faster bug bounty hunter.

---

## 🌍 Real-World Example

A researcher found a critical authentication bypass on a major platform simply by understanding that the application was using JWT tokens for session management and that the `alg: none` vulnerability wasn't patched. The fix would have been trivial, but required understanding what JWTs are.

---

## 📋 Step-by-Step Methodology

### How HTTP Works

```
CLIENT (Browser)         SERVER (Web App)
      │                        │
      │  → GET /page HTTP/1.1  │
      │  → Host: example.com   │
      │  → Cookie: session=xyz │
      │                        │
      │  ← HTTP/1.1 200 OK     │
      │  ← Content-Type: html  │
      │  ← Set-Cookie: ...     │
      │  ← [HTML Body]         │
```

### HTTP Methods

| Method | Purpose | Common Bugs |
|--------|---------|-------------|
| `GET` | Retrieve resource | Info disclosure in URL params |
| `POST` | Submit data | CSRF, SQLi, XSS |
| `PUT` | Update resource | Unauthorized modification |
| `DELETE` | Remove resource | IDOR, unauthorized deletion |
| `PATCH` | Partial update | Mass assignment |
| `OPTIONS` | Check allowed methods | CORS misconfiguration |
| `HEAD` | Get headers only | Info disclosure |

### HTTP Status Codes

```
1xx - Informational
2xx - Success
    200 OK
    201 Created
    204 No Content
3xx - Redirection
    301 Moved Permanently
    302 Found (Temporary Redirect)
    304 Not Modified
4xx - Client Errors
    400 Bad Request
    401 Unauthorized (not logged in)
    403 Forbidden (logged in, no permission)
    404 Not Found
    429 Too Many Requests (rate limiting)
5xx - Server Errors
    500 Internal Server Error (often leaks info)
    502 Bad Gateway
    503 Service Unavailable
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept and analyze HTTP traffic |
| **curl** | Make HTTP requests from terminal |
| **Browser DevTools** | Inspect requests, storage, JavaScript |

---

## 💡 Key Concepts with Examples

### HTTP Request Structure

```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGc...
Cookie: session=abc123
Accept: application/json
Content-Type: application/json
User-Agent: Mozilla/5.0...
```

### HTTP Response Structure

```http
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: session=xyz789; HttpOnly; Secure; SameSite=Strict
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000

{"id": 123, "name": "Alice", "email": "alice@example.com"}
```

### Cookies Deep Dive

```
Set-Cookie: name=value; 
            Domain=.example.com;    ← Accessible to subdomains
            Path=/;                 ← Accessible everywhere
            Expires=...;            ← When it expires
            HttpOnly;               ← JS cannot read (XSS protection)
            Secure;                 ← HTTPS only
            SameSite=Strict         ← CSRF protection
```

**Security issues to look for:**
- Missing `HttpOnly` flag → XSS can steal cookies
- Missing `Secure` flag → transmitted over HTTP
- Missing `SameSite` → CSRF possible
- Too-broad `Domain` → subdomain takeover risk

### Sessions vs Tokens

```
Session-based Auth:
    User logs in → Server creates session ID → Stored server-side
    Session ID sent in cookie → Server looks up session on each request

Token-based Auth (JWT):
    User logs in → Server creates signed JWT → Sent to client
    Client sends JWT in header → Server verifies signature
    Stateless — server doesn't need to store sessions
```

### JWT Structure

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.    ← Header (base64)
eyJzdWIiOiIxMjM0IiwicmVsZSI6InVzZXIifQ.  ← Payload (base64)
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  ← Signature
```

**JWT vulnerabilities:**
```python
# alg:none attack - remove signature verification
import jwt
token = jwt.encode({"sub": "admin"}, "", algorithm="none")

# Weak secret brute forcing
hashcat -a 0 -m 16500 jwt.txt wordlist.txt
```

---

## 🛡️ Prevention

| Issue | Prevention |
|-------|-----------|
| Insecure cookies | Use HttpOnly, Secure, SameSite flags |
| Weak session IDs | Use cryptographically random 128-bit tokens |
| JWT issues | Use strong algorithms (RS256), validate properly |
| HTTPS | Always enforce HTTPS with HSTS |

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger | [portswigger.net](https://portswigger.net/web-security/authentication) | Authentication labs |
| DVWA | localhost | Session management testing |
| Juice Shop | localhost:3000 | JWT challenges |

---

## 📚 Additional Reading

- [HTTP Headers Reference](./http-headers.md) — Security headers deep dive
- [Authentication Attacks](./auth-attacks.md) — Common auth vulnerabilities

---

<div align="center">

[← Module 03: Setting Up Labs](../03.%20Setting%20Up%20Labs/README.md) | [Next Module: SQL Injection →](../05.%20SQL%20Injection/README.md)

</div>
