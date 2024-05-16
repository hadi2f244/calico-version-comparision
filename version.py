import requests
from packaging import version

def get_calico_versions(api_url):
    # Send a GET request to the GitHub API
    response = requests.get(api_url)
    releases = response.json()
    
    # Check if the response contains valid data
    if not isinstance(releases, list):
        raise ValueError("Invalid API response")
    
    min_version = version.parse("3.25.0")
    valid_versions = []

    # Loop through each release and filter based on version
    for release in releases:
        # Extract the tag name which contains the version
        ver = version.parse(release['tag_name'].lstrip('v'))
        # Compare versions
        if ver >= min_version:
            valid_versions.append(release['tag_name'])
    
    return valid_versions

# API URL
api_url = "https://api.github.com/repos/projectcalico/calico/releases"
# Get and print valid versions
valid_versions = get_calico_versions(api_url)
print("Valid Calico versions:", valid_versions)
