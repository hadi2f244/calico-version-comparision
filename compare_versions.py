import os
import difflib
from packaging import version

excluded_dirs = [".git"]

def get_sorted_versions(directory):
    # Get all directories and sort them by version
    versions = [dir for dir in os.listdir(directory) if os.path.isdir(os.path.join(directory, dir)) and dir.strip() not in excluded_dirs ]
    versions.sort(key=lambda ver: version.parse(ver.lstrip('v')))
    return versions

def compare_files(file1, file2):
    # Read the contents of each file
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()
    
    # Create a Differ object and calculate the differences
    differ = difflib.Differ()
    diff = list(differ.compare(file1_lines, file2_lines))
    
    # Generate a readable diff output
    diff_text = []
    for line in diff:
        if line.startswith('+ ') or line.startswith('- '):
            diff_text.append(line)
    
    return diff_text

def main():
    directory = '.'  # Directory where the version folders are located
    versions = get_sorted_versions(directory)
    
    # Compare files between consecutive versions
    for i in range(len(versions) - 1):
        current_version = versions[i]
        next_version = versions[i + 1]
        file1 = os.path.join(directory, current_version, 'calico.yaml')
        file2 = os.path.join(directory, next_version, 'calico.yaml')
        differences = compare_files(file1, file2)

        # Formatting the header for clearer differentiation
        print("#############################################################")
        print(f"################### Differences between {current_version} and {next_version}:######################")
        
        if differences:
            for diff in differences:
                print(diff)
        else:
            print("No differences found.")

if __name__ == "__main__":
    main()

