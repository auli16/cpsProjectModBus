from pymodbus.client.tcp import ModbusTcpClient

# Inizializzare il client
client = ModbusTcpClient('localhost', port=502)

# Interrogare tutti gli indirizzi (1-247) per i coils, holding registers, etc.

address = 0

try:
    # Leggere i coils
    coils = client.read_coils(address=address, count=100)
    if not coils.isError():
        print(f"Coils from slave {address}: {coils.bits}")
    
    # Leggere i holding registers
    holding_registers = client.read_holding_registers(address=address, count=100)
    if not holding_registers.isError():
        print(f"Holding Registers from slave {address}: {holding_registers.registers}")
    
    # Leggere altri registri, ad esempio discrete inputs o input registers
    discrete_inputs = client.read_discrete_inputs(address=address, count=100)
    if not discrete_inputs.isError():
        print(f"Discrete Inputs from slave {address}: {discrete_inputs.bits}")
    
    input_registers = client.read_input_registers(address=address, count=100)
    if not input_registers.isError():
        print(f"Input Registers from slave {address}: {input_registers.registers}")

except Exception as e:
    print(f"Error communicating with slave {address}: {str(e)}")

# Chiudere il client
client.close()
