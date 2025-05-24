import os 
import shutil
from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from content_generator import generate_page, generate_pages_recursive
import sys

static_path = "./static"
dest_path = "./docs" 
from_path = "./content"
template_path = "./template.html"

default_path = "/"

def main():
    base_path = default_path
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    print("Copying static files to docs dir...")
    copy_files_recursive(static_path, dest_path)
    
    print("generating page...")
    generate_pages_recursive(from_path, template_path, dest_path, base_path)

main()