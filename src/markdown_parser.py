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
      image_tuples = extract_markdown_images(old_node.text)
      if len(image_tuples) < 1:
         new_nodes.append(TextNode(old_node.text, TextType.TEXT, None))
         continue
      
      split_nodes = []
      counter = 0
      for i in range(len(image_tuples)):
          if i == 0:
             split_nodes = old_node.text.split(f"![{image_tuples[i][0]}]({image_tuples[i][1]})", 1)
             continue
          image_element = split_nodes.pop(i)
          split_nodes += image_element.split(f"![{image_tuples[i][0]}]({image_tuples[i][1]})", 1)
       
      #print(f"SPLIT_NODES : {split_nodes}\n")
      for split_node in split_nodes:
          if split_node == "":
             continue
          new_nodes.append(TextNode(split_node, TextType.TEXT, None))
          if counter <  len(image_tuples) and len(image_tuples) != 1:
             new_nodes.append(TextNode(image_tuples[counter][0], TextType.IMAGE, image_tuples[counter][1]))
             counter += 1

      if len(image_tuples) == 1:
         new_nodes.append(TextNode(image_tuples[0][0], TextType.IMAGE, image_tuples[0][1]))
         continue
   #print(f"NEW NODES LIST : {new_nodes} \n")
   return new_nodes

def split_nodes_link(old_nodes):
   new_nodes = []
   for old_node in old_nodes:
      link_tuples = extract_markdown_links(old_node.text)
      if len(link_tuples) < 1:
         new_nodes.append(TextNode(old_node.text, TextType.TEXT, None))
         continue
      
      split_nodes = []
      counter = 0
      for i in range(len(link_tuples)):
          if i == 0:
             split_nodes = old_node.text.split(f"[{link_tuples[i][0]}]({link_tuples[i][1]})", 1)
             continue
          link_element = split_nodes.pop(i)
          split_nodes += link_element.split(f"[{link_tuples[i][0]}]({link_tuples[i][1]})", 1)
       
      #print(f"SPLIT_NODES : {split_nodes}\n")
      for split_node in split_nodes:
          if split_node == "":
             continue
          new_nodes.append(TextNode(split_node, TextType.TEXT, None))
          if counter <  len(link_tuples) and len(link_tuples) != 1:
             new_nodes.append(TextNode(link_tuples[counter][0], TextType.LINK, link_tuples[counter][1]))
             counter += 1
      
      if len(link_tuples) == 1:
         new_nodes.append(TextNode(link_tuples[0][0], TextType.LINK, link_tuples[0][1]))
         continue
   #print(f"NEW NODES LIST : {new_nodes} \n")
   return new_nodes

def extract_markdown_images(text):
   matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return matches

def extract_markdown_links(text):
   matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return matches