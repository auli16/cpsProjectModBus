import random
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartTcpServer

# Define the Modbus registers
coils = ModbusSequentialDataBlock(1, [False] * 100) # digital outputs, 0 or 1
discrete_inputs = ModbusSequentialDataBlock(1, [False] * 100) # read only, digital inputs, 0 or 1
holding_registers = ModbusSequentialDataBlock(1, [0] * 100) # each register is 16 bits, 0 to 65535
input_registers = ModbusSequentialDataBlock(1, [0] * 100) # read only, each register is 16 bits, 0 to 65535

temperature_values = [random.randint(4, 15) for _ in range(7)]
holding_registers.setValues(1, temperature_values)
print("temperature_values:", temperature_values)

# Define the Modbus slave context
slave_context = ModbusSlaveContext(
    di=discrete_inputs,
    co=coils,
    hr=holding_registers,
    ir=input_registers
)

# Define the Modbus server context
server_context = ModbusServerContext(slaves=slave_context, single=True)

# Start the Modbus TCP server
StartTcpServer(context=server_context, address=("localhost", 502))
