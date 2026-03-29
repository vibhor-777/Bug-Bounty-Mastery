# ⚙️ Module 16: Automating VAPT

> **Level:** 🔴 Advanced | **Time:** ~4 hours | **Prerequisites:** Module 01-15

---

## 📖 Overview

Automation is the force multiplier in bug bounty hunting. While manual testing finds complex, logic-based bugs, automated tools help you cover vast attack surfaces efficiently. This module teaches you to build recon pipelines, automate vulnerability scanning, and create custom scripts that work while you sleep.

---

## ❓ Why It Matters

Top bug bounty earners don't just work harder — they work smarter with automation. A well-built recon pipeline can continuously monitor thousands of subdomains and alert you when new services appear. Being first to find a new asset often means being first to find its bugs.

---

## 🌍 Real-World Example

A top HackerOne researcher built an automated pipeline that monitored 500+ bug bounty programs for new subdomains. When a new development subdomain appeared at 2 AM, their system automatically scanned it and discovered a default credential login. They submitted the report before anyone else woke up — earning a $3,000 bounty.

---

## 📋 Step-by-Step Recon Workflow

```
Phase 1: Subdomain Discovery
    subfinder + amass → passive enumeration
    dnsx → DNS resolution/validation
    httpx → HTTP probing (find live web servers)
        ↓
Phase 2: Content Discovery  
    ffuf → directory/file fuzzing
    waybackurls + gau → historical URL collection
    JS file analysis → endpoint extraction
        ↓
Phase 3: Vulnerability Scanning
    nuclei → template-based scanning
    dalfox → XSS scanning
    sqlmap → SQLi scanning
        ↓
Phase 4: Notification
    Slack/Discord webhook → new findings alert
    Email notification → daily summary
```

---

## 🛠️ Tools Used

| Tool | Purpose | Install |
|------|---------|---------|
| **subfinder** | Passive subdomain enum | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| **amass** | Active/passive subdomain enum | `go install github.com/owasp-amass/amass/v4/...@master` |
| **httpx** | HTTP probing | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` |
| **nuclei** | Template-based vuln scanner | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
| **dnsx** | DNS toolkit | `go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest` |
| **ffuf** | Web fuzzer | `go install github.com/ffuf/ffuf/v2@latest` |
| **dalfox** | XSS scanner | `go install github.com/hahwul/dalfox/v2@latest` |
| **waybackurls** | Historical URLs | `go install github.com/tomnomnom/waybackurls@latest` |
| **gau** | Get all URLs | `go install github.com/lc/gau/v2/cmd/gau@latest` |
| **anew** | Append new lines | `go install github.com/tomnomnom/anew@latest` |
| **notify** | Send notifications | `go install github.com/projectdiscovery/notify/cmd/notify@latest` |

---

## 💡 Automation Scripts

### Complete Recon Script (Bash)

```bash
#!/bin/bash
# recon.sh - Automated Bug Bounty Recon Pipeline
# Usage: ./recon.sh target.com

TARGET=$1
OUTPUT_DIR="./recon-$TARGET"
DATE=$(date +%Y%m%d-%H%M%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] Starting recon for: $TARGET${NC}"
mkdir -p "$OUTPUT_DIR"

# Phase 1: Subdomain Enumeration
echo -e "${YELLOW}[*] Phase 1: Subdomain Enumeration${NC}"

# Passive subdomain discovery
echo -e "[*] Running subfinder..."
subfinder -d "$TARGET" -silent -o "$OUTPUT_DIR/subfinder.txt" 2>/dev/null

echo -e "[*] Running amass..."
amass enum -passive -d "$TARGET" -o "$OUTPUT_DIR/amass.txt" 2>/dev/null

# Certificate transparency
echo -e "[*] Querying crt.sh..."
curl -s "https://crt.sh/?q=%25.$TARGET&output=json" 2>/dev/null | \
    jq -r '.[].name_value' 2>/dev/null | \
    sed 's/\*\.//g' | \
    sort -u > "$OUTPUT_DIR/crtsh.txt"

# Combine all subdomains
echo -e "[*] Combining and deduplicating results..."
cat "$OUTPUT_DIR/subfinder.txt" "$OUTPUT_DIR/amass.txt" "$OUTPUT_DIR/crtsh.txt" 2>/dev/null | \
    sort -u > "$OUTPUT_DIR/all_subdomains.txt"

echo -e "${GREEN}[+] Found $(wc -l < "$OUTPUT_DIR/all_subdomains.txt") unique subdomains${NC}"

# Phase 2: DNS Resolution & HTTP Probing
echo -e "${YELLOW}[*] Phase 2: Probing for live hosts${NC}"

# Resolve DNS
cat "$OUTPUT_DIR/all_subdomains.txt" | \
    dnsx -silent -a -resp-only | \
    sort -u > "$OUTPUT_DIR/resolved_ips.txt"

# Find live web servers
cat "$OUTPUT_DIR/all_subdomains.txt" | \
    httpx -silent -status-code -title -tech-detect \
          -o "$OUTPUT_DIR/live_hosts.txt" 2>/dev/null

echo -e "${GREEN}[+] Found $(wc -l < "$OUTPUT_DIR/live_hosts.txt") live web servers${NC}"

# Phase 3: URL Collection
echo -e "${YELLOW}[*] Phase 3: Collecting URLs${NC}"

# Wayback Machine URLs
cat "$OUTPUT_DIR/all_subdomains.txt" | \
    waybackurls 2>/dev/null | \
    sort -u > "$OUTPUT_DIR/wayback_urls.txt"

# GAU URLs
cat "$OUTPUT_DIR/all_subdomains.txt" | \
    gau --threads 5 2>/dev/null | \
    sort -u >> "$OUTPUT_DIR/wayback_urls.txt"

cat "$OUTPUT_DIR/wayback_urls.txt" | sort -u -o "$OUTPUT_DIR/all_urls.txt"
echo -e "${GREEN}[+] Collected $(wc -l < "$OUTPUT_DIR/all_urls.txt") URLs${NC}"

# Phase 4: Vulnerability Scanning
echo -e "${YELLOW}[*] Phase 4: Scanning for vulnerabilities${NC}"

# Nuclei scan
echo -e "[*] Running nuclei..."
awk '{print $1}' "$OUTPUT_DIR/live_hosts.txt" | \
    nuclei -silent \
           -severity medium,high,critical \
           -o "$OUTPUT_DIR/nuclei_findings.txt" 2>/dev/null

echo -e "${GREEN}[+] Nuclei scan complete. Findings: $(wc -l < "$OUTPUT_DIR/nuclei_findings.txt")${NC}"

# Summary
echo ""
echo -e "${GREEN}============ RECON COMPLETE ============${NC}"
echo -e "Target:          $TARGET"
echo -e "Subdomains:      $(wc -l < "$OUTPUT_DIR/all_subdomains.txt")"
echo -e "Live hosts:      $(wc -l < "$OUTPUT_DIR/live_hosts.txt")"
echo -e "URLs collected:  $(wc -l < "$OUTPUT_DIR/all_urls.txt")"
echo -e "Nuclei findings: $(wc -l < "$OUTPUT_DIR/nuclei_findings.txt")"
echo -e "Output dir:      $OUTPUT_DIR"
echo -e "${GREEN}=======================================${NC}"
```

### Continuous Monitoring Script

```bash
#!/bin/bash
# monitor.sh - Monitor for new subdomains and notify
# Usage: ./monitor.sh target.com
# Run with cron for continuous monitoring

TARGET=$1
MONITOR_DIR="./monitoring/$TARGET"
mkdir -p "$MONITOR_DIR"

NEW_FILE="$MONITOR_DIR/new_$(date +%Y%m%d).txt"

# Get current subdomains
subfinder -d "$TARGET" -silent | \
    amass enum -passive -d "$TARGET" -o /dev/null 2>/dev/null | \
    sort -u > "$MONITOR_DIR/current.txt"

# Compare with previous run
if [ -f "$MONITOR_DIR/previous.txt" ]; then
    comm -23 \
        <(sort "$MONITOR_DIR/current.txt") \
        <(sort "$MONITOR_DIR/previous.txt") \
        > "$NEW_FILE"
    
    if [ -s "$NEW_FILE" ]; then
        echo "[!] New subdomains found for $TARGET:"
        cat "$NEW_FILE"
        
        # Probe new subdomains
        cat "$NEW_FILE" | httpx -silent -status-code -title > "$MONITOR_DIR/new_live.txt"
        
        # Quick nuclei scan on new hosts
        cat "$MONITOR_DIR/new_live.txt" | awk '{print $1}' | \
            nuclei -silent -severity high,critical >> "$MONITOR_DIR/new_vulns.txt"
        
        # Send notification (configure notify tool first)
        cat "$NEW_FILE" | notify -provider slack -id recon-alerts
    fi
fi

# Update previous list
cp "$MONITOR_DIR/current.txt" "$MONITOR_DIR/previous.txt"
```

### Python: Automated Vulnerability Checker

```python
#!/usr/bin/env python3
"""
vuln_checker.py - Check common vulnerabilities across targets
Usage: python3 vuln_checker.py -f targets.txt
"""

import requests
import argparse
import concurrent.futures
from urllib.parse import urljoin

requests.packages.urllib3.disable_warnings()

def check_security_headers(url):
    """Check for missing security headers"""
    findings = []
    try:
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers
        
        required_headers = {
            'X-Frame-Options': 'Missing X-Frame-Options (Clickjacking risk)',
            'X-Content-Type-Options': 'Missing X-Content-Type-Options',
            'Strict-Transport-Security': 'Missing HSTS header',
            'Content-Security-Policy': 'Missing Content-Security-Policy',
        }
        
        for header, message in required_headers.items():
            if header not in headers:
                findings.append(f"[MEDIUM] {url} - {message}")
    
    except Exception as e:
        pass
    
    return findings

def check_exposed_files(url):
    """Check for exposed sensitive files"""
    findings = []
    sensitive_paths = [
        '/.git/HEAD',
        '/.env',
        '/config.php',
        '/wp-config.php',
        '/database.yml',
        '/.htpasswd',
        '/backup.zip',
        '/backup.sql',
        '/admin',
        '/phpmyadmin',
    ]
    
    for path in sensitive_paths:
        try:
            full_url = urljoin(url, path)
            response = requests.get(full_url, timeout=10, verify=False, 
                                   allow_redirects=False)
            
            if response.status_code == 200:
                findings.append(f"[HIGH] Exposed file: {full_url}")
            elif response.status_code == 403:
                findings.append(f"[LOW] Forbidden (exists): {full_url}")
        
        except Exception:
            pass
    
    return findings

def scan_target(url):
    """Scan a single target"""
    if not url.startswith('http'):
        url = 'https://' + url
    
    findings = []
    findings.extend(check_security_headers(url))
    findings.extend(check_exposed_files(url))
    
    return findings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File with targets')
    parser.add_argument('-u', '--url', help='Single URL target')
    parser.add_argument('-t', '--threads', type=int, default=10)
    args = parser.parse_args()
    
    targets = []
    if args.file:
        with open(args.file) as f:
            targets = [line.strip() for line in f if line.strip()]
    elif args.url:
        targets = [args.url]
    
    print(f"[*] Scanning {len(targets)} targets with {args.threads} threads")
    
    all_findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_target, t): t for t in targets}
        for future in concurrent.futures.as_completed(futures):
            findings = future.result()
            all_findings.extend(findings)
            for f in findings:
                print(f)
    
    print(f"\n[+] Total findings: {len(all_findings)}")

if __name__ == '__main__':
    main()
```

### Nuclei Custom Templates

```yaml
# custom-template.yaml - Find exposed .env files
id: exposed-env-file

info:
  name: Exposed .env File
  author: security-researcher
  severity: high
  description: Exposed .env file containing sensitive configuration

requests:
  - method: GET
    path:
      - "{{BaseURL}}/.env"
      - "{{BaseURL}}/.env.local"
      - "{{BaseURL}}/.env.production"
    
    matchers-condition: and
    matchers:
      - type: status
        status:
          - 200
      
      - type: word
        words:
          - "DB_PASSWORD"
          - "APP_SECRET"
          - "DATABASE_URL"
          - "API_KEY"
        condition: or
```

---

## 🧪 Practice Labs

| Lab | Description |
|-----|------------|
| Set up your own pipeline | Follow the recon.sh script |
| HackTheBox | Test automation on retired machines |
| Bug bounty programs | Apply to real targets with permission |

---

## 📚 Additional Reading

- [Recon Automation Scripts](./scripts/) — All scripts from this module

---

<div align="center">

[← Module 15: Insecure Captcha](../15.%20Insecure%20Captcha/README.md) | [Next Module: Documenting & Reporting →](../17.%20Documenting%20%26%20Reporting/README.md)

</div>
