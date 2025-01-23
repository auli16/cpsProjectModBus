from pymodbus.client.sync import ModbusTcpClient    
import threading

def modbus_client(client_id):
    print(f"Client {client_id} connecting to Modbus server")
    client = ModbusTcpClient("127.0.0.1", port=1502)
    if not client.connect():
        print(f"Client {client_id} could not connect to Modbus server")
        return
    
    try:
        print(f"Client {client_id} writing to coils...")
        client.write_coils(1, [True, True, False, True, False])
        coils = client.read_coils(address=1, count=5)
        print(f"Clients {client_id} coils:", coils.bits[:5])

        print(f"Client {client_id} writing to holding registers...")
        client.write_registers(1, [123, 456, 789, 101, 102])
        holding_registers = client.read_holding_registers(address=1, count=5)
        print(f"Client {client_id} holding registers:", holding_registers.registers)

    finally:
        client.close()
        print(f"Client {client_id} disconnected from Modbus server")

threads = []
for i in range(3):
    thread = threading.Thread(target=modbus_client, args=(i*10,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()