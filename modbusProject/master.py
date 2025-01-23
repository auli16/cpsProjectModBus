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

async def master_read():
    """
    Crea il client Modbus e legge i dati da più slave.
    """
    # Crea il client Modbus asincrono
    client = AsyncModbusTcpClient("localhost", port=502, source_address=("192.168.1.10"))

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

from pymodbus.client import AsyncModbusTcpClient
import asyncio

async def master_connected():
    """
    Crea il client Modbus e lo lascia connesso per un minuto.
    Gestisce la disconnessione tramite pacchetto TCP FIN.
    """
    # Crea il client Modbus asincrono
    client = AsyncModbusTcpClient("localhost", port=502)

    try:
        # Connetti il client
        print("Attempting to connect...")
        connection = await client.connect()

        # Verifica se la connessione è avvenuta correttamente
        if connection:
            print("Client connected successfully.")
        else:
            print("Connection failed!")

        # Lascia il client connesso per 60 secondi
        print("Client connected for 60 seconds...")
        await asyncio.sleep(60)

        # Verifica se la connessione è ancora attiva
        if not client.transport.is_open:
            print("Client was disconnected before close.")
        else:
            print("Client will disconnect now...")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Chiudi il client
        client.close()
        print("Client disconnected.")

# Funzione principale
async def main():
    await master_connected()  # Chiamata della funzione asincrona

# Esegui la funzione asincrona principale
asyncio.run(main())



# Funzione principale
async def main():
    await master_connected()  # Chiamata della funzione asincrona

# Esegui la funzione asincrona principale
asyncio.run(main())
