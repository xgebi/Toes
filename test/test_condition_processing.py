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
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={"test_num1": 5})
		
		result_gt = Toe.process_condition(toe, "3 gt test_num1")
		self.assertEquals(result_gt, False)