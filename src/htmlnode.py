class HTMlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Derived classes must override the method")
    
    def to_HTML_props(self):
        if self.props is None:
            return ""
        props_string = ""
        for key, item in self.props.items():
            props_string += f" {key}=\"{item}\""
        
        return props_string
    
    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, children: {self.children}, {self.props}"
    
class LeafNode(HTMlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf node must has a value")
        if self.tag == None:
            return self.value
        
        props_string = self.to_HTML_props()
        return f'<{self.tag}{props_string}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode: {self.tag}, {self.value}, {self.props}'

class ParentNode(HTMlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must has a tag")
        
        if self.children == None or self.children == []:
            raise ValueError("Parent node must have children")

        props_string = self.to_HTML_props()
        children_HTML = "".join(child.to_html() for child in self.children) # using generator expression
        return f'<{self.tag}{props_string}>{children_HTML}</{self.tag}>'
    
    def __repr__(self):
         return f'ParentNode: {self.tag}, {self.value}, children: {self.children}, {self.props}'
    
