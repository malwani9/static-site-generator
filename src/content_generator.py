from markdown_blocks import markdown_to_html_node
from htmlnode import HTMlNode
import os
from pathlib import Path

def generate_pages_recursive(content_path, template_path, dest_path, base_path):
    for item in os.listdir(content_path):
        from_path = os.path.join(content_path, item)
        dst_path = os.path.join(dest_path, item)
        if os.path.isfile(from_path):
            new_dest_path = Path(dst_path).with_suffix(".html")
            generate_page(from_path, template_path, new_dest_path, base_path)
        else:
            generate_pages_recursive(from_path, template_path, dst_path, base_path)

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generate page from from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
       from_content = from_file.read()
    with open(template_path, "r") as template_file:
       template_content = template_file.read()
    
    html_node = markdown_to_html_node(from_content)
    html_code = html_node.to_html()

    title = extract_title(from_content)

    final_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_code)

    final_content = final_content.replace('href="/', 'href="' + base_path)
    final_content = final_content.replace('src="/', 'src="' + base_path)

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