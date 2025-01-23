from pymodbus.client import ModbusTcpClient

# Funzione per scansionare tutti gli slave
def modbus_scan(ip_address, port=502, start_id=1, end_id=247):
    """
    Scansiona tutti gli ID degli slave Modbus per reperire informazioni.
    
    Args:
        ip_address (str): L'indirizzo IP del target Modbus TCP.
        port (int): La porta Modbus TCP (default: 502).
        start_id (int): L'ID dello slave da cui iniziare la scansione (default: 1).
        end_id (int): L'ultimo ID dello slave da scansionare (default: 247).
    
    Returns:
        dict: Informazioni reperite dagli slave disponibili.
    """
    # Dizionario per memorizzare i risultati
    results = {}

    # Creazione del client Modbus TCP
    client = ModbusTcpClient(ip_address, port=port)

    # Connessione al server Modbus
    if not client.connect():
        print("Errore: impossibile connettersi al server Modbus TCP.")
        return None

    print(f"Inizio scansione su {ip_address}:{port}...")
    for slave_id in range(start_id, end_id + 1):
        print(f"Scansionando Slave ID: {slave_id}")
        try:
            # Prova a leggere i registri degli holding registers (indirizzo 0, 10 registri)
            response = client.read_holding_registers(address=0, count=10, slave=slave_id)

            if not response.isError():
                # Se la risposta è valida, salvala
                results[slave_id] = response.registers
                print(f"  -> Slave {slave_id} risponde: {response.registers}")
            else:
                print(f"  -> Nessuna risposta da Slave {slave_id}")
        except Exception as e:
            print(f"  -> Errore comunicando con Slave {slave_id}: {str(e)}")

    # Disconnetti il client
    client.close()

    print("Scansione completata.")
    return results


# Esegui la scansione
if __name__ == "__main__":
    target_ip = "localhost"  # IP del server Modbus
    target_port = 502            # Porta Modbus TCP
    results = modbus_scan(target_ip, target_port)

    if results:
        print("\nRisultati della scansione:")
        for slave_id, data in results.items():
            print(f"  - Slave ID {slave_id}: {data}")
    else:
        print("Nessun dispositivo trovato.")
