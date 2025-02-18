import subprocess
import shlex
import asyncio
from qemu.qmp import QMPClient
import socket
import json

class GuestAgentClient:
    def __init__(self):
        self.socket = socket.socket(family=socket.AF_UNIX)

    def connect(self, path):
        self.socket.connect(path)

    def execute_command(self, command, arguments=None):
        self.socket.sendall(bytes(json.dumps({
            "execute": command
        }), encoding="utf-8"))

        response = b""
        while True:
            buffer = self.socket.recv(4096)
            if len(buffer) == 0:
                break
            response += buffer

        return json.loads(response.decode())

    def __del__(self):
        self.socket.close()

class GuestMachine:
    def __init__(self, path, client_name):
        self.image_path = path
        self.qmp_client = QMPClient(f"guest-machine-{client_name}")
        self.qga_client = GuestAgentClient()
        self.guest_agent_ready = False

    async def start_vm_process(self):
        # Added -chardev and -device options for guest agent support
        cmd = shlex.split(
            f"qemu-system-x86_64 "
            f"-drive file={self.image_path},format=qcow2 "
            f"-m 2G "
            f"-qmp unix:qmp.sock,server=on,wait=off "
            f"-chardev socket,path=/tmp/qga.sock,server=on,wait=off,id=qga0 "
            f"-device virtio-serial "
            f"-device virtserialport,chardev=qga0,name=org.qemu.guest_agent.0 "
            f"-nic user,model=virtio-net-pci "
            f"-daemonize "
            f"-enable-kvm"
        )
        subprocess.run(cmd)
        await self.qmp_client.connect("qmp.sock")
        self.qga_client.connect("/tmp/qga.sock")

        print(await self.execute_qmp_command("query-commands"))
        
        # Wait for guest agent to become ready
        await self.wait_for_guest_agent(60*1)

    async def wait_for_guest_agent(self, timeout=60):
        start_time = asyncio.get_event_loop().time()
        print(start_time)
        while not self.guest_agent_ready:
            try:
                response = await self.qga_client.execute_command('guest-ping')
                print("Pinging")
                print(response)
                if response["return"] == {}:
                    self.guest_agent_ready = True
                    print("Guest is ready")
                    break
            except Exception as e:
                print(e)
                if asyncio.get_event_loop().time() - start_time > timeout:
                    raise TimeoutError("Guest agent did not become ready within timeout period")
                await asyncio.sleep(1)

    async def execute_qmp_command(self, command, arguments=None):
        return await self.qmp_client.execute(command, arguments)

    async def execute_guest_command(self, command):
        """Execute a command in the guest using guest-exec"""
        if not self.guest_agent_ready:
            raise RuntimeError("Guest agent is not ready")
        
        # Execute the command
        exec_response = await self.execute_qga_command('guest-exec', {
            'path': '/bin/sh',
            'arg': ['-c', command],
            'capture-output': True
        })
        
        # Get the command status and output
        pid = exec_response['pid']
        while True:
            status = await self.execute_qmp_command('guest-exec-status', 
                                                  {'pid': pid})
            if status['exited']:
                return {
                    'exit-code': status['exitcode'],
                    'out-data': status.get('out-data', ''),
                    'err-data': status.get('err-data', '')
                }
            await asyncio.sleep(0.1)

    def listener(self, event=None):
        return self.qmp_client.listener(event)

    async def disconnect(self):
        await self.execute_qmp_command("system_powerdown")
        await self.qmp_client.disconnect()