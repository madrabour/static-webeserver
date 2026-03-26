from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os
from shutil import copy, rmtree
from blocks import markdown_to_html_node, extract_title
import sys

"""

    os.path.exists
    os.listdir
    os.path.join
    os.path.isfile
    os.mkdir
    shutil.copy
    shutil.rmtree

"""

def copy_dir(source, target):
    if not os.path.exists(source):
        raise Exception("source-path does not exists")
    if os.path.exists(target):
        print(f"deleting old target-path")
        rmtree(target)
    print(f"creating empty target-path")
    os.mkdir(target)

    
    print(f"copying files")
    dir_content = os.listdir(source)
    #print(f"dc: {dir_content}")
    for pi in dir_content:
        if os.path.isdir(f"{source}/{pi}"):
            print(f"copying dir {source}/{pi} to {target}/{pi}")
            copy_dir(f"{source}/{pi}", f"{target}/{pi}")
    for pi in dir_content:
        if os.path.isfile(f"{source}/{pi}"):
            print(f"copying file {source}/{pi} to {target}/{pi}")
            copy(f"{source}/{pi}", f"{target}/{pi}")
            


def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} for basepath {basepath}")
    source_file = open(from_path)
    md = source_file.read(100000)
    template_file = open(template_path)
    templ = template_file.read(100000)
    #print(f"md: {md}")
    html_node = markdown_to_html_node(md)
    #print(f"html_node: {html_node}")
    html = html_node.to_html()
    #print(f"html: {html}")
    title = extract_title(md)
    
    replacers = [
                    ("{{ Title }}",title),
                    ("{{ Content }}",html),
                    ("href=\"/", f"href=\"{basepath}/"),
                    ("src=\"/", f"src=\"{basepath}/"),
                ]
    html_output = templ
    for replacer in replacers:
        #print (f"0: {replacer[0]}, 1: {replacer[1]}")
        html_output = html_output.replace(replacer[0], replacer[1])
    #print (f"ho: {html_output}")
    dir_dest = os.path.dirname(dest_path)
    if not os.path.exists(dir_dest):
        os.makedirs(dir_dest)
    target_file = open(dest_path, "w")
    target_file.write(html_output)   

def generate_pages_recursive(basepath, source = "./content"):
    #for_generator_soll = ["index", "blog/glorfindel/index", "blog/tom/index", "blog/majesty/index", "contact/index"]
    dir_content = os.listdir(source)
    for pi in dir_content:
        pi_path = f"{source}/{pi}"
        is_md = pi_path[-3:] == ".md"
        if os.path.isdir(pi_path):
            generate_pages_recursive(basepath, pi_path)
        elif os.path.isfile(f"{source}/{pi}") and is_md:
            inner_path = pi_path.replace("./content/", "").replace(".md","")
            gi_s = "./content/" + inner_path + ".md"
            gi_t = "./docs/" + inner_path + ".html"
            generate_page(basepath, gi_s, "./template.html", gi_t)
    


def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        print ("No basepath submitted, taking '/' ")
        basepath = "/"
    
    copy_dir("./static", "./docs")
    generate_pages_recursive(basepath)
    

main()