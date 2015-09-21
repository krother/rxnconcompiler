#!/usr/bin/env python

"""
-------------------------
Module complex_builder.py
-------------------------
Algorithms for building complexes:
- positive complexes from a booliean contingency
- negative complexes from a positive complex and a root molecule 
- required complexes from a group of positive complexes and a root molecule

Positive complexes - one or more BiologicalComplex
    created from a boolean contingency kept by AlternativeComplexes.
    AND - one complex, OR - more complexes.
    Main contingency type (!, x, K+, K-) does not matter here.
    All compexes in this group can fulfill their biological function.

Root molecule - Molecule that conects the complex to the reaction.
    e.g. for a reaction: A_ppi_B and a complex: X-Y-A-Z it is A.

Negative complexes - one or more BiologicalComplex
    that doesn't have some Moleules (one or more) missing
    in comparison to a single positive complex so it cannot 
    fulfill its biological function.
    To create negative complexes a root molecule is neccesary.
    It allows to built a tree of Molecules so they can be sistematically cat out.
    OR - one complex, AND - more complexes.  
    Main contingency type (!, x, K+, K-) does not matter here.

Required complexes - one or more complexes created based on 
    positive and negative complexes and main contingency type
    (of the boolean contingency) - !, x, K+, K-.
    First required complex will be just positive complex.
    Second will be a sum (complex_addition) 
    of second positive and negative from first.


--------------------------------------------------------------
How contingencies with Input states inside boolean are treated?
--------------------------------------------------------------
- input_conditions parameter is set to a Contingency for liable complexes.
- it is done at the end of the process.
(- later in the flow when applying complexes on reaction it will change reaction rate.) 
"""

from biological_complex import BiologicalComplex, \
        AlternativeComplexes
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.util.util import product
from rxnconcompiler.molecule.state import get_state
import itertools
import copy

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

#def format_id(id):
#    """
#    formating the identifier
#    """
#   return id.strip().replace(" ", "")

class Node:
    """

    """
    def __init__(self, name, id, new_lvl=True):
        self.id = id
        self.name = name
        self.new_lvl = new_lvl
        self.__children = []
        self.parent = None
        self.__cont = []

    def __repr__(self):
        return self.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def cont(self):
        return self.__cont

    @property
    def children(self):
        return self.__children

    def update_children(self, id, mode=_ADD):
        if mode == _ADD:
            self.children.append(id)
        if mode == _DELETE:
            self.children.remove(id)
        if mode == _INSERT:
            self.children = [id]


class Tree(object):
    def __init__(self):
        self.nodes = []

    def get_highest_id(self):
        max_id = 0
        for node in self.nodes:
            if node.id > max_id:
                max_id = node.id
        return max_id

    def add_Node(self, name, id=None, parent=None, parent_id=None):
        """
        add a node in a tree
        """
        #if not self.contains(identifier):
        if id == None:
            id = self.get_highest_id()
            id += 1
        node = Node(name=name, id = id)
        self.nodes.append(node)
        parent_node = self.__update_children(parent, node.id, _ADD, parent_id)
        if parent is None:
            node.parent = (None, None)
        else:
            #parent = self.get_node(id=parent_id)
            node.parent = (parent_node.name, parent_node.id)

        return node

    def set_parent(self, node, children, levelup=False):
        """
        change the parent of one or more children
        """
        for children_id in children:
            child_node = self.get_node(id=children_id)
            new_child = copy.copy(child_node)
            children_of_new_child = self.get_children(new_child.id)

            # we have to instances to manipulate
            # 1) the list of nodes in the tree
            # 2) the treeTracker information
            # To update the nodes list we have to remove the node change the information and put it back
            # to update the treeTracker we have also to remove the old entry and replace it with the new one to make sure that everything is in correct position

            old_node_idx =  self.nodes.index(child_node)
            old_node = self.nodes.pop(old_node_idx)  # remove the node by its index from nodes list
            self.__update_children(child_node.parent, child_node.id, _DELETE)  # remove the respective entry in treeTracker

            if levelup:
                old_node.parent = node.parent  # change the parent of the old node
            else:
                old_node.parent = node.id  # change the parent of the old node
            self.nodes.append(old_node)  # put the node back in the nodes list
            self.__update_children(old_node.parent, old_node.id, _ADD)  # add the node again in the treeTracker

    def remove_Node(self, id):
        """
        remove a node from the tree
        """
        if self.contains(id):
            node = self.get_node(id=id)
            children = self.get_children(node.id)
            self.set_parent(node, children, levelup=True)
            self.__update_children(node.parent, node.id, _DELETE)
            self.nodes.remove(node)
        else:
            raise("Node {0} not known!".format(id))
            #print "Node {0} not known!".format(id)

    def expand_tree(self, position, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        node = self.get_node(id=position)
        yield node
        queue = node.children
        while queue:
            node = self.get_node(id=queue[0])
            yield node
            expansion = node.children
            if mode is _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode is _WIDTH:
                queue = queue[1:] + expansion  # width-first

    def is_branch(self, position):
        return self[position].children

    def __update_children(self, parent, id, mode, parent_id=None):
        if parent is None:
            return
        else:
            if parent_id == None:
                self[parent].update_children(id, mode)
                return self[parent]
            else:
                parent = self.get_node(id=parent_id)
                parent.update_children(id, mode)
                return parent

    def get_index(self, name):
        """
        get the index of identifier
        """
        for i, node in enumerate(self.nodes):
            if node.name == name:
                return i


    def show(self, position, level=_ROOT):
        """
        basic visualisation of the tree for testing and developing
        """
        if self.contains(position):
            node = self.get_node(id=position)
            queue = node.children
            print("\t" * level, "{0} [{1}] parent: {2}".format(node.name, node.id, node.parent))
            if node.new_lvl:
                level += 1
                for element in queue:
                    self.show(element, level)  # recursive call
        else:
            raise NameError("Node {0} does not exists!".format(position))

    def get_leaf(self, position):
        """
        get the leafes of a node
        gets identifier type str
        return list of identifier type str
        """
        #leafes = [node for node in self.expand_tree(position) if self.get_children(node) == []]
        leafes = []
        leafes = [node for node in self.expand_tree(position) if self.get_children(node.name) == []]
        return leafes

    def get_root_nodes(self):
        root_nodes = [node for node in self.nodes if node.parent == (None, None)]
        return root_nodes

    def get_parent(self, id):
        """
        get the parent of a specific node
        """
        for node in self.nodes:
            if node.id == id:
                return node.parent

    def get_children(self, name):
        """
        get all children of a specific node
        """
        children = [node for node in self.nodes if node.parent == name]
        return children

    def get_node(self, id=None, name=None, parent_id=None):
        for node in self.nodes:
            if id != None and node.id == id:
                return node
            elif (name != None and parent_id != None) and (node.name == name and node.parent[1] == parent_id):
                return node
            elif name != None and parent_id == None and node.name == name: # we have a root node
                return node

    def __getitem__(self, name):
        return self.nodes[self.get_index(name)]

    def contains(self, id):
        """
        test if a node already exists
        """
        for node in self.nodes:
            if node.id == id:
                return True

    def list_of_node_names(self):
        names = [node.name for node in self.nodes]
        return names

    def children_by_name(self, node):
        result = []
        for child_id in node.children:
            child_node = self.get_node(child_id)
            result.append(child_node.name)
        return result

    def get_all_cont(self):
        result = []
        for node in self.nodes:
            result.extend(node.cont)
        return result

class ComplexBuilder:
    """

    """
    def __init__(self):
        self.states = []
        self.final_states = []

    def flatten_bool(self, bool_cont):
        """
        Builds a flatten list from boolean (containing children) contingency <cont>.
        It can be normal boolean or defined complex
        (which is in fact AND boolean).

        Returns a list of lists of contingencies.

        @param bool_cont:  ContingencyFactory obj
        @return final_states: list of contingencies
        @type final_states: list
        """

        self.get_state_sets(bool_cont) # we want only the list
        return self.final_states

    def check_for_structured_complex(self, complexes):
        """
        This function checks if a complex is already structured.
        @return: structured complex
        """
        for complex_tuple in complexes:
            for complex in complex_tuple[1]:
                for cont in complex:
                    if "--" in cont.ctype:
                        return complex
                    break

        return []

    def structure_complex(self, complexes, reaction_container):
        self.complexes_test = complexes
        possible_roots = reaction_container.get_reactants()
        self.structured_complexes = self.check_for_structured_complex(complexes)

        self.tree = Tree()
        if self.structured_complexes:
            pass
        else:
            #root_id = 0
            for root in possible_roots:
                # check if the other root allready exists in the tree
                #root_id += 1
                self.tree.add_Node(root.name)
                for complex_tuple in complexes:
                    for complex in complex_tuple[1]:
                        self.get_structured_complex(complex, self.tree.get_node(name=root.name))
                        #self.structured_complexes.append(complex)
        self.process_structured_complex()

    def process_structured_complex(self):
        for root in self.tree.get_root_nodes():
            if root.children:
                self.update_tree_contingencies(root.id)


    def update_tree_contingencies(self, node_id):
        if self.tree.contains(node_id):
            node = self.tree.get_node(id=node_id)
            queue = node.children
            if node.new_lvl:

                for i, child_id in enumerate(queue):
                    child_node = self.tree.get_node(child_id)
                    root_cont = node.cont[i]
                    if root_cont.state.components[0].name == node.name:
                        sid = "{0}--{1}".format(node.id ,child_node.id)
                    else:
                        sid = "{0}--{1}".format(child_node.id, node.id)
                    state = get_state(root_cont.state.state_str, sid)
                    # if we have a boolean AND/OR we can change the ctype into --
                    # else we should keep the contingency and just change the cid (complex id)
                    if root_cont.ctype in ["and", "or"]:
                        root_cont.ctype = sid
                    root_cont.state = state
                    self.update_tree_contingencies(child_id)  # recursive call
        else:
            raise NameError("NodeID {0} does not exists!".format(node_id))

    def get_structured_complex(self, inner_list, root):
        """

        """
        stack = [root]

        while stack:
            stack = self._get_complex_layer(inner_list, stack)

    def _get_complex_layer(self, inner_list, root_list):
        """
        Helper function for get_ordered_tree.

        save the path of a certain component
        use the mol structure for saving the id and the path
        """
        already = self.tree.get_all_cont()
        new_roots = []
        for root in root_list:
            root_cont = []
            root_node = self.tree.get_node(id=root.id)
            for cont in inner_list:
                if cont.state.has_component(root):
                    root_cont.append(cont)
            for bond in root_cont:
                if bond not in already:  # to avoid double contingency recognistion A--B, root: A next root B
                    if bond.state.type == "Association":
                        new_root = bond.state.get_partner(bond.state.get_component(root.name))
                        if not new_root.name in self.tree.children_by_name(root): # check if the node already exists
                            self.tree.add_Node(new_root.name, parent=root.name, parent_id=root.id)
                        else:
                            child = self.tree.get_node(name=new_root.name, parent_id=root.id)
                            root.update_children(child.id, _ADD)
                        root_node.cont.append(bond)
                        new_roots.append(self.tree.get_node(name=new_root.name, parent_id=root.id))
                    else:
                        new_roots = new_roots
        return new_roots

    def get_state_sets(self, bool_cont):
        """
        Traverses through a contingencies list.
        Starts with root contingency that keeps all other contingencies.
        Uses get_states to go one level deeper until there are no more
        contingencies with children. 
        At the end the self.final_states list contain lists with states.
        Each list corresponding to a complex.
        """
        self.states.append([bool_cont])
        while self.states:  # [AND A--C, AND <NOT>]
            state_list = self.states.pop()  # [AND A--C, AND <NOT>]
            self.get_states(state_list)

    def check_bool_type(self, children):
        """
        It is not allowed to mix bool types hence if one child has a specific bool the other children should have the same
        This function is written to test this
        @param children: children of a specific boolean
        @return: True if everything is fine
        @return: False if booleans are mixed


        """
        # TODO: if not implemented bool raise error/warning add it to warnings don't raise and break the program
        reference_child_ctype = children[0].ctype
        for child in children[1:]:
            if not "--" in reference_child_ctype and reference_child_ctype != child.ctype:
                raise Exception('Boolean not properly defined mix of {0} and {1}'.format(reference_child_ctype, child.ctype))
        return True

    def get_states(self, node_list):
        """
        Moves contingencies from a given list to
        either self.states (booleans - children) 
        or to self.final_states (leafs - no children)
        """
        to_remove = []
        to_add = []
        to_clone = []
        
        for node in node_list: # [AND <NOT>]
            if node.has_children: # [NOT A--E]
                if len(node.children) > 1:
                    self.check_bool_type(node.children)
                to_remove.append(node)
                child = node.children[0]

                if child.ctype == 'and' or '--' in child.ctype:
                    to_add.extend(node.children)
                elif child.ctype == 'or':
                    if node.ctype!= None and (node.ctype == "and" or '--' in node.ctype):
                        to_clone.append(node.children) # [[AND A--C, AND A--E], [AND A--F, AND A--D]]
                    else:
                        to_clone.extend(node.children) # [AND A--C, AND A--E , AND A--F, AND A--D]
                elif child.ctype == 'not' and (node.ctype!= None and (node.ctype == "and" or '--' in node.ctype)):
                    for child in node.children:
                        child.ctype = "x"
                        to_add.append(child)
                elif child.ctype == 'not' and node.ctype == "or":
                    for child in node.children:
                        child.ctype = "x"
                        to_clone.append(child)

        for node in to_remove:
            node_list.remove(node)

        if to_add:
            for node in to_add:
                node_list.append(node)  # [<complB>, A--F, A--E] AND A--C -> [AND A--C]
            bool_flag = False
            for node in node_list:
                if node.has_children and len(node.children) > 0:
                    bool_flag = True
            if bool_flag:
                self.states.append(node_list)  # [<complA>, <complB>]
            else:
                self.final_states.append(node_list)

        elif to_clone:

            to_clone_copy = copy.deepcopy(to_clone)
            # remove all lists from to_clone and just keep single ORs
            # lists are saved in another object for later combination
            to_combine = [to_clone.pop(to_clone.index(ele)) for ele in reversed(to_clone_copy) if isinstance(ele,list)]

            # get combinations of this boolean OR level if the previous lvl was an AND
            to_combine = list(itertools.product(*to_combine))  # this returns at least an empty tuple
            if to_combine[0]:
                to_clone += to_combine

            for node in to_clone:
                if isinstance(node, tuple):
                    result = node_list + list(node) # [] + [OR A--C] -> [[OR A--C]] # [AND A--D] + [OR A--C] -> [AND A--D, OR A--C]
                else:
                    result = node_list + [node]
                bool_flag = False
                for node in result:
                    if node.has_children and len(node.children) > 0:
                        bool_flag = True
                if bool_flag:
                    self.states.append(result)
                else:
                    self.final_states.append(result)


if __name__ == "__main__":
    tree = Tree()
    tree.add_Node("A", id=3)
    tree.add_Node("B", id=4 , parent="A")
    tree.add_Node("B", parent="B", parent_id=4)
    tree.add_Node("D", parent="B")
    tree.add_Node("C", parent="B", parent_id=5)
    #leafs = tree.get_leaf(3)
    tree.show(3)