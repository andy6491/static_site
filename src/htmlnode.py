class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            return self.value or ""
    
        # If tag is provided, we need either value or children
        if self.value is None and (self.children is None or len(self.children) == 0):
            raise ValueError("HTMLNode with tag but no content")
    
        # Build props string
        props_str = ""
        if self.props:
            for key, value in self.props.items():
                props_str += f' {key}="{value}"'
    
        # Build children HTML
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
    
        # If we have value, use it as content
        if self.value is not None:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
        # Otherwise use children as content
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result = ""

        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("No value given")
        
        if self.tag is None:
            return self.value
        
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        props_html = self.props_to_html()

        result = f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

        return result

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag missing")
        
        if self.children is None:
            raise ValueError("children missing")
        
        children_html = [child.to_html() for child in self.children]

        children_content = "".join(children_html)

        if self.props is None:
            return f"<{self.tag}>{children_content}</{self.tag}>"
            
        return f"<{self.tag}{self.props_to_html()}>{children_content}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

