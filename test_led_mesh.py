import asyncio
from bleak import BleakClient, BleakScanner
from struct import pack

CORE_WRITE_UUID = '72c90004-57a9-4d40-b746-534e22ec9f9e'

async def test_simple_write():
    print("Scanning for MESH devices...")
    devices = await BleakScanner.discover()

    device = next((d for d in devices if "MESH" in d.name), None)
    if not device:
        print("No MESH devices found.")
        return

    print(f"Found device: {device.name} - {device.address}")
    async with BleakClient(device) as client:
        print("Connected to device!")

        try:
            # Send a simple test command
            await client.write_gatt_char(CORE_WRITE_UUID, pack('<BBBB', 1, 0, 0, 0), response=True)
            print("Simple write successful.")
        except Exception as e:
            print(f"Error during simple write: {e}")

asyncio.run(test_simple_write())
