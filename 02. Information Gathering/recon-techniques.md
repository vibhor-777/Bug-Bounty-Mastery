# 🔍 Advanced Recon Techniques

## DNS Reconnaissance

### Record Types to Enumerate

| Record | Purpose | Tool |
|--------|---------|------|
| A | IPv4 address | `dig A target.com` |
| AAAA | IPv6 address | `dig AAAA target.com` |
| MX | Mail servers | `dig MX target.com` |
| TXT | SPF, DKIM, verification | `dig TXT target.com` |
| NS | Nameservers | `dig NS target.com` |
| CNAME | Aliases | `dig CNAME sub.target.com` |
| SOA | Zone authority | `dig SOA target.com` |

### Zone Transfer (if misconfigured)

```bash
dig axfr @ns1.target.com target.com
```

## Certificate Transparency

Certificates are logged publicly — great for subdomain discovery:

```bash
# crt.sh query
curl -s "https://crt.sh/?q=%25.target.com&output=json" | \
    jq -r '.[].name_value' | \
    sed 's/\*\.//g' | \
    sort -u

# Using certspotter
curl -s "https://api.certspotter.com/v1/issuances?domain=target.com&include_subdomains=true&expand=dns_names" | \
    jq -r '.[].dns_names[]' | sort -u
```

## Wayback Machine Mining

```bash
# Get historical URLs
waybackurls target.com | tee wayback_urls.txt

# Filter interesting URLs
cat wayback_urls.txt | grep -E "\.(php|asp|aspx|jsp|json|xml|txt|bak|old|backup|conf|config)"

# Find old API endpoints
cat wayback_urls.txt | grep "/api/"

# Look for parameters
cat wayback_urls.txt | grep "?" | sort -u
```

## GitHub OSINT

```bash
# Search GitHub for leaked credentials
# Searches to perform on github.com:
# "target.com" password
# "target.com" api_key
# "target.com" secret_key  
# "target.com" token
# "target.com" aws_access_key

# Use truffleHog for automated scanning
trufflehog github --org=targetorg
```

## ASN & IP Range Discovery

```bash
# Find ASN for organization
whois -h whois.radb.net "! -i origin AS12345"

# Get IP ranges from ASN
amass intel -asn 12345

# Convert CIDR to hosts
prips 192.168.1.0/24
```

## Favicon Hash Matching (Shodan)

```python
import requests
import mmh3
import codecs

# Get favicon hash for Shodan search
response = requests.get('https://target.com/favicon.ico')
favicon = codecs.encode(response.content, 'base64')
hash_value = mmh3.hash(favicon)
print(f"Shodan favicon search: http.favicon.hash:{hash_value}")
```

## Port Scanning Strategy

```bash
# Fast scan of common ports
nmap -T4 --top-ports 1000 -oN quick_scan.txt target.com

# Full TCP scan
nmap -p- -T4 -oN full_scan.txt target.com

# Service/version detection
nmap -sV -sC -p 80,443,8080,8443,8888 -oN service_scan.txt target.com

# UDP scan (slower but valuable)
nmap -sU --top-ports 100 -oN udp_scan.txt target.com
```

## Technology Fingerprinting

```bash
# WhatWeb - identifies technologies
whatweb -a 3 target.com

# Wappalyzer CLI
wappalyzer https://target.com

# Check response headers manually
curl -I https://target.com
```

## Directory Fuzzing

```bash
# Basic fuzzing with ffuf
ffuf -u https://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# With specific extensions
ffuf -u https://target.com/FUZZ -w wordlist.txt -e .php,.asp,.html,.txt,.bak

# With authentication
ffuf -u https://target.com/FUZZ -w wordlist.txt -H "Cookie: session=TOKEN"

# Recursive fuzzing
ffuf -u https://target.com/FUZZ -w wordlist.txt -recursion -recursion-depth 2
```

## Notes and Documentation Template

```markdown
# Target: example.com
## Date: YYYY-MM-DD

### Subdomains Found
- sub1.example.com (live, Apache 2.4)
- api.example.com (live, Node.js)
- dev.example.com (live, PHP 7.4)

### Interesting Findings
- [ ] dev.example.com - no authentication on /api/users
- [ ] api.example.com - v1 endpoints still accessible (check for older vulns)

### Technologies
- Frontend: React, Bootstrap
- Backend: Node.js, Express
- Database: MySQL (inferred from errors)
- CDN: Cloudflare

### Open Ports
- 80/tcp - HTTP
- 443/tcp - HTTPS  
- 8080/tcp - Alternative HTTP (Tomcat)
```
