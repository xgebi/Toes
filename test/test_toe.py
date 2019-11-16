import unittest
import xml

from src.toes import Toe, render_toe, Variable_Scope

class ToeTest(unittest.TestCase):

	def setUp(self):
		self.toe = Toe(path_to_templates="test/resources", template="empty.toe", data={ "num": 3})
	
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
		doc = xml.dom.minidom.Document()
		decrease = doc.createElement("toe:modify")
		decrease.setAttribute("var", "num")
		decrease.setAttribute("toe:dec", None)
		self.toe.process_modify_tag(decrease)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 2)
	
	def test_toe_modify_tag_incrementation(self):
		doc = xml.dom.minidom.Document()
		increase = doc.createElement("toe:modify")
		increase.setAttribute("var", "num")
		increase.setAttribute("toe:inc", None)
		self.toe.process_modify_tag(increase)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 4)

	def test_toe_modify_tag_addition(self):
		doc = xml.dom.minidom.Document()
		addition = doc.createElement("toe:modify")
		addition.setAttribute("var", "num")
		addition.setAttribute("toe:add", 2)
		self.toe.process_modify_tag(addition)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 5)

	def test_toe_modify_tag_subtraction(self):
		doc = xml.dom.minidom.Document()
		subtraction = doc.createElement("toe:modify")
		subtraction.setAttribute("var", "num")
		subtraction.setAttribute("toe:sub", 5)
		self.toe.process_modify_tag(subtraction)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, -2)

	def test_toe_modify_tag_multiplication(self):
		doc = xml.dom.minidom.Document()
		multiplication = doc.createElement("toe:modify")
		multiplication.setAttribute("var", "num")
		multiplication.setAttribute("toe:mul", 2)
		self.toe.process_modify_tag(multiplication)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 6)

	def test_toe_modify_tag_division(self):
		doc = xml.dom.minidom.Document()
		division = doc.createElement("toe:modify")
		division.setAttribute("var", "num")
		division.setAttribute("toe:div", 2)
		self.toe.process_modify_tag(division)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 1.5)

	def test_toe_modify_tag_power(self):
		doc = xml.dom.minidom.Document()
		power = doc.createElement("toe:modify")
		power.setAttribute("var", "num")
		power.setAttribute("toe:pow", 3)
		self.toe.process_modify_tag(power)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 27)

	def test_toe_modify_tag_module(self):
		doc = xml.dom.minidom.Document()
		module = doc.createElement("toe:modify")
		module.setAttribute("var", "num")
		module.setAttribute("toe:mod", 2)
		self.toe.process_modify_tag(module)
		assigned = self.toe.current_scope.find_variable("num")
		self.assertEqual(assigned, 1)

	def test_toe_if_attr(self):
		doc = xml.dom.minidom.Document()
		div = doc.createElement('div')
		div.setAttribute("class", "visible")
		div.setAttribute("toe:if", "num gte 3")

		result = self.toe.process_if_attribute(self.toe.new_tree.childNodes[1], div)
		self.assertEqual(result.nodeType, xml.dom.minidom.Node.ELEMENT_NODE)
		self.assertEqual(result.getAttribute("class"), "visible")

		div2 = doc.createElement('div')
		div2.setAttribute("class", "invisible")
		div2.setAttribute("toe:if", "num gt 3")
		result = self.toe.process_if_attribute(self.toe.new_tree.childNodes[1], div2)
		self.assertEqual(result, None)

	def test_toe_for_attr(self):
		doc = xml.dom.minidom.Document()

	def test_toe_while_attr(self):
		doc = xml.dom.minidom.Document()

if __name__ == '__main__':
	unittest.main()