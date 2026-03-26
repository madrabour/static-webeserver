import re
from enum import Enum
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import text_to_textnodes




def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    block_node_list = []
    for block in block_list:
        stripped_block = block.strip()
        if stripped_block:
            block_node_list.append(stripped_block)
    return block_node_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):

    block_filter_list = [
        (r"^#{1,6} .*$", BlockType.HEADING),
        (r"^```\n(.*\n)+```\n?$", BlockType.CODE),
        (r"^(>\s?.*\n)+(>\s?.*\n?)?|(>\s?.*\n?)$", BlockType.QUOTE),
        (r"^(-\s.*\n)+(-\s.*\n?)?|(-\s.*\n?)$", BlockType.ULIST),
        (r"^([0-9]+\.\s.*\n)+([0-9]+\.\s.*\n?)?|([0-9]+\.\s.*\n?)$", BlockType.OLIST),
       ]
    for fitup in block_filter_list:
        fa_erg = re.fullmatch(fitup[0], block)
        #print(f"faerg: {fa_erg}")
        if fa_erg:
            return fitup[1]
    return BlockType.PARAGRAPH



def text_to_html_nodes(text):

    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                bp = re.findall(r"^(#{1,6}) (.*)$", block)
                bi_nodes_html = text_to_html_nodes(bp[0][1])
                tag = f"h{len(bp[0][0])}"
                html_node = ParentNode(tag, bi_nodes_html)
                html_nodes.append(html_node)
              
            case BlockType.CODE:
                bp = re.findall(r"^```\n((.*\n)+)```\n?$", block)
                #print(f"bp: {bp}")
                html_node = LeafNode("code", bp[0][0])
                html_node = ParentNode("pre", [html_node])
                html_nodes.append(html_node)

            case BlockType.QUOTE:
                bp_liste = re.findall(r"^((>\s?.*\n)+(>\s?.*\n?)?|(>\s?.*\n?))$", block)
                quote = ""
                quote_lines = bp_liste[0][0].splitlines()
                for ql in quote_lines:
                    quote += ql[2:] + "\n"
                bi_nodes_html = text_to_html_nodes(quote.replace("\n", "<br>"))                   
                html_node = ParentNode("blockquote", bi_nodes_html)
                html_nodes.append(html_node)
    
            case BlockType.ULIST:
                list_items = []
                bp_liste = re.findall(r"^(((-\s.*\n)+(-\s.*\n?)?)|(-\s.*\n?))$", block)
                #print(f"bpl: {bp_liste}")
                bp_listeninhalt = bp_liste[0][0]
                bp_liste_li = bp_listeninhalt.split("\n")
                for li in bp_liste_li:
                    #print(f"li2: {li[2:]}")
                    bi_nodes_html = text_to_html_nodes(li[2:])
                    list_items.append(ParentNode("li",bi_nodes_html))



                html_node = ParentNode("ul", list_items)
                #html_node = LeafNode("ul", "ulist not impl")
                html_nodes.append(html_node)
    
            case BlockType.OLIST:
                list_items = []
                bp_liste = re.findall(r"^(([0-9]+\.\s.*\n)+([0-9]+\.\s.*\n?)?|([0-9]+\.\s.*\n?))$", block)
                #print(f"bpl: {bp_liste}")
                bp_listeninhalt = bp_liste[0][0]
                bp_liste_li = bp_listeninhalt.split("\n")
                for li in bp_liste_li:
                    #print(f"li2: {li[2:]}")
                    bi_nodes_html = text_to_html_nodes(li.split(".",1)[1].strip())
                    list_items.append(ParentNode("li",bi_nodes_html))

                html_node = ParentNode("ol", list_items)
                #html_node = LeafNode("span", "olist not implemented yet")
                html_nodes.append(html_node)
    
            case BlockType.PARAGRAPH:
                bi_nodes_html = text_to_html_nodes(block)
                html_node = ParentNode("p", bi_nodes_html)

                #html_node = LeafNode("span", "para not implemented yet")
                html_nodes.append(html_node)

            case _:
                raise Exception(f"Unknown BlockType {block_to_block_type(block).value}")

    return ParentNode("div", html_nodes)


def extract_title(markdown):
 
    return re.findall(r"(# (.*))\n?", markdown)[0][1]





#r"^(-\s.*\n)+(-\s.*\n?)?$", BlockType.ULIST
#(-.*\n?)+
