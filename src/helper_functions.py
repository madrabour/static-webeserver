import re

def extract_markdown_images(text):
    img_filter = r"\!\[(.*?)\]\((.*?)\)"
    return re.findall(img_filter, text)
    
def extract_markdown_links(text):
    link_filter = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(link_filter, text)


