from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode









def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    
    htmlTest = HTMLNode("b", "Ein Fetter TEXT", [], {"class": "rot", "style": "font-weight:bold"})
    print (f"ht: {htmlTest}")

main()