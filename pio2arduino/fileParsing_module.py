import os
import shutil
import glob
import re
import errno

_DEBUG_PRINT = True

def compileProject(main_dir, save_dir, project_name, addMessage):
  isSuccess = buildDir(save_dir, project_name, addMessage)
  if not isSuccess:
    addMessage('Program Halted')
    return False
  
  copyOperations = [copyMain, copySrc, copyLib, copyLibDeps]
  copyArgs = [(main_dir, save_dir, project_name, addMessage)] * len(copyOperations)
  for func, arg in zip(copyOperations, copyArgs):
    if not func(*arg):
      addMessage('Program Halted')
      return False
    
  isSuccess, all_files = getAllFiles(save_dir, project_name)
  if not isSuccess:
    addMessage('Program Halted')
    return False
  
  isSuccess = updateIncludes(all_files, addMessage)
  if not isSuccess:
    addMessage('Program Halted')
    return False
  
  isSuccess = deleteMainCpp(save_dir, project_name, addMessage)
  if not isSuccess:
    addMessage('Program Halted')
    return False
  
  return True




def buildDir(save_dir, project_name, addMessage):
  dir_path = os.path.join(save_dir, project_name)
  try:
    os.makedirs(dir_path, exist_ok=False)
    return True
  except OSError as e:
    if e.errno == errno.EEXIST:
      addMessage(f'Directory {dir_path} already exists.')
    elif e.errno in {errno.ENOTDIR, errno.EINVAL}:
      addMessage(f'Invalid character in the name {project_name}.')
    else:
      addMessage(f'Failed to create directory {dir_path}.')
      debugPrint(e)
      return False
  except Exception as e:
    addMessage(f'Failed to create directory {dir_path}.')
    debugPrint(e)
    return False
    
def copyMain(main_dir, save_dir, project_name, addMessage):
  try:
    shutil.copy2(f'{main_dir}/src/main.cpp', f'{os.path.join(save_dir, project_name)}/{project_name}.ino')
    return True
  except Exception as e:
    addMessage(f'Failed to copy main file from {main_dir}/src/main.cpp to {os.path.join(save_dir, project_name)}/{project_name}.ino')
    debugPrint(e)
    return False
    
def copySrc(main_dir, save_dir, project_name, addMessage):
  try:
    for file in glob.glob(f'{main_dir}/src/*'):
      if file != f'{main_dir}/src/main.cpp':
        destination = os.path.join(save_dir, project_name)
        shutil.copy2(file, destination)
        addMessage(f'Successfully copied {os.path.basename(file)} from {file} to {destination}')
    return True
  except Exception as e:
    addMessage(f'Failed to copy files from {main_dir}/src to {os.path.join(save_dir, project_name)}')
    debugPrint(e)
    return False
  
def copyLib(main_dir, save_dir, project_name, addMessage):
  try:
    for dir in glob.glob(f'{main_dir}/lib/*'):
      for file in glob.glob(f'{dir}/src/*'):
        destination = os.path.join(save_dir, project_name)
        shutil.copy2(file, destination)
        addMessage(f'Successfully copied {os.path.basename(file)} from {file} to {destination}')
    return True
  except Exception as e:
    addMessage(f'Failed to copy library files from {main_dir}/lib to {os.path.join(save_dir, project_name)}')
    debugPrint(e)
    return False
  
def copyLibDeps(main_dir, save_dir, project_name, addMessage):
  try:
    for root, dirs, files in os.walk(f'{main_dir}/.pio/libdeps'):
      dirs[:] = [d for d in dirs if d.lower() not in ['examples', 'example', 'tests', 'test']]
      for file in files:
        if file.endswith(('.h', '.cpp', '.c')):
          source = os.path.join(root, file)
          destination = os.path.join(save_dir, project_name)
          shutil.copy2(source, destination)
          addMessage(f'Successfully copied {file} from {source} to {destination}')
    return True
  except Exception as e:
    addMessage(f'Failed to copy all library dependencies from {main_dir}/.pio/libdeps to {os.path.join(save_dir, project_name)}')
    debugPrint(e)
    return False
  
def getAllFiles(save_dir, project_name):
  try:
    all_files = glob.glob(f'{os.path.join(save_dir, project_name)}/*.h') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.cpp') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.c') + glob.glob(f'{os.path.join(save_dir, project_name)}/*.ino')
    return True, all_files
  except Exception as e:
    debugPrint(e)
    return False, None
  
def updateIncludes(all_files, addMessage):
  parsed_includes = 0
  try:
    for file_path in all_files:
      with open(file_path, 'rb') as file:
          content = file.read().decode('utf-8', errors='ignore')
          content = re.sub(r'#include "([^"]*[\\/])([^\\/"]*)"', r'#include "\2"', content)
      for include_file in all_files:
          file_name = os.path.basename(include_file)
          content = re.sub(f'#include <{re.escape(file_name)}>', f'#include "{file_name}"', content)
          parsed_includes += 1
      with open(file_path, 'wb') as file:
          file.write(content.encode('utf-8'))
    addMessage(f'Successfully parsed {parsed_includes} #include statements in all files')
    return True
  except Exception as e:
    debugPrint(e)
    return False
  
def deleteMainCpp(save_dir, project_name, addMessage):
  try:
    main_cpp_path = os.path.join(save_dir, project_name, 'main.cpp')
    if os.path.exists(main_cpp_path):
      os.remove(main_cpp_path)
      addMessage(f'Successfully deleted {main_cpp_path}')
    return True
  except Exception as e:
    addMessage(f'Failed to delete {main_cpp_path}')
    debugPrint(e)
    return False
  
def debugPrint(message):
  if _DEBUG_PRINT:
    print(message)