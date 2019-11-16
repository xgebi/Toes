import unittest

from src.toes import Toe, render_toe, Variable_Scope

class ToeTest(unittest.TestCase):

	def test_true_false_values(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={})

		with self.assertRaises(ValueError):
			result = Toe.process_condition(toe, "True")

		with self.assertRaises(ValueError):
			result = Toe.process_condition(toe, "True")

	def test_gt_batch(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 5, "test_num2": 3, "test_num3": 2})
		
		result_gt_1 = Toe.process_condition(toe, "3 gt test_num1")
		self.assertEquals(result_gt_1, False)

		result_gt_2 = Toe.process_condition(toe, "3 gt test_num2")
		self.assertEquals(result_gt_2, False)

		result_gt_3 = Toe.process_condition(toe, "3 gt test_num3")
		self.assertEquals(result_gt_3, True)

	def test_gte_batch(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 5, "test_num2": 3, "test_num3": 2})
		
		result_gte_1 = Toe.process_condition(toe, "3 gte test_num1")
		self.assertEquals(result_gte_1, False)

		result_gte_2 = Toe.process_condition(toe, "3 gte test_num2")
		self.assertEquals(result_gte_2, True)

		result_gte_3 = Toe.process_condition(toe, "3 gte test_num3")
		self.assertEquals(result_gte_3, True)

	def test_lt_batch(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 5, "test_num2": 3, "test_num3": 2})
		
		result_lt_1 = Toe.process_condition(toe, "3 lt test_num1")
		self.assertEquals(result_lt_1, True)

		result_lt_2 = Toe.process_condition(toe, "3 lt test_num2")
		self.assertEquals(result_lt_2, False)

		result_lt_3 = Toe.process_condition(toe, "3 lt test_num3")
		self.assertEquals(result_lt_3, False)

	def test_lte_batch(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 5, "test_num2": 3, "test_num3": 2})
		
		result_lte_1 = Toe.process_condition(toe, "3 lte test_num1")
		self.assertEquals(result_lte_1, True)

		result_lte_2 = Toe.process_condition(toe, "3 lte test_num2")
		self.assertEquals(result_lte_2, True)

		result_lte_3 = Toe.process_condition(toe, "3 lte test_num3")
		self.assertEquals(result_lte_3, False)

	def test_eq_batch(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 3, "test_str": "a"})
		
		result_eq_1 = Toe.process_condition(toe, "3 eq test_num1")
		self.assertEquals(result_eq_1, True)

		result_eq_2 = Toe.process_condition(toe, "3 eq test_str")
		self.assertEquals(result_eq_2, False)

		result_eq_3 = Toe.process_condition(toe, "'a' eq test_str")
		self.assertEquals(result_eq_3, True)

	def test_neq_batch(self):
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 3, "test_str": "a"})
		
		result_neq_1 = Toe.process_condition(toe, "3 neq test_num1")
		self.assertEquals(result_neq_1, False)

		result_neq_2 = Toe.process_condition(toe, "3 neq test_str")
		self.assertEquals(result_neq_2, True)

		result_neq_3 = Toe.process_condition(toe, "'a' neq test_str")
		self.assertEquals(result_neq_3, False)