[source](https://medium.com/@ihouelecaurcy/the-complete-nftables-guide-modern-linux-firewall-mastery-79fb86894d5c)

- [ The Complete nftables Guide: Modern Linux Firewall Mastery](#link_1)
  - [ 🚀 Why nftables? The Evolution Story](#link_2)
  - [ The Old World: Multiple Tools, Multiple Headaches](#link_3)
  - [ The New World: One Tool, Unified Power](#link_4)
  - [ Key Advantages of nftables](#link_5)
  - [ 🏗️ nftables Architecture Deep Dive](#link_6)
  - [ Core Concepts Hierarchy](#link_7)
  - [ Address Families Explained](#link_8)
  - [ Hook Points in Network Stack](#link_9)
  - [ 🔧 Basic nftables Operations](#link_10)
  - [ Installation and Setup](#link_11)
  - [ Essential Commands Structure](#link_12)
  - [ Your First nftables Configuration](#link_13)
  - [ 📚 Tables: The Foundation](#link_14)
  - [ Creating and Managing Tables](#link_15)
  - [ Table Configuration Examples](#link_16)
  - [ ⛓️ Chains: Traffic Flow Control](#link_17)
  - [ Chain Types and Hooks](#link_18)
  - [ Chain Priorities (Execution Order)](#link_19)
  - [ Advanced Chain Examples](#link_20)
  - [ 📏 Rules: The Logic Engine](#link_21)
  - [ Rule Syntax Structure](#link_22)
  - [ Match Expressions](#link_23)
  - [ Statements (Actions)](#link_24)
  - [ 🏢 Practical Configuration Examples](#link_25)
  - [ 1. Basic Home Firewall](#link_26)
  - [ 2. Web Server Configuration](#link_27)
  - [ 3. Enterprise Network Gateway](#link_28)
  - [ 🗃️ Sets and Maps: Data Structures](#link_29)
  - [ Sets: Efficient IP/Port Collections](#link_30)
  - [ Maps: Key-Value Lookups](#link_31)
  - [ Dynamic Set Management](#link_32)
  - [ 🔄 Connection Tracking Deep Dive](#link_33)
  - [ Connection States](#link_34)
  - [ Connection Tracking Helpers](#link_35)
  - [ Advanced Connection Tracking](#link_36)
  - [ 🚦 Traffic Shaping and QoS](#link_37)
  - [ Rate Limiting](#link_38)
  - [ Traffic Classification](#link_39)
  - [ 🔍 Logging and Monitoring](#link_40)
  - [ Comprehensive Logging Setup](#link_41)
  - [ Advanced Logging with JSON](#link_42)
  - [ Monitoring Script Integration](#link_43)
  - [ 🔒 Security-Focused Configurations](#link_44)
  - [ DDoS Protection](#link_45)
  - [ Intrusion Detection Integration](#link_46)
  - [ Geo-blocking Implementation](#link_47)

# The Complete nftables Guide: Modern Linux Firewall Mastery <a name="link_1"></a>

_The definitive guide to nftables — the modern replacement for iptables, ip6tables, arptables, and ebtables. From basic concepts to enterprise-level configurations._

If you’re still using iptables in 2024, you’re missing out on the power and elegance of nftables. This comprehensive guide covers everything you need to master Linux’s modern firewall framework, from fundamental concepts to advanced enterprise configurations.

## 🚀 Why nftables? The Evolution Story <a name="link_2"></a>

## The Old World: Multiple Tools, Multiple Headaches <a name="link_3"></a>

```
#Before nftables - 4 different tools, 4 different syntaxes
iptables -A INPUT -p tcp --dport 22 -j ACCEPT    # IPv4
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT   # IPv6
arptables -A INPUT --source-ip 1.2.3.4 -j ACCEPT # ARP
ebtables -A INPUT -s 00:11:22:33:44:55 -j ACCEPT # Ethernet
```

## The New World: One Tool, Unified Power <a name="link_4"></a>

```
#With nftables - one tool for everything
nft add rule ip filter input tcp dport 22 accept
nft add rule ip6 filter input tcp dport 22 accept
nft add rule arp filter input ip saddr 1.2.3.4 accept
nft add rule bridge filter input ether saddr 00:11:22:33:44:55 accept
```

## Key Advantages of nftables <a name="link_5"></a>

Feature iptables nftables **Performance** Linear rule processing O(n) Optimized lookup O(log n) **Syntax** Complex, inconsistent Clean, unified **IPv4/IPv6** Separate tools Single tool **Sets/Maps** External ipset Built-in **Atomicity** Rule-by-rule Transaction-based **Debugging** Limited Advanced tracing

## 🏗️ nftables Architecture Deep Dive <a name="link_6"></a>

## Core Concepts Hierarchy <a name="link_7"></a>

```
nftables Framework
├── Tables (Container for chains)
│   ├── Chains (Container for rules)
│   │   ├── Rules (Filtering logic)
│   │   └── Expressions (Match conditions)
│   ├── Sets (Efficient data storage)
│   └── Maps (Key-value lookups)
└── Address Families (ip, ip6, inet, arp, bridge, netdev)
```

## Address Families Explained <a name="link_8"></a>

Family Purpose Layer Hooks Available `ip` IPv4 only Layer 3 input, forward, output, prerouting, postrouting `ip6` IPv6 only Layer 3 input, forward, output, prerouting, postrouting `inet` IPv4 + IPv6 Layer 3 input, forward, output, prerouting, postrouting `arp` ARP packets Layer 2.5 input, output `bridge` Ethernet frames Layer 2 input, forward, output, prerouting, postrouting `netdev` Early packet processing Layer 2 ingress, egress

## Hook Points in Network Stack <a name="link_9"></a>

```
NETDEV (ingress)
                      ↓
    ┌─────────────────────────────────────────┐
    │              PREROUTING                 │
    │        (routing decisions)              │
    └─────────────────┬───────────────────────┘
                      ↓
              ┌───────────────┐
              │   ROUTING     │
              │   DECISION    │
              └───────┬───────┘
                      ↓
        ┌─────────────┴─────────────┐
        │                           │
        ↓                           ↓
   ┌─────────┐                 ┌─────────┐
   │  INPUT  │                 │ FORWARD │
   │(local)  │                 │(route)  │
   └────┬────┘                 └────┬────┘
        │                           │
        ↓                           ↓
   ┌─────────┐                 ┌───────────┐
   │ OUTPUT  │                 │POSTROUTING│
   │(local)  │                 │   (NAT)   │
   └────┬────┘                 └────┬──────┘
        │                           │
        └─────────────┬─────────────┘
                      ↓
                ┌─────────────┐
                │POSTROUTING  │
                │   (final)   │
                └─────────────┘
                      ↓
                 NETDEV (egress)
```

## 🔧 Basic nftables Operations <a name="link_10"></a>

## Installation and Setup <a name="link_11"></a>

```bash
#Install nftables (most modern distros include it)
#Debian/Ubuntu
sudo apt update && sudo apt install nftables
```

```bash
#CentOS/RHEL/Fedora
sudo dnf install nftables# Enable and start
sudo systemctl enable nftables
sudo systemctl start nftables# Check version
nft --version
```

## Essential Commands Structure <a name="link_12"></a>

```
#Basic command structure
nft [options] command [family] [table] [chain] [rule]
```

```bash
#Examples:
nft list ruleset                    # List everything
nft add table ip filter             # Add table
nft add chain ip filter input       # Add chain
nft add rule ip filter input accept # Add rule
```

## Your First nftables Configuration <a name="link_13"></a>

```
#!/usr/bin/nft -f

#Clear everything
flush ruleset# Create basic IPv4 firewall
table ip filter {
    # Define chains with their properties
    chain input {
        type filter hook input priority 0; policy drop;

        # Allow loopback
        iif lo accept

        # Allow established connections
        ct state established,related accept

        # Allow SSH
        tcp dport 22 accept
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

## 📚 Tables: The Foundation <a name="link_14"></a>

## Creating and Managing Tables <a name="link_15"></a>

```bash
#Create tables for different address families
nft add table ip filter          # IPv4 table
nft add table ip6 filter         # IPv6 table
nft add table inet filter        # Dual-stack table
nft add table arp filter         # ARP table
nft add table bridge filter      # Bridge table
```

```bash
#List tables
nft list tables# List specific table
nft list table ip filter# Delete table (removes all chains and rules)
nft delete table ip filter# Flush table (removes rules but keeps structure)
nft flush table ip filter
```

## Table Configuration Examples <a name="link_16"></a>

```
#Complete table with multiple chains
table ip filter {
    # Input chain for incoming packets
    chain input {
        type filter hook input priority 0; policy drop;
        # Rules go here
    }

    # Forward chain for routed packets
    chain forward {
        type filter hook forward priority 0; policy drop;
        # Rules go here
    }

    # Output chain for outgoing packets
    chain output {
        type filter hook output priority 0; policy accept;
        # Rules go here
    }

    # Custom chain (no hook, called from other chains)
    chain custom_ssh {
        tcp dport 22 limit rate 3/minute accept
        log prefix "SSH attempt: " drop
    }
}

```

## ⛓️ Chains: Traffic Flow Control <a name="link_17"></a>

## Chain Types and Hooks <a name="link_18"></a>

```
#Filter chains (most common)
chain input {
    type filter hook input priority 0; policy drop;
}

#NAT chains
chain prerouting {
    type nat hook prerouting priority -100;
}chain postrouting {
    type nat hook postrouting priority 100;
}# Route chains (modify routing decisions)
chain output {
    type route hook output priority -150;
}
```

## Chain Priorities (Execution Order) <a name="link_19"></a>

Priority Typical Use Example -400 Connection tracking `ct helper` -300 Raw table equivalent `notrack` -225 SELinux operations `selinux` -200 Connection tracking `ct state` -150 Mangle operations `mangle` -100 DNAT `dnat to` 0 Filter operations Standard filtering 100 SNAT `snat to`, `masquerade` 300 Security operations `reject`, `drop`

## Advanced Chain Examples <a name="link_20"></a>

```
table inet filter {
    # Base chain with connection tracking
    chain input {
        type filter hook input priority 0; policy drop;

        # Connection state handling
        ct state invalid drop
        ct state established,related accept

        # Jump to custom chains
        tcp dport 22 jump ssh-rules
        tcp dport { 80, 443 } jump web-rules

        # Final catch-all
        log prefix "Dropped: " drop
    }

    # Custom chain for SSH rules
    chain ssh-rules {
        # Rate limiting
        limit rate 3/minute accept

        # Log excessive attempts
        log prefix "SSH brute force: "
        drop
    }

    # Custom chain for web traffic
    chain web-rules {
        # Allow HTTP/HTTPS
        accept
    }

    # Output chain (usually permissive)
    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

## 📏 Rules: The Logic Engine <a name="link_21"></a>

## Rule Syntax Structure <a name="link_22"></a>

```bash
#Basic syntax
nft add rule [family] [table] [chain] [matches] [statements]
```

```bash
#Examples with different components
nft add rule ip filter input tcp dport 22 accept
nft add rule ip filter input ip saddr 192.168.1.0/24 tcp dport 80 counter accept
nft add rule ip filter input ct state established,related counter accept
```

## Match Expressions <a name="link_23"></a>

```bash
#Protocol matching
tcp dport 22              # TCP destination port
udp sport 53              # UDP source port
icmp type echo-request    # ICMP type
ip protocol tcp           # IP protocol
```

```bash
#Address matching
ip saddr 192.168.1.0/24          # Source IP range
ip daddr != 10.0.0.0/8           # Destination IP (not)
ip saddr { 1.2.3.4, 5.6.7.8 }    # Multiple IPs# Interface matching
iif eth0                  # Input interface
oif "wlan*"              # Output interface (wildcard)
iifname "docker0"        # Interface by name# Connection tracking
ct state established     # Connection state
ct state new,related     # Multiple states
ct direction original    # Connection direction# Time-based matching
meta hour "09:00"-"17:00"        # Time range
meta day { "Monday", "Friday" }   # Specific days# Packet properties
meta length 40-100       # Packet size range
meta mark 0x123         # Packet mark
meta priority 0         # Priority
```

## Statements (Actions) <a name="link_24"></a>

```
#Basic actions
accept                   # Allow packet
drop                    # Silent drop
reject                  # Send rejection
return                  # Return to calling chain

#Logging
log                     # Basic logging
log prefix "SSH: "      # With prefix
log level emerg         # Log level# Counters and statistics
counter                 # Count packets/bytes
counter packets 100 bytes 8000  # Set initial values# Target modification
snat to 1.2.3.4         # Source NAT
dnat to 192.168.1.10    # Destination NAT
masquerade              # Dynamic SNAT# Packet modification
meta mark set 0x123     # Set packet mark
meta priority set 0     # Set priority# Rate limiting
limit rate 10/minute    # Basic rate limiting
limit rate over 100/minute drop  # Burst protection# Advanced actions
queue                   # Send to userspace
dup to device eth1      # Duplicate packet
```

## 🏢 Practical Configuration Examples <a name="link_25"></a>

## 1. Basic Home Firewall <a name="link_26"></a>

```
#!/usr/bin/nft -f

flush rulesettable inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Allow loopback
        iif lo accept

        # Allow established connections
        ct state established,related accept

        # Allow SSH with rate limiting
        tcp dport 22 limit rate 3/minute accept

        # Allow web browsing responses
        tcp sport { 80, 443 } ct state established accept

        # Allow ping
        icmp type echo-request limit rate 5/second accept
        icmpv6 type { echo-request, nd-neighbor-solicit, nd-neighbor-advert } accept

        # Log and drop everything else
        log prefix "Dropped: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
```

## 2. Web Server Configuration <a name="link_27"></a>

```
#!/usr/bin/nft -f

flush rulesettable inet filter {
    # Define sets for efficiency
    set admin_ips {
        type ipv4_addr
        elements = { 192.168.1.100, 10.0.0.50 }
    }

    set web_ports {
        type inet_service
        elements = { 80, 443, 8080, 8443 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Basic allows
        iif lo accept
        ct state invalid drop
        ct state established,related accept

        # SSH only from admin IPs
        ip saddr @admin_ips tcp dport 22 accept

        # Web services
        tcp dport @web_ports accept

        # ICMP
        icmp type echo-request limit rate 5/second accept
        icmpv6 type { echo-request, nd-neighbor-solicit, nd-neighbor-advert } accept

        # Rate limiting for web services
        tcp dport @web_ports ct state new limit rate 100/second accept

        # DDoS protection
        tcp flags syn tcp dport @web_ports meter ddos_protection { ip saddr limit rate 10/second } accept

        # Log suspicious activity
        log prefix "Suspicious: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}# NAT table for port redirection
table ip nat {
    chain prerouting {
        type nat hook prerouting priority -100;

        # Redirect HTTP to HTTPS
        tcp dport 80 redirect to :443
    }
}
```

## 3. Enterprise Network Gateway <a name="link_28"></a>

```
#!/usr/bin/nft -f

flush ruleset# Main filter table
table inet filter {
    # Network definitions
    set internal_nets {
        type ipv4_addr
        flags interval
        elements = { 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12 }
    }

    set dmz_servers {
        type ipv4_addr
        elements = { 10.1.0.10, 10.1.0.11, 10.1.0.12 }
    }

    set blocked_countries {
        type ipv4_addr
        flags interval
        # Would be populated with country IP ranges
    }

    # Custom chains for organization
    chain wan_input {
        # WAN interface rules
        tcp dport { 80, 443 } dnat to 10.1.0.10
        tcp dport 25 dnat to 10.1.0.11
        drop
    }

    chain lan_forward {
        # LAN to Internet rules
        ip saddr @internal_nets accept

        # Block known bad destinations
        ip daddr @blocked_countries reject

        # Web filtering
        tcp dport { 80, 443 } jump web_filter

        accept
    }

    chain web_filter {
        # Content filtering logic
        # This would integrate with external tools
        accept
    }

    # Main chains
    chain input {
        type filter hook input priority 0; policy drop;

        iif lo accept
        ct state established,related accept

        # Management access
        iifname "eth0" jump wan_input
        iifname "eth1" ip saddr @internal_nets accept

        # ICMP
        icmp type echo-request limit rate 5/second accept

        log prefix "INPUT-DROP: " drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;

        ct state established,related accept

        # Route based on source
        iifname "eth1" jump lan_forward
        iifname "eth0" ip daddr @dmz_servers accept

        log prefix "FORWARD-DROP: " drop
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}# NAT table for internet sharing
table ip nat {
    chain prerouting {
        type nat hook prerouting priority -100;

        # Port forwarding to DMZ
        iifname "eth0" tcp dport 80 dnat to 10.1.0.10:80
        iifname "eth0" tcp dport 443 dnat to 10.1.0.10:443
        iifname "eth0" tcp dport 25 dnat to 10.1.0.11:25
    }

    chain postrouting {
        type nat hook postrouting priority 100;

        # Masquerading for internal networks
        oifname "eth0" ip saddr @internal_nets masquerade
    }
}
```

## 🗃️ Sets and Maps: Data Structures <a name="link_29"></a>

## Sets: Efficient IP/Port Collections <a name="link_30"></a>

```
#Create different types of sets
table ip filter {
    # Simple IP set
    set blacklist {
        type ipv4_addr
        elements = { 192.168.1.100, 192.168.1.101 }
    }

    # Port set
    set web_ports {
        type inet_service
        elements = { 80, 443, 8080, 8443 }
    }

    # IP range set with intervals
    set private_nets {
        type ipv4_addr
        flags interval
        elements = { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 }
    }

    # Timeout set (dynamic, auto-expiring)
    set rate_limit {
        type ipv4_addr
        timeout 1h
        size 10000
    }

    # Using sets in rules
    chain input {
        type filter hook input priority 0; policy drop;

        # Block blacklisted IPs
        ip saddr @blacklist drop

        # Allow web ports
        tcp dport @web_ports accept

        # Allow internal networks
        ip saddr @private_nets accept
    }
}
```

## Maps: Key-Value Lookups <a name="link_31"></a>

```
table ip nat {
    # Port redirection map
    map port_redirect {
        type inet_service : ipv4_addr . inet_service
        elements = {
            80 : 192.168.1.10 . 8080,
            443 : 192.168.1.10 . 8443,
            25 : 192.168.1.11 . 25
        }
    }

    # QoS marking map
    map qos_marks {
        type ipv4_addr : mark
        elements = {
            192.168.1.10 : 0x1,  # High priority
            192.168.1.20 : 0x2,  # Medium priority
            192.168.1.30 : 0x3   # Low priority
        }
    }

    chain prerouting {
        type nat hook prerouting priority -100;

        # Use map for port redirection
        tcp dport map @port_redirect dnat to

        # QoS marking
        meta mark set ip saddr map @qos_marks
    }
}
```

## Dynamic Set Management <a name="link_32"></a>

```bash
#Add elements to sets at runtime
nft add element ip filter blacklist { 192.168.1.200 }

#Add multiple elements
nft add element ip filter blacklist { 192.168.1.201, 192.168.1.202 }# Delete elements
nft delete element ip filter blacklist { 192.168.1.200 }# List set contents
nft list set ip filter blacklist# Timeout elements (auto-remove after time)
nft add element ip filter rate_limit { 192.168.1.100 timeout 30m }# Flush all elements from set
nft flush set ip filter blacklist
```

## 🔄 Connection Tracking Deep Dive <a name="link_33"></a>

## Connection States <a name="link_34"></a>

```
#Available connection states
ct state new           # First packet of new connection
ct state established   # Packets of established connection
ct state related       # Related to existing connection (FTP data)
ct state invalid       # Invalid packets
ct state untracked     # Not tracked

#Practical examples
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Drop invalid packets immediately
        ct state invalid counter drop

        # Allow established connections
        ct state established,related counter accept

        # Handle new connections
        ct state new tcp dport { 22, 80, 443 } counter accept

        # Everything else drops
        counter drop
    }
}
```

## Connection Tracking Helpers <a name="link_35"></a>

```
#FTP helper for data connections
table inet filter {
    chain prerouting {
        type filter hook prerouting priority -200;

        # Enable FTP helper
        tcp dport 21 ct helper set "ftp"
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Allow FTP control
        tcp dport 21 ct state new accept

        # Allow FTP data (marked as related by helper)
        ct state related accept
    }
}
```

## Advanced Connection Tracking <a name="link_36"></a>

```
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Connection direction
        ct direction original accept
        ct direction reply accept

        # Connection mark handling
        ct mark 0x123 accept

        # Connection labels (for complex state)
        ct label "web_conn" accept

        # Conntrack zones (namespace separation)
        ct zone 1 accept
    }
}
```

## 🚦 Traffic Shaping and QoS <a name="link_37"></a>

## Rate Limiting <a name="link_38"></a>

```
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # Basic rate limiting
        tcp dport 22 limit rate 3/minute accept

        # Burst handling
        tcp dport 80 limit rate 100/second burst 200 packets accept

        # Per-source rate limiting with meters
        tcp dport 80 meter http_rate { ip saddr limit rate 10/second } accept

        # Rate limiting with logging
        tcp dport 22 limit rate 5/minute accept
        tcp dport 22 log prefix "SSH rate limit exceeded: " drop
    }
}
```

## Traffic Classification <a name="link_39"></a>

```
table inet mangle {
    # QoS map for different traffic types
    map dscp_map {
        type inet_service : dscp
        elements = {
            22 : cs6,      # SSH - high priority
            80 : af21,     # HTTP - normal
            443 : af21,    # HTTPS - normal
            25 : af11      # SMTP - low priority
        }
    }

    chain postrouting {
        type filter hook postrouting priority -150;

        # Mark packets based on destination port
        ip dscp set tcp dport map @dscp_map

        # Alternative: mark based on source
        ip saddr 192.168.1.10 meta priority set 1
        ip saddr 192.168.1.20 meta priority set 2
    }
}
```

## 🔍 Logging and Monitoring <a name="link_40"></a>

## Comprehensive Logging Setup <a name="link_41"></a>

```
table inet filter {
    # Logging chain
    chain log_and_drop {
        limit rate 5/minute log prefix "DROPPED: " level warn
        counter drop
    }

    chain log_and_accept {
        log prefix "ACCEPTED: " level info
        counter accept
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Allow known good traffic
        ct state established,related counter accept
        iif lo accept

        # Log SSH attempts
        tcp dport 22 log prefix "SSH attempt from: " accept

        # Log web traffic (sample only)
        tcp dport { 80, 443 } limit rate 1/minute log prefix "WEB: "
        tcp dport { 80, 443 } accept

        # Log everything else before dropping
        jump log_and_drop
    }
}
```

## Advanced Logging with JSON <a name="link_42"></a>

```
#Configure structured logging
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;

        # JSON-formatted logs
        tcp dport 22 log prefix '{"event":"ssh_attempt","src":"' \
                       log suffix '","dst":"local","action":"accept"}' accept

        # Rate-limited verbose logging
        limit rate 1/minute log prefix "DETAILED: " \
                            flags all level debug accept
    }
}
```

## Monitoring Script Integration <a name="link_43"></a>

```bash
#!/bin/bash
#nftables monitoring script

#Real-time rule statistics
watch_rules() {
    watch -n 2 'nft list ruleset | grep counter'
}
#Connection tracking statistics
watch_conntrack() {
    watch -n 1 '
    echo "=== Connection Tracking Stats ==="
    echo "Active: $(cat /proc/net/nf_conntrack | wc -l)"
    echo "Max: $(cat /proc/sys/net/netfilter/nf_conntrack_max)"
    echo
    echo "=== Top Connections ==="
    cat /proc/net/nf_conntrack | awk "{print \$1, \$3}" | sort | uniq -c | sort -nr | head -10
    '
}
#Log analysis
analyze_logs() {
    echo "=== nftables Log Analysis ==="

    # SSH attempts
    echo "SSH attempts in last hour:"
    grep "$(date --date='1 hour ago' '+%b %d %H')" /var/log/messages | \
    grep "SSH attempt" | wc -l

    # Dropped packets by source
    echo -e "\nTop dropped sources:"
    grep "DROPPED:" /var/log/messages | \
    awk '{print $NF}' | sort | uniq -c | sort -nr | head -10
}case "$1" in
    rules) watch_rules ;;
    conntrack) watch_conntrack ;;
    logs) analyze_logs ;;
    *) echo "Usage: $0 {rules|conntrack|logs}" ;;
esac
```

## 🔒 Security-Focused Configurations <a name="link_44"></a>

## DDoS Protection <a name="link_45"></a>

```
table inet filter {
    # Rate limiting sets
    set syn_flood_limit {
        type ipv4_addr
        timeout 1m
        size 10000
    }

    set ddos_protection {
        type ipv4_addr
        timeout 10m
        size 10000
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Basic flood protection
        tcp flags syn meter syn_rate { ip saddr limit rate 10/second } accept
        tcp flags syn add @syn_flood_limit { ip saddr timeout 1m } drop

        # Connection limit per IP
        tcp dport { 80, 443 } meter connections { ip saddr ct count over 20 } drop

        # Packet size anomaly detection
        meta length > 1000 tcp flags syn drop

        # Fragment attack protection
        ip protocol tcp ip fragoff & 0x1fff != 0 drop

        # Bogus TCP flags
        tcp flags & (fin|syn|rst|psh|ack|urg) == fin|syn|rst|psh|ack|urg drop
        tcp flags & (fin|syn|rst|psh|ack|urg) == 0 drop

        # XMAS and NULL scans
        tcp flags & (fin|syn|rst|psh|ack|urg) == fin|syn|rst|ack|urg drop
        tcp flags & (fin|syn|rst|psh|ack|urg) == syn|rst drop
    }
}
```

## Intrusion Detection Integration <a name="link_46"></a>

```
table inet filter {
    # Suspicious activity detection
    set port_scanners {
        type ipv4_addr
        timeout 1h
        size 10000
    }

    set brute_force_ips {
        type ipv4_addr
        timeout 24h
        size 10000
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Block known bad actors
        ip saddr @port_scanners drop
        ip saddr @brute_force_ips drop

        # Detect port scanning
        tcp flags syn meter port_scan { ip saddr and 255.255.255.0 limit rate 5/second burst 10 packets } accept
        tcp flags syn add @port_scanners { ip saddr }
        tcp flags syn log prefix "Port scan detected: " drop

        # SSH brute force detection
        tcp dport 22 ct state new meter ssh_attempts { ip saddr limit rate 3/minute } accept
        tcp dport 22 ct state new add @brute_force_ips { ip saddr }
        tcp dport 22 ct state new log prefix "SSH brute force: " drop

        # Legitimate traffic
        ct state established,related accept
        tcp dport { 80, 443 } accept
    }
}
```

## Geo-blocking Implementation <a name="link_47"></a>

```
#!/usr/bin/nft -f

#This would typically load country IP ranges from external files
define CHINA_IPS = { 1.2.4.0/22, 1.2.8.0/21 }  # Simplified example
define RUSSIA_IPS = { 5.8.8.0/21, 5.8.16.0/20 }  # Simplified example

table inet filter {
    set blocked_countries {
        type ipv4_addr
        flags interval
        elements = { $CHINA_IPS, $RUSSIA_IPS }
    }

    set allowed_countries {
        type ipv4_addr
        flags interval
        # Would contain allowed country ranges
    }

    chain input {
        type filter hook input priority 0; policy drop;

        # Allow internal networks
        ip saddr { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 } accept

        # Block specific countries
        ip saddr @blocked_countries log prefix "Geo-blocked: " drop

        # Only allow from specific countries (if whitelist mode)
        # ip saddr @
```
