import math


class Calculator:
    def __init__(self, equation):
        self.equation = equation
        self.ans = 0  # Answer of equation

    # Calculate answer and show it
    def show_ans(self):
        checked_equation = self.operator_check(self.eq)         # Check more than 2 operator to 1
        listed_equation = self.str_to_list(checked_equation)    # Split string to list
        print self.calculate(listed_equation)                   # Calculate and print answer

    @staticmethod
    def operator_check(equation_string):     # Check more than 2 operator to 1
        new_str = ""                         # String that save new equation
        i = 0
        while i < len(equation_string):      # Loop until i at last of eq)
            # Find "+" or "-"
            if equation_string[i] == "+" or equation_string[i] == "-":
                operator_output = equation_string[i]
                i += 1
                while equation_string[i] in "+-":                               # Loop until is not "+" and "-"
                    if operator_output + equation_string[i] == "+-" \
                            or operator_output + equation_string[i] == "-+":    # Change to minus
                        operator_output = "-"
                    elif operator_output + equation_string[i] == "++" \
                            or operator_output + equation_string[i] == "--":    # Change to plus
                        operator_output = "+"
                    i += 1
                if equation_string == "":           # Detect eq_str is null
                    if operator_output != "+":      # Detect operator_output that is not "+"
                        new_str += operator_output  # Add to operator in new string
                else:
                    # Detect last of equation is "(" and operator_output is "+" to do nothing
                    if equation_string[-1] == "(" and operator_output == "+":
                        pass
                    else:
                        new_str += operator_output  # Add operator to new_str
            new_str += equation_string[i]  # Add text to new string
            i += 1
        print new_str
        return new_str

    @staticmethod
    def str_to_list(eq_str):
        ls = []
        number_string = ""
        i = 0
        while i < len(eq_str):
            if eq_str[i].isdigit() or eq_str[i] == ".":
                number_string += eq_str[i]
            else:
                if number_string != "":
                    ls.append(number_string)
                    number_string = ""
                if eq_str[i] == "-":
                    if eq_str[i - 1] != ")" and eq_str[i + 1].isdigit() and not eq_str[i - 1].isdigit():
                        number_string += "-"
                    elif i == 0 and eq_str[i + 1].isdigit():
                        number_string += "-"
                    else:
                        ls.append("-")
                else:
                    ls.append(eq_str[i])
            i += 1
        if number_string != "":
            ls.append(number_string)
        print ls
        return ls

    def calculate(self, equation, recursive=False):
        print "--------------"
        number_list = []
        operator_list = []
        data = equation[0]
        if recursive:
            endloop_boolean = data != ")"
        else:
            endloop_boolean = len(equation) > 0

        while endloop_boolean:
            data = equation.pop(0)
            if data == ")":
                break
            elif data.isdigit():
                number_list.append(data)
            elif data == "(":
                answer = self.calculate(equation, True)
                if len(operator_list) > 0 and operator_list[-1] in "+-":
                    if len(operator_list) > 1 and operator_list[-2] in "*/^":
                        if operator_list[-1] == "+":
                            number_list.append(answer)
                            operator_list.pop()
                        elif operator_list[-1] == "-":
                            number_list.append(str(-float(answer)))
                            operator_list.pop()
                    elif len(operator_list) == 1:
                        if operator_list[-1] == "+":
                            number_list.append(answer)
                            operator_list.pop()
                        elif operator_list[-1] == "-":
                            number_list.append(str(-float(answer)))
                            operator_list.pop()
                        if len(operator_list) == 0:
                            operator_list.append("+")
                    else:
                        number_list.append(answer)
                else:
                    number_list.append(answer)
            else:
                if data in "+-":
                    if len(operator_list) > 0 and operator_list[-1] in "*/" and equation[0] != "(":
                        while len(operator_list) > 0 and operator_list[0] not in "+-":
                            operator = operator_list.pop(0)
                            number1 = number_list.pop(0)
                            number0 = number_list.pop(0)
                            answer = self.get_str_ans(number0, number1, operator)
                            number_list.insert(0, answer)
                        operator_list.append(data)
                    elif len(operator_list) > 0 and operator_list[-1] == "^" and data != "-":
                        expo = number_list.pop()
                        number = number_list.pop()
                        answer = str(math.pow(float(number), float(expo)))
                        number_list.append(answer)
                        operator_list.append(data)
                    else:
                        operator_list.append(data)
                elif data in "*/":
                    if len(operator_list) > 0 and operator_list[-1] in "+-":
                        number1 = equation.pop(0)
                        number0 = number_list.pop()
                        answer = self.get_str_ans(number0, number1, data)
                        number_list.append(answer)
                    elif len(operator_list) > 0 and operator_list[-1] == "^":
                        expo = number_list.pop()
                        number = number_list.pop()
                        answer = str(math.pow(float(number), float(expo)))
                        number_list.append(answer)
                        operator_list.append(data)
                    else:
                        operator_list.append(data)
                elif data == "^":
                    if equation[0].isdigit():
                        number = number_list.pop()
                        expo = equation.pop(0)
                        answer = str(math.pow(float(number), float(expo)))
                        number_list.append(answer)
                    else:
                        operator_list.append("^")
                else:
                    number_list.append(data)

            if recursive:
                endloop_boolean = data != ")"
            else:
                endloop_boolean = len(equation) > 0
            print operator_list, number_list
        while len(operator_list) > 0:
            operator = operator_list.pop(0)
            if operator == "^":
                number = number_list.pop(0)
                expo = number_list.pop(0)
                answer = str(math.pow(float(number), float(expo)))
                number_list.insert(0, answer)
            elif len(operator_list) == 0 and len(number_list) == 1:
                number0 = number_list.pop(0)
                if operator == "+":
                    number_list.insert(0, number0)
                elif operator == "-":
                    number_list.insert(0, str(-float(number0)))
            else:
                number0 = number_list.pop(0)
                number1 = number_list.pop(0)
                answer = self.get_str_ans(number0, number1, operator)
                number_list.insert(0, answer)
        print number_list[0]
        print "**************"
        return number_list.pop()

    # Calculate answer
    @staticmethod
    def get_str_ans(x, y, op):
        if op == "+":  # op is plus
            return str(float(x) + float(y))  # x + y
        elif op == "-":  # op is minus
            return str(float(x) - float(y))  # x - y
        elif op == "*":  # op is multiply
            return str(float(x) * float(y))  # x * y
        elif op == "/":  # op is divine
            return str(float(x) / float(y))  # x / y"""

equation = raw_input("Enter equation : ")  # Set equation
cal = Calculator(equation)  # Use calculator
cal.show_ans()  # Calculate answer and show it
