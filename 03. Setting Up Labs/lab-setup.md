# 🧪 Detailed Lab Setup Guide

## Virtual Machine Setup (Recommended)

### Why Use a VM?
- Isolated from your host machine
- Snapshots let you restore quickly
- Simulate different OS environments
- Safe to install malicious tools

### Recommended VM Software
- **VirtualBox** (free): virtualbox.org
- **VMware Workstation** (paid): vmware.com
- **UTM** (Mac ARM): mac.getutm.app

### Recommended OS for Pentesting
- **Kali Linux** — most tools pre-installed
- **Parrot OS** — lighter than Kali
- **Ubuntu** — clean slate, install what you need

## Complete Kali Linux Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y \
    burpsuite \
    nmap \
    nikto \
    sqlmap \
    gobuster \
    ffuf \
    hydra \
    john \
    hashcat \
    metasploit-framework \
    git \
    python3 \
    python3-pip \
    curl \
    wget \
    jq

# Install Go tools
sudo apt install -y golang
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Install subfinder
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Install httpx
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Install nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Install amass
go install -v github.com/owasp-amass/amass/v4/...@master

# Install waybackurls
go install github.com/tomnomnom/waybackurls@latest

# Install gau
go install github.com/lc/gau/v2/cmd/gau@latest
```

## Docker Lab Setup

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Run all labs
docker run -d --name dvwa -p 8080:80 vulnerables/web-dvwa
docker run -d --name juiceshop -p 3000:3000 bkimminich/juice-shop
docker run -d --name webgoat -p 8081:8080 webgoat/webgoat-8.0

# Check running containers
docker ps

# Stop labs when done
docker stop dvwa juiceshop webgoat

# Start labs again
docker start dvwa juiceshop webgoat
```

## Burp Suite Configuration

### Essential Burp Settings

```
1. Set Java heap size: -Xmx2048m
2. Enable dark mode (optional but easier on eyes)
3. Configure scope to avoid testing unintended targets
4. Set up project files to save work
```

### Burp Extensions (free)

| Extension | Purpose |
|-----------|---------|
| **Retire.js** | Find vulnerable JS libraries |
| **Param Miner** | Discover hidden parameters |
| **Autorize** | Test authorization issues |
| **JWT Editor** | Analyze/modify JWT tokens |
| **Software Vulnerability Scanner** | CVE lookup |
| **Turbo Intruder** | High-speed fuzzing |

### Useful Burp Shortcuts

```
Ctrl+I     → Send to Intruder
Ctrl+R     → Send to Repeater
Ctrl+S     → Save project
Ctrl+Z     → Undo
F12        → Toggle intercept
```

## TryHackMe Setup

```
1. Create account at tryhackme.com
2. Download OpenVPN config file
3. Connect to VPN:
   sudo openvpn username.ovpn
4. Access machine IPs through VPN
5. Start beginner path: "Pre-Security" or "Jr Penetration Tester"
```

## HackTheBox Setup

```
1. Create account at hackthebox.com
2. Complete entry challenge (tests basic hacking skills)
3. Download VPN config
4. Connect: sudo openvpn hackthebox.ovpn
5. Start with "Starting Point" machines for beginners
```

## Wordlists

```bash
# Install SecLists (essential wordlist collection)
git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists

# Common wordlist locations in Kali
/usr/share/wordlists/rockyou.txt          # Passwords
/usr/share/wordlists/dirb/common.txt      # Directories
/opt/SecLists/Discovery/DNS/              # Subdomains
/opt/SecLists/Discovery/Web-Content/      # Web paths
/opt/SecLists/Fuzzing/                    # Fuzzing payloads
```
