from scapy.all import IP, TCP, send

def send_tcp_fin(target_ip, target_port, source_ip, source_port):
    """
    Invia un pacchetto TCP con il flag FIN impostato.
    """
    fin_packet = IP(src=source_ip, dst=target_ip) / \
                 TCP(sport=source_port, dport=target_port, flags="F")

    # Invia il pacchetto FIN
    send(fin_packet, verbose=0)
    print(f"Inviato pacchetto FIN da {source_ip}:{source_port} a {target_ip}:{target_port}")

# Esegui il pacchetto TCP FIN
send_tcp_fin("127.0.0.1", 502, "127.0.0.1", 12345)
