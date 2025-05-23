import os
import shutil

def copy_files_recursive(src, dst):
    print(os.listdir(src))
    if not os.path.exists(dst):
       os.mkdir(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)


             
