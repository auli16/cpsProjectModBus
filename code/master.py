from pymodbus.client import AsyncModbusTcpClient
import asyncio

async def read_slave_data(client, slave_id):
    """
    function to read all the registers from a specific slave.

    Params:
        client: The Modbus client to use for reading data.
        slave_id: ID of the slave to read data from.
    
    Returns:
        A dictionary containing the data read from the slave.
    """

    try:
        '''
        In the following function calls:
            'address' is the starting address to read from;
            'count' is the number of registers to read;
            'slave' is the slave ID to read from.
        '''
        coils = await client.read_coils(address=0, count=100, slave=slave_id) 
        discrete_inputs = await client.read_discrete_inputs(address=0, count=100, slave=slave_id)
        holding_registers = await client.read_holding_registers(address=0, count=100, slave=slave_id)
        input_registers = await client.read_input_registers(address=0, count=100, slave=slave_id)

        return {
            "coils": coils.bits if not coils.isError() else f"Error: {coils}",
            "discrete_inputs": discrete_inputs.bits if not discrete_inputs.isError() else f"Error: {discrete_inputs}",
            "holding_registers": holding_registers.registers if not holding_registers.isError() else f"Error: {holding_registers}",
            "input_registers": input_registers.registers if not input_registers.isError() else f"Error: {input_registers}",
        }
    except Exception as e:
        return {"error": str(e)}

async def master_read():
    """
    Function which create a client, establish a connection and read data 
    from the slave thoruh the functin 'read_slave_data'.
    """
    # Create the Modbus client and connect to the server
    try: 
        client = AsyncModbusTcpClient("localhost", port=503)
        await client.connect()
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Read data from the slave 1
    print("Reading data from Slave 1...")
    slave_1_data = await read_slave_data(client, slave_id=1)
    print("Slave 1 Data:", slave_1_data)

# ----------------------------------------------------------------

async def monitor_connection(client):
    """
    Function to monitor the connection status of the client.
    Args:
        client: The Modbus client to monitor.
    It prints true if the client is connected, false otherwise each 0.5 seconds.
    """
    while True:
        print(f"Connection Status: {client.connected}")
        await asyncio.sleep(0.5) 

async def master_connected(time_wait=5):
    """
    Create a modbus client, wait for time_wait seconds, then try to read coils from the slave.
    Wait other time_wait seconds and then close the connection.
    """
    # Create the Modbus client
    client = AsyncModbusTcpClient("localhost", port=503)

    try:
        # Connection to the server
        print("Attempting to connect...")
        connection = await client.connect()

        # Verify if the connection was successful
        if connection:
            print("Client connected successfully.")
        else:
            print("Connection failed!")

        # Montoring the connection status
        asyncio.create_task(monitor_connection(client))

        print(f"Client connected, wait {time_wait} seconds...")
        await asyncio.sleep(time_wait)

        # Send a request to read the coils from the slave 1
        values = await client.read_coils(address=0, count=10, slave=1)
        # Print the values read
        print(f"Coils values: {values.bits}")

        # Leave the client connected for another time_wait seconds
        print(f"Client disconnection in {time_wait} seconds...")
        await asyncio.sleep(time_wait)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Disconnection of the client
        if client.connected:
            print("Closing client connection...")
            client.close() 
            print("Client disconnected.")
        else:
            print("Client was already disconnected.")

# ----------------------------------------------------------------

async def master_write():
    """
    Function to write data to the slave.
    """
    # Create the Modbus client and connect to the server
    client = AsyncModbusTcpClient("localhost", port=503)
    await client.connect()

    # Write data to the slave 1
    print("Writing data to Slave 1...")
    try:
        # Write a value to a coil
        await client.write_registers(address=0, values=[0x00, 0x00, 0x00, 0x00], slave=1)
        print("Data written successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Close the connection
    finally:
        # Disconnection of the client
        if client.connected:
            print("Closing client connection...")
            client.close() 
            print("Client disconnected.")
        else:
            print("Client was already disconnected.")



async def main():
    '''
    We have used master_connected while trying to do the FIN flood attack, 
    and other various interruption attack we have tried.
    master_write is used for the modification attack.
    '''
    await master_read()
    # await master_write()
    # await master_connected(5)

if __name__ == "__main__":
    asyncio.run(main())