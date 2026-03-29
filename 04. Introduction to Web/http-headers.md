# 🔒 HTTP Security Headers Reference

## Essential Security Headers

### Content-Security-Policy (CSP)
Prevents XSS and data injection attacks by specifying trusted content sources.

```http
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' https://trusted-cdn.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com;
    font-src 'self';
    frame-ancestors 'none';
```

**Bug bounty opportunity:** Missing or weak CSP that allows XSS escalation.

### X-Frame-Options
Prevents clickjacking by controlling iframe embedding.

```http
X-Frame-Options: DENY          # Never in iframe
X-Frame-Options: SAMEORIGIN    # Only same origin
```

**Bug bounty opportunity:** Missing header → clickjacking vulnerabilities.

### Strict-Transport-Security (HSTS)
Forces HTTPS connections.

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### X-Content-Type-Options
Prevents MIME sniffing.

```http
X-Content-Type-Options: nosniff
```

### Referrer-Policy
Controls referrer information.

```http
Referrer-Policy: strict-origin-when-cross-origin
```

### Permissions-Policy
Controls browser features.

```http
Permissions-Policy: geolocation=(), camera=(), microphone=()
```

## Analyzing Headers with curl

```bash
# View all response headers
curl -I https://target.com

# Follow redirects
curl -IL https://target.com

# View headers in verbose mode
curl -v https://target.com 2>&1 | grep "^[<>]"
```

## Security Header Checklist

| Header | Critical | Check |
|--------|----------|-------|
| Content-Security-Policy | Yes | Present and restrictive? |
| X-Frame-Options | Yes | DENY or SAMEORIGIN? |
| HSTS | Yes | Long max-age? includeSubDomains? |
| X-Content-Type-Options | Medium | nosniff? |
| Referrer-Policy | Medium | Appropriate policy? |
| Permissions-Policy | Low | Restricts dangerous features? |

## Tools for Header Analysis

```bash
# securityheaders.com alternative
curl -I https://target.com | grep -i "x-frame\|content-security\|strict-transport\|x-content"

# Use nuclei for automated header checks
nuclei -u https://target.com -t ~/nuclei-templates/miscellaneous/security-headers.yaml
```
