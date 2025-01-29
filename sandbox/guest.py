import subprocess
import shlex
from qemu.qmp import QMPClient

class GuestMachine:
  def __init__(self, path, client_name):
    self.image_path = path
    self.qmp_client = QMPClient(f"guest-machine-{client_name}")

  async def start_vm_process(self):
    subprocess.run(shlex.split(f"qemu-system-x86_64 -drive file={self.image_path},format=qcow2 -m 2G -qmp unix:qmp.sock,server=on,wait=off -daemonize -enable-kvm"))
    await self.qmp_client.connect("qmp.sock")

  async def execute_qmp_command(self, command, arguments=None):
    return await self.qmp_client.execute(command, arguments)
  
  def listener(self, event=None):
    return self.qmp_client.listener(event)
  
  async def disconnect(self):
    await self.qmp_client.disconnect()

