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


def split_nodes_image(old_nodes):
   new_nodes = []
   for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
         new_nodes.append(old_node)
         continue
      
      original_text = old_node.text
      image_tuples = extract_markdown_images(original_text)

      if len(image_tuples) < 1:
         new_nodes.append(old_node)
         continue
      
      for image_tuple in image_tuples:
         parts = original_text.split(f"![{image_tuple[0]}]({image_tuple[1]})", 1)
         if len(parts) != 2:
            raise Exception("Invalid markdown!, missing iamge closing")
        
         if parts[0] != "":
           new_nodes.append(TextNode(parts[0], TextType.TEXT, None))
        
         new_nodes.append(TextNode(image_tuple[0], TextType.IMAGE, image_tuple[1]))

         original_text = parts[1]

      if original_text != "":
         new_nodes.append(TextNode(original_text, TextType.TEXT, None))

   return new_nodes

def split_nodes_link(old_nodes):
   new_nodes = []
   for old_node in old_nodes:
      if old_node.text_type != TextType.TEXT:
         new_nodes.append(old_node)
      
      original_text = old_node.text
      link_tuples = extract_markdown_links(original_text)

      if len(link_tuples) < 1:
         new_nodes.append(TextNode(original_text, TextType.TEXT, None))
      
      for link_tuple in link_tuples:
         parts = original_text.split(f"[{link_tuple[0]}]({link_tuple[1]})", 1)

         if len(parts) != 2:
            raise Exception("Invalid markdown!, missing link closing")
         
         if parts[0] != "":
            new_nodes.append(TextNode(parts[0], TextType.TEXT, None))
        
         new_nodes.append(TextNode(link_tuple[0], TextType.LINK, link_tuple[1]))

         original_text = parts[1]
      
      if original_text != "":
         new_nodes(TextNode(original_text, TextType.TEXT, None))

   return new_nodes

def extract_markdown_images(text):
   matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return matches

def extract_markdown_links(text):
   matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return matches