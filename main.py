def is_simple_grammar(rules):
    """
    This function checks if a given grammar is simple based on the rules in the image.
    Simple grammar rules are of the form: A -> a\u03b1
    1. Every rule must start with a terminal.
    2. For a non-terminal, no two rules can start with the same terminal.
    """
    for non_terminal, productions in rules.items():
        terminals_seen = set()
        for production in productions:
            # Check if the rule starts with a terminal
            if not production or not production[0].islower():
                return False  # Not simple because it doesn't start with a terminal
            # Check for terminal repetition in rules for the same non-terminal
            first_terminal = production[0]
            if first_terminal in terminals_seen:
                return False  # Not simple because terminals are not disjoint
            terminals_seen.add(first_terminal)
    return True

def input_grammar():
    """ Function to input grammar rules from the user. """
    rules = {}
    num_non_terminals = int(input("Enter the number of non-terminals: "))
    for i in range(num_non_terminals):
        non_terminal = input(f"Enter non-terminal {i+1}: ").strip()
        num_rules = int(input(f"Enter the number of rules for non-terminal '{non_terminal}': "))
        productions = []
        for j in range(num_rules):
            rule = input(f"Enter rule {j+1} for non-terminal '{non_terminal}': ").strip()
            productions.append(rule)
        rules[non_terminal] = productions
    return rules

# Main Program
while True:
    print("\n👇 Grammars 👇")
    grammar_rules = input_grammar()
    if is_simple_grammar(grammar_rules):
        print("The Grammar is Simple ✅")
        break  # Exit the loop if grammar is valid
    else:
        print("The Grammar is NOT Simple ❌. Please enter the rules again.")
        print("===========================================")

print("\n1-Another Grammar.\n2-Another String.\n3-Exit")
