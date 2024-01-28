import asyncio
import sys

from bleak import BleakClient

batt_level = '00002a19-0000-1000-8000-00805f9b34fb'
uart_tx = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
uart_rx = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'


def data_received(sender, data):
    print(data)


async def main(mac):
    async with BleakClient(mac) as client:
        battery = await client.read_gatt_char(batt_level)
        print(f"Battery: {int(battery[0])}%")

        await client.start_notify(uart_rx, data_received)

        print("handshake")
        await client.write_gatt_char(uart_tx, b'\x5b\xfa\xed\x37\xa1\x1c')
        await client.write_gatt_char(uart_tx, b'BS')
        await client.write_gatt_char(uart_tx, b'PUB?')

        while True:
            print("left blinker")
            await client.write_gatt_char(uart_tx, b'LN')
            await asyncio.sleep(5)

            print("off")
            await client.write_gatt_char(uart_tx, b'ON')
            await asyncio.sleep(5)

            print("right blinker")
            await client.write_gatt_char(uart_tx, b'RN')
            await asyncio.sleep(5)

            print("off")
            await client.write_gatt_char(uart_tx, b'ON')
            await asyncio.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please pass your helmet's BLE MAC address as a command line argument.")
        sys.exit(1)

    mac = sys.argv[1]
    asyncio.run(main(mac))