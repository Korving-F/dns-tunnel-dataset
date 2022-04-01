# C2 over DNS Tunnel
```
# To see overall scenario execution
asciinema play daca_interactive_dnscat.cast
asciinema play daca_interactive_dnstcp.cast

# To see the tunnel generation and reverse shell issue for example:
asciinema play ./af88c701c4dea95b51e33748eafb76ab/dns2tcpserver/dns2tcp_server_c2.cast
asciinema play ./af88c701c4dea95b51e33748eafb76ab/dns2tcpserver/dns2tcp_server_reverse_shell.cast
asciinema play ./af88c701c4dea95b51e33748eafb76ab/dns2tcpclient/dns2tcp_client_reverse_shell.cast
```

Commands issued within each shell:
```bash
whoami
pwd
w
uname -a
ip a
env
```