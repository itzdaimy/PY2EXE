import subprocess
import sys
import requests
import os
import json

VERSION_URL = "https://raw.githubusercontent.com/itzdaimy/.py-to-.exe/refs/heads/main/versions.json"  
BAT_URL = "https://raw.githubusercontent.com/itzdaimy/.py-to-.exe/refs/heads/main/converter.bat" 

def create_bin_folder():
    if not os.path.exists("bin"):
        os.makedirs("bin")
        print("Created 'bin' folder.")

def check_local_version():
    version_file = "bin/version.json"
    if os.path.exists(version_file):
        with open(version_file, "r") as file:
            data = json.load(file)
            return data.get("version")
    return None

def update_local_version(version):
    version_data = {"version": version}
    with open("bin/version.json", "w") as file:
        json.dump(version_data, file)
    print(f"Local version updated to {version} in 'bin/version.json'.")

def get_github_version():
    try:
        response = requests.get(VERSION_URL)
        response.raise_for_status() 
        github_version = response.json().get("version")
        print(f"GitHub version: {github_version}")
        return github_version
    except Exception as e:
        print(f"Error fetching version from GitHub: {e}")
        return None

def download_bat_file(url, filename):
    print(f"Downloading {filename} from GitHub...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully.")
    else:
        print(f"Failed to download {filename}. HTTP Status: {response.status_code}")

def install_pyinstaller():
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def check_pyinstaller_version():
    try:
        result = subprocess.run(["pyinstaller", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("PyInstaller is not installed or not found in the PATH.")
            return False
        installed_version = result.stdout.strip()
        
        response = requests.get("https://pypi.org/pypi/pyinstaller/json")
        latest_version = response.json()["info"]["version"]
        
        if installed_version == latest_version:
            print(f"PyInstaller is up-to-date (version {installed_version}).")
            return True
        else:
            print(f"PyInstaller version {installed_version} is installed, but version {latest_version} is available.")
            print("Consider updating using: pip install --upgrade pyinstaller")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def reinstall_bat_if_needed():
    github_version = get_github_version()
    local_version = check_local_version()

    if not github_version:
        print("Failed to get GitHub version. Exiting...")
        return

    if local_version != github_version:
        print(f"Version mismatch. Local version: {local_version}, GitHub version: {github_version}")
        print("Reinstalling converter.bat...")
        
        download_bat_file(BAT_URL, "converter.bat")
        update_local_version(github_version)  

        subprocess.run(["converter.bat"]) 
    else:
        print("Versions match. No update required.")

if __name__ == "__main__":
    create_bin_folder()
    
    if not check_pyinstaller_version():
        install_pyinstaller()

    reinstall_bat_if_needed()
