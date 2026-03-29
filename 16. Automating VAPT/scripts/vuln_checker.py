#!/usr/bin/env python3
"""
vuln_checker.py - Automated vulnerability checker for bug bounty
Usage: python3 vuln_checker.py -f targets.txt
       python3 vuln_checker.py -u https://target.com
"""

import requests
import argparse
import concurrent.futures
import sys
import json
from urllib.parse import urljoin, urlparse
from datetime import datetime

requests.packages.urllib3.disable_warnings()

TIMEOUT = 10
SENSITIVE_PATHS = [
    '/.git/HEAD',
    '/.git/config',
    '/.env',
    '/.env.local',
    '/.env.production',
    '/.env.staging',
    '/config.php',
    '/wp-config.php',
    '/database.yml',
    '/.htpasswd',
    '/backup.zip',
    '/backup.sql',
    '/dump.sql',
    '/debug.log',
    '/error.log',
    '/phpinfo.php',
    '/info.php',
    '/test.php',
    '/admin',
    '/administrator',
    '/phpmyadmin',
    '/pma',
    '/wp-admin',
    '/manager/html',
    '/actuator',
    '/actuator/health',
    '/actuator/env',
    '/api/swagger',
    '/swagger-ui.html',
    '/api-docs',
    '/v1/api-docs',
    '/graphql',
    '/graphiql',
]

SECURITY_HEADERS = {
    'X-Frame-Options': 'Missing X-Frame-Options (Clickjacking risk)',
    'X-Content-Type-Options': 'Missing X-Content-Type-Options (MIME sniffing risk)',
    'Strict-Transport-Security': 'Missing HSTS header',
    'Content-Security-Policy': 'Missing Content-Security-Policy (XSS risk)',
    'X-XSS-Protection': 'Missing X-XSS-Protection header',
}


def print_finding(level, url, message):
    colors = {
        'CRITICAL': '\033[91m',
        'HIGH': '\033[91m',
        'MEDIUM': '\033[93m',
        'LOW': '\033[94m',
        'INFO': '\033[92m',
    }
    reset = '\033[0m'
    color = colors.get(level, '')
    print(f"{color}[{level}]{reset} {url} - {message}")


def check_security_headers(url):
    findings = []
    try:
        response = requests.get(url, timeout=TIMEOUT, verify=False,
                                allow_redirects=True)
        headers = {k.lower(): v for k, v in response.headers.items()}

        for header, message in SECURITY_HEADERS.items():
            if header.lower() not in headers:
                findings.append({
                    'level': 'MEDIUM',
                    'url': url,
                    'message': message,
                    'type': 'missing_header'
                })

        # Check for information disclosure in headers
        server = headers.get('server', '')
        if server and any(v in server.lower() for v in ['apache/', 'nginx/', 'iis/']):
            findings.append({
                'level': 'LOW',
                'url': url,
                'message': f'Server version disclosed: {server}',
                'type': 'info_disclosure'
            })

        x_powered_by = headers.get('x-powered-by', '')
        if x_powered_by:
            findings.append({
                'level': 'LOW',
                'url': url,
                'message': f'X-Powered-By disclosed: {x_powered_by}',
                'type': 'info_disclosure'
            })

    except requests.exceptions.ConnectionError:
        pass
    except Exception:
        pass

    return findings


def check_exposed_files(url):
    findings = []

    for path in SENSITIVE_PATHS:
        try:
            full_url = urljoin(url.rstrip('/') + '/', path.lstrip('/'))
            response = requests.get(full_url, timeout=TIMEOUT, verify=False,
                                    allow_redirects=False)

            if response.status_code == 200:
                content = response.text[:500].lower()

                # Verify it's actually sensitive content
                if path == '/.git/HEAD' and 'ref:' in content:
                    findings.append({
                        'level': 'CRITICAL',
                        'url': full_url,
                        'message': 'Exposed .git directory! Source code may be extractable.',
                        'type': 'exposed_file'
                    })
                elif path in ['/.env', '/.env.local', '/.env.production']:
                    if any(k in content for k in ['password', 'secret', 'key', 'token', 'database']):
                        findings.append({
                            'level': 'CRITICAL',
                            'url': full_url,
                            'message': 'Exposed .env file with potential secrets!',
                            'type': 'exposed_file'
                        })
                elif path in ['/phpinfo.php', '/info.php']:
                    if 'phpinfo' in content or 'php version' in content:
                        findings.append({
                            'level': 'MEDIUM',
                            'url': full_url,
                            'message': 'Exposed phpinfo() page - information disclosure',
                            'type': 'exposed_file'
                        })
                elif response.status_code == 200 and len(response.content) > 100:
                    findings.append({
                        'level': 'HIGH',
                        'url': full_url,
                        'message': f'Potentially sensitive path accessible: {path}',
                        'type': 'exposed_path'
                    })

            elif response.status_code == 403:
                findings.append({
                    'level': 'LOW',
                    'url': full_url,
                    'message': f'Forbidden resource exists (403): {path}',
                    'type': 'forbidden_resource'
                })

        except requests.exceptions.ConnectionError:
            break  # Host unreachable
        except Exception:
            pass

    return findings


def check_cors(url):
    findings = []
    try:
        headers = {'Origin': 'https://evil.com'}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, verify=False)

        acao = response.headers.get('Access-Control-Allow-Origin', '')
        acac = response.headers.get('Access-Control-Allow-Credentials', '')

        if acao == 'https://evil.com' and acac.lower() == 'true':
            findings.append({
                'level': 'HIGH',
                'url': url,
                'message': 'CORS misconfiguration: reflects arbitrary Origin with credentials!',
                'type': 'cors'
            })
        elif acao == 'null':
            findings.append({
                'level': 'MEDIUM',
                'url': url,
                'message': 'CORS: Trusts null origin',
                'type': 'cors'
            })
        elif acao == '*' and acac.lower() == 'true':
            findings.append({
                'level': 'HIGH',
                'url': url,
                'message': 'CORS: wildcard (*) with credentials - invalid but may indicate misconfig',
                'type': 'cors'
            })

    except Exception:
        pass

    return findings


def scan_target(url):
    """Scan a single target for common vulnerabilities"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    all_findings = []
    all_findings.extend(check_security_headers(url))
    all_findings.extend(check_exposed_files(url))
    all_findings.extend(check_cors(url))

    return all_findings


def main():
    parser = argparse.ArgumentParser(
        description='Automated vulnerability checker for bug bounty',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 vuln_checker.py -u https://target.com
  python3 vuln_checker.py -f targets.txt
  python3 vuln_checker.py -f targets.txt -t 20 -o results.json
        """
    )
    parser.add_argument('-u', '--url', help='Single URL to scan')
    parser.add_argument('-f', '--file', help='File containing URLs to scan')
    parser.add_argument('-t', '--threads', type=int, default=10,
                        help='Number of concurrent threads (default: 10)')
    parser.add_argument('-o', '--output', help='Output file (JSON format)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show all findings including LOW severity')
    args = parser.parse_args()

    if not args.url and not args.file:
        parser.print_help()
        sys.exit(1)

    targets = []
    if args.file:
        try:
            with open(args.file) as f:
                targets = [line.strip() for line in f if line.strip()
                           and not line.startswith('#')]
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
    elif args.url:
        targets = [args.url]

    print(f"\n[*] Bug Bounty Mastery - Vulnerability Checker")
    print(f"[*] Scanning {len(targets)} target(s) with {args.threads} threads")
    print(f"[*] Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_target = {executor.submit(scan_target, t): t for t in targets}
        for future in concurrent.futures.as_completed(future_to_target):
            try:
                findings = future.result()
                for finding in findings:
                    if args.verbose or finding['level'] not in ('LOW', 'INFO'):
                        print_finding(finding['level'], finding['url'],
                                      finding['message'])
                all_findings.extend(findings)
            except Exception as e:
                pass

    # Summary
    print("\n" + "=" * 60)
    print("[+] Scan Complete!")
    print(f"[+] Total findings: {len(all_findings)}")

    level_counts = {}
    for f in all_findings:
        level_counts[f['level']] = level_counts.get(f['level'], 0) + 1

    for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
        count = level_counts.get(level, 0)
        if count > 0:
            print(f"    {level}: {count}")

    # Save output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump({
                'scan_time': datetime.now().isoformat(),
                'targets': targets,
                'findings': all_findings
            }, f, indent=2)
        print(f"[+] Results saved to: {args.output}")


if __name__ == '__main__':
    main()
