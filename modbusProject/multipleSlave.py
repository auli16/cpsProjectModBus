import random
import asyncio
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import ModbusTcpServer  # Usa ModbusTcpServer per il server senza SSL

# Funzione per creare il contesto dello slave
def create_slave_context():
    coils = ModbusSequentialDataBlock(1, [True] * 100)  # digital outputs, 0 or 1
    discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100)  # read only, digital inputs, 0 or 1
    holding_registers = ModbusSequentialDataBlock(1, [0] * 100)  # 16-bit registers, 0 to 65535
    input_registers = ModbusSequentialDataBlock(1, [0] * 100)  # read only, 16-bit registers, 0 to 65535

    # Simula valori casuali per i registri holding
    temperature_values = [random.randint(4, 15) for _ in range(7)]
    holding_registers.setValues(1, temperature_values)
    print(f"Slave holding register values: {temperature_values}")

    # Crea il contesto dello slave
    return ModbusSlaveContext(
        di=discrete_inputs,
        co=coils,
        hr=holding_registers,
        ir=input_registers
    )

# Crea il contesto per uno slave
slave_context = create_slave_context()

# Configura il server Modbus
server_context = ModbusServerContext(slaves={1: slave_context}, single=True)

# Funzione asincrona per avviare il server e fermarlo dopo un certo tempo
async def start_server_for_duration(server, duration):
    # Avvia il server in modo asincrono
    server_task = asyncio.create_task(server.serve_forever())
    
    # Aspetta per il periodo di tempo desiderato (in secondi)
    await asyncio.sleep(duration)
    
    # Dopo il tempo di durata, fermiamo il server
    server_task.cancel()
    await server_task

# Crea il server Modbus TCP (senza SSL)
server = ModbusTcpServer(
    context=server_context,
    address=("localhost", 502)  # Specifica l'indirizzo e la porta
)

# Esegui il server per 10 secondi all'interno di un loop asincrono
async def main():
    await start_server_for_duration(server, 10)

if __name__ == "__main__":
    # Usa asyncio.run() per avviare il loop asincrono
    asyncio.run(main())
