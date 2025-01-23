from pymodbus.client.tcp import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=1502)

if not client.connect():
    print("Could not connect to Modbus server")
    exit(1)

try:
    print("Writing to coils")
    client.write_coils(1, [True, True, False, True, False])

    print("Writing to holding registers")
    client.write_registers(1, [123, 456, 789, 101, 102])

    coils = client.read_coils(address=1, count=5)
    holding_registers = client.read_holding_registers(address=1, count=5)

    if not coils.isError() and not holding_registers.isError():
        print("Coils:", coils.bits)
        print("Holding Registers:", holding_registers.registers)
    else:
        print("Error reading coils or holding registers")
    
finally:
    client.close()