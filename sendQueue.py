import paramiko
import pyserial

PI_HOST = '192.168.1.15'  # <-- Replace with your Pi's IP address
PI_USER = 'pi'
PI_PASS = 'raspberry'     # <-- Replace with your Pi's password

def _send_cmd_arduino(data):
    """Send a command to the Arduino."""
    with pyserial.Serial('COM_PORT', 9600) as ser: #TODO verify, this code is all chatgpt lol
        ser.write(data.encode())
        ser.flush()
        print("Command sent to Arduino.")


def _send_cmd_pi(data):
    """Send a command to the Raspberry Pi."""
    # --- Connection Details ---

    # Create an SSH client instance
    client = paramiko.SSHClient()

    # Automatically add the server's host key (less secure, but good for starting)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        print("Connecting to the Raspberry Pi...")
        client.connect(hostname=PI_HOST, username=PI_USER, password=PI_PASS)
        print("Successfully connected!")

        # --- Execute a command ---
        command = 'hostname -I' # Example: get the IP address of the Pi itself
        print(f"Executing command: {command}")
        
        stdin, stdout, stderr = client.exec_command(command)

        # Read and print the command's output
        output = stdout.read().decode('utf-8').strip()
        errors = stderr.read().decode('utf-8').strip()

        if output:
            print("\n--- Output ---")
            print(output)
            
        if errors:
            print("\n--- Errors ---")
            print(errors)

    except Exception as e:
        print(f"Connection Failed: {e}")

    finally:
        # Always close the connection
        print("Closing connection.")
        client.close()




def add_command_to_queue(command):
    """Add a command to the send queue."""
    send_queue.append(command)

def send_command_to_device():
    """Send the next command in the send queue to the device."""
    if send_queue:
        command = send_queue.pop(0)
        # Here you would add the code to actually send the command to the device.

        print(f"Sending command: {command}")
    else:
        print("Send queue is empty.")

def wait_for_ack():
    """Wait until there is at least one item in the send queue."""
    while not send_queue:
        pass  # In a real implementation, consider using threading.Condition or similar.

send_queue = []