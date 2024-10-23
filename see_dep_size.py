

import pkg_resources
import os

installed_packages = pkg_resources.working_set
package_sizes = {}

for package in installed_packages:
    package_path = package.location
    package_size = sum(os.path.getsize(os.path.join(package_path, f)) for f in os.listdir(package_path) if os.path.isfile(os.path.join(package_path, f)))
    package_sizes[package.project_name] = package_size

# Dump the sizes to size.txt
with open("size.txt", "w") as file:
    for name, size in package_sizes.items():
        file.write(f"{name}: {size / (1024 * 1024):.2f} MB\n")  # Convert bytes to MB

print("Package sizes have been written to size.txt.")
