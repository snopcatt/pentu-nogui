#!/bin/bash
# PENTU CLI Installation Script
# =============================
# Lightweight terminal-based penetration testing toolkit

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art Banner
echo -e "${RED}"
cat << "EOF"
    ____  ______ _   __ ______ __  __     _______ __    ____
   / __ \/ ____// | / //_  __// / / /    / ____// /   /  _/
  / /_/ / __/  /  |/ /  / /  / / / /    / /    / /    / /  
 / ____/ /___ / /|  /  / /  / /_/ /    / /___ / /____/ /   
/_/   /_____//_/ |_/  /_/   \____/     \____//_____/___/   
                                                           
🔥 CLI PENETRATION TESTING ARSENAL 🔥
EOF
echo -e "${NC}"

echo -e "${CYAN}========================================${NC}"
echo -e "${YELLOW}Starting PENTU CLI Installation...${NC}"
echo -e "${CYAN}========================================${NC}\n"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should NOT be run as root${NC}"
   echo -e "${YELLOW}Please run as regular user. Sudo will be used when needed.${NC}"
   exit 1
fi

# Check OS compatibility
echo -e "${BLUE}🔍 Checking system compatibility...${NC}"
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ This installer is designed for Linux systems${NC}"
    exit 1
fi

# Check if Kali Linux
if grep -q "kali" /etc/os-release 2>/dev/null; then
    echo -e "${GREEN}✅ Kali Linux detected - optimal compatibility${NC}"
    KALI_LINUX=true
else
    echo -e "${YELLOW}⚠️  Non-Kali system detected - some tools may need manual installation${NC}"
    KALI_LINUX=false
fi

# Check Python version
echo -e "${BLUE}🐍 Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"
else
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Update system packages
echo -e "${BLUE}📦 Updating system packages...${NC}"
sudo apt update -qq

# Install minimal system dependencies (no GUI packages)
echo -e "${BLUE}🔧 Installing minimal system dependencies...${NC}"
sudo apt install -y python3 python3-pip git curl wget

# Install minimal Python dependencies
echo -e "${BLUE}🐍 Installing minimal Python dependencies...${NC}"
pip3 install -r requirements-cli.txt --user

# Make pentu-cli.py executable
echo -e "${BLUE}🔧 Making PENTU CLI executable...${NC}"
chmod +x pentu-cli.py

# Create symlink for easy access
echo -e "${BLUE}🔗 Creating command alias...${NC}"
CURRENT_DIR=$(pwd)
sudo ln -sf "$CURRENT_DIR/pentu-cli.py" /usr/local/bin/pentu-cli

# Tool availability check
echo -e "${BLUE}🔍 Checking penetration testing tools...${NC}"

declare -A tools=(
    ["nmap"]="Network scanner"
    ["sqlmap"]="SQL injection testing"
    ["nikto"]="Web vulnerability scanner"
    ["gobuster"]="Directory brute forcing"
    ["dirb"]="Web content scanner"
    ["ffuf"]="Fast web fuzzer"
    ["hydra"]="Password brute forcing"
    ["john"]="Password cracking"
    ["aircrack-ng"]="Wireless security"
    ["theharvester"]="OSINT gathering"
    ["enum4linux"]="SMB enumeration"
    ["masscan"]="Fast port scanner"
    ["nuclei"]="Vulnerability scanner"
    ["wpscan"]="WordPress scanner"
)

missing_tools=()

for tool in "${!tools[@]}"; do
    if command -v "$tool" &> /dev/null || dpkg -l | grep -q "$tool" 2>/dev/null; then
        echo -e "${GREEN}✅ $tool - ${tools[$tool]}${NC}"
    else
        echo -e "${RED}❌ $tool - ${tools[$tool]} (missing)${NC}"
        missing_tools+=("$tool")
    fi
done

# Install missing tools on Kali
if [[ ${#missing_tools[@]} -gt 0 ]] && [[ "$KALI_LINUX" == true ]]; then
    echo -e "\n${YELLOW}🔧 Installing missing tools on Kali Linux...${NC}"
    for tool in "${missing_tools[@]}"; do
        echo -e "${BLUE}Installing $tool...${NC}"
        sudo apt install -y "$tool" 2>/dev/null || echo -e "${YELLOW}⚠️  Could not auto-install $tool${NC}"
    done
fi

# Create results directory
echo -e "${BLUE}📁 Setting up results directory...${NC}"
mkdir -p pentu-results

# Set up logging directory
echo -e "${BLUE}📝 Setting up logging...${NC}"
mkdir -p logs
touch logs/pentu-cli.log

# Create CLI-specific documentation
echo -e "${BLUE}📚 Setting up CLI documentation...${NC}"
mkdir -p docs
cat > docs/CLI_GUIDE.md << 'EOF'
# PENTU CLI - Command Line Guide

## Quick Start

### Interactive Mode (Recommended for beginners)
```bash
./pentu-cli.py --interactive
# or
pentu-cli --interactive
```

### Command Line Mode
```bash
# Network scan
pentu-cli -t 192.168.1.1 -m nmap --scan-type aggressive

# Web scan
pentu-cli -t http://example.com -m web --tool nikto

# SQL injection test
pentu-cli -t "http://example.com/page?id=1" -m sqli

# OSINT gathering
pentu-cli -t example.com -m osint

# Vulnerability scan
pentu-cli -t http://example.com -m vuln
```

### Available Scan Types (Nmap)
- `basic`: Standard TCP SYN scan with service detection
- `stealth`: Slow, fragmented scan to avoid detection
- `aggressive`: Full aggressive scan with OS detection
- `vuln`: Vulnerability script scanning
- `all_ports`: Scan all 65535 ports
- `udp`: UDP port scan (top 1000 ports)
- `fast`: Fast scan of common ports

### Available Web Tools
- `nikto`: Web vulnerability scanner
- `gobuster`: Directory and file brute forcing
- `dirb`: Web content scanner
- `ffuf`: Fast web fuzzer

## System Requirements

### Minimal Requirements
- Linux OS (any distribution)
- Python 3.6+
- 512MB RAM
- 100MB disk space

### Recommended Requirements
- Kali Linux (for automatic tool installation)
- Python 3.8+
- 2GB RAM
- 1GB disk space

## Tool Dependencies

The following tools are integrated:
- **nmap**: Network discovery and security auditing
- **sqlmap**: Automatic SQL injection testing
- **nikto**: Web server scanner
- **gobuster**: URI and DNS subdomain brute-forcer
- **dirb**: Web content scanner
- **ffuf**: Fast web fuzzer
- **hydra**: Network logon cracker
- **john**: Password cracker
- **aircrack-ng**: Wireless network security
- **theharvester**: OSINT gathering
- **enum4linux**: SMB enumeration
- **masscan**: Fast internet-wide port scanner
- **nuclei**: Vulnerability scanner
- **wpscan**: WordPress security scanner

## Usage Examples

### Basic Network Discovery
```bash
# Quick scan of local network
pentu-cli -t 192.168.1.0/24 -m nmap --scan-type fast

# Full scan of single host
pentu-cli -t 192.168.1.100 -m nmap --scan-type aggressive
```

### Web Application Testing
```bash
# Vulnerability scan
pentu-cli -t http://target.com -m web --tool nikto

# Directory enumeration
pentu-cli -t http://target.com -m web --tool gobuster

# SQL injection testing
pentu-cli -t "http://target.com/login.php?user=admin" -m sqli
```

### Information Gathering
```bash
# OSINT gathering
pentu-cli -t target.com -m osint

# Vulnerability assessment
pentu-cli -t http://target.com -m vuln
```

## Output and Results

All scan results are automatically saved to the `pentu-results/` directory with timestamps.

Use the interactive menu option "View Results" to browse saved scans.

## Tips for Weak Hardware

1. **Use stealth scans** to reduce CPU usage
2. **Scan smaller ranges** instead of entire networks
3. **Use the fast scan option** for quick reconnaissance
4. **Close unnecessary programs** before running intensive scans
5. **Use command line mode** instead of interactive for scripting

## Legal Notice

⚠️ **IMPORTANT**: Only use PENTU CLI for authorized security testing!

- Obtain proper written authorization before testing
- Respect applicable laws and regulations
- Use responsibly and ethically
- Test only systems you own or have permission to test

## Support

For issues and feature requests, check the main PENTU documentation or create an issue in the repository.
EOF

# Final checks and summary
echo -e "\n${CYAN}========================================${NC}"
echo -e "${GREEN}🎉 PENTU CLI Installation Complete!${NC}"
echo -e "${CYAN}========================================${NC}\n"

echo -e "${PURPLE}📊 Installation Summary:${NC}"
echo -e "✅ PENTU CLI installed to: ${CURRENT_DIR}"
echo -e "✅ Command alias created: pentu-cli"
echo -e "✅ Minimal Python dependencies installed"
echo -e "✅ Results directory created"
echo -e "✅ CLI documentation created"

echo -e "\n${YELLOW}🚀 Quick Start:${NC}"
echo -e "1. Run: ${GREEN}pentu-cli --interactive${NC} (interactive mode)"
echo -e "2. Or: ${GREEN}./pentu-cli.py --interactive${NC}"
echo -e "3. For direct commands: ${GREEN}pentu-cli -t [target] -m [mode]${NC}"
echo -e "4. Check docs/CLI_GUIDE.md for detailed usage"

if [[ ${#missing_tools[@]} -gt 0 ]] && [[ "$KALI_LINUX" != true ]]; then
    echo -e "\n${YELLOW}⚠️  Missing Tools (install manually):${NC}"
    for tool in "${missing_tools[@]}"; do
        echo -e "   - $tool"
    done
fi

echo -e "\n${BLUE}💡 Performance Tips for Weak Hardware:${NC}"
echo -e "• Use 'fast' or 'basic' scan types"
echo -e "• Scan smaller IP ranges"
echo -e "• Run one tool at a time"
echo -e "• Use command line mode for automation"

echo -e "\n${RED}⚠️  IMPORTANT REMINDER:${NC}"
echo -e "${RED}Only use PENTU CLI for authorized security testing!${NC}"
echo -e "${RED}You are responsible for compliance with all applicable laws.${NC}"

echo -e "\n${GREEN}Happy Hacking! 🔥${NC}"
