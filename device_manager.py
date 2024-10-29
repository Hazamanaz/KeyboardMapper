# device_manager.py

import hid

class DeviceManager:
    def __init__(self, vendor_id=None, product_id=None):
        """Initializes the DeviceManager."""
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
        print("DeviceManager initialized")

    def enumerate_devices(self):
        """Lists all connected HID devices with vendor/product details."""
        devices = hid.enumerate()
        device_list = []
        for d in devices:
            device_info = {
                "vendor_id": d['vendor_id'],
                "product_id": d['product_id'],
                "product_string": d.get('product_string', "Unknown Device")
            }
            device_list.append(device_info)
        return device_list

    def select_device(self, vendor_id, product_id):
        """Selects and opens the specified HID device."""
        self.vendor_id = vendor_id
        self.product_id = product_id
        try:
            self.device = hid.device()
            self.device.open(vendor_id, product_id)
            print(f"Device selected and opened: Vendor ID {vendor_id}, Product ID {product_id}")
        except OSError as e:
            print(f"Failed to open device: {e}")
            self.device = None

    def start_key_detection(self):
        """Detects a single key press for mapping purposes."""
        if not self.device:
            print("Device is not connected.")
            return None
        try:
            print("Starting key detection mode...")
            report = self.device.read(64)  # Read max 64 bytes per report
            if report:
                key_event = report[0]  # For simplicity, just reading the first byte
                print(f"Detected key event: {key_event}")
                return key_event
        except OSError:
            print("Error reading from the device.")
        return None

    def listen_for_keys(self, callback):
        """Continuously listens for keys and triggers callback with the key event."""
        if not self.device:
            print("Device is not connected.")
            return
        try:
            print("Listening for key inputs...")
            while True:
                report = self.device.read(64)
                if report:
                    key_event = report[0]
                    print(f"Key event detected: {key_event}")
                    callback(key_event)
        except OSError:
            print("Error reading from the device. Check the connection.")

    def close_device(self):
        """Closes the HID device connection."""
        if self.device:
            self.device.close()
            print("Device closed")
