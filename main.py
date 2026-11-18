from binary_expression_tree import BinaryExpressionTree


def main():

    expressions = [
        "5 3 8 * +",
        "8 2 / 3 -",
        "10 5 +",
        "4 2 * 6 +",
        "-2.5 3.5 +",
        "10 2 / 3 *"
    ]

    for expression in expressions:

        print("-----------------------------------")
        print("Original Postfix:", expression)

        try:
            tree = BinaryExpressionTree(expression)

            print("Infix Expression:", tree.to_infix())
            print("Generated Postfix:", tree.to_postfix())
            print("Evaluated Result:", tree.evaluate())

        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error)

    # Test invalid expressions separately.
    invalid_expressions = [
        "",
        "5 +",
        "5 3",
        "5 3 &"
    ]

    print("\nTesting Invalid Expressions")

    for expression in invalid_expressions:

        print("-----------------------------------")
        print("Expression:", repr(expression))

        try:
            tree = BinaryExpressionTree(expression)
            print("Result:", tree.evaluate())

        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
