from pymodbus.client import AsyncModbusTcpClient
import asyncio

# Funzione per leggere i dati da uno specifico slave
async def read_slave_data(client, slave_id):
    """
    Legge i dati da uno specifico slave Modbus.
    
    Args:
        client: Il client Modbus asincrono.
        slave_id: L'ID dello slave da cui leggere i dati.
    
    Returns:
        Un dizionario con i dati letti dallo slave.
    """
    try:
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

# Funzione principale
async def main():
    # Crea il client Modbus asincrono
    client = AsyncModbusTcpClient("localhost", port=502)

    # Connetti il client
    await client.connect()

    # Leggi i dati dallo slave 1
    print("Reading data from Slave 1...")
    slave_1_data = await read_slave_data(client, slave_id=1)
    print("Slave 1 Data:", slave_1_data)

    # Leggi i dati dallo slave 2
    print("Reading data from Slave 2...")
    slave_2_data = await read_slave_data(client, slave_id=2)
    print("Slave 2 Data:", slave_2_data)

    # Chiudi il client
    client.close()

# Esegui la funzione asincrona principale
asyncio.run(main())
