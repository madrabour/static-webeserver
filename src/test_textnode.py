import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_nr2(self):
        node = TextNode("bootdev thinks they're better than everyone else for using Linux.", TextType.BOLD)
        node2 = TextNode("bootdev thinks they're better than everyone else for using Linux.", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_nr3(self):
        node = TextNode("bootdev thinks they're better than everyone else for using Linux.", TextType.BOLD)
        node2 = TextNode("bootdev thinks they're better than everyone else for using Linux.", TextType.ITALIC)
        node_vergleich = node == node2
        self.assertFalse(node_vergleich)

    def test_nr4(self):
        node = TextNode("bootdev thinks they're better than everyone else for using Linux.", TextType.LINK)
        node2 = TextNode("bootdev thinks they're better than everyone else for using Linux.", TextType.LINK, "http://www.www.ww")
        self.assertNotEqual(node, node2)


    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    #own tests
    def test_img(self):
        node = TextNode("Madrabours Eck Logo", TextType.IMAGE, "https://andrich-radebeul.de/bilder/logo-me.gif")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://andrich-radebeul.de/bilder/logo-me.gif", "alt":"Madrabours Eck Logo"})
        
    def test_link(self):
        node = TextNode("Madrabours Eck", TextType.LINK, "https://andrich-radebeul.de/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Madrabours Eck")
        self.assertEqual(html_node.props, {"href":"https://andrich-radebeul.de/"})
        self.assertEqual(html_node.to_html(), "<a href=\"https://andrich-radebeul.de/\">Madrabours Eck</a>" )
        
    def test_bold(self):
        node = TextNode("Madrabours Eck", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Madrabours Eck")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<b>Madrabours Eck</b>" )
        
    def test_bold(self):
        node = TextNode("Madrabours Eck", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Madrabours Eck")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<i>Madrabours Eck</i>" )
        
    def test_bold(self):
        node = TextNode("Madrabours Eck", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Madrabours Eck")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<code>Madrabours Eck</code>" )
        
    
    







if __name__ == "__main__":
    unittest.main()