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
    client = AsyncModbusTcpClient("localhost", port=503, trace_packet=packet_logger)

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
    client = AsyncModbusTcpClient("localhost", port=503) #, trace_packet=packet_logger)

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
        await asyncio.sleep(15)

        # invio un messaggio di lettura coil al server 
        values = await client.read_coils(address=0, count=10, slave=1)
        print(f"Coils values: {values.bits}")

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


# Funzione principale
async def main():
    # Avvia il master_connected
    await master_connected()

# Esegui il programma principale
if __name__ == "__main__":
    asyncio.run(main())