
from pio2arduino.frontEnd_module import get_user_input

# Get user input
project_name, main_dir, save_dir = get_user_input()

print(f'Project Name: {project_name}')
print(f'Main Directory: {main_dir}')
print(f'Save Directory: {save_dir}')