import os 
import shutil
from textnode import TextNode, TextType
from copystatic import copy_files_recursive

src = "./static" 
dst = "./public" 

def main():
    if os.path.exists(dst):
        shutil.rmtree(dst)
    
    copy_files_recursive(src, dst)
    

main()