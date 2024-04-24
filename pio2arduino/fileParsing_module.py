import os
import shutil
import glob
import re

debug_print = True

def buildDir(save_dir, project_name):
  try:
    os.makedirs(os.path.join(save_dir, project_name), exist_ok=True)
    return True
  except Exception as e:
    debugPrint(e)
    return False
    
def copyMain(main_dir, save_dir, project_name):
  try:
    shutil.copy2(f'{main_dir}/src/main.cpp', f'{os.path.join(save_dir, project_name)}/{project_name}.ino')
    return True
  except Exception as e:
    debugPrint(e)
    return False
    
def copySrc(main_dir, save_dir, project_name):
  copied_filed = []
  try:
    for file in glob.glob(f'{main_dir}/src/*'):
      if file != f'{main_dir}/src/main.cpp':
        shutil.copy2(file, os.path.join(save_dir, project_name))
        copied_filed.append(os.path.basename(file))
    return True, copied_filed
  except Exception as e:
    debugPrint(e)
    return False, None
  
def copyLib(main_dir, save_dir, project_name):
  copied_filed = []
  try:
    for dir in glob.glob(f'{main_dir}/lib/*'):
      for file in glob.glob(f'{dir}/src/*'):
        shutil.copy2(file, os.path.join(save_dir, project_name))
        copied_filed.append(os.path.basename(file))
    return True, copied_filed
  except Exception as e:
    debugPrint(e)
    return False, None
  
def copyLibDeps(main_dir, save_dir, project_name):
  copied_filed = []
  try:
    for root, dirs, files in os.walk(f'{main_dir}/.pio/libdeps'):
      dirs[:] = [d for d in dirs if d.lower() not in ['examples', 'example', 'tests', 'test']]
      for file in files:
        if file.endswith(('.h', '.cpp', '.c')):
          shutil.copy2(os.path.join(root, file), os.path.join(save_dir, project_name))
          copied_filed.append(file)
    return True, copied_filed
  except Exception as e:
    debugPrint(e)
    return False, None
  
def getAllFiles(save_dir, project_name):
  try:
    all_files = glob.glob(f'{os.path.join(save_dir, project_name)}/*.h') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.cpp') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.c') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.ino')
    return True, all_files
  except Exception as e:
    debugPrint(e)
    return False, None
  
def updateIncludes(all_files):
  parsed_includes = 0
  try:
    for file_path in all_files:
      with open(file_path, 'rb') as file:
          content = file.read().decode('utf-8', errors='ignore')
      for include_file in all_files:
          file_name = os.path.basename(include_file)
          content = re.sub(f'#include <{re.escape(file_name)}>', f'#include "{file_name}"', content)
          parsed_includes += 1
      with open(file_path, 'wb') as file:
          file.write(content.encode('utf-8'))
    return True, parsed_includes
  except Exception as e:
    debugPrint(e)
    return False, None
  
def deleteMainCpp(save_dir, project_name):
  try:
    main_cpp_path = os.path.join(save_dir, project_name, 'main.cpp')
    if os.path.exists(main_cpp_path):
      os.remove(main_cpp_path)
    return True
  except Exception as e:
    debugPrint(e)
    return False
  
def debugPrint(message):
  if debug_print:
    print(message)