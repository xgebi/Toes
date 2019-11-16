import unittest
import xml

from src.toes import Toe, render_toe, Variable_Scope

class ToeTest(unittest.TestCase):

	def setUp(self):
		self.toe = Toe(path_to_templates="test/resources", template="empty.html", data={ "num": 3})
	
	def test_toe_constructor(self):				
		self.assertNotEqual(self.toe.new_tree, None)
		self.assertEqual(type(self.toe.new_tree), xml.dom.minidom.Document)

	def test_toe_import_tag(self):
		doc = xml.dom.minidom.Document()
		import_node = doc.createElement('toe:import')
		import_node.setAttribute("file", "import.toe")

		imported_tree = self.toe.process_toe_import_tag(self.toe.new_tree.childNodes[1], import_node)
		self.assertEqual(imported_tree.tagName, "div")
		self.assertEqual(len(imported_tree.childNodes), 1)
		self.assertEqual(imported_tree.childNodes[0].nodeType, xml.dom.Node.TEXT_NODE)



	def test_toe_assign_tag(self):
		doc = xml.dom.minidom.Document()
		assign = doc.createElement("toe:assign")
		assign.setAttribute("var", "num")
		assign.setAttribute("value", 4)
		self.toe.process_assign_tag(assign)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 4)
		

	def test_toe_create_tag(self):
		doc = xml.dom.minidom.Document()
		create_fail = doc.createElement("toe:create")
		create_fail.setAttribute("var", "num")
		create_fail.setAttribute("value", 4)
		with self.assertRaises(ValueError):
			self.toe.process_create_tag(create_fail)
		
		doc = xml.dom.minidom.Document()
		create_success = doc.createElement("toe:create")
		create_success.setAttribute("var", "number")
		create_success.setAttribute("value", 4)
		self.toe.process_create_tag(create_success)
		assigned = self.toe.current_scope.find_variable("number")
		self.assertEqual(assigned, 4)

	def test_toe_modify_tag_decrementation(self):
		pass
	
	def test_toe_modify_tag_incrementation(self):
		pass

	def test_toe_modify_tag_addition(self):
		pass

	def test_toe_modify_tag_subtraction(self):
		pass

	def test_toe_modify_tag_multiplication(self):
		pass

	def test_toe_modify_tag_division(self):
		pass

	def test_toe_modify_tag_power(self):
		pass

	def test_toe_modify_tag_module(self):
		pass

	def test_toe_if_attr(self):
		pass

	def test_toe_for_attr(self):
		pass

	def test_toe_while_attr(self):
		pass

if __name__ == '__main__':
	unittest.main()