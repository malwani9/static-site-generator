from markdown_blocks import markdown_to_html_node
from htmlnode import HTMlNode
import os
from pathlib import Path

def generate_pages_recursive(base_path, template_path, dest_path):
    for item in os.listdir(base_path):
        src_path = os.path.join(base_path, item)
        dst_path = os.path.join(dest_path, item)
        if os.path.isfile(src_path):
            new_dest_path = Path(dst_path).with_suffix(".html")
            generate_page(src_path, template_path, new_dest_path)
        else:
            generate_pages_recursive(src_path, template_path, dst_path)

def generate_page(base_path, template_path, dest_path):
    print(f"Generate page from from {base_path} to {dest_path} using {template_path}")
    with open(base_path, "r") as from_file:
       from_content = from_file.read()
    with open(template_path, "r") as template_file:
       template_content = template_file.read()
    
    html_node = markdown_to_html_node(from_content)
    html_code = html_node.to_html()

    title = extract_title(from_content)

    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_code)

    href_rerplace = "href=\"/"
    src_replace = "src=\"/"

    final_content = final_content.replace(href_rerplace, f"href=\"{base_path}").replace(src_replace, f"src=\"{base_path}")

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w") as dest_file:
       dest_file.write(final_content)

    
def extract_title(markdown):
   first_line = markdown.split("\n")[0]
   if markdown.startswith("# "):
      title = first_line[2:].strip()
      return title
   else:
      raise ValueError("No title found!")