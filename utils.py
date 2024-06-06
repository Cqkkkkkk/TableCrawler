import os
import glob
import shutil


def get_newest_file(directory):
    # Get list of all files in the directory
    list_of_files = glob.glob(os.path.join(directory, '*'))
    
    # Filter out directories, keep only xlsx files
    list_of_files = [f for f in list_of_files if os.path.isfile(f) and f.endswith('.xlsx')]
    
    if not list_of_files:
        return None
    
    # Find the newest file
    newest_file = max(list_of_files, key=os.path.getmtime)
    if(not newest_file.endswith('.xlsx')):
        return None
    # return os.path.basename(newest_file)
    return newest_file


def move_file(src_path, dest_dir):
    # Create the destination directory if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Construct full file path
    file_name = os.path.basename(src_path)
    flatten_file_name = file_name.lower().replace(' ', '_')
    dest_file = os.path.join(dest_dir, flatten_file_name)
    
    # Move the file
    shutil.move(src_path, dest_file)
    print(f'Moved: {src_path} -> {dest_file}')
    return dest_file