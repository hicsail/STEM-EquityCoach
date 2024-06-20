import os
import shutil
import zipfile
import rarfile
import tarfile

def is_compressed_file(mime_type) -> bool:
    compressed_mime_types = [
        'application/zip',
        'application/x-rar-compressed',
        'application/x-7z-compressed',
        'application/x-tar',
        'application/gzip'
    ]
    return mime_type in compressed_mime_types

# unzip content to a new folder
def extract_file(file_path, delete_zip=True) -> str:
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(file_path.replace('.zip', ''))
    elif file_path.endswith('.rar'):
        with rarfile.RarFile(file_path, 'r') as rar_ref:
            rar_ref.extractall(file_path.replace('.rar', ''))
    elif file_path.endswith('.tar'):
        with tarfile.open(file_path, 'r') as tar_ref:
            tar_ref.extractall(file_path.replace('.tar', ''))
    else:
        print('File format not supported')
        return None
    
    if delete_zip:
        os.remove(file_path)

    return file_path.replace('.zip', '').replace('.rar', '').replace('.tar', '')

def remove_directory(path) -> bool:
    try:
        shutil.rmtree(path)
        return True
    except Exception as e:
        print(f'Failed to delete {path}. Reason: {e}')
        return False

# clear all files in a directory
def clear_directory(path) -> bool:
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            return False
        
    return True