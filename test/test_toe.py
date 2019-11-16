import unittest
import xml

from src.toes import Toe, render_toe, Variable_Scope

class ToeTest(unittest.TestCase):

	def setUp(self):
		self.toe = Toe(path_to_templates="test/resources", template="empty.html", data={})
	
	def test_toe_constructor(self):				
		self.assertNotEqual(self.toe.new_tree, None)
		self.assertEqual(type(self.toe.new_tree), xml.dom.minidom.Document)

	# to be removed?
	def test_subtree(self):
		pass

	def test_toe_import_tag(self):
		# <toe:import file="header.html" />
		doc = xml.dom.minidom.Document()
		import_node = doc.createElement('toe:import')
		import_node.setAttribute("file", "import.toe")

		imported_tree = self.toe.process_toe_import_tag(self.toe.new_tree.childNodes[1], import_node)
		self.assertEqual(imported_tree.tagName, "div")
		self.assertEqual(len(imported_tree.childNodes), 1)
		self.assertEqual(imported_tree.childNodes[0].nodeType, xml.dom.Node.TEXT_NODE)



	def test_toe_assign_tag(self):
		pass

	def test_toe_create_tag(self):
		pass

	def test_toe_modify_tag(self):
		pass

	def test_toe_if_attr(self):
		pass

	def test_toe_for_attr(self):
		pass

	def test_toe_while_attr(self):
		pass

	def test_variable_scope(self):
		pass

	def test_find_in_scope(self):
		pass

	def test_find_in_current_scope(self):
		pass

	def test_is_variable_in_scope(self):
		pass

if __name__ == '__main__':
	unittest.main()