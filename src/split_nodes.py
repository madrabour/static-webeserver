from textnode import TextNode, TextType
from helper_functions import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    #print(f"anz oldnodes: {len(old_nodes)}")

    if not text_type.value:
        raise Exception("Unknown TextType")

    new_nodes = []
    for on in old_nodes:
        if on.text_type.value != "text":
            new_nodes.append(on)
        else:
            sub_nodes_text = on.text.split(delimiter)
            count_subnodes = len(sub_nodes_text)
            #print(f"sn for {sub_nodes_text} = {count_subnodes}")
            match count_subnodes:
                case 1:
                    new_nodes.append(on)

                case int() if count_subnodes % 2 != 0:
                    for i in range(0,count_subnodes):
                        if sub_nodes_text[i]:
                            if i % 2 == 0:
                                new_node = TextNode(sub_nodes_text[i], TextType.TEXT)
                            else:
                                new_node = TextNode(sub_nodes_text[i], text_type)
                            new_nodes.append(new_node)
                    
                case _:
                    raise Exception("invalid Markdown syntax, closing delimiter is missing")
        
    return new_nodes
    
    
    
    
def split_nodes_image(old_nodes):
    #print(f"anz oldnodes: {len(old_nodes)}")
    new_nodes = []
    for on in old_nodes:
        if on.text_type.value != "text":
            new_nodes.append(on)
        else:
            extract = extract_markdown_images(on.text)
            sub_nodes_text = on.text
            for tup in extract:
                deli = f"![{tup[0]}]({tup[1]})"
                sub_nodes_text_list = sub_nodes_text.split(deli,1)
                if sub_nodes_text_list[0]:
                    nn1 = TextNode(sub_nodes_text_list[0], TextType.TEXT)
                    new_nodes.append(nn1)
                nn2 = TextNode(tup[0], TextType.IMAGE, tup[1])
                new_nodes.append(nn2)
                sub_nodes_text = sub_nodes_text_list[1]
                
            if sub_nodes_text:
                nnl = TextNode(sub_nodes_text, TextType.TEXT)
                new_nodes.append(nnl)

    return new_nodes



def split_nodes_link(old_nodes):
    #print(f"anz oldnodes: {len(old_nodes)}")
    new_nodes = []
    for on in old_nodes:
        if on.text_type.value != "text":
            new_nodes.append(on)
        else:
            extract = extract_markdown_links(on.text)
            sub_nodes_text = on.text
            for tup in extract:
                deli = f"[{tup[0]}]({tup[1]})"
                #print(f"deli_img: {deli}")
                sub_nodes_text_list = sub_nodes_text.split(deli,1)
                if sub_nodes_text_list[0]:
                    nn1 = TextNode(sub_nodes_text_list[0], TextType.TEXT)
                    new_nodes.append(nn1)
                nn2 = TextNode(tup[0], TextType.LINK, tup[1])
                new_nodes.append(nn2)
                sub_nodes_text = sub_nodes_text_list[1]
                
            if sub_nodes_text:
                nnl = TextNode(sub_nodes_text, TextType.TEXT)
                new_nodes.append(nnl)

    return new_nodes




def text_to_textnodes(text):
    complete_node = TextNode(text, TextType.TEXT)
    links_and_images_nodes = split_nodes_link(split_nodes_image([complete_node]))
    cib_nodes = split_nodes_delimiter(
                    split_nodes_delimiter(
                        split_nodes_delimiter(links_and_images_nodes, "**", TextType.BOLD
                    ), "_", TextType.ITALIC
                ), "`", TextType.CODE)
    return cib_nodes



##BootDev Lösung:
'''
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes    
    
'''
