import os 
import shutil
from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from content_generator import generate_page, generate_pages_recursive
import sys

src = "./static" 
dst = "./docs"
dest_path = "./docs" 
from_path = "./content"
template_path = "./template.html"

base_path = sys.argv[0] or "/"

def main():
    print("Deleting public directory...")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    print("Copying static files to public dir...")
    copy_files_recursive(src, dst)
    
    print("generating page...")
    generate_pages_recursive(from_path, template_path, dest_path)

main()