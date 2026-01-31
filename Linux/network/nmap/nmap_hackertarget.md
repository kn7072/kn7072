[source](https://hackertarget.com/nmap-cheatsheet-a-quick-reference-guide/)

# Nmap Cheat Sheet

Nmap has a lot of options and the syntax can feel daunting at first. This Nmap cheatsheet gives you practical example commands for running Nmap and getting the most from this network scanner.

**Current Version**:This Cheat Sheet was Updated in 2025 to reflect Nmap 7.96 (Released May 2025) which brings parallel DNS resolution, 612 NSE scripts, and enhanced IPv6 support

![](nmap_hackertarget_images/2f36469c14c221ffeab57714c6275467_MD5.png)

Just need the commands? [Jump straight to the compact cheatsheet](https://hackertarget.com/nmap-cheatsheet-a-quick-reference-guide/#compact)

Contents:

- [ Nmap Target Selection](#link_1)
- [ Nmap Port Selection](#link_2)
- [ Nmap Port Scan types](#link_3)
- [ Timing and Performance Controls](#link_4)
- [ Nmap Host Discovery](#link_5)
- [ Service and OS Detection](#link_6)
- [ Nmap Output Formats](#link_7)
- [ Nmap Output to CSV](#link_8)
- [ Digging deeper with NSE Scripts](#link_9)
  - [ Everyday NSE one-liners](#link_10)
  - [ NSE Script Examples](#link_11)
    - [# HTTP Service Information](#link_12)
    - [# IP / Metadata Lookups](#link_13)
    - [# SSH Service information](#link_14)
    - [# Vulnerability Checks (Selected Examples)](#link_15)
- [ Additional Resources](#link_16)
  - [ Related Tools for External Exposure Checks](#link_17)
  - [ Frequently Asked Questions about Nmap](#link_18)
    - [# Does Nmap require root privileges?](#link_19)
    - [# How long does an Nmap scan take?](#link_20)
    - [# What is the difference between -sS and -sT?](#link_21)
    - [# Can Nmap crash systems or networks?](#link_22)
    - [# What does -Pn mean in Nmap?](#link_23)
    - [# How do I scan all 65535 ports?](#link_24)
    - [# What is the fastest Nmap scan?](#link_25)

### Nmap Target Selection <a name="link_1"></a>

| Scan Type                     | Command                       |
| ----------------------------- | ----------------------------- |
| Scan a single IP              | nmap 192.168.1.1              |
| Scan a host                   | nmap **www.testhostname.com** |
| Scan a range of IPs           | nmap 192.168.1.**1-20**       |
| Scan a subnet                 | nmap 192.168.1.0**/24**       |
| Scan targets from a text file | nmap **-iL** list-of-ips.txt  |
| Scan IPv6                     | nmap **-6** fe80::1           |

These are all default scans, which will scan 1000 TCP ports. Host discovery will take place.

**Tip**: For IPv6 scanning, IPv6 hosts can’t be discovered with ARP, so ping scans often miss them. For link-local addresses, specify your interface, for example: `nmap -6 fe80::1%eth0`.

### Nmap Port Selection <a name="link_2"></a>

| Scan Type                         | Command                            |
| --------------------------------- | ---------------------------------- |
| Scan a single Port                | nmap **-p 22** 192.168.1.1         |
| Scan a range of ports             | nmap **-p 1-100** 192.168.1.1      |
| Scan 100 most common ports (Fast) | nmap **-F** 192.168.1.1            |
| Scan all 65535 ports              | nmap **-p-** 192.168.1.1           |
| Scan specific ports               | nmap **-p 22,80,443** 192.168.1.1  |
| Scan ports by name                | nmap **-p http,https** 192.168.1.1 |

### Nmap Port Scan types <a name="link_3"></a>

| Scan Type                             | Command                                 |
| ------------------------------------- | --------------------------------------- |
| TCP connect scan                      | nmap **-sT** 192.168.1.1                |
| TCP SYN scan (default, requires root) | nmap **-sS** 192.168.1.1                |
| UDP port scan                         | nmap **-sU -p** 123,161,162 192.168.1.1 |
| Fast Scan & skip discovery            | nmap **-Pn -F** 192.168.1.1             |
| TCP ACK scan (Firewall rule mapping)  | nmap **-sA** 192.168.1.1                |

Privileged access is required for the default `SYN` scan. If privileges are insufficient, a TCP connect scan will be used. TCP connect requires a full TCP connection to be established, making it a slower scan.

If a host is up but a firewall is blocking the default ICMP echo request (PING), the scan will fail unless the `-Pn` flag is used to skip discovery and go straight to port scanning. This does increase scan times as you could end up sending scan probes to hosts that are not there.

TCP ACK Scan: Used to map firewall rules. It does not determine if a port is open/closed, only if it is filtered/unfiltered.

Once you know what you’re scanning, the next question is: how fast can I push this without breaking things?”

### Timing and Performance Controls <a name="link_4"></a>

| Purpose                                   | Command                                 |
| ----------------------------------------- | --------------------------------------- |
| Increase scan speed (minimum packet rate) | nmap **--min-rate** 5000 192.168.1.1    |
| Throttle scan speed (maximum packet rate) | nmap **--max-rate** 1000 192.168.1.1    |
| Limit retries (avoid slow networks)       | nmap **--max-retries** 2 192.168.1.1    |
| Set a timeout per host                    | nmap **--host-timeout** 30s 192.168.1.1 |

Nmap’s timing templates `(-T0 to -T5)` still appear in shortcut commands such as `-A -T4`, but for predictable performance on real networks the rate-based options (`--min-rate`, `--max-rate`, `--max-retries`) are recommended.

### Nmap Host Discovery <a name="link_5"></a>

| Discovery Type                          | Command                     |
| --------------------------------------- | --------------------------- |
| No scan (list targets only)             | nmap **-sL** 192.168.1.0/24 |
| Disable host discovery - port scan only | nmap **-Pn** 192.168.1.1    |
| Ping scan only (no port scan)           | nmap **-sn** 192.168.1.0/24 |
| TCP SYN discovery on port 443           | nmap **-PS443** 192.168.1.1 |
| TCP ACK discovery on port 80            | nmap **-PA80** 192.168.1.1  |
| UDP discovery on port 53                | nmap **-PU53** 192.168.1.1  |

No scan (list targets only): Verifies target range and performs DNS resolution without sending probes to the targets.  
Ping scan only (no port scan): Quickly finds live hosts using only discovery probes.

### Service and OS Detection <a name="link_6"></a>

| Detection Type                    | Command                                        |
| --------------------------------- | ---------------------------------------------- |
| Standard Version detection        | nmap **-sV** 192.168.1.1                       |
| Aggressive Service Detection      | nmap **-sV --version-intensity** 5 192.168.1.1 |
| Lighter banner grabbing detection | nmap **-sV --version-intensity** 0 192.168.1.1 |
| Detect OS and Services            | nmap **-A** 192.168.1.1                        |
| OS detection only                 | nmap **-O** 192.168.1.1                        |
| Aggressive scan and traceroute    | nmap **-A -T4** 192.168.1.1                    |

Service and OS detection rely on different methods to determine the operating system or service running on a particular port. More aggressive detection helps with services running on unusual ports. Lighter detection is much faster as it simply grabs the banner without deep inspection.

**Tip**: Database services are usually fingerprinted accurately with `-sV`. For deeper checks on SQL ports (1433, 3306, 5432, 1521), simply combine `-sV` with targeted port selection.

Standard Version Detection: Identifies the service and its exact version (default intensity 7).

### Nmap Output Formats <a name="link_7"></a>

| Scan Type                         | Command                                 |
| --------------------------------- | --------------------------------------- |
| Save default output to file       | nmap **-oN** outputfile.txt 192.168.1.1 |
| Save results as XML               | nmap **-oX** outputfile.xml 192.168.1.1 |
| Save results in a format for grep | nmap **-oG** outputfile.txt 192.168.1.1 |
| Save in all formats               | nmap **-oA** outputfile 192.168.1.1     |

The default format can also be saved to a file using a simple file redirect `command > file`. Using the `-oN` option allows the results to be saved but also can be monitored in the terminal as the scan is under way.

### Nmap Output to CSV <a name="link_8"></a>

Nmap, by default has no `csv` output format. Use the `XML` output to extract the relevant fields into `CSV` with `python`.

Grab our sample python script on [Github](https://github.com/hackertarget/nmap-csv-xlsx "Nmap XML output to CSV") that can be easily modified depending on your requirements. With `CSV` files it is easy to convert into `xlsx` for reporting, either manually or using our included `python` conversion script.

|                                                                                           |
| ----------------------------------------------------------------------------------------- |
| [Nmap XML to CSV](https://github.com/hackertarget/nmap-csv-xlsx "Nmap XML output to CSV") |

## Digging deeper with NSE Scripts <a name="link_9"></a>

The Nmap Scripting Engine (NSE) is Nmap's most powerful feature. It's where Nmap stops being just a port scanner and becomes a flexible recon and assessment toolkit. As of Nmap 7.96, there are 612 NSE scripts covering vulnerability detection, exploitation, discovery, and more. If you are serious about your network scanning you really should take the time to get familiar with some of them.

### Everyday NSE one-liners <a name="link_10"></a>

| Purpose                          | Command                                             |
| -------------------------------- | --------------------------------------------------- |
| Run default safe scripts         | nmap **-sV -sC** 192.168.1.1                        |
| Run a specific script            | nmap -sV -p 22 **--script=ssh-hostkey** 192.168.1.1 |
| Run a script category / wildcard | nmap -sV **--script=smb\*** 192.168.1.1             |
| View help for a script           | nmap **--script-help=**http-enum                    |

**Tip**: Notice the use of the `-sV` service version detection parameter. NSE scripts are generally more effective when `-sV` is included as it ensures the script is run against the correct, verified version.

Help documentation for a script is available with the `--script-help=$scriptname` option. Example: `nmap --script-help=http-enum`. To get a list of installed scripts try `locate nse | grep script`.

Now that you’ve seen everyday NSE usage, here are some focused examples you can drop into real workflows.

### NSE Script Examples <a name="link_11"></a>

###### HTTP Service Information <a name="link_12"></a>

| Purpose                                 | Command                                                               |
| --------------------------------------- | --------------------------------------------------------------------- |
| Quick web recon (title + server header) | nmap -p 80,443 **--script=http-title,http-server-header** 192.168.1.1 |
| HTTP security headers (HSTS, CSP, etc)  | nmap -p 80,443 **--script=http-security-headers** 192.168.1.1         |
| Gather page titles                      | nmap **--script=http-title** 192.168.1.0/24                           |
| Get HTTP headers                        | nmap **--script=http-headers** 192.168.1.0/24                         |
| Enumerate known paths (noisy)           | nmap **--script=http-enum** 192.168.1.0/24                            |

There are many HTTP information gathering scripts, the table above shows a few simple but helpful ones when examining larger networks.

**Tip**: `http-enum` script is particularly noisy. It is similar to [Nikto](https://hackertarget.com/nikto-website-scanner/) in that it will attempt to enumerate known paths of web applications and scripts and will generate hundreds of `404 HTTP responses` that will be logged by the web server.

###### IP / Metadata Lookups <a name="link_13"></a>

| Purpose                   | Command                                                                 |
| ------------------------- | ----------------------------------------------------------------------- |
| ASN, Whois, GeoIP lookups | nmap **--script=asn-query,whois,ip-geolocation-maxmind** 192.168.1.0/24 |

Gather information related to the IP address and netblock owner of the IP address. Uses ASN, Whois and GeoIP location lookups. See the [IP Tools](https://hackertarget.com/ip-tools/ "IP and Domain Information Tools") for more information and similar IP address and DNS lookups.

###### SSH Service information <a name="link_14"></a>

| Purpose                 | Command                                                          |
| ----------------------- | ---------------------------------------------------------------- |
| SSH Host key collection | nmap -p 22 **--script=ssh-hostkey,ssh-auth-methods** 192.168.1.1 |

Useful for tracking server migrations or detecting MITM and for spotting unexpected key changes that shouldn’t be there.

###### Vulnerability Checks (Selected Examples) <a name="link_15"></a>

| Purpose                                    | Command                                                                                                  |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| UDP DDoS reflector exposure (NTP/DNS/SNMP) | nmap -sU -A -Pn -n -pU:19,53,123,161 **--script=ntp-monlist,dns-recursion,snmp-sysdescr** 192.168.1.0/24 |
| Check for SSL Heartbleed                   | nmap -sV -p 443 **--script=ssl-heartbleed** 192.168.1.0/24                                               |
| TLS cert + cipher information              | nmap -p 443 **--script=ssl-cert,ssl-enum-ciphers** 192.168.1.1                                           |

UDP based DDoS reflection attacks are a common problem that network defenders come up against. This is a handy Nmap command that will scan a target list for systems with open UDP services that allow these attacks to take place. Full details of the command and the background can be found on the [Sans Institute Blog](https://isc.sans.edu/diary/Using+nmap+to+scan+for+DDOS+reflectors/18193) where it was first posted.

Although Heartbleed (CVE-2014-0160) is a legacy issue, this script remains a useful example of SSL-focused vulnerability checks. Specify alternative ports to test SSL on mail and other protocols.

While the security community has created additional NSE scripts for specific use cases, all scripts listed here are from official scripts included with Nmap. Only run third-party scripts if you trust the author and have audited the code yourself.

## Additional Resources <a name="link_16"></a>

The above commands are just a taste of the power of Nmap and what it can do. For deeper understanding check out our [Nmap Tutorial](https://hackertarget.com/nmap-tutorial/) that has more information and tips.

Full reference documentation is available in the [official Nmap manual](https://nmap.org/book/man.html), which covers every scan type, flag, timing option, and NSE script in detail. You can also view Nmap's full set of features by running it with no options.

### Related Tools for External Exposure Checks <a name="link_17"></a>

[Domain Profiler](https://hackertarget.com/domain-profiler/) gives you an instant view of which hosts, IPs, and subdomains are exposed to the internet. Use it as a perimeter snapshot before running external scans.

External scanning shows what the internet can really reach and is useful for verifying:

- Exposed services
- Firewall behaviour vs expected policy
- Gaps that internal scans miss or don't detect.

![](nmap_hackertarget_images/84530362bc324f1ed1e703518080108a_MD5.webp)

It’s a simple step, but as Shodan regularly shows, many organisations never test their perimeter from an attacker’s perspective.

No external vantage point? Use our [online Nmap port scanner](https://hackertarget.com/nmap-online-port-scanner/) to run perimeter checks from the internet without additional setup.

### Frequently Asked Questions about Nmap <a name="link_18"></a>

###### Does Nmap require root privileges? <a name="link_19"></a>

SYN scans (`-sS`) and OS detection (`-O`) generally require root/administrator privileges.  
TCP connect scans (`-sT`):

- Work without elevated privileges
- Are slower and more detectable
- Log full TCP connections on the target

###### How long does an Nmap scan take? <a name="link_20"></a>

A default scan of 1000 ports typically takes a few seconds to under a minute per host on a responsive network. Full port scans `-p-` can take significantly longer, depending on latency, firewalls, and rate limits. Use `--min-rate` to tune performance.

###### What is the difference between -sS and -sT? <a name="link_21"></a>

`-sS` (SYN scan) sends a SYN packet and doesn't complete the TCP handshake, making it stealthier and faster. `-sT` (TCP connect) completes the full handshake, works without root privileges, but is slower and logs connections.

###### Can Nmap crash systems or networks? <a name="link_22"></a>

Nmap is generally safe, but aggressive scans (`-T5`, `--max-rate` without limits) can overwhelm weak systems or trigger IDS/IPS blocks. Always get authorization before scanning networks you don't own.

###### What does -Pn mean in Nmap? <a name="link_23"></a>

`-Pn` skips host discovery (ping) and treats all targets as online. Essential when scanning hosts behind firewalls that block ICMP, but increases scan time as Nmap probes non-existent hosts.

###### How do I scan all 65535 ports? <a name="link_24"></a>

Use `nmap -p- <target>` to scan all TCP ports. Add `--min-rate 5000` to speed it up: `nmap -p- --min-rate 5000 <target>`

###### What is the fastest Nmap scan? <a name="link_25"></a>

Fastest in practice depends on your network and risk tolerance. `nmap -T5 -F <target>` or `nmap --min-rate 10000 -F <target>` scans only the 100 most common ports at maximum speed. May miss ports or trigger security alerts.
