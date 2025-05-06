import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
   new_nodes = []
   for node in old_nodes:
      if node.text_type != TextType.TEXT:
         new_nodes.append(node)
         continue
      
      split_nodes = []
      sections = node.text.split(delimiter)

      if len(sections) < 3 or len(sections) % 2 == 0:
         raise Exception(f"Invalid markdown syntax, missing closing {delimiter}")
      
      for i in range(len(sections)):
         if sections[i] == "":
            continue
         if i % 2 == 0:
            split_nodes.append(TextNode(sections[i], TextType.TEXT, None))
         else:
            split_nodes.append(TextNode(sections[i], text_type, None))

      new_nodes.extend(split_nodes)
   return new_nodes


def extract_markdown_images(text):
   if text == "":
      return None
   matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return matches

def extract_markdown_links(text):
   if text == "":
      return None
   matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return matches