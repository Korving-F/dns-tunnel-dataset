#!/bin/env python3
from pprint import pprint
import yaml
from pathlib import Path


TABLE = """
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
"""

def readme(file_transfer, c2):
    README=f"""
# DNS Tunneling Dataset
[![License MIT](https://img.shields.io/badge/license-MIT-blue)](https://en.wikipedia.org/wiki/MIT_License)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/Korving-F/daca)](https://github.com/Korving-F/DACA)

## Introduction
This repository documents a DNS tunneling scenario written in [DACA](https://github.com/Korving-F/DACA/) configuration language and the generated datasets it creates.
Samples can be used for detection tuning or for educational purposes.

This dataset was created as part of Master thesis work at [TalTech](https://taltech.ee/).

To reproduce the generated datasets, follow these instructions:
```bash
# 1. Install Vagrant and VirtualBox

# 2. Install Vagrant modules
vagrant plugin install vagrant-vbguest
vagrant plugin install vagrant-scp

# 3A Start and stop the VMs of a single dataset, data collection will follow automatically.
cd directory/with/Vagrantfile
vagrant up
vagrant halt

# 3B Alternatively generate and run and recreate all datasets in the scenario.
pip3 install pipenv
git clone git@github.com:Korving-F/DACA.git
cd DACA
pipenv install

python3 daca.py run -d data/ --path /path/to/scenario_file.yaml
```

## MITRE ATT&CK
* [C2 Application Layer Protocol: DNS - T1071.004](https://attack.mitre.org/techniques/T1071/004/)
* [C2 Protocol Tunneling - T1572](https://attack.mitre.org/techniques/T1572/)
* [Exfiltration Over Alternative Protocol - T1048](https://attack.mitre.org/techniques/T1048/)

## Scenario
Used DNS Tunneling software: [IODINE](https://github.com/yarrick/iodine) / [DNS2TCP](https://github.com/alex-sector/dns2tcp) / [DNSCAT](https://github.com/iagox86/dnscat2)

Used DNS Servers: [BIND 9](https://www.isc.org/bind/) / [CoreDNS](https://coredns.io/) / [Dnsmasq](https://thekelleys.org.uk/dnsmasq/doc.html) / [PowerDNS](https://www.powerdns.com/)

## Consume Datasets
Collected data within this repository comes in a variety of formats:
* .log  - Flatfiles containing query logs as produced by the DNS Server.
* .json - Same flatfiles but then relayed by Filebeat. This allows for post-hoc ingestion into an elasticsearch cluster.
* .cast - [asciinema](https://asciinema.org/) recordings of attacker's perspective. Replay by issuing: `asciinema play *.cast`.
* .pcap - Standard packet capture looking at traffic on port 53.

## Architecture
![](images/dns_tunnel.drawio.png)
> **Fig 1:** DNS Tunnel high-level overview. Encoded/encrypted DNS queries establish a communications channel.
</br>  
</br>  

![](images/dns_tunnel_simulated.drawio.png)
> **Fig 2:** Overview on how the DNS Tunnels are simulated and allow for C2 / data transfers.
</br>  
</br>  

![](images/dns_tunnel_devops.drawio.png)
> **Fig 3:** Runthrough of the VM Creation, Provisioning, Data Generation and Acquisition process using IaC / DevOps tooling.
</br>  


## Detection Rules
* [Sigma](detections/sigma/)
* [SEC](detections/SEC/)
* [Suricata](detections/suricata/)

## Datasets
### File transfer over DNS Tunnel
{file_transfer}

### C2 over DNS Tunnel
{c2}

## License
> DACA is licensed under the [MIT](#) license.  
> Copyright &copy; 2022, Frank Korving
    """
    return README


def gen_table(title, columns, rows):
    HEADER  = f"#### {title}\n"
    COLUMNS = "| "
    for c in columns:
        COLUMNS += f"{c} | "
    COLUMNS += "\n"
    for c in columns:
        COLUMNS += f"| ------------- "
    COLUMNS += "|\n"
    
    ROWS = ""
    for row in rows:
        ROWS += "| "
        for c in columns:
            ROWS += f"{row[c]} | "
        ROWS += "\n"
    
    return HEADER + COLUMNS + ROWS + "\n"


def gen_c2(path):
    pass


def gen_file_transfer(path):
    files = Path(path).glob('*')
    data_dirs = [i for i in files if i.is_dir() and i.name != 'scenario']

    iodine_cols  = ['DNS SERVER', 'AUTOMATION LEVEL','DNS RECORD TYPE', 'ENCODING', 'PASSPHRASE', 'LINK', 'DATA LINK']
    iodine_rows  = []

    dnscat_cols  = ['DNS SERVER', 'AUTOMATION LEVEL', 'LINK', 'DATA LINK']
    dnscat_rows  = []

    dns2tcp_cols = ['DNS SERVER', 'AUTOMATION LEVEL', 'DNS RECORD TYPE', 'COMPRESSION', 'PASSPHRASE', 'LINK', 'DATA LINK']
    dns2tcp_rows = []

    for d in data_dirs:
        row = {}
        with open(f"{d}/.metadata", 'r') as f:
            meta = f.read()
        meta_loaded = yaml.safe_load(meta)

        # Add link to directory
        row['LINK'] = f"[Scenario files]({d})"
        # Add link to data file
        row['DATA LINK'] = f"[Data files]({d}/{d.name}_full_dataset.tar.gz)"
        # Specify which DNS Server was used
        for component in meta_loaded['scenario']['components']:
            if "bind9" in component["name"].lower():
                row['DNS SERVER'] = "BIND9"
                break
            elif "dnsmasq" in component["name"].lower():
                row['DNS SERVER'] = "DNSMASQ"
                break
            elif "coredns" in component["name"].lower():
                row['DNS SERVER'] = "COREDNS"
                break
            elif "powerdns" in component["name"].lower():
                row['DNS SERVER'] = "POWERDNS"
                break

        for component in meta_loaded['scenario']['components']:
            if "iodine" in component["name"]:
                row['AUTOMATION LEVEL'] = "Fully Automated"
                row['DNS RECORD TYPE']   = meta_loaded["variables"]["record_type"].upper()
                row['ENCODING']          = meta_loaded["variables"]["encoding"].upper()
                row['PASSPHRASE']        = meta_loaded["variables"]["passphrase"]
                iodine_rows.append(row)
                break
                
            if "dns2tcp" in component["name"]:
                row['AUTOMATION LEVEL'] = "Fully Automated"
                row['DNS RECORD TYPE']   = meta_loaded["variables"]["record_type"].upper()
                row['COMPRESSION']       = "YES" if meta_loaded["variables"]["compression"] == "-c" else "NO"
                row['PASSPHRASE']        = meta_loaded["variables"]["passphrase"]
                dns2tcp_rows.append(row)
                break
                
            if "dnscat" in component["name"]:
                row['AUTOMATION LEVEL'] = "Partly Manual"
                dnscat_rows.append(row)
                break

    iodine_rows_sorted  = sorted(iodine_rows,  key=lambda d: (d['DNS SERVER'], d['DNS RECORD TYPE']))
    dns2tcp_rows_sorted = sorted(dns2tcp_rows, key=lambda d: (d['DNS SERVER'], d['DNS RECORD TYPE']))
    dnscat_rows_sorted  = sorted(dnscat_rows,  key=lambda d: (d['DNS SERVER'], d['DNS RECORD TYPE']))
    
    tables = []
    tables.append(gen_table("IODINE",  iodine_cols,  iodine_rows_sorted))
    tables.append(gen_table("DNS2TCP", dns2tcp_cols, dns2tcp_rows_sorted))
    tables.append(gen_table("DNSCAT",  dnscat_cols,  dnscat_rows_sorted))
    return "\n".join(tables)
        

    

if __name__ == '__main__':
    # FIRST GENERATE REPORT ON FILE TRANSFER DATASETS
    ft = gen_file_transfer('dns_tunnel_file_transfer')

    # SECONDLY GENERATE REPORT ON C2 DATASET
    c2 = gen_c2('dns_tunnel_c2')
    
    # RENDER README AND WRITE TO DISK
    with open("README.md",'w') as f:
        f.write(readme(ft, c2))