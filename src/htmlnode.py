class HTMlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Derived classes must override the method")
    
    def to_HTML_props(self):
        if self.props == None:
            return ""
        props_string = ""
        for key, item in self.props.items():
            props_string += f" {key}=\"{item}\""
        
        return props_string
    
    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, children: {self.children}, {self.props}"