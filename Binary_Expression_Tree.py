
import re
from stack import Stack


class BinaryTree:
    """A linked binary tree with positional navigation."""

    class _Node:
        __slots__ = "_element", "_parent", "_left", "_right"

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position:
        """A position represents a node in the tree."""

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return (
                isinstance(other, type(self))
                and other._node is self._node
            )

    def __init__(self):
        self._root = None
        self._size = 0

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("p must be a valid Position")
        if p._container is not self:
            raise ValueError("Position does not belong to this tree")
        return p._node

    def _make_position(self, node):
        if node is None:
            return None
        return self.Position(self, node)

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)

    def is_leaf(self, p):
        node = self._validate(p)
        return node._left is None and node._right is None

    def add_root(self, element):
        if self._root is not None:
            raise ValueError("Tree already has a root")

        self._root = self._Node(element)
        self._size = 1
        return self._make_position(self._root)

    def attach_subtrees(self, left_tree, right_tree):
        """
        Attach two existing trees beneath this tree's root.

        The trees must be separate, nonempty trees. Their nodes are
        transferred, not copied. The donor trees become empty afterward.
        """

        if left_tree is self or right_tree is self:
            raise ValueError("A tree cannot be attached to itself")

        if left_tree is right_tree:
            raise ValueError("The two subtrees must be different trees")

        if self._root is None:
            raise ValueError("The receiving tree must have a root")

        if self._root._left is not None or self._root._right is not None:
            raise ValueError("Root already has children")

        if left_tree._root is None or right_tree._root is None:
            raise ValueError("Both subtrees must be nonempty")

        # Transfer the roots to the new parent.
        self._root._left = left_tree._root
        self._root._right = right_tree._root

        left_tree._root._parent = self._root
        right_tree._root._parent = self._root

        # Update the size of the receiving tree.
        self._size += left_tree._size + right_tree._size

        # Empty the donor trees so nodes cannot belong to two trees.
        left_tree._root = None
        left_tree._size = 0

        right_tree._root = None
        right_tree._size = 0

    def __len__(self):
        return self._size

    def preorder(self):
        """Visit root, left subtree, right subtree."""

        if self._root is not None:
            yield from self._subtree_preorder(self._make_position(self._root))

    def _subtree_preorder(self, p):
        yield p

        if self.left(p) is not None:
            yield from self._subtree_preorder(self.left(p))

        if self.right(p) is not None:
            yield from self._subtree_preorder(self.right(p))

    def inorder(self):
        """Visit left subtree, root, right subtree."""

        if self._root is not None:
            yield from self._subtree_inorder(self._make_position(self._root))

    def _subtree_inorder(self, p):
        if self.left(p) is not None:
            yield from self._subtree_inorder(self.left(p))

        yield p

        if self.right(p) is not None:
            yield from self._subtree_inorder(self.right(p))

    def postorder(self):
        """Visit left subtree, right subtree, root."""

        if self._root is not None:
            yield from self._subtree_postorder(self._make_position(self._root))

    def _subtree_postorder(self, p):
        if self.left(p) is not None:
            yield from self._subtree_postorder(self.left(p))

        if self.right(p) is not None:
            yield from self._subtree_postorder(self.right(p))

        yield p


class BinaryExpressionTree(BinaryTree):
    """Builds and evaluates a binary expression tree from postfix input."""

    OPERATORS = {"+", "-", "*", "/"}

    def __init__(self, postfix=None):
        super().__init__()

        if postfix is not None:
            self._build_tree(postfix)

    def _is_number(self, token):
        """Check whether a token is a valid integer or decimal."""

        return re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)",
            token
        ) is not None

    def _build_tree(self, postfix):
        """Build the expression tree using a stack of partial trees."""

        if not isinstance(postfix, str) or not postfix.strip():
            raise ValueError("Expression cannot be empty")

        tokens = postfix.split()
        stack = Stack()

        for token in tokens:

            # If the token is a number, create a leaf tree.
            if self._is_number(token):
                new_tree = BinaryExpressionTree()
                new_tree.add_root(token)
                stack.push(new_tree)

            # If the token is an operator, combine two trees.
            elif token in self.OPERATORS:

                if stack.size() < 2:
                    raise ValueError("Too few operands")

                # The first tree popped is the RIGHT subtree.
                right_tree = stack.pop()

                # The second tree popped is the LEFT subtree.
                left_tree = stack.pop()

                new_tree = BinaryExpressionTree()
                new_tree.add_root(token)

                new_tree.attach_subtrees(left_tree, right_tree)

                stack.push(new_tree)

            else:
                raise ValueError("Unsupported token: " + token)

        # Exactly one complete tree must remain.
        if stack.size() != 1:
            raise ValueError("Invalid expression: extra operands")

        final_tree = stack.pop()

        # Transfer the final tree into this expression tree.
        self._root = final_tree._root
        self._size = final_tree._size

        final_tree._root = None
        final_tree._size = 0

    def evaluate(self):
        """Evaluate the expression recursively."""

        if self._root is None:
            raise ValueError("Expression tree is empty")

        return self._evaluate_recur(self.root())

    def _evaluate_recur(self, p):

        # A leaf contains a numeric operand.
        if self.is_leaf(p):
            return float(p.element())

        operator = p.element()

        left_value = self._evaluate_recur(self.left(p))
        right_value = self._evaluate_recur(self.right(p))

        if operator == "+":
            return left_value + right_value

        elif operator == "-":
            return left_value - right_value

        elif operator == "*":
            return left_value * right_value

        elif operator == "/":
            if right_value == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return left_value / right_value

    def to_infix(self):
        """Return the fully parenthesized infix expression."""

        if self._root is None:
            raise ValueError("Expression tree is empty")

        return self._infix_recur(self.root())

    def _infix_recur(self, p):

        if self.is_leaf(p):
            return p.element()

        left_expression = self._infix_recur(self.left(p))
        right_expression = self._infix_recur(self.right(p))

        return (
            "(" + left_expression + " "
            + p.element() + " "
            + right_expression + ")"
        )

    def to_postfix(self):
        """Return the expression in postfix notation."""

        return " ".join(str(p.element()) for p in self.postorder())
