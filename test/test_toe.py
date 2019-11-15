import unittest
import xml

from src.toes import Toe, render_toe, Variable_Scope

class ToeTest(unittest.TestCase):
	
	def test_toe_constructor(self):		
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={})
		self.assertNotEqual(toe.new_tree, None)
		self.assertEqual(type(toe.new_tree), xml.dom.minidom.Document)

	def test_subtree(self):
		pass

	def test_toe_import_tag(self):
		pass

	def test_toe_assign_tag(self):
		pass

	def test_toe_create_tag(self):
		pass

	def test_toe_modify_tag(self):
		pass

	def test_process_condition(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 5})

		with self.assertRaises(ValueError):
			result = Toe.process_condition(toe, "True")

		# There will need to be done more work on processing coditions
		result_gt = Toe.process_condition(toe, "3 gt test_num1")
		self.assertEquals(result_gt, False)

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