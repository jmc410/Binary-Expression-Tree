import unittest
from binary_expression_tree import BinaryExpressionTree


class TestBinaryExpressionTree(unittest.TestCase):

    def test_basic_addition(self):
        tree = BinaryExpressionTree("5 3 +")
        self.assertAlmostEqual(tree.evaluate(), 8.0)

    def test_nested_expression(self):
        tree = BinaryExpressionTree("5 3 8 * +")
        self.assertAlmostEqual(tree.evaluate(), 29.0)

    def test_subtraction_order(self):
        tree = BinaryExpressionTree("8 2 -")
        self.assertAlmostEqual(tree.evaluate(), 6.0)

    def test_division_order(self):
        tree = BinaryExpressionTree("8 2 / 3 -")
        self.assertAlmostEqual(tree.evaluate(), 1.0)

    def test_decimal_and_negative_numbers(self):
        tree = BinaryExpressionTree("-2.5 3.5 +")
        self.assertAlmostEqual(tree.evaluate(), 1.0)

    def test_extra_operands(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("5 3 8 +")

    def test_too_few_operands(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("5 +")

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("")

    def test_unsupported_token(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("5 3 &")

    def test_division_by_zero(self):
        tree = BinaryExpressionTree("8 0 /")

        with self.assertRaises(ZeroDivisionError):
            tree.evaluate()

    def test_postfix_output(self):
        expression = "5 3 8 * +"
        tree = BinaryExpressionTree(expression)

        self.assertEqual(tree.to_postfix(), expression)

    def test_infix_output(self):
        tree = BinaryExpressionTree("5 3 8 * +")

        self.assertEqual(
            tree.to_infix(),
            "(5 + (3 * 8))"
        )

    def test_preorder_traversal(self):
        tree = BinaryExpressionTree("5 3 +")

        result = [
            p.element() for p in tree.preorder()
        ]

        self.assertEqual(result, ["+", "5", "3"])

    def test_inorder_traversal(self):
        tree = BinaryExpressionTree("5 3 +")

        result = [
            p.element() for p in tree.inorder()
        ]

        self.assertEqual(result, ["5", "+", "3"])

    def test_postorder_traversal(self):
        tree = BinaryExpressionTree("5 3 +")

        result = [
            p.element() for p in tree.postorder()
        ]

        self.assertEqual(result, ["5", "3", "+"])


if __name__ == "__main__":
    unittest.main()
