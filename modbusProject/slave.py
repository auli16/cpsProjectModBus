import asyncio
import random
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import ModbusTcpServer

def create_slave_context(slave_id):
    """
    Funzione per creare un contesto per uno slave.
    Ogni slave avrà un ID e i registri saranno inizializzati con valori random.
    """
    coils = ModbusSequentialDataBlock(1, [True] * 100)  # digital outputs, 0 or 1
    discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100)  # read only, digital inputs
    holding_registers = ModbusSequentialDataBlock(1, [0] * 100)  # holding registers
    input_registers = ModbusSequentialDataBlock(1, [0] * 100)  # input registers

    # Creazione di valori random per temperature per ogni slave
    some_values = [random.randint(4, 15) for _ in range(7)]
    holding_registers.setValues(1, some_values)
    print(f"Slave {slave_id} - some_values:", some_values)

    # Creazione del contesto per lo slave con ID specificato
    slave_context = ModbusSlaveContext(
        di=discrete_inputs,
        co=coils,
        hr=holding_registers,
        ir=input_registers
    )

    return slave_context

async def run():
    # Creazione del contesto per entrambi gli slave
    slave_context_1 = create_slave_context(1)
    slave_context_2 = create_slave_context(2)
    slave_context_3 = create_slave_context(3)

    # Aggiungi entrambi gli slave al contesto del server
    server_context = ModbusServerContext(slaves={1: slave_context_1, 2: slave_context_2, 3: slave_context_3}, single=False)

    # Avvia il server
    server = ModbusTcpServer(context=server_context, address=("localhost", 502))

    await server.serve_forever()  # Start the Modbus TCP server and keep it running

if __name__ == "__main__":
    asyncio.run(run())  # Use asyncio to run the coroutine
