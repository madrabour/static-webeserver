

class HTMLNode:
    
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Not implemented yet")
    
    
    def props_to_html(self):
        form_string = "";
        if self.props:
            for item in self.props:
                form_string += " " + item + '="' + self.props[item] + '"'
        return form_string


    def __eq__(self, other):
        h1 = self.props
        if self.props:
            h1 = dict(sorted(self.props.items()))
        h2 = other.props
        if self.props:
            h2 = dict(sorted(other.props.items()))
        
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and h1 == h2
        )

    def __repr__(self):
        return f"HTMLNode(T: {self.tag}, v: {self.value}, c: {self.children}, p: {self.props_to_html()})"




class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag,value,None,props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("Value is missing")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



    def __eq__(self, other):
        h1 = self.props
        if self.props:
            h1 = dict(sorted(self.props.items()))
        h2 = other.props
        if self.props:
            h2 = dict(sorted(other.props.items()))
        
        return (
            self.tag == other.tag
            and self.value == other.value
            and h1 == h2
        )

    def __repr__(self):
        return f"HTMLNode(T: {self.tag}, v: {self.value}, c: NO CHILDREN ALLOWED, p: {self.props_to_html()})"



class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag,None,children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is missing")
        if not self.children:
            raise ValueError("Children is missing")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result
        
        
    def __eq__(self, other):
        h1 = self.props
        if self.props:
            h1 = dict(sorted(self.props.items()))
        h2 = other.props
        if self.props:
            h2 = dict(sorted(other.props.items()))
        
        return (
            self.tag == other.tag
            and self.children == other.children
            and h1 == h2
        )

    def __repr__(self):
        return f"HTMLNode(T: {self.tag}, v: NO VALUE ALLOWED, c: {self.children}, p: {self.props_to_html()})"

        
    




        