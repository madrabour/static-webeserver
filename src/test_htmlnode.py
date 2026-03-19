import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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






if __name__ == "__main__":
    unittest.main()