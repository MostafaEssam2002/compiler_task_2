def is_simple_grammar(rules):
    """
    التحقق من إذا كان الجرامر Simple.
    Simple Grammar:
    1. كل قاعدة تبدأ برمز طرفي (حرف صغير).
    2. لكل Non-Terminal، لا يتكرر الرمز الطرفي في بداية القواعد.
    """
    for non_terminal, productions in rules.items():
        terminals_seen = set()
        for production in productions:
            if not production or not production[0].islower():
                return False
            first_terminal = production[0]
            if first_terminal in terminals_seen:
                return False
            terminals_seen.add(first_terminal)
    return True

def parse_string(rules, start_symbol, string):
    """
    التحقق مما إذا كانت السلسلة مقبولة بناءً على الجرامر مع طباعة التفاصيل.
    """
    stack = [start_symbol]
    index = 0
    print("\nThe input String: ", list(string))
    while stack:
        # print("\nStack after checking: ", stack)
        # print("The rest of unchecked string: ", list(string[index:]))
        top = stack.pop()
        if index >= len(string):
            print("❌ No more input to check.")
            return False
        if top.islower():  # Terminal check
            if top == string[index]:
                index += 1
            else:
                print(f"❌ Mismatch: Expected '{top}' but found '{string[index]}'.")
                return False
        elif top.isupper():  # Non-terminal, expand using rules
            expanded = False
            for production in rules[top]:
                if production[0] == string[index]:
                    for symbol in reversed(production):
                        stack.append(symbol)
                    expanded = True
                    break
            if not expanded:
                print(f"❌ No valid rule for Non-Terminal '{top}' with '{string[index]}' at position {index}.")
                return False
    print("\nStack after checking: ", stack)
    print("The rest of unchecked string: ", list(string[index:]))
    return index == len(string)

def enter_grammer():
    print("\n👇 Enter Your Grammar Rules 👇")
    grammar_rules = {}
    non_terminals = ["S", "B"]  # ثابت: 2 Non-Terminal فقط
    for non_terminal in non_terminals:
        # print(f"\nEnter rules for Non-Terminal '{non_terminal}':")
        rules = []
        for i in range(2):  # كل Non-Terminal له قاعدتان
            rule = input(f"Rule Number {i + 1} for non terminal '{non_terminal}' ").strip()
            rules.append(rule)
        grammar_rules[non_terminal] = rules
    return grammar_rules

start_symbol = "S"
# استدعاء إدخال القواعد مع التأكد أنها Simple
while True:
    grammar_rules = enter_grammer()
    if is_simple_grammar(grammar_rules):
        print("\n✅ The Grammar is Simple ✅")
        break  # الخروج من الحلقة إذا كانت القواعد Simple
    else:
        print("\n❌ The Grammar is NOT Simple. Please enter a valid Simple Grammar.")
# إذا كانت القواعد Simple، البدء في تنفيذ الخيارات
while True:
    print("\n1-Enter another grammar ")
    print("2-Enter a String to Check")
    print("3-Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        # إدخال قواعد جديدة مع التأكد أنها Simple
        while True:
            grammar_rules = enter_grammer()
            if is_simple_grammar(grammar_rules):
                print("\n✅ The new Grammar is Simple ✅")
                break
            else:
                print("\n❌ The Grammar is NOT Simple. Please enter a valid Simple Grammar.")
    elif choice == "2":
        string = input("Enter the string to be checked: ").strip()
        result = parse_string(grammar_rules, start_symbol, string)
        if result:
            print("\n🎉 The input string is Accepted.")
        else:
            print("\n❌ The input string is Rejected.")
    elif choice == "3":
        print("Exiting... Goodbye!")
        exit()
    else:
        print("Invalid choice, please try again.")

