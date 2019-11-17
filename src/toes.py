from xml.dom import minidom
from xml.dom.minidom import Node
import xml

from pathlib import Path
import os
from collections.abc import Iterable
import re


def render_toe(*args, template, path_to_templates, data=None, **kwargs):
	if path_to_templates is None:
		return None

	toe_engine = Toe(path_to_templates, template, data=data,**kwargs)
	return toe_engine.process_tree()

class Toe:
	tree = {}
	new_tree = {}
	path_to_templates = ""
	template_load_error = False
	variables = None
	current_scope = None

	def __init__(self, path_to_templates, template, data=None, **kwargs):
		self.path_to_templates = path_to_templates
		self.variables = Variable_Scope(data, None)
		self.current_scope = self.variables

		impl = minidom.getDOMImplementation()
		doctype = impl.createDocumentType('html', None, None) 
		self.new_tree = impl.createDocument(xml.dom.XHTML_NAMESPACE, 'html', doctype)

		for node in self.new_tree.childNodes:
			if node.nodeType == Node.ELEMENT_NODE:
				lang = self.current_scope.find_variable('lang')
				node.setAttribute('lang', lang if lang is not None else 'en')

		template_file = ""
		if template.endswith(".toe"):
			with open(os.path.join(path_to_templates, template)) as f:			
					template_file = str(f.read())
		else:
			self.template_load_error = True
			return

		self.tree = minidom.parseString(template_file)
		self.remove_blanks(self.tree)
		self.tree.normalize()
	
	def process_tree(self):
		# There can only be one root element
		if len(self.tree.childNodes) != 1:
			return None

		for node in self.tree.childNodes[0].childNodes:
			res = self.process_subtree(self.new_tree.childNodes[1], node)

			if res is not None:				
				self.new_tree.childNodes[1].appendChild(res)

		return self.new_tree.toxml()[self.new_tree.toxml().find('?>') + 2:]
	
	def process_subtree(self, new_tree_parent, tree):
		"""
		Params:
			new_tree_parent: Document or Node object
			tree: Document or Node object
		Returns
			Document or Node object
		"""
		if tree.nodeType == Node.TEXT_NODE:
			return self.new_tree.createTextNode(tree.wholeText)
			

		# check for toe tags
		if (tree.tagName.startswith('toe:')):
			return self.process_toe_tag(new_tree_parent, tree)

		# check for toe attributes
		attributes = dict(tree.attributes).keys()
		for attribute in attributes:
			if attribute == 'toe:if':
				return self.process_if_attribute(new_tree_parent, tree)				
			if attribute == 'toe:for':
				return self.process_for_attribute(new_tree_parent, tree)	
			if attribute == 'toe:while':
				return self.process_while_attribute(new_tree_parent, tree)		
			

		# append regular element to parent element
		new_tree_node = self.new_tree.createElement(tree.tagName)
		if tree.attributes is not None or len(tree.attributes) > 0:
			for key in tree.attributes.keys():
				if key == 'toe:value':
					self.process_toe_value_attribute(tree, new_tree_node)
				elif key == 'toe:attr':
					self.process_toe_attr_attribute(tree, new_tree_node, key)
				elif key == 'toe:content':
					self.process_toe_content_attribute(tree, new_tree_node)				
				else:
					new_tree_node.setAttribute(key, tree.getAttribute(key))

		for node in tree.childNodes:			
			res = self.process_subtree(new_tree_node, node)

			if type(res) is list:
				for temp_node in res:
					new_tree_node.appendChild(temp_node)	
			if res is not None:
				new_tree_node.appendChild(res)

		return new_tree_node

	def process_toe_tag(self, parent_element, element):
		if len(element.getAttribute('toe:if')) > 0:
			if not self.process_condition(element.getAttribute('toe:if'))["value"]:
				return None

		if element.tagName.find('import') > -1:
			return self.process_toe_import_tag(parent_element, element)

		if element.tagName.find('assign') > -1:
			return self.process_assign_tag(element)

		if element.tagName.find('create') > -1:
			return self.process_create_tag(element)

		if element.tagName.find('modify') > -1:
			return self.process_modify_tag(element)

	def process_toe_import_tag(self, parent_element, element):
		file_name = element.getAttribute('file')

		imported_tree = {}

		if file_name.endswith(".toe") or file_name.endswith(".toe"):
			with open(os.path.join(self.path_to_templates, file_name)) as f:			
					imported_tree = minidom.parseString(str(f.read()))
		if type(imported_tree) is xml.dom.minidom.Document:
			self.remove_blanks(imported_tree)
			imported_tree.normalize()
		
			top_node = self.new_tree.createElement(imported_tree.childNodes[0].childNodes[0].tagName)
			for child_node in imported_tree.childNodes[0].childNodes[0].childNodes:				
				new_node = self.process_subtree(top_node, child_node)
				top_node.appendChild(new_node)
			return top_node
		return None


	# toe:value="value"
	def process_toe_value_attribute(self, tree, new_node):
		value = tree.getAttribute("toe:value")	

		if type(value) == str and value[0] == "'":
			new_node.setAttribute("value", value[1: len(value) - 1])
		else:
			try:
				value_int = int(value)
				value_float = float(value)
				
				if value_int == value_float:
					new_node.setAttribute("value", value_int)
				else:
					new_node.setAttribute("value", value_float)
			except ValueError:
				resolved_value = self.current_scope.find_variable(value)
				if  resolved_value is not None:
					new_node.setAttribute("value", resolved_value)
				else:
					raise ValueError('Variable is not defined')

	# toe:attr-[attribute name]="value"
	def process_toe_attr_attribute(self, tree, new_node, key):
		new_key = key[key.find("-") + 1:]
		value = tree.getAttribute(key)

		if type(value) == str and value[0] == "'":
			new_node.setAttribute(new_key, value[1: len(value) - 1])
		else:
			try:
				value_int = int(value)
				value_float = float(value)
				
				if value_int == value_float:
					new_node.setAttribute(new_key, value_int)
				else:
					new_node.setAttribute(new_key, value_float)
			except ValueError:
				resolved_value = self.current_scope.find_variable(value)
				if  resolved_value is not None:
					new_node.setAttribute(new_key, resolved_value)
				else:
					raise ValueError('Variable is not defined')
	
	# toe:content="value"
	def process_toe_content_attribute(self, tree, new_node):
		value = tree.getAttribute("toe:content")	

		if type(value) == str and value[0] == "'":
			new_node.appendChild(self.new_tree.createTextNode(value[1: len(value) - 1]))
		else:
			try:
				value_int = int(value)
				value_float = float(value)
				
				if value_int == value_float:
					new_node.appendChild(self.new_tree.createTextNode(str(value_int)))
				else:
					new_node.appendChild(self.new_tree.createTextNode(str(value_float)))
			except ValueError:
				resolved_value = self.current_scope.find_variable(value)
				if  resolved_value is not None:
					new_node.appendChild(self.new_tree.createTextNode(str(resolved_value)))
				else:
					raise ValueError('Variable is not defined')

	def process_assign_tag(self, element):
		var_name = element.getAttribute('var')
		var_value = element.getAttribute('value')

		if var_name is None or len(var_name) == 0:
			raise ValueError('Variable cannot have no name')

		variable = self.current_scope.find_variable(var_name)
		if variable is None:
			raise ValueError('Variable doesn\'t exist')

		self.current_scope.assign_variable(var_name, var_value)
		return None

	def process_create_tag(self, element):
		var_name = element.getAttribute('var')
		var_value = element.getAttribute('value')

		if var_name is None or len(var_name) == 0:
			raise ValueError('Variable cannot have no name')

		if self.current_scope.is_variable_in_current_scope(var_name):
			raise ValueError('Variable cannot be created twice')

		self.current_scope.variables[var_name] = var_value
		return None

	def process_modify_tag(self, element):
		var_name = element.getAttribute('var')
		var_value = element.getAttribute('value')

		if var_name is None or len(var_name) == 0:
			raise ValueError('Variable cannot have no name')

		variable = self.current_scope.find_variable(var_name)
		if variable is None:
			raise ValueError('Variable doesn\'t exist')

		if element.hasAttribute('toe:inc'):
			if type(variable) == int or type(variable) == float:
				self.current_scope.assign_variable(var_name, variable + 1)
				return None
		
		if element.hasAttribute('toe:dec'):
			if type(variable) == int or type(variable) == float:
				self.current_scope.assign_variable(var_name, variable - 1)
				return None

		if element.hasAttribute('toe:add'):
			if (type(variable) == int or type(variable) == float):
				self.current_scope.assign_variable(var_name, variable + float(element.getAttribute('toe:add')))
				return None

		if element.hasAttribute('toe:sub'):
			if (type(variable) == int or type(variable) == float):
				self.current_scope.assign_variable(var_name, variable - float(element.getAttribute('toe:sub')))
				return None

		if element.hasAttribute('toe:mul'):
			if (type(variable) == int or type(variable) == float):
				self.current_scope.assign_variable(var_name, variable * float(element.getAttribute('toe:mul')))
				return None

		if element.hasAttribute('toe:div'):
			if (type(variable) == int or type(variable) == float):
				if (float(element.getAttribute('toe:div')) != 0):
					self.current_scope.assign_variable(var_name, variable / float(element.getAttribute('toe:div')))
					return None
				raise ZeroDivisionError()

		if element.hasAttribute('toe:mod'):
			if (type(variable) == int or type(variable) == float):
				if (float(element.getAttribute('toe:mod')) != 0):
					if (float(element.getAttribute('toe:mod')) != 0):
						self.current_scope.assign_variable(var_name, variable % float(element.getAttribute('toe:mod')))
					return None
				raise ZeroDivisionError()

		if element.hasAttribute('toe:pow'):
			if (type(variable) == int or type(variable) == float):
				self.current_scope.assign_variable(var_name, variable ** float(element.getAttribute('toe:pow')))
				return None

		return None



	def process_if_attribute(self, parent_element, element):
		if not self.process_condition(element.getAttribute('toe:if')):
			return None
		element.removeAttribute('toe:if')
		return self.process_subtree(parent_element, element)

	def process_for_attribute(self, parent_element, element):
		result_nodes = []
		# get toe:for attribute
		iterable_cond = element.getAttribute('toe:for')
		# split string between " in "
		items = iterable_cond.split(" in ")
		# find variable on the right side
		# create python for loop
		iterable_item = self.current_scope.find_variable(items[1])
		if iterable_item is None:
			return None

		element.removeAttribute('toe:for')

		for thing in iterable_item:
		# local scope creation
			local_scope = Variable_Scope({}, self.current_scope)
			self.current_scope = local_scope

			self.current_scope.variables[items[0]] = thing

			# process subtree
			result_node = self.process_subtree(parent_element, element)
			if result_node is not None:
				result_nodes.append(result_node)

			# local scope destruction
			self.current_scope = self.current_scope.parent_scope
			local_scope = None
		return result_nodes

	def process_while_attribute(self, parent_element, element):
		result_nodes = []
		# get toe:for attribute
		iterable_cond = element.getAttribute('toe:while')
		
		contains_condition = False
		for cond in (" gt ", " gte ", " lt ", " lte ", " eq ", " neq "):
			if cond in iterable_cond:
				contains_condition = True
				break
		
		if not contains_condition:
			return None

		element.removeAttribute('toe:while')

		while self.process_condition(iterable_cond):
			# local scope creation
			local_scope = Variable_Scope({}, self.current_scope)
			self.current_scope = local_scope

			# process subtree
			result_node = self.process_subtree(parent_element, element)
			if result_node is not None:
				result_nodes.append(result_node)

			# local scope destruction
			self.current_scope = self.current_scope.parent_scope
			local_scope = None

		return result_nodes

	def process_condition(self, condition):		
		if type(condition) == str:
			condition = {
				"value": str(condition),
				"processed": False
			}

		if condition["value"][0] == "(" and condition["value"][-1] == ")":
			condition["value"] = condition["value"][1: len(condition["value"]) - 1].strip()

		condition["value"] = condition["value"].strip()
		if condition["value"].find(" ") == -1:
			if condition["value"].lower() == "true" or condition["value"].lower() == "false":
				raise ValueError('Condition not allowed')
			return self.current_scope.find_variable(condition["value"])



		if (condition["value"].count("and") > 0 or condition["value"].count("or") > 0):
			raise ValueError('Complicated expressions aren\'t implemented yet')

		# split condition["value"] by " xxx? "
		sides = re.split(" [a-z][a-z][a-z]? ", condition["value"])
		# at least one side has to be a variable
		if len(sides) != 2:
			raise ValueError('Unsupported expression')

		if not self.current_scope.is_variable(sides[0]) and not self.current_scope.is_variable(sides[1]):
			raise ValueError('At least one side has to be a variable')

		#resolve variable
		resolved = []
		for idx in range(len(sides)):
			if sides[idx][0] == "'":
				resolved.append(sides[idx][1: len(sides[idx]) - 1])
			else:
				try:
					resolved.append(float(sides[idx]))
				except ValueError:
					resolved_var = self.current_scope.find_variable(sides[idx])
					if  resolved_var is not None:
						resolved.append(resolved_var)
					else:
						raise ValueError('Variable is not defined')


		if " gte " in condition["value"]:
			return resolved[0] >= resolved[1]
		if " gt "  in condition["value"]:
			return resolved[0] > resolved[1]
		if " lte "  in condition["value"]:
			return resolved[0] <= resolved[1]
		if " lt "  in condition["value"]:
			return resolved[0] < resolved[1]
		if " neq "  in condition["value"]:
			return resolved[0] != resolved[1]
		if " eq "  in condition["value"]:
			return resolved[0] == resolved[1]
		return False

	# Adapted from https://stackoverflow.com/a/16919069/6588356
	def remove_blanks(self, node):
		for x in node.childNodes:
			if x.nodeType == Node.TEXT_NODE:
				if x.nodeValue:
					x.nodeValue = x.nodeValue.strip()
			elif x.nodeType == Node.ELEMENT_NODE:
				self.remove_blanks(x)

class Variable_Scope:
	variables = {}
	parent_scope = None

	def __init__(self, variable_dict, parent_scope = None):
		self.variables = variable_dict if variable_dict is not None else {}
		self.parent_scope = parent_scope

	def find_variable(self, variable_name):
		if self.variables.get(variable_name) is not None:
			return self.variables[variable_name]
		
		if self.parent_scope is not None:
			return self.parent_scope.find_variable(variable_name)
		return None

	def assign_variable(self, name, value):
		if self.is_variable_in_current_scope(name):
			self.variables[name] = value
		else:
			self.parent_scope.assign_variable(name, value)

	def create_variable(self, name, value):
		if self.is_variable_in_current_scope(name):
			raise ValueError("Variable already exists")
		self.variables[name] = value

	def is_variable(self, variable_name):
		if self.variables.get(variable_name) is not None:
			return True
		if self.parent_scope is None:
			return False
		if self.parent_scope.is_variable(variable_name):
			return True
		return False

	def is_variable_in_current_scope(self, variable_name):
		return self.variables.get(variable_name) is not None
	