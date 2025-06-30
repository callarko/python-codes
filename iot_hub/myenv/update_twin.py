from azure.iot.hub import IoTHubRegistryManager
import certifi
import ssl
import json

# Connection details
CONNECTION_STRING = "HostName=iothub-jein02-np-eas-ua-eztr01.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=MmjcbQ0RCmuIK/JfGO28odyxCf9ZN7TL9AIoTHrJNvA="
DEVICE_ID = "NodeMCU"

# Path to the CA bundle
ca_cert_path = certifi.where()

try:
    # Create IoTHubRegistryManager
    registry_manager = IoTHubRegistryManager.from_connection_string(CONNECTION_STRING, ca_cert=ca_cert_path)
   
    # Twin update properties
    twin_patch = {
        "properties": {
            "desired": {
                "temp": "100"
            }
        }
    }

    # Update the desired properties
    twin = registry_manager.update_twin(DEVICE_ID, json.dumps(twin_patch))

    print("Device twin updated successfully.")
    print(twin)

except Exception as ex:
    print(f"Error updating device twin: {str(ex)}")
    raise
