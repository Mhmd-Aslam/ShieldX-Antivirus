from sandbox.guest import GuestMachine
import asyncio

async def main():
  client = GuestMachine("sandbox/images/arch-linux.qcow2", "arch-linux")
  await client.start_vm_process()

  with client.listener() as listener:
    print(await listener.get())

  await client.disconnect()

if __name__ == "__main__":
  asyncio.run(main())