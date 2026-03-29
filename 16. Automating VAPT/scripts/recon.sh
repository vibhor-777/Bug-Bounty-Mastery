#!/bin/bash
# recon.sh - Automated Bug Bounty Recon Pipeline
# Usage: ./recon.sh target.com
# Author: Bug Bounty Mastery Course

TARGET=$1

if [ -z "$TARGET" ]; then
    echo "Usage: $0 target.com"
    exit 1
fi

OUTPUT_DIR="./recon-$TARGET-$(date +%Y%m%d)"
mkdir -p "$OUTPUT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[+]${NC} $1"; }
info() { echo -e "${BLUE}[*]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }

echo -e "${GREEN}"
echo "  ____  _____ ____ ___  _   _ "
echo " |  _ \| ____/ ___/ _ \| \ | |"
echo " | |_) |  _|| |  | | | |  \| |"
echo " |  _ <| |__| |__| |_| | |\  |"
echo " |_| \_\_____\____\___/|_| \_|"
echo ""
echo " Bug Bounty Mastery - Recon Script"
echo -e "${NC}"
echo "Target: $TARGET"
echo "Output: $OUTPUT_DIR"
echo "-----------------------------------"

# Phase 1: Subdomain Enumeration
info "Phase 1: Subdomain Enumeration"

info "Running subfinder..."
if command -v subfinder &>/dev/null; then
    subfinder -d "$TARGET" -silent -o "$OUTPUT_DIR/subfinder.txt" 2>/dev/null
    log "subfinder: $(wc -l < "$OUTPUT_DIR/subfinder.txt" 2>/dev/null || echo 0) subdomains"
else
    warn "subfinder not found, skipping..."
    touch "$OUTPUT_DIR/subfinder.txt"
fi

info "Running amass..."
if command -v amass &>/dev/null; then
    timeout 300 amass enum -passive -d "$TARGET" -o "$OUTPUT_DIR/amass.txt" 2>/dev/null
    log "amass: $(wc -l < "$OUTPUT_DIR/amass.txt" 2>/dev/null || echo 0) subdomains"
else
    warn "amass not found, skipping..."
    touch "$OUTPUT_DIR/amass.txt"
fi

info "Querying crt.sh..."
curl -s --max-time 30 "https://crt.sh/?q=%25.$TARGET&output=json" 2>/dev/null | \
    python3 -c "import json,sys; data=json.load(sys.stdin); [print(d['name_value']) for d in data]" 2>/dev/null | \
    sed 's/\*\.//g' | \
    grep -v "^$" | \
    sort -u > "$OUTPUT_DIR/crtsh.txt" 2>/dev/null
log "crt.sh: $(wc -l < "$OUTPUT_DIR/crtsh.txt" 2>/dev/null || echo 0) subdomains"

# Combine all subdomains
cat "$OUTPUT_DIR/subfinder.txt" "$OUTPUT_DIR/amass.txt" "$OUTPUT_DIR/crtsh.txt" 2>/dev/null | \
    grep -E "^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$" | \
    sort -u > "$OUTPUT_DIR/all_subdomains.txt"

TOTAL_SUBS=$(wc -l < "$OUTPUT_DIR/all_subdomains.txt")
log "Total unique subdomains: $TOTAL_SUBS"

# Phase 2: HTTP Probing
info "Phase 2: Probing for live hosts"

if command -v httpx &>/dev/null; then
    cat "$OUTPUT_DIR/all_subdomains.txt" | \
        httpx -silent -status-code -title -tech-detect \
              -o "$OUTPUT_DIR/live_hosts.txt" 2>/dev/null
    log "Live web servers: $(wc -l < "$OUTPUT_DIR/live_hosts.txt")"
else
    warn "httpx not found, using curl fallback..."
    while IFS= read -r subdomain; do
        for proto in https http; do
            status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$proto://$subdomain" 2>/dev/null)
            if [[ "$status" =~ ^[23] ]]; then
                echo "$proto://$subdomain [$status]" >> "$OUTPUT_DIR/live_hosts.txt"
                break
            fi
        done
    done < "$OUTPUT_DIR/all_subdomains.txt"
fi

# Phase 3: URL Collection
info "Phase 3: Collecting historical URLs"

if command -v waybackurls &>/dev/null; then
    cat "$OUTPUT_DIR/all_subdomains.txt" | waybackurls 2>/dev/null | \
        sort -u > "$OUTPUT_DIR/wayback_urls.txt"
    log "Wayback URLs: $(wc -l < "$OUTPUT_DIR/wayback_urls.txt")"
else
    warn "waybackurls not found, skipping..."
    touch "$OUTPUT_DIR/wayback_urls.txt"
fi

# Phase 4: Vulnerability Scanning
info "Phase 4: Scanning for vulnerabilities"

if command -v nuclei &>/dev/null; then
    awk '{print $1}' "$OUTPUT_DIR/live_hosts.txt" | \
        nuclei -silent \
               -severity medium,high,critical \
               -o "$OUTPUT_DIR/nuclei_findings.txt" 2>/dev/null
    log "Nuclei findings: $(wc -l < "$OUTPUT_DIR/nuclei_findings.txt" 2>/dev/null || echo 0)"
else
    warn "nuclei not found, skipping vulnerability scan..."
fi

# Summary
echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}           RECON COMPLETE             ${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
printf "%-20s %s\n" "Target:" "$TARGET"
printf "%-20s %s\n" "Subdomains found:" "$(wc -l < "$OUTPUT_DIR/all_subdomains.txt")"
printf "%-20s %s\n" "Live hosts:" "$(wc -l < "$OUTPUT_DIR/live_hosts.txt" 2>/dev/null || echo 0)"
printf "%-20s %s\n" "URLs collected:" "$(wc -l < "$OUTPUT_DIR/wayback_urls.txt" 2>/dev/null || echo 0)"
printf "%-20s %s\n" "Vuln findings:" "$(wc -l < "$OUTPUT_DIR/nuclei_findings.txt" 2>/dev/null || echo 0)"
printf "%-20s %s\n" "Output directory:" "$OUTPUT_DIR"
echo ""
echo -e "${YELLOW}Review findings in: $OUTPUT_DIR${NC}"
