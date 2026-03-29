# 📝 Professional Bug Report Template

## Report Structure

Copy and adapt this template for every bug bounty submission.

---

```markdown
# [BUG TYPE] in [Component] Allows [Impact]

## Summary

**Vulnerability Type:** [XSS / SQLi / SSRF / IDOR / etc.]  
**Severity:** [Critical / High / Medium / Low]  
**CVSS Score:** [X.X - Calculate at cvss.first.org]  
**Affected Asset:** [URL or endpoint]  
**Browser/Platform:** [Chrome 120 / Firefox 121 / Mobile API]

Brief description (2-3 sentences):
A [vulnerability type] exists in the [component/feature] of [target]. 
An attacker can [what they can do] by [how]. 
This could result in [impact to users/company].

---

## Technical Details

### Vulnerability Location
```
Endpoint: POST https://app.target.com/api/user/update
Parameter: bio
```

### Root Cause
[Explain why the vulnerability exists - e.g., "User input is
not sanitized before being stored and rendered in HTML context"]

---

## Steps to Reproduce

**Prerequisites:**
- Create two test accounts: attacker@test.com and victim@test.com
- Use Chrome/Firefox with developer tools open

**Steps:**

1. Log in to the application as attacker@test.com
   - URL: https://app.target.com/login
   
2. Navigate to profile settings
   - URL: https://app.target.com/settings/profile
   
3. In the "Bio" field, enter the following payload:
   ```
   [PAYLOAD HERE]
   ```
   
4. Click "Save Changes"

5. Log out and log in as victim@test.com

6. Navigate to attacker's profile page:
   - URL: https://app.target.com/user/attacker
   
7. **Expected result:** Profile bio displayed as plain text
8. **Actual result:** [Payload executes / Data is returned / etc.]

---

## Proof of Concept

### HTTP Request (Step 3)
```http
POST /api/user/update HTTP/2
Host: app.target.com
Cookie: session=ATTACKER_SESSION
Content-Type: application/json
Content-Length: XX

{
    "bio": "<PAYLOAD>"
}
```

### HTTP Response
```http
HTTP/2 200 OK
Content-Type: application/json

{
    "status": "success",
    "message": "Profile updated"
}
```

### Screenshot 1: Payload Insertion
[Insert screenshot showing payload in bio field]

### Screenshot 2: Vulnerable Page
[Insert screenshot showing the vulnerability triggering]

### Screenshot 3: Impact Demonstration
[Insert screenshot showing the impact - stolen cookie, data, etc.]

### Video PoC
[Optional but highly recommended for complex bugs]
[Screen recording link]

---

## Impact

**Who is affected:** All users who visit a profile with a malicious bio

**What an attacker can do:**
1. Steal session cookies of any victim who views the profile
2. Take over victim accounts without needing credentials
3. Perform actions on behalf of victims (send messages, make purchases, etc.)
4. Spread the attack virally if placed on high-traffic profiles

**Estimated affected users:** Any of the platform's [X million] users who view profiles

---

## Remediation

**Immediate mitigations:**
1. Strip/encode HTML entities in the bio field output
2. Implement Content-Security-Policy header

**Proper fix:**
```python
# Server-side: encode before storing or rendering
from html import escape
bio = escape(user_input_bio)

# Frontend: use textContent instead of innerHTML  
element.textContent = bio;  # Safe
# element.innerHTML = bio;  // DANGEROUS
```

**Additional hardening:**
- Set HttpOnly flag on session cookies
- Implement CSP: `script-src 'self'`
- Consider using DOMPurify for HTML content

---

## References

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [CWE-79: Improper Neutralization of Input During Web Page Generation](https://cwe.mitre.org/data/definitions/79.html)
- [PortSwigger XSS Research](https://portswigger.net/research/xss)

---

## Timeline

- **Discovery:** [Date]
- **Report submitted:** [Date]
- **Triage:** [Date when triaged - fill in later]
- **Resolved:** [Date - fill in later]
```

---

## Report Writing Tips

### DO:
✅ Use numbered steps that anyone can follow  
✅ Include exact URLs and endpoints  
✅ Show HTTP requests and responses  
✅ Attach annotated screenshots  
✅ Calculate a realistic CVSS score  
✅ Suggest specific remediation  
✅ Demonstrate actual impact (not theoretical)  
✅ Test the PoC yourself before submitting  

### DON'T:
❌ Submit without screenshots or PoC  
❌ Exaggerate the severity  
❌ Include unnecessary technical jargon  
❌ Submit duplicate bugs intentionally  
❌ Threaten or pressure the company  
❌ Disclose the bug publicly before it's fixed  
❌ Access more data than needed to prove the bug  
❌ Use production user data in your PoC  

## Sample CVSS Calculation

```
For a Stored XSS that steals cookies:

Attack Vector: Network (AV:N)
Attack Complexity: Low (AC:L)  
Privileges Required: Low (PR:L) - need account to post
User Interaction: Required (UI:R) - victim must view page
Scope: Changed (S:C) - affects victim's browser
Confidentiality: High (C:H) - can steal cookies/data
Integrity: High (I:H) - can modify page content
Availability: None (A:N)

CVSS 3.1 Score: 8.7 (HIGH)
Vector: CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N

Calculate yours at: https://www.first.org/cvss/calculator/3.1
```
