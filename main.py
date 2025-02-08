from sandbox.guest import GuestMachine
import asyncio

async def main():
  client = GuestMachine("sandbox/images/arch-linux.qcow2", "arch-linux")
  try:
    await client.start_vm_process()

    #await client.execute_guest_command("")

    await client.disconnect()
  except Exception:
    await client.disconnect()

if __name__ == "__main__":
  asyncio.run(main())