import paramiko

# VM and disk details
HOST = "172.203.248.105"  # VM's public IP
USERNAME = "arko"
PASSWORD = "Welcome@12345"
VG_NAME = "vg_data_new"  # New VG name
LV_NAME = "lv_data_new"  # New LV name
MOUNT_POINT = "/mnt/data_new"  # New mount point

# Commands to create PV, VG, LV, format, and mount the filesystem with non-interactive flags
commands = [
    "echo y | sudo pvcreate -ff /dev/sdb",  # Added -ff to force initialize pvcreate
    f"sudo vgcreate {VG_NAME} /dev/sdb",
    f"sudo lvcreate -y -l 100%FREE -n {LV_NAME} {VG_NAME}",
    f"sudo mkfs.ext4 -F /dev/{VG_NAME}/{LV_NAME}",
    f"sudo mkdir -p {MOUNT_POINT}",
    f"sudo mount /dev/{VG_NAME}/{LV_NAME} {MOUNT_POINT}",
    f"echo '/dev/{VG_NAME}/{LV_NAME} {MOUNT_POINT} ext4 defaults 0 0' | sudo tee -a /etc/fstab"
]

def execute_commands(commands):
    print("Debug: Starting command execution on /dev/sdb with new volume group and logical volume names")
    try:
        # Establish SSH connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USERNAME, password=PASSWORD)
        
        # Execute each command
        for command in commands:
            print(f"Executing: {command}")
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print(f"Output: {output}")
            if error:
                print(f"Error: {error}")
        
        print("Disk setup completed successfully with new names.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

# Run the function
execute_commands(commands)
