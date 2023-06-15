# coding=utf-8


class TreeNode:

    def __init__(self, name='root', data=None, parent=None, children=None):
        self.name = name
        self.data = data

        if parent:
            assert isinstance(parent, TreeNode)
            parent.add_child(self)
        self.parent = parent

        self.children = []
        if children:
            for child in children:
                self.add_child(child)

    def add_child(self, node):
        """
        Set `node` to the child-node of `self`.
        :param `node`: an TreeNode object.
        :raise `AssertionError`: `node` is not a TreeNode object.
        """

        assert isinstance(node, TreeNode)
        node.parent = self
        self.children.append(node)

    def add_children(self, nodes):
        """
        Set each node in `nodes` to the child-node of `self`.
        :param `nodes`: an iterable object containing nodes.
        :type `nodes`: iterable
        :raise `AssertionError`: there are non-TreeNode elements in `nodes`.
        """

        for node in nodes:
            self.add_child(node)

    def remove(self, node):
        """
        Remove the sub-tree rooted to `node` from the tree rooted to `self`.
        :param `node`: the TreeNode object that you want to remove
        :raise `AssertionError`: `node` is not in the tree rooted to `self`.
        """

        assert self.find(node.name)
        node.parent.children.remove(node)
        node.parent = None

    def move(self, node, new_parent):
        """
        Remove the sub-tree rooted to `node` from the tree rooted to `self`;
        Set `node`'s parent to `new_parent`.
        :param `node`: the TreeNode object that you want to move
        :param `new_parent`: the new parent-node of `node`
        :raise `AssertionError`: `node` is not in the tree rooted to `self`.
        :raise `AssertionError`: `new_parent` is not a TreeNode object.
        """

        assert isinstance(new_parent, TreeNode)
        self.remove(node)
        new_parent.add_child(node)

    def find(self, name):
        """
        Find the node named `name` in the tree rooted to `self`.
        
        Returns
        -------
        target : TreeNode
            the node named `name`.
        None : NoneType
            `None` means that there are no nodes named `name` in the tree rooted to `self`.
        """

        if self.name == name:
            return self
        for node in self.children:
            target = node.find(name)
            if target:
                return target

    def get_siblings(self, node):
        """
        Get siblings of `node`.
        
        :rtype: list
        :raise `AssertionError`: `node` is not in the tree rooted to `self`.
        :raise `AssertionError`: `node` is a root-node of the tree.
        """

        assert self.find(node.name) and node.parent
        return list(filter(lambda x: x is not node, node.parent.children))

    def get_descendants(self, node):
        """
        Get all descendant-nodes of `node`.
        
        :rtype: list
        :raise `AssertionError`: `node` is not in the tree rooted to `self`.
        """

        assert self.find(node.name)

        def operate(node):
            descendants = node.children.copy()

            for child in node.children:
                descendants.extend(operate(child))
            return descendants

        return operate(node)

    def get_tier(self, node):
        """
        Get the tier of `node` in the tree rooted to `self`.
        
        :rtype: int
        :raise `AssertionError`: `node` is not in the tree rooted to `self`.
        """

        assert self.find(node.name)

        def operate(root_node, node):
            if node is root_node:
                return 0
            return operate(root_node, node.parent) + 1

        return operate(self, node)

    def _to_strings(self, xs, _prefix='', _last=True):
        """
        Generate a line string from the node, add it to list *xs*, 
        then recursively operate all children of the node.
        Parameters
        ----------
        xs : list
            A list of strings containing lines of the tree representation
        _prefix : str
            Prefix string of the node line, only used by self recursion
        _last : bool
            Boolean for whether the node is the last child, only used by self recursion
        """
        xs.append(''.join([_prefix, '└── ' if _last else '├── ', self.name]))
        _prefix += '    ' if _last else '│   '
        count = len(self.children)
        for n, node in enumerate(self.children):
            _last = n == (count - 1)
            node._to_strings(xs, _prefix, _last)

    def __repr__(self):
        return self.name

    def __str__(self):
        xs = [self.name]
        if self.children:
            for node in self.children[:-1]:
                node._to_strings(xs, _last=False)
            self.children[-1]._to_strings(xs, _last=True)
        return '\n'.join(xs)


if __name__ == '__main__':
    root = TreeNode()

    # replace following lines with your own testing data
    a = TreeNode(name='A', parent=root)
    a1 = TreeNode(name='A1', parent=a)
    a2 = TreeNode(name='A2', parent=a)
    a21 = TreeNode(name='A21', parent=a2)
    a22 = TreeNode(name='A22', parent=a2)
    b = TreeNode(name='B', parent=root)
    c = TreeNode(name='C', parent=root)
    c1 = TreeNode(name='C1')
    c2 = TreeNode(name='C2')
    c.add_child(c1)
    c.add_child(c2)
    c21 = TreeNode(name='C21', parent=c2)
    c22 = TreeNode(name='C22', parent=c2)

    print(root)
    print()

    # add test cases below for your functions

    # testing of add_children
    b1 = TreeNode(name='B1')
    b2 = TreeNode(name='B2')
    nodes = [b1, b2]
    b.add_children(nodes)
    print(root)
    print()

    # testing of move
    root.move(c, b)
    print(root)
    print()

    # testing of remove
    root.remove(c)
    print(root)
    print()

    # testing of find
    print(root.find('B2'))
    print()

    # testing of get_siblings
    print(root.get_siblings(a))
    print()

    # testing of descendants
    print(root.get_descendants(root))
    print()

    # testing of tier
    print(root.get_tier(a21))
    print()