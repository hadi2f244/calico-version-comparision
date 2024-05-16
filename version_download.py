import requests
import os
from packaging import version

BASE_VERSION = "v3.24.0"

def get_calico_versions(api_url):
    response = requests.get(api_url)
    releases = response.json()
    
    if not isinstance(releases, list):
        raise ValueError("Invalid API response")
    
    min_version = version.parse(BASE_VERSION)
    valid_versions = []

    for release in releases:
        ver = version.parse(release['tag_name'].lstrip('v'))
        if ver >= min_version:
            valid_versions.append(release['tag_name'])
    
    return valid_versions

def download_calico_file(version, base_url):
    url = base_url.replace('<calico_version>', version)
    response = requests.get(url)
    if response.status_code == 200:
        # Ensure the directory for the version exists
        dir_path = f"./{version}"
        os.makedirs(dir_path, exist_ok=True)
        # Write the response content to a file
        with open(os.path.join(dir_path, "calico.yaml"), "wb") as file:
            file.write(response.content)
        print(f"Downloaded calico.yaml for {version} successfully.")
    else:
        print(f"Failed to download calico.yaml for {version}.")

# API URL for Calico releases
api_url = "https://api.github.com/repos/projectcalico/calico/releases"
# Base URL for downloading calico.yaml
base_url = "https://raw.githubusercontent.com/projectcalico/calico/<calico_version>/manifests/calico.yaml"

# Get valid versions
valid_versions = get_calico_versions(api_url)
# Download calico.yaml for each version
for version in valid_versions:
    download_calico_file(version, base_url)

