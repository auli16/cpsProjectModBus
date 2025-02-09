import asyncio
import random
import logging
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import ModbusTcpServer

# Funzione di callback per tracciare le connessioni
def trace_connection(is_connected, client_address):
    if is_connected:
        print(f"Dispositivo connesso: {client_address}")
    else:
        print(f"Dispositivo disconnesso: {client_address}")

def create_slave_context(slave_id):
    """
    Funzione per creare un contesto per uno slave.
    Ogni slave avrà un ID e i registri saranno inizializzati con valori random.
    """
    coils = ModbusSequentialDataBlock(1, [True] * 100)  # digital outputs, 0 or 1
    discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100)  # read only, digital inputs
    holding_registers = ModbusSequentialDataBlock(1, [0] * 100)  # holding registers
    input_registers = ModbusSequentialDataBlock(1, [0] * 100)  # input registers

    # Creazione di valori random per ogni slave
    some_values = [random.randint(4, 15) for _ in range(7)]
    holding_registers.setValues(1, some_values)
    print(f"Slave {slave_id} - some_values:", holding_registers.getValues(1, 7), "coils", coils.getValues(1, 7))

    # Creazione del contesto per lo slave con ID specificato
    slave_context = ModbusSlaveContext(
        di=discrete_inputs,
        co=coils,
        hr=holding_registers,
        ir=input_registers
    )

    return slave_context

# Configurazione del logging per tracciare tutte le richieste Modbus
logging.basicConfig(level=logging.DEBUG)  # Imposta il livello di log a DEBUG
log = logging.getLogger()

async def run():
    # Creazione del contesto per uno slave
    slave_context_1 = create_slave_context(1)
    server_context = ModbusServerContext(slaves={1: slave_context_1}, single=False)

    # Avvia il server con il callback trace_connection per le connessioni/disconnessioni
    server = ModbusTcpServer(context=server_context, address=("localhost", 502), trace_connect=trace_connection)

    print("Server Modbus avviato...")

    # Esegui il server Modbus
    await server.serve_forever()  # Avvia il server Modbus TCP e mantienilo in esecuzione

if __name__ == "__main__":
    asyncio.run(run())  # Usa asyncio per eseguire la coroutine
