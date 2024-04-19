import os
import shutil
import glob
import re
import tkinter as tk
from tkinter import filedialog, simpledialog

# Create a root window and hide it
root = tk.Tk()
root.withdraw()

# Prompt the user for the project name
project_name = simpledialog.askstring("Input", "Enter the project name:", parent=root)

# Prompt the user to select the main directory
main_dir = filedialog.askdirectory(title="Select the main directory")

# Prompt the user to select the save directory
save_dir = filedialog.askdirectory(title="Select the directory to save the new project to")

# Create a new directory with the project name in the save directory
os.makedirs(os.path.join(save_dir, project_name), exist_ok=True)
print(f'successfully created new directory @ {os.path.join(save_dir, project_name)}')

# Copy and rename main.cpp to main.ino
shutil.copy2(f'{main_dir}/src/main.cpp', f'{os.path.join(save_dir, project_name)}/{project_name}.ino')
print(f'successfully found main.cpp and renamed it to {project_name}.ino')

print('Searching src directory.................')
# Copy all other files from the src directory to the new directory
for file in glob.glob(f'{main_dir}/src/*'):
    if file != f'{main_dir}/src/main.cpp':
        shutil.copy2(file, os.path.join(save_dir, project_name))
        print(f'Found and copied {os.path.basename(file)} to the {os.path.join(save_dir, project_name)} folder')

print('Searching lib directory.................')
# Copy all library files from the lib directory to the new directory
for dir in glob.glob(f'{main_dir}/lib/*'):
    for file in glob.glob(f'{dir}/src/*'):
        shutil.copy2(file, os.path.join(save_dir, project_name))
        print(f'Found and copied {os.path.basename(file)} to the {os.path.join(save_dir, project_name)} folder')


print('Searching .pio/libdeps directory.................')
# Copy all library files from the .pio/libdeps directory to the new directory
for root, dirs, files in os.walk(f'{main_dir}/.pio/libdeps'):
    dirs[:] = [d for d in dirs if d.lower() not in ['examples', 'example', 'tests', 'test']]
    for file in files:
        if file.endswith(('.h', '.cpp', '.c')):
            shutil.copy2(os.path.join(root, file), os.path.join(save_dir, project_name))
            print(f'Found and copied {file} to the {os.path.join(save_dir, project_name)} folder')

print('Gathering all .h, .cpp, and .c files.................')
# Get a list of all .h, .cpp, and .c files in the new directory
all_files = glob.glob(f'{os.path.join(save_dir, project_name)}/*.h') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.cpp') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.c') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.ino')

print(f'Parsing all files in {project_name} for #include statements..........................')
# Replace <> with "" in #include statements in all files
parsed_includes = 0
for file_path in all_files:
    with open(file_path, 'rb') as file:
        content = file.read().decode('utf-8', errors='ignore')
    for include_file in all_files:
        file_name = os.path.basename(include_file)
        content = re.sub(f'#include <{re.escape(file_name)}>', f'#include "{file_name}"', content)
        parsed_includes += 1
    with open(file_path, 'wb') as file:
        file.write(content.encode('utf-8'))
print(f'Found and changed {parsed_includes} #include statements in all files in {project_name}')

# Check if main.cpp exists in the new directory and delete it if it does
main_cpp_path = os.path.join(save_dir, project_name, 'main.cpp')
if os.path.exists(main_cpp_path):
    os.remove(main_cpp_path)
    print(f'successfully deleted {main_cpp_path}')

print('Release script complete!')