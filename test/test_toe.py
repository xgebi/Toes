import unittest
import xml

from src.toes import Toe, render_toe

class ToeTest(unittest.TestCase):
	
	def test_toe_constructor(self):		
		toe = Toe(path_to_templates="test/resources", template="empty.html", data={})
		self.assertNotEqual(toe.new_tree, None)
		self.assertEqual(type(toe.new_tree), xml.dom.minidom.Document)

		#render_toe(template="test.html", path_to_templates=os.path.join(os.getcwd(), 'src', 'cms', 'app', 'templates'), title="Ahoy", description="I've got this", enabled=True, lang="cs", way_out=[1,2,3])

#if __name__ == '__main__':
	#unittest.main()