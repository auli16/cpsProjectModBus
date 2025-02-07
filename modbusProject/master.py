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
    client = AsyncModbusTcpClient("localhost", port=1502, trace_packet=packet_logger)

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


from pymodbus.client import AsyncModbusTcpClient
import asyncio

async def monitor_connection(client):
    """
    Monitora il valore di 'client.connected' ogni 0.5 secondi.
    """
    while True:
        print(f"Connection Status: {client.connected}")
        await asyncio.sleep(0.5)  # Attende 0.5 secondi prima del prossimo controllo

def packet_logger(request: bool, data: bytes):
    """
    Callback per registrare i pacchetti inviati/ricevuti.
    Args:
        request: Se True, il pacchetto è stato inviato dal client, se False, ricevuto dal client.
        data: Dati del pacchetto (bytes).
    """
    if request:
        print(f"Sent Packet: {data.hex()}")  # Mostra i pacchetti inviati
    else:
        print(f"Received Packet: {data.hex()}")  # Mostra i pacchetti ricevuti

async def master_connected():
    """
    Crea il client Modbus e lo lascia connesso per un minuto.
    Gestisce la disconnessione tramite pacchetto TCP FIN.
    """
    # Crea il client Modbus asincrono con la funzione di tracing
    client = AsyncModbusTcpClient("localhost", port=502, trace_packet=packet_logger)

    try:
        # Connetti il client
        print("Attempting to connect...")
        connection = await client.connect()

        # Verifica se la connessione è avvenuta correttamente
        if connection:
            print("Client connected successfully.")
        else:
            print("Connection failed!")

        # Esegui il monitoraggio della connessione
        asyncio.create_task(monitor_connection(client))

        # Lascia il client connesso per 60 secondi
        print("Client connected for 20 seconds...")
        await asyncio.sleep(20)

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Forza la chiusura della connessione TCP
        if client.connected:
            print("Closing client connection...")
            client.close()  # Chiusura del client
            print("Client disconnected.")
        else:
            print("Client was already disconnected.")

from pymodbus.client import AsyncModbusTcpClient
import asyncio

async def send_packet_after_delay(client, slave_id):
    """
    Collega il client allo slave, invia un pacchetto dopo 30 secondi e
    disconnette dopo 60 secondi.
    
    Args:
        client: Il client Modbus asincrono.
        slave_id: L'ID dello slave da cui inviare il pacchetto.
    """
    try:
        # Connetti il client
        print("Connecting to Modbus server...")
        connected = await client.connect()

        if connected:
            print("Connected successfully.")
        else:
            print("Failed to connect.")
            return
        
        # Monitoraggio della connessione (facoltativo)
        asyncio.create_task(monitor_connection(client))

        # Attendi 30 secondi prima di inviare il pacchetto
        print("Waiting for 15 seconds before sending a packet...")
        # await asyncio.sleep(10)

        # Esegui l'invio di un pacchetto (per esempio, una scrittura di coil)
        print(f"Sending a packet to Slave {slave_id}...")
        valuesToWrite = [1,1,1,1,1,1]
        result = await client.write_registers(1, valuesToWrite)
        if not result.isError():
            print(f"Successfully sent packet to Slave {slave_id}.")
        else:
            print(f"Error sending packet to Slave {slave_id}: {result}")

        newValues = await client.read_holding_registers(1, count=15)
        print(newValues)


        # Attendi un altro 15 secondi (totale 30 secondi di connessione)
        # await asyncio.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Chiudi la connessione dopo 60 secondi
        if client.connected:
            print("Closing connection after 60 seconds...")
            client.close()
            print("Connection closed.")
        else:
            print("Client was already disconnected.")

async def monitor_connection(client):
    """
    Monitora lo stato della connessione ogni 0.5 secondi.
    """
    while client.connected:
        print(f"Connection Status: {client.connected}")
        await asyncio.sleep(0.5)

# Funzione principale
async def main():
    # Crea il client Modbus asincrono
    client = AsyncModbusTcpClient("localhost", port=502)

    # Invoca la funzione che invia un pacchetto dopo 30 secondi
    await send_packet_after_delay(client, slave_id=1)

# Esegui la funzione asincrona principale
asyncio.run(main())