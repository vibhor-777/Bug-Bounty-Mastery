# 🔧 Module 06: Web Application Basics

> **Level:** 🟡 Intermediate | **Time:** ~3 hours | **Prerequisites:** Module 01-05

---

## 📖 Overview

Modern web applications have complex architectures with multiple security boundaries. This module covers the core concepts — authentication, authorization, session management, input validation, and common web application patterns — that you must understand to find vulnerabilities effectively.

---

## ❓ Why It Matters

The vast majority of web vulnerabilities stem from broken authentication, authorization flaws (IDOR), or improper input handling. Understanding how web apps should work helps you identify when they don't.

---

## 🌍 Real-World Example

A researcher discovered that a fintech app's API used sequential integer IDs for transaction records. By simply changing `/api/transactions/12345` to `/api/transactions/12344`, they could view another user's financial transaction details — a classic IDOR (Insecure Direct Object Reference). This earned a **$7,500 high severity bounty**.

---

## 📋 Step-by-Step Methodology

### Authentication Testing

```
1. Test for default credentials
2. Test password reset flow
3. Test brute force protection
4. Check for username enumeration
5. Test MFA bypass techniques
6. Check "remember me" token security
7. Test OAuth/SSO implementation
```

### Authorization Testing (IDOR)

```
1. Identify resource identifiers (IDs, UUIDs, usernames)
2. Create two test accounts (Account A and Account B)
3. As Account A, capture requests with resource IDs
4. As Account B, replay those requests
5. Check if Account B can access Account A's resources
```

### Session Management Testing

```
1. Examine session token entropy and randomness
2. Test session invalidation on logout
3. Test session fixation
4. Check cookie security flags
5. Test concurrent sessions
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept and modify requests |
| **Burp Autorize** | Automated IDOR testing |
| **JWT.io** | Decode and analyze JWT tokens |
| **curl** | Command-line HTTP testing |

---

## 💡 Payload Examples

### Username Enumeration

```bash
# Different error messages reveal valid usernames
# Test login with:
valid_user@target.com + wrong_password   → "Invalid password"
invalid@target.com + wrong_password      → "User not found"

# Also test password reset:
# Valid email → "Reset link sent"
# Invalid email → "Email not found"
```

### IDOR Testing

```bash
# Capture request as User A
GET /api/account/1234/profile
Authorization: Bearer <user_a_token>

# Replay as User B  
GET /api/account/1234/profile
Authorization: Bearer <user_b_token>

# If successful: IDOR vulnerability!

# Test different ID formats:
/api/account/1234          → Integer ID
/api/account/user_1234     → Prefixed ID
/api/account/abc123xyz     → Alphanumeric
/api/account/<UUID>        → UUID (still test!)

# Horizontal vs Vertical privilege escalation
# Horizontal: User A accesses User B's data (same privilege level)
# Vertical: User accesses admin functionality (higher privilege)
```

### Mass Assignment

```json
// Registration request
POST /api/users/register
{
    "username": "hacker",
    "password": "password123",
    "email": "hacker@test.com"
}

// Add extra fields hoping they get assigned
{
    "username": "hacker",
    "password": "password123",
    "email": "hacker@test.com",
    "role": "admin",              // Add admin role!
    "isVerified": true,           // Skip email verification
    "credits": 99999              // Add credits
}
```

### Password Reset Testing

```
1. Request reset for victim@example.com
2. Examine reset link structure:
   https://target.com/reset?token=abc123
   
3. Test if token is:
   - Predictable/sequential
   - Weak (short or low entropy)
   - Reusable (can same token reset multiple times?)
   - Never expires
   
4. Test host header injection in reset email:
   Host: attacker.com
   → Does reset link point to attacker.com?
```

### JWT Attacks

```bash
# Decode JWT (base64)
echo "eyJhbGciOiJIUzI1NiJ9" | base64 -d

# None algorithm attack
# Modify header to: {"alg":"none","typ":"JWT"}
# Remove signature
# Submit modified token

# RS256 to HS256 attack
# If server uses RS256 but can be tricked into HS256:
# Sign token with public key as HMAC secret

# Brute force weak secret
hashcat -a 0 -m 16500 jwt_token.txt /usr/share/wordlists/rockyou.txt
```

---

## 🛡️ Prevention

### Secure Authentication

```python
# Password hashing with bcrypt
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt)

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

### Secure Session Management

```python
# Generate secure session tokens
import secrets

def generate_session_token():
    return secrets.token_hex(32)  # 256-bit random token

# Always set secure cookie flags
response.set_cookie(
    'session',
    token,
    httponly=True,
    secure=True,
    samesite='Strict',
    max_age=3600
)
```

### Access Control

```python
# Check authorization on EVERY request
def get_resource(resource_id, current_user):
    resource = db.get(resource_id)
    
    # ALWAYS verify ownership/permission
    if resource.owner_id != current_user.id:
        raise PermissionError("Access denied")
    
    return resource
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger Auth Labs | [portswigger.net/web-security/authentication](https://portswigger.net/web-security/authentication) | Auth vulnerability labs |
| PortSwigger Access Control | [portswigger.net/web-security/access-control](https://portswigger.net/web-security/access-control) | IDOR and access control |
| DVWA | localhost | Authentication module |
| Juice Shop | localhost:3000 | Login bypass challenges |

---

<div align="center">

[← Module 05: SQL Injection](../05.%20SQL%20Injection/README.md) | [Next Module: Cross-Site Scripting →](../07.%20Cross%20Site%20Scripting%20(XSS)/README.md)

</div>
