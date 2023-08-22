import os
import subprocess

# file name to run
progfilename = "n_marine_interface.py"

# Specify the path to the directory
directory_path = r"C:/Users/lahar/Downloads/success_multi_move_5/success_multi_move_5"

# Initialize an empty list to store the paths of .pth files
pth_file_paths = []
# Loop through all files in the directory
for filename in sorted(os.listdir(directory_path)):
    # Check if the file has a .pth extension
    c+=1
    if filename.endswith(".pth"):
        # Create the full path to the file
        file_path = os.path.join(directory_path, filename)
        modified_file_path = file_path.rsplit("\\", 1)[0] + "/" + filename
        try:
            subprocess.run(["python", progfilename, modified_file_path, filename], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running program with path {e}")
