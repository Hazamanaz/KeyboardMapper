import os
import platform

if platform.system() == "Windows":
    lib_path = os.path.join(os.path.dirname(__file__), "lib")
    os.add_dll_directory(lib_path)

import hid


devices = hid.enumerate()
for device in devices:
    print(f"Vendor ID: {device['vendor_id']}, Product ID: {device['product_id']}, Product: {device['product_string']}")
