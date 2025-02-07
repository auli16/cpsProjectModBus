from scapy.all import IP, TCP, sniff, Raw

def packet_handler(packet):
    # Verifica se il pacchetto ha il layer TCP e il layer Raw (che contiene il payload)
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load  # Ottieni il payload
        print("Payload del pacchetto:", payload)


# Avvia lo sniffing dei pacchetti
sniff(iface="Software Loopback Interface 1", prn=packet_handler, filter="tcp port 1502", count=10)

'''
packets = []
packets.append(sniff(iface="Software Loopback Interface 1", prn=packet_callback, filter="tcp port 1502", count=10))
print(packets)
print(packets[0])

'''