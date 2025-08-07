#!/usr/bin/env python3
"""
PENTU CLI - Command Line Penetration Testing Toolkit
Lightweight terminal-based penetration testing suite for weak hardware and CLI enthusiasts
Integrating: Nmap, Metasploit, sqlmap, Nikto, Gobuster, Dirb, FFuF, Aircrack-ng, 
John the Ripper, TheHarvester, Enum4linux, and more

Author: Security Research Team
Version: 2.0.0 CLI
Platform: Linux (Optimized for Kali Linux)
WARNING: Use ethically and legally only.
"""

import os
import sys
import subprocess
import argparse
import json
import time
import threading
from datetime import datetime
from pathlib import Path
import socket
import re

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color
    
    @staticmethod
    def print_colored(text, color):
        print(f"{color}{text}{Colors.NC}")
    
    @staticmethod
    def print_banner():
        banner = f"""
{Colors.RED}    ____  ______ _   __ ______ __  __     _______ __    ____
   / __ \\/ ____// | / //_  __// / / /    / ____// /   /  _/
  / /_/ / __/  /  |/ /  / /  / / / /    / /    / /    / /  
 / ____/ /___ / /|  /  / /  / /_/ /    / /___ / /____/ /   
/_/   /_____//_/ |_/  /_/   \\____/     \\____//_____/___/   
                                                           
{Colors.YELLOW}🔥 PENETRATION TESTING CLI ARSENAL 🔥{Colors.NC}
{Colors.CYAN}Lightweight • Fast • Terminal-Based • Resource-Efficient{Colors.NC}
"""
        print(banner)

class PentuCLI:
    def __init__(self):
        self.tools_config = {
            'nmap': {'installed': False, 'path': ''},
            'metasploit': {'installed': False, 'path': ''},
            'sqlmap': {'installed': False, 'path': ''},
            'nikto': {'installed': False, 'path': ''},
            'gobuster': {'installed': False, 'path': ''},
            'dirb': {'installed': False, 'path': ''},
            'ffuf': {'installed': False, 'path': ''},
            'john': {'installed': False, 'path': ''},
            'aircrack-ng': {'installed': False, 'path': ''},
            'theharvester': {'installed': False, 'path': ''},
            'enum4linux': {'installed': False, 'path': ''},
            'masscan': {'installed': False, 'path': ''},
            'hydra': {'installed': False, 'path': ''},
            'wpscan': {'installed': False, 'path': ''},
            'nuclei': {'installed': False, 'path': ''}
        }
        self.results_dir = Path('./pentu-results')
        self.results_dir.mkdir(exist_ok=True)
        
    def check_tools(self):
        """Check availability of penetration testing tools"""
        Colors.print_colored("\n🔍 Checking installed tools...", Colors.BLUE)
        
        for tool in self.tools_config:
            try:
                result = subprocess.run(['which', tool], capture_output=True, text=True)
                if result.returncode == 0:
                    self.tools_config[tool]['installed'] = True
                    self.tools_config[tool]['path'] = result.stdout.strip()
                    Colors.print_colored(f"✅ {tool} - Found at {result.stdout.strip()}", Colors.GREEN)
                else:
                    Colors.print_colored(f"❌ {tool} - Not found", Colors.RED)
            except Exception as e:
                Colors.print_colored(f"❌ {tool} - Error checking: {str(e)}", Colors.RED)
    
    def run_command(self, command, timeout=300):
        """Execute a command with timeout and output capture"""
        try:
            Colors.print_colored(f"\n🚀 Executing: {command}", Colors.YELLOW)
            
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            error_lines = []
            
            # Real-time output display
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    output_lines.append(output.strip())
            
            # Get any remaining output
            stdout, stderr = process.communicate()
            if stdout:
                output_lines.extend(stdout.strip().split('\n'))
            if stderr:
                error_lines.extend(stderr.strip().split('\n'))
            
            return {
                'success': process.returncode == 0,
                'returncode': process.returncode,
                'stdout': '\n'.join(output_lines),
                'stderr': '\n'.join(error_lines)
            }
            
        except subprocess.TimeoutExpired:
            Colors.print_colored(f"⏰ Command timed out after {timeout} seconds", Colors.RED)
            return {'success': False, 'error': 'Timeout'}
        except Exception as e:
            Colors.print_colored(f"❌ Error executing command: {str(e)}", Colors.RED)
            return {'success': False, 'error': str(e)}
    
    def save_results(self, tool_name, target, results):
        """Save scan results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tool_name}_{target.replace('/', '_').replace(':', '_')}_{timestamp}.txt"
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            f.write(f"PENTU CLI - {tool_name.upper()} Results\n")
            f.write(f"Target: {target}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
            f.write("="*60 + "\n\n")
            f.write(results)
        
        Colors.print_colored(f"💾 Results saved to: {filepath}", Colors.GREEN)
        return filepath
    
    def nmap_scan(self, target, scan_type='basic'):
        """Network scanning with Nmap"""
        if not self.tools_config['nmap']['installed']:
            Colors.print_colored("❌ Nmap not installed", Colors.RED)
            return
        
        scan_options = {
            'basic': '-sS -sV -O',
            'stealth': '-sS -f -T2',
            'aggressive': '-A -T4',
            'vuln': '--script=vuln',
            'all_ports': '-p-',
            'udp': '-sU --top-ports=1000',
            'fast': '-F -T5'
        }
        
        options = scan_options.get(scan_type, scan_options['basic'])
        command = f"nmap {options} {target}"
        
        Colors.print_colored(f"\n🎯 Starting Nmap {scan_type} scan on {target}", Colors.CYAN)
        result = self.run_command(command)
        
        if result['success']:
            self.save_results('nmap', target, result['stdout'])
        return result
    
    def web_scan(self, target, tool='nikto'):
        """Web application scanning"""
        if tool == 'nikto' and self.tools_config['nikto']['installed']:
            command = f"nikto -h {target} -Format txt"
        elif tool == 'gobuster' and self.tools_config['gobuster']['installed']:
            wordlist = "/usr/share/wordlists/dirb/common.txt"
            command = f"gobuster dir -u {target} -w {wordlist} -x php,html,txt,js"
        elif tool == 'dirb' and self.tools_config['dirb']['installed']:
            command = f"dirb {target}"
        elif tool == 'ffuf' and self.tools_config['ffuf']['installed']:
            wordlist = "/usr/share/wordlists/dirb/common.txt"
            command = f"ffuf -w {wordlist} -u {target}/FUZZ -fc 404"
        else:
            Colors.print_colored(f"❌ {tool} not available", Colors.RED)
            return
        
        Colors.print_colored(f"\n🌐 Starting {tool} scan on {target}", Colors.CYAN)
        result = self.run_command(command)
        
        if result['success']:
            self.save_results(tool, target, result['stdout'])
        return result
    
    def sql_injection_test(self, target):
        """SQL injection testing with sqlmap"""
        if not self.tools_config['sqlmap']['installed']:
            Colors.print_colored("❌ sqlmap not installed", Colors.RED)
            return
        
        command = f"sqlmap -u '{target}' --batch --level=3 --risk=2"
        
        Colors.print_colored(f"\n💉 Starting SQL injection test on {target}", Colors.CYAN)
        result = self.run_command(command, timeout=600)  # Longer timeout for sqlmap
        
        if result['success']:
            self.save_results('sqlmap', target, result['stdout'])
        return result
    
    def password_attack(self, target, username_list=None, password_list=None, service='ssh'):
        """Password brute force attacks"""
        if not self.tools_config['hydra']['installed']:
            Colors.print_colored("❌ Hydra not installed", Colors.RED)
            return
        
        if not username_list:
            username_list = "/usr/share/wordlists/metasploit/unix_users.txt"
        if not password_list:
            password_list = "/usr/share/wordlists/rockyou.txt.gz"
        
        # Check if wordlists exist
        if not os.path.exists(username_list):
            Colors.print_colored(f"❌ Username list not found: {username_list}", Colors.RED)
            return
        if not os.path.exists(password_list):
            Colors.print_colored(f"❌ Password list not found: {password_list}", Colors.RED)
            return
        
        command = f"hydra -L {username_list} -P {password_list} -t 4 {target} {service}"
        
        Colors.print_colored(f"\n🔓 Starting {service} brute force on {target}", Colors.CYAN)
        result = self.run_command(command, timeout=1800)  # 30 min timeout
        
        if result['success']:
            self.save_results('hydra', target, result['stdout'])
        return result
    
    def wireless_attack(self, interface='wlan0'):
        """Wireless network attacks"""
        if not self.tools_config['aircrack-ng']['installed']:
            Colors.print_colored("❌ Aircrack-ng suite not installed", Colors.RED)
            return
        
        Colors.print_colored(f"\n📡 Starting wireless reconnaissance on {interface}", Colors.CYAN)
        
        # Monitor mode
        Colors.print_colored("Setting interface to monitor mode...", Colors.YELLOW)
        self.run_command(f"sudo airmon-ng start {interface}")
        
        # Scan for networks
        Colors.print_colored("Scanning for wireless networks (30 seconds)...", Colors.YELLOW)
        command = f"timeout 30s airodump-ng {interface}mon"
        result = self.run_command(command)
        
        if result['success']:
            self.save_results('airodump', interface, result['stdout'])
        
        # Stop monitor mode
        self.run_command(f"sudo airmon-ng stop {interface}mon")
        return result
    
    def osint_gathering(self, domain):
        """OSINT information gathering"""
        if not self.tools_config['theharvester']['installed']:
            Colors.print_colored("❌ TheHarvester not installed", Colors.RED)
            return
        
        sources = "google,bing,linkedin,twitter,yahoo"
        command = f"theharvester -d {domain} -b {sources} -l 500"
        
        Colors.print_colored(f"\n🕵️  Starting OSINT gathering for {domain}", Colors.CYAN)
        result = self.run_command(command)
        
        if result['success']:
            self.save_results('theharvester', domain, result['stdout'])
        return result
    
    def vulnerability_scan(self, target):
        """Vulnerability scanning with Nuclei"""
        if not self.tools_config['nuclei']['installed']:
            Colors.print_colored("❌ Nuclei not installed", Colors.RED)
            return
        
        command = f"nuclei -u {target} -severity critical,high,medium"
        
        Colors.print_colored(f"\n🔍 Starting vulnerability scan on {target}", Colors.CYAN)
        result = self.run_command(command)
        
        if result['success']:
            self.save_results('nuclei', target, result['stdout'])
        return result
    
    def show_menu(self):
        """Display main menu"""
        Colors.print_banner()
        print(f"""
{Colors.WHITE}PENTU CLI - Main Menu{Colors.NC}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}

{Colors.GREEN}RECONNAISSANCE & SCANNING{Colors.NC}
  1. Network Scan (Nmap)
  2. Web Application Scan
  3. Vulnerability Scan (Nuclei)
  4. OSINT Gathering

{Colors.YELLOW}EXPLOITATION{Colors.NC}
  5. SQL Injection Test
  6. Password Attacks
  7. Wireless Attacks

{Colors.BLUE}UTILITIES{Colors.NC}
  8. Check Tool Status
  9. View Results
  10. Custom Command

{Colors.RED}OTHER{Colors.NC}
  0. Exit

{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.NC}
""")
    
    def interactive_menu(self):
        """Run interactive menu system"""
        while True:
            self.show_menu()
            try:
                choice = input(f"{Colors.YELLOW}pentu-cli> {Colors.NC}").strip()
                
                if choice == '0':
                    Colors.print_colored("\n👋 Exiting PENTU CLI. Stay secure!", Colors.GREEN)
                    break
                elif choice == '1':
                    self.nmap_menu()
                elif choice == '2':
                    self.web_scan_menu()
                elif choice == '3':
                    target = input("Enter target URL/IP: ").strip()
                    if target:
                        self.vulnerability_scan(target)
                elif choice == '4':
                    domain = input("Enter domain for OSINT: ").strip()
                    if domain:
                        self.osint_gathering(domain)
                elif choice == '5':
                    target = input("Enter target URL with parameter: ").strip()
                    if target:
                        self.sql_injection_test(target)
                elif choice == '6':
                    self.password_attack_menu()
                elif choice == '7':
                    interface = input("Enter wireless interface (default: wlan0): ").strip()
                    if not interface:
                        interface = 'wlan0'
                    Colors.print_colored("⚠️  This requires root privileges!", Colors.YELLOW)
                    confirm = input("Continue? (y/N): ").strip().lower()
                    if confirm == 'y':
                        self.wireless_attack(interface)
                elif choice == '8':
                    self.check_tools()
                elif choice == '9':
                    self.show_results()
                elif choice == '10':
                    self.custom_command()
                else:
                    Colors.print_colored("❌ Invalid choice", Colors.RED)
                
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.NC}")
                
            except KeyboardInterrupt:
                Colors.print_colored("\n\n👋 Exiting PENTU CLI. Stay secure!", Colors.GREEN)
                break
            except EOFError:
                break
    
    def nmap_menu(self):
        """Nmap scanning submenu"""
        print(f"""
{Colors.WHITE}Nmap Scan Types:{Colors.NC}
  1. Basic Scan (-sS -sV -O)
  2. Stealth Scan (-sS -f -T2)
  3. Aggressive Scan (-A -T4)
  4. Vulnerability Scripts (--script=vuln)
  5. All Ports (-p-)
  6. UDP Scan (-sU --top-ports=1000)
  7. Fast Scan (-F -T5)
""")
        
        target = input("Enter target IP/range: ").strip()
        if not target:
            return
            
        scan_choice = input("Choose scan type (1-7): ").strip()
        
        scan_types = {
            '1': 'basic', '2': 'stealth', '3': 'aggressive',
            '4': 'vuln', '5': 'all_ports', '6': 'udp', '7': 'fast'
        }
        
        scan_type = scan_types.get(scan_choice, 'basic')
        self.nmap_scan(target, scan_type)
    
    def web_scan_menu(self):
        """Web scanning submenu"""
        print(f"""
{Colors.WHITE}Web Scanning Tools:{Colors.NC}
  1. Nikto (Vulnerability Scanner)
  2. Gobuster (Directory Bruteforce)
  3. Dirb (Web Content Scanner)
  4. FFuF (Fast Web Fuzzer)
""")
        
        target = input("Enter target URL: ").strip()
        if not target:
            return
            
        tool_choice = input("Choose tool (1-4): ").strip()
        
        tools = {'1': 'nikto', '2': 'gobuster', '3': 'dirb', '4': 'ffuf'}
        tool = tools.get(tool_choice, 'nikto')
        self.web_scan(target, tool)
    
    def password_attack_menu(self):
        """Password attack submenu"""
        print(f"""
{Colors.WHITE}Password Attack Services:{Colors.NC}
  1. SSH
  2. FTP
  3. Telnet
  4. HTTP Basic Auth
  5. Custom Service
""")
        
        target = input("Enter target IP: ").strip()
        if not target:
            return
            
        service_choice = input("Choose service (1-5): ").strip()
        services = {'1': 'ssh', '2': 'ftp', '3': 'telnet', '4': 'http-get', '5': ''}
        
        if service_choice == '5':
            service = input("Enter custom service: ").strip()
        else:
            service = services.get(service_choice, 'ssh')
        
        username_list = input("Username list (Enter for default): ").strip()
        password_list = input("Password list (Enter for default): ").strip()
        
        self.password_attack(target, username_list or None, password_list or None, service)
    
    def show_results(self):
        """Show saved results"""
        results_files = list(self.results_dir.glob('*.txt'))
        
        if not results_files:
            Colors.print_colored("📁 No results found", Colors.YELLOW)
            return
        
        Colors.print_colored(f"\n📋 Found {len(results_files)} result files:", Colors.GREEN)
        for i, file in enumerate(results_files, 1):
            print(f"  {i}. {file.name}")
        
        try:
            choice = int(input("\nEnter file number to view (0 to cancel): "))
            if 1 <= choice <= len(results_files):
                with open(results_files[choice-1], 'r') as f:
                    print(f"\n{Colors.CYAN}{'='*60}{Colors.NC}")
                    print(f.read())
                    print(f"{Colors.CYAN}{'='*60}{Colors.NC}")
        except (ValueError, IndexError):
            Colors.print_colored("❌ Invalid choice", Colors.RED)
    
    def custom_command(self):
        """Execute custom command"""
        Colors.print_colored("⚠️  Custom Command Mode - Use with caution!", Colors.YELLOW)
        command = input("Enter command: ").strip()
        if command:
            result = self.run_command(command)
            if result.get('stdout'):
                save = input("Save output? (y/N): ").strip().lower()
                if save == 'y':
                    self.save_results('custom', 'command', result['stdout'])

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='PENTU CLI - Command Line Penetration Testing Toolkit')
    parser.add_argument('-t', '--target', help='Target IP/URL/Domain')
    parser.add_argument('-m', '--mode', choices=['nmap', 'web', 'sqli', 'osint', 'vuln'], 
                       help='Scan mode')
    parser.add_argument('--scan-type', default='basic', 
                       help='Scan type for nmap (basic, stealth, aggressive, vuln, all_ports, udp, fast)')
    parser.add_argument('--tool', default='nikto', choices=['nikto', 'gobuster', 'dirb', 'ffuf'],
                       help='Web scanning tool')
    parser.add_argument('--check-tools', action='store_true', help='Check installed tools')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    pentu = PentuCLI()
    
    # Check tools on startup
    if args.check_tools:
        pentu.check_tools()
        return
    
    # Interactive mode
    if args.interactive or not any([args.target, args.mode]):
        pentu.interactive_menu()
        return
    
    # Command line mode
    if not args.target:
        Colors.print_colored("❌ Target required for non-interactive mode", Colors.RED)
        return
    
    Colors.print_banner()
    
    if args.mode == 'nmap':
        pentu.nmap_scan(args.target, args.scan_type)
    elif args.mode == 'web':
        pentu.web_scan(args.target, args.tool)
    elif args.mode == 'sqli':
        pentu.sql_injection_test(args.target)
    elif args.mode == 'osint':
        pentu.osint_gathering(args.target)
    elif args.mode == 'vuln':
        pentu.vulnerability_scan(args.target)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Colors.print_colored("\n\n👋 Exiting PENTU CLI. Stay secure!", Colors.GREEN)
        sys.exit(0)
