import os
import random
import string
import time
from urllib.parse import urlparse
import ctypes

# -------------------------------------------------------
# Create a random folder inside ProgramData
# -------------------------------------------------------




def generate_random_folder():
    folder_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    base_path = r"C:\ProgramData"
    final_path = os.path.join(base_path, folder_name)

    if not os.path.exists(final_path):
        os.makedirs(final_path)

    return final_path

random_folder = generate_random_folder()



save_file_path = os.path.join(random_folder, "blocked_sites.txt")

# -------------------------------------------------------
# Collecting sites from the user
# -------------------------------------------------------

list_Options = []
i = 1

while True:
    user = input(f"Enter Option [{i}] (If you want to stop, enter 0): ")
    if user == "0":
        break
    list_Options.append(user)
    i += 1

# -------------------------------------------------------
# Domain extraction only
# -------------------------------------------------------

def get_domain(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    return parsed.netloc

list_Options_2 = [get_domain(a) for a in list_Options]

# -------------------------------------------------------
# Hosts file management
# -------------------------------------------------------

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

def update_hosts():
    try:
        with open(hosts_path, "r+") as file:
            content = file.read()
            for x in list_Options_2:
                entries = [x, f"www.{x}"]
                for entry in entries:
                    if entry not in content:
                        file.write(f"{redirect_ip} {entry}\n")
                        print(f"[{entry}] has been blocked.")
    except PermissionError:
        print("Error: Please run this script as Administrator to modify the hosts file.")

# Save websites to a file inside a random folder
with open(save_file_path, "w") as save_file:
    for x in list_Options_2:
        save_file.write(x + "\n")


ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

while True:
    update_hosts()
    time.sleep(60)


    