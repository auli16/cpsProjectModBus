import asyncio
import random
import logging
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import ModbusTcpServer

def create_slave_context(slave_id):
    """
    Function to create a Modbus slave context with random values.
    params:
        slave_id: The slave ID for the context.
    """
    coils = ModbusSequentialDataBlock(1, [True] * 100)  # digital outputs, 0 or 1, this data can be written
    discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100)  # read only, digital inputs
    holding_registers = ModbusSequentialDataBlock(1, [0] * 100)  # holding registers, this data can be written
    input_registers = ModbusSequentialDataBlock(1, [0] * 100)  # input registers

    # Here we insert some random values to the registers
    some_values = [random.randint(4, 15) for _ in range(7)]
    holding_registers.setValues(1, some_values)
    # print the updated values
    print(f"Slave {slave_id} - some_values:", holding_registers.getValues(1, 7), "coils", coils.getValues(1, 7))

    # Creation of the slave context, which will be returned by the function to be used in the server context
    slave_context = ModbusSlaveContext(
        di=discrete_inputs,
        co=coils,
        hr=holding_registers,
        ir=input_registers
    )

    return slave_context

# Logging configuration to trace the server activity
logging.basicConfig(level=logging.DEBUG) 
log = logging.getLogger()


async def run():
    '''
    Main function to run the Modbus server.
    '''
    # Creation of the slave context for slave 1, with ModbusTcpServer it's possible to add multiple slaves (have more than one server)
    slave_context_1 = create_slave_context(1)
    server_context = ModbusServerContext(slaves={1: slave_context_1}, single=False)

    # Creation of the Modbus TCP server and start it throuh server_forever
    server = ModbusTcpServer(context=server_context, address=("localhost", 503))

    print("Server started...")
    await server.serve_forever() 

if __name__ == "__main__":
    asyncio.run(run())