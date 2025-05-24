import os 
import shutil
from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from content_generator import generate_page, generate_pages_recursive

src = "./static" 
dst = "./public"
dest_path = "./public" 
from_path = "./content"
template_path = "./template.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    print("Copying static files to public dir...")
    copy_files_recursive(src, dst)
    
    print("generating page...")
    generate_pages_recursive(from_path, template_path, dest_path)

main()