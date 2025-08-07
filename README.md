# PENTU CLI - Command Line Penetration Testing Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux-green.svg)](https://www.linux.org/)
[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org/)
[![Terminal](https://img.shields.io/badge/Interface-Terminal-black.svg)](https://en.wikipedia.org/wiki/Command-line_interface)

## 🔥 Lightweight Terminal-Based Penetration Testing Arsenal

PENTU CLI is a streamlined, command-line version of the PENTU penetration testing toolkit, specifically designed for:

- **Weak Hardware**: Minimal resource usage, no GUI overhead
- **Terminal Enthusiasts**: Pure command-line interface
- **Headless Systems**: Perfect for servers and remote systems
- **Script Automation**: Easy integration into automation workflows
- **Resource Constraints**: Runs on systems with limited RAM/CPU

---

## ✨ Features

### 🎯 **Core Capabilities**
- **Network Scanning**: Comprehensive Nmap integration
- **Web Application Testing**: Nikto, Gobuster, Dirb, FFuF
- **SQL Injection Testing**: sqlmap automation
- **Password Attacks**: Hydra brute force capabilities
- **Wireless Security**: Aircrack-ng suite integration
- **OSINT Gathering**: TheHarvester and reconnaissance tools
- **Vulnerability Scanning**: Nuclei and custom scripts

### ⚡ **Performance Optimized**
- **Minimal Dependencies**: Only essential Python libraries
- **Low Memory Usage**: < 50MB RAM typical usage
- **Fast Startup**: No GUI initialization overhead
- **Efficient Processing**: Streamlined command execution
- **Resource-Aware**: Automatic adjustment for weak hardware

### 🛠️ **User-Friendly**
- **Interactive Menu**: Guided menu system for beginners
- **Command Line Mode**: Direct command execution for experts
- **Auto-Save Results**: All scans automatically saved with timestamps
- **Real-time Output**: Live command output and progress
- **Tool Status Check**: Automatic detection of installed tools

---

## 📋 System Requirements

### 🟢 **Minimal Requirements**
- **OS**: Any Linux distribution
- **Python**: 3.6 or newer
- **RAM**: 512MB minimum
- **Storage**: 100MB free space
- **Network**: Internet connection for tool updates

### 🔵 **Recommended Requirements**
- **OS**: Kali Linux (for automatic tool installation)
- **Python**: 3.8 or newer
- **RAM**: 2GB for optimal performance
- **Storage**: 1GB for results and logs
- **Network**: Stable connection for external scans

---

## 🚀 Quick Installation

### **Automatic Installation (Recommended)**
```bash
# Clone or download PENTU
git clone https://github.com/your-repo/PENTU.git
cd PENTU

# Run CLI installer
./install-cli.sh
```

### **Manual Installation**
```bash
# Install minimal dependencies
pip3 install -r requirements-cli.txt --user

# Make executable
chmod +x pentu-cli.py

# Create symlink (optional)
sudo ln -sf $(pwd)/pentu-cli.py /usr/local/bin/pentu-cli
```

---

## 💻 Usage Examples

### **Interactive Mode (Beginner-Friendly)**
```bash
# Start interactive menu
./pentu-cli.py --interactive
# or if symlink created
pentu-cli --interactive
```

### **Direct Command Mode (Advanced)**
```bash
# Network scanning
pentu-cli -t 192.168.1.100 -m nmap --scan-type aggressive

# Web application testing
pentu-cli -t http://example.com -m web --tool nikto

# SQL injection testing
pentu-cli -t "http://example.com/page?id=1" -m sqli

# OSINT gathering
pentu-cli -t example.com -m osint

# Vulnerability scanning
pentu-cli -t http://example.com -m vuln

# Check installed tools
pentu-cli --check-tools
```

### **Scan Types Available**

#### **Network Scanning (Nmap)**
- `basic`: Standard TCP SYN scan with service detection
- `stealth`: Slow, fragmented scan to avoid detection
- `aggressive`: Full aggressive scan with OS detection
- `vuln`: Vulnerability script scanning
- `all_ports`: Scan all 65535 ports
- `udp`: UDP port scan (top 1000 ports)  
- `fast`: Fast scan of common ports

#### **Web Application Testing**
- `nikto`: Comprehensive web vulnerability scanner
- `gobuster`: Directory and file brute forcing
- `dirb`: Web content scanner with wordlists
- `ffuf`: Fast web fuzzer with customizable options

---

## 🛠️ Integrated Tools

| Tool | Purpose | Auto-Install (Kali) |
|------|---------|---------------------|
| **nmap** | Network discovery and security auditing | ✅ |
| **sqlmap** | Automatic SQL injection testing | ✅ |
| **nikto** | Web server vulnerability scanner | ✅ |
| **gobuster** | URI and DNS subdomain brute-forcer | ✅ |
| **dirb** | Web content scanner | ✅ |
| **ffuf** | Fast web fuzzer | ✅ |
| **hydra** | Network logon cracker | ✅ |
| **john** | Password cracker | ✅ |
| **aircrack-ng** | Wireless network security suite | ✅ |
| **theharvester** | OSINT information gathering | ✅ |
| **enum4linux** | SMB enumeration tool | ✅ |
| **masscan** | Fast internet-wide port scanner | ✅ |
| **nuclei** | Vulnerability scanner | ✅ |
| **wpscan** | WordPress security scanner | ✅ |

---

## 📊 Performance Comparison

| Aspect | PENTU CLI | PENTU GUI | Improvement |
|--------|-----------|-----------|-------------|
| **Memory Usage** | ~30-50MB | ~200-400MB | **75% Less** |
| **Startup Time** | <2 seconds | 5-10 seconds | **80% Faster** |
| **CPU Usage** | Minimal | Moderate | **60% Less** |
| **Storage** | ~100MB | ~500MB+ | **80% Less** |
| **Remote Access** | Perfect | Requires X11 | **SSH Ready** |

---

## 📁 Output and Results

All scan results are automatically saved to:
```
./pentu-results/
├── nmap_192.168.1.100_20240806_143022.txt
├── nikto_example.com_20240806_143155.txt
├── sqlmap_target_url_20240806_143301.txt
└── ...
```

Use the interactive menu option **"View Results"** to browse saved scans.

---

## 💡 Tips for Weak Hardware

### **Optimize Performance**
1. **Use stealth scans** (`--scan-type stealth`) to reduce CPU usage
2. **Scan smaller ranges** instead of entire networks
3. **Use fast scan option** (`--scan-type fast`) for quick reconnaissance  
4. **Close unnecessary programs** before running intensive scans
5. **Use command line mode** instead of interactive for scripting

### **Memory Management**
- Run one tool at a time
- Use basic scan types for initial reconnaissance
- Clear results regularly to save disk space
- Monitor system resources with `htop`

### **Network Considerations**
- Use slower timing templates for network scans
- Avoid aggressive scans on weak network connections
- Schedule intensive scans during off-peak hours
- Use UDP scans sparingly

---

## 🔒 Legal and Ethical Usage

### ⚠️ **IMPORTANT DISCLAIMER**
- **Authorization Required**: Only test systems you own or have explicit written permission to test
- **Legal Compliance**: Ensure compliance with all local, state, and federal laws
- **Ethical Guidelines**: Follow responsible disclosure practices
- **Professional Use**: Obtain proper certifications and training

### 📜 **Best Practices**
- Always get written authorization before testing
- Respect scope limitations and testing windows
- Document all testing activities
- Report vulnerabilities responsibly
- Use appropriate testing methodologies

---

## 🤝 Support and Community

### **Getting Help**
- Check the `docs/CLI_GUIDE.md` for detailed documentation
- Review example commands and use cases
- Use `--help` flag for command-line options
- Check tool status with `--check-tools`

### **Troubleshooting**
- Ensure all dependencies are installed
- Check tool availability with interactive menu option 8
- Verify network connectivity for external scans
- Review logs in `logs/pentu-cli.log`

---

## 📈 Changelog

### **Version 2.0.0 CLI**
- Initial CLI-only release
- Lightweight terminal interface
- Optimized for weak hardware
- Full tool integration
- Auto-save results functionality
- Interactive and command-line modes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 Why Choose PENTU CLI?

### **For Resource-Constrained Environments**
- Perfect for older hardware or virtual machines with limited resources
- Runs efficiently on Raspberry Pi and similar single-board computers
- Ideal for penetration testing labs with budget constraints

### **For Command-Line Enthusiasts** 
- Pure terminal experience without GUI overhead
- Easy integration into existing command-line workflows
- Perfect for automation and scripting scenarios

### **For Remote and Headless Systems**
- Works perfectly over SSH connections
- No X11 forwarding or VNC required
- Ideal for cloud instances and remote servers

### **For Professional Use**
- Clean, professional output suitable for reports
- Automatic result saving and organization
- Consistent interface across all tools

---

**🔥 Ready to start? Run `./install-cli.sh` and begin your lightweight penetration testing journey!**

*Remember: Use responsibly and ethically. Happy hacking!* 🛡️
