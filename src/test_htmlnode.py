import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from helper_functions import extract_markdown_images, extract_markdown_links
from blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestHTMLNode(unittest.TestCase):
    
    #own tests
    #HTML
    def test_eq(self):
        node =  HTMLNode("p", "This is a html paragraph node")
        node2 = HTMLNode("p", "This is a html paragraph node")
        self.assertEqual(node, node2)

    def test_nr2(self):
        node = HTMLNode("p", "This is a html paragraph node")
        node2 = HTMLNode("a", "This is a link node", None, {"href":"http://www.www.www"})
        self.assertNotEqual(node, node2)

    def test_nr3(self):
        node = HTMLNode("a", "This is a link node", None, {"href":"http://www.www.www"})
        node_repr = "HTMLNode(T: a, v: This is a link node, c: None, p:  href=\"http://www.www.www\")"
        self.assertEqual(
            node_repr, repr(node)
        )

    def test_nr4(self):
        node = HTMLNode("a", "This is a link node", None, {"target":"_blank", "href":"http://www.www.www"})
        node2 = HTMLNode("a", "This is a link node", None, {"href":"http://www.www.www", "target":"_blank"})
        self.assertEqual(node, node2)


    #LEAF
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_nr5(self):
        node = LeafNode("a", "This is a link node", {"target":"_blank", "href":"http://www.www.www"})
        node2 = LeafNode("a", "Another Link", {"href":"http://www.www.vvv"})
        self.assertNotEqual(node, node2)

    def test_nr6(self):
        node = LeafNode("a", "This is a link node", {"href":"http://www.www.www", "target":"_blank"}).to_html()
        node2 = '<a href="http://www.www.www" target="_blank">This is a link node</a>'
        self.assertEqual(node, node2)


   #Parent
   
    def test_nr7(self):
        
        b_red = LeafNode("b", "grandchild", {"class":"red"})
        ger_text = LeafNode(None, ": In german a grandchild is called ")
        enkel_link = LeafNode("a", "Enkel", {"href":"https://de.wikipedia.org/wiki/Enkel_(Begriffskl%C3%A4rung)", "title":"wiki Enkel", "target":"_blank"})
        br = LeafNode(None, "<br>")
        
        eft_span = ParentNode("span", [b_red, ger_text, enkel_link, br], {"class":"eft", "style":"text-align:center;"})
        trenner = LeafNode(None, "--------------------<br>")
        sot_span = LeafNode("span", "for more informations look in the link above<br>", {"class":"sot"})
        
        outer_div = ParentNode("div", [eft_span, trenner, sot_span], {"class":"tb1"})
        self.assertEqual(
            outer_div.to_html(),
            "<div class=\"tb1\"><span class=\"eft\" style=\"text-align:center;\"><b class=\"red\">grandchild</b>: In german a grandchild is called <a href=\"https://de.wikipedia.org/wiki/Enkel_(Begriffskl%C3%A4rung)\" title=\"wiki Enkel\" target=\"_blank\">Enkel</a><br></span>--------------------<br><span class=\"sot\">for more informations look in the link above<br></span></div>",
        )

    def test_nr8_splitnodesdel(self):
        text_node_old = [ TextNode("Sometimes we need **bold** words", TextType.TEXT) ]
        new_node_list = [ TextNode("Sometimes we need ", TextType.TEXT),  TextNode("bold", TextType.BOLD),  TextNode(" words", TextType.TEXT) ]
        self.assertEqual(split_nodes_delimiter(text_node_old, "**", TextType.BOLD), new_node_list)
        
    def test_nr9_splitnodesdel2(self):
        text_node_old = [ TextNode("schickes Bild", TextType.IMAGE, "schickes_bild.jpg"), TextNode("Sometimes we need **bold** words", TextType.TEXT), TextNode("and sometimes we need _italic_ words", TextType.TEXT) ]
        new_node_list = [
                            TextNode("schickes Bild", TextType.IMAGE, "schickes_bild.jpg"),
                            TextNode("Sometimes we need ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" words", TextType.TEXT),
                            TextNode("and sometimes we need ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" words", TextType.TEXT)
                        ]
        self.assertEqual(split_nodes_delimiter(split_nodes_delimiter(text_node_old, "**", TextType.BOLD), "_", TextType.ITALIC), new_node_list)
        

    def test_nr10_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [cool Link](https://www.madrabour.de) and another [Link to some page](https://www.zitzschewig.de) for testing."
        )
        self.assertListEqual([("cool Link", "https://www.madrabour.de"), ("Link to some page", "https://www.zitzschewig.de")], matches)

    def test_nr10_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![cool Link](https://www.madrabour.de) and another [Link to some page](https://www.zitzschewig.de) for testing."
        )
        self.assertListEqual([("Link to some page", "https://www.zitzschewig.de")], matches)



    def test_nr11_split_images_and_links(self):
        node = TextNode(
            "[madrabour.de](https://www.madrabour.de) is my own page. This is picture from the site: ![a cat named Lola(!)](http://www.madrabour.de/person/bilder/lola02_titel.jpg) and here is another ![cat named Hercules](http://www.madrabour.de/person/bilder/hercules95ng_01.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link(split_nodes_image([node]))
        self.assertListEqual(
            [
                TextNode("madrabour.de", TextType.LINK, "https://www.madrabour.de"),
                TextNode(" is my own page. This is picture from the site: ", TextType.TEXT),
                TextNode("a cat named Lola(!)", TextType.IMAGE, "http://www.madrabour.de/person/bilder/lola02_titel.jpg"),
                TextNode(" and here is another ", TextType.TEXT),
                TextNode(
                    "cat named Hercules", TextType.IMAGE, "http://www.madrabour.de/person/bilder/hercules95ng_01.jpg"
                ),
            ],
            new_nodes,
        )

    def test_nr12_all_splits(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
       

    def test_nr13_markdown_to_blocks(self):
        md = """
# Überschrif 1

## Überschrift1.1

This is **bolded** paragraph

## Überschrift1.2

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

## Überschrift1.3

- This is a list
- with items

# Überschrif 2

## Überschrift2.1

[madrabour.de](https://www.madrabour.de) is my own page.
This is picture from the site: ![a cat named Lola(!)](http://www.madrabour.de/person/bilder/lola02_titel.jpg)

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Überschrif 1",
                "## Überschrift1.1",
                "This is **bolded** paragraph",
                "## Überschrift1.2",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "## Überschrift1.3",
                "- This is a list\n- with items",
                "# Überschrif 2",
                "## Überschrift2.1",
                "[madrabour.de](https://www.madrabour.de) is my own page.\nThis is picture from the site: ![a cat named Lola(!)](http://www.madrabour.de/person/bilder/lola02_titel.jpg)"
            ],
        )

    def test_nr14_markdown_to_blocktyps(self):
        md = """
# Überschrif 1

## Überschrift1.1

This is **bolded** paragraph

## Überschrift1.2

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

## Überschrift1.3

- This is a list
- with items

# Überschrif 2

## Überschrift2.1

1. [madrabour.de](https://www.madrabour.de) is my own page.
2. This is picture from the site: ![a cat named Lola(!)](http://www.madrabour.de/person/bilder/lola02_titel.jpg)

## Überschrift2.2

```
print("hello world!")
print("hello world!")
print("hello world!")
```

## Überschrift2.3

> Es war einmal...
> Es begab sich einst...
> Dingdong palim palim!

"""
        blocks = markdown_to_blocks(md)
        block_typs = []
        i = 0
        for block in blocks:
            i += 1
            #print(f"\n{i}.: ~{block}~")
            bt = block_to_block_type(block)
            block_typs.append(bt)
            #print(f"btv {bt.value}")
        self.assertEqual(
            block_typs,
            [ 
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.HEADING,
                BlockType.ULIST,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.OLIST,
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.HEADING,                
                BlockType.QUOTE,
            ],
        )

    def test_nr15_markdown_to_html_ueber(self):
        md = """
# Überschrif 1

### Ü3

###### Ü6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Überschrif 1</h1><h3>Ü3</h3><h6>Ü6</h6></div>",
        )
        
    def test_nr16_markdown_to_html_uecoquo(self):
        md = """
# Überschrif 1

```
<xml>Palim</xml>
print("palim")
```

###### Ü6

> Quote Z1
> Quote Z2
> Quote Z3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Überschrif 1</h1><pre><code><xml>Palim</xml>\nprint(\"palim\")\n</code></pre><h6>Ü6</h6><blockquote>Quote Z1<br>Quote Z2<br>Quote Z3<br></blockquote></div>",
        )
        
    def test_nr17_markdown_to_html_ulioli(self):
        md = """
# Überschrif 1

```
<xml>Palim</xml>
print("palim")
```

###### Ü6

- Listenpunkt 1

1. Menüpunkt 1
2. Menüpunkt 2
4. Menüpunkt 3

- Listenpunkt 1
- Pistenlunkt 2
- Punktenlist 3

Hier steht noch ein
abschließender Text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        #print (f"\nhtml:\n{html}")
        self.assertEqual(
            html,
            "<div><h1>Überschrif 1</h1><pre><code><xml>Palim</xml>\nprint(\"palim\")\n</code></pre><h6>Ü6</h6><ul><li>Listenpunkt 1</li></ul><ol><li>Menüpunkt 1</li><li>Menüpunkt 2</li><li>Menüpunkt 3</li></ol><ul><li>Listenpunkt 1</li><li>Pistenlunkt 2</li><li>Punktenlist 3</li></ul><p>Hier steht noch ein abschließender Text</p></div>",
        )
        
    def test_nr18_markdown_to_title(self):
        md = """
# Überschrif für Palim Dingeldong

```
<xml>Palim</xml>
print("palim")
```

###### Ü6

- Listenpunkt 1

1. Menüpunkt 1
2. Menüpunkt 2
4. Menüpunkt 3

- Listenpunkt 1
- Pistenlunkt 2
- Punktenlist 3

Hier steht noch ein
abschließender Text
"""
        title = extract_title(md)
        #print (f"\nhtml:\n{html}")
        self.assertEqual(
            title,
            "Überschrif für Palim Dingeldong",
        )


       


#################################################
    #from bootdev
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(T: p, v: What a strange world, c: None, p:  class=\"primary\")",
        )
        
        #    "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",       
        #    node_repr = "HTMLNode(T: a, v: This is a link node, c: None, p:  href=\"http://www.www.www\")"

        

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )



###

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

###


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://wikipedia.org"),
            ],
            matches,
        )

###


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )



    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )





if __name__ == "__main__":
    unittest.main()