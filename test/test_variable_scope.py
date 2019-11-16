import unittest
import xml

from src.toes import Toe, render_toe, Variable_Scope

class VariableScopeTest(unittest.TestCase):

	def setUp(self):
		parent_scope = Variable_Scope({ "var_in_parent": 3 }, None)
		self.child_scope = Variable_Scope({ "var_in_child": 4 }, parent_scope=parent_scope)

		self.standalone_scope = Variable_Scope({ "var_in_standalone": 5 }, None)


	def test_variable_scope(self):
		self.assertNotEqual(self.child_scope, None)
		self.assertNotEqual(self.standalone_scope, None)

	def test_is_variable(self):
		self.assertEqual(self.child_scope.is_variable("var_in_child"), True)
		self.assertEqual(self.child_scope.is_variable("var_in_parent"), True)
		self.assertEqual(self.child_scope.is_variable("pikachu"), False)

	def test_find_variable(self):
		self.assertEqual(self.child_scope.find_variable("var_in_child"), 4)
		self.assertEqual(self.child_scope.find_variable("var_in_parent"), 3)
		self.assertEqual(self.child_scope.find_variable("pikachu"), None)

	def test_is_variable_in_scope(self):
		self.assertEqual(self.standalone_scope.is_variable_in_current_scope("var_in_standalone"), True)
		self.assertEqual(self.standalone_scope.is_variable_in_current_scope("non_existent"), False)
