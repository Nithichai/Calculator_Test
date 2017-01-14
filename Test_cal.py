import math


class Calculator:
    def __init__(self, equation):
        self.equation = equation

    # Calculate answer and show it
    def show_answer(self):
        try:
            checked_equation = self.operator_check(self.equation)  # Check more than 2 operator to 1
            listed_equation = self.str_to_list(checked_equation)  # Split string to  list
            print self.calculate(listed_equation)  # Calculate and print answer
        except IndexError:
            print "Syntax error"
        except ZeroDivisionError:
            print "Math error"

    @staticmethod
    def operator_check(equation_string):     # Check more than 2 operator to 1
        new_string = ""                      # String that save new equation
        i = 0
        while i < len(equation_string):      # Loop until at last of equation
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
                new_string += operator_output  # Add to operator in new string
            new_string += equation_string[i]   # Add data to new_string
            i += 1
        return new_string      # Return string that is set

    @staticmethod
    def str_to_list(equation_string):       # Set string to list
        equation_list = []                  # List that save data
        number_string = ""                  # String of number
        i = 0
        while i < len(equation_string):     # Loop until last of equation
            # Detect number and dot to save into number_string
            if equation_string[i].isdigit() or equation_string[i] == ".":
                number_string += equation_string[i]
            else:
                if number_string != "":         # Push number to equation_list and reset number_string
                    equation_list.append(number_string)
                    number_string = ""
                if equation_string[i] == "-":
                    if equation_string[i-1] != ")" and equation_string[i+1].isdigit() \
                            and not equation_string[i-1].isdigit(): # Detect (-a... to save - in number
                        number_string += "-"
                    elif i == 0 and equation_string[i+1].isdigit(): # Detect -a... to save - in number
                        number_string += "-"
                    else:
                        equation_list.append("-")                   # Save minus in list
                else:
                    equation_list.append(equation_string[i])        # Save operator in list
            i += 1
        if number_string != "":
            equation_list.append(number_string)      # Push all number to list
        return equation_list                         # Return list of equation

    def calculate(self, equation, recursive=False):  # Calculate and print answer
        number_list = []        # List that save numbers
        operator_list = []      # List that save operators
        data = equation[0]      # Data to check
        # Use recursive mode to get end of loop boolean
        if recursive:
            endloop_boolean = data != ")"        # until data is ")"
        else:
            endloop_boolean = len(equation) > 0  # until last of equation

        while endloop_boolean:
            data = equation.pop(0)          # Pop data from first index of equation
            if recursive and data == ")":   # Detect "(" to break loop (recursive mode)
                break
            elif data.isdigit():            # Detect number to push in number_list
                number_list.append(data)
            elif data == "(":
                answer = self.calculate(equation, True)     # Get answer from inside bracket
                # Detect + or - before left bracket
                if len(operator_list) > 0 and operator_list[-1] in "+-":
                    # Detect *, /, ^ before +, -
                    if len(operator_list) > 1 and operator_list[-2] in "*/^":
                        if operator_list[-1] == "+":                # Add answer to number_list and pop operator
                            number_list.append(answer)
                            operator_list.pop()
                        elif operator_list[-1] == "-":              # Add -answer to number_list and pop operator
                            number_list.append(str(-float(answer)))
                            operator_list.pop()
                    elif len(operator_list) == 1:                   # Detect +, - that is only one sign
                        if operator_list[-1] == "+":                # Add answer to number_list and pop operator
                            number_list.append(answer)
                            operator_list.pop()
                        elif operator_list[-1] == "-":              # Add -answer to number_list and pop operator
                            number_list.append(str(-float(answer)))
                            operator_list.pop()
                        # Protect no sign in operator_list after change sign before (
                        if len(operator_list) == 0:
                            operator_list.append("+")
                    else:
                        number_list.append(answer)                  # Push answer to number_list
                else:
                    number_list.append(answer)
            else:
                if data in "+-":
                    # Detect *, / before +, - so multiply or divine at first of
                    # two numbers and push at first of number_list
                    if len(operator_list) > 0 and operator_list[-1] in "*/" and equation[0] != "(":
                        while len(operator_list) > 0 and operator_list[0] not in "+-":
                            operator = operator_list.pop(0)
                            number0 = number_list.pop(0)
                            number1 = number_list.pop(0)
                            answer = self.get_str_ans(number0, number1, operator)
                            number_list.insert(0, answer)
                        operator_list.append(data)
                    # Detect ^ before +, - so powered from left until operator_list[0] == "+", "-", "*", "/"
                    elif len(operator_list) > 0 and operator_list[-1] == "^":
                        while len(operator_list) > 0 and operator_list[0] not in "+-*/":
                            number = number_list.pop(0)
                            expo = number_list.pop(0)
                            operator_list.pop(0)
                            answer = str(math.pow(float(number), float(expo)))
                            number_list.insert(0, answer)
                        operator_list.append(data)
                    else:
                        operator_list.append(data)
                elif data in "*/":
                    # Detect +,- before *,/ so multiply, divine from behind first
                    if len(operator_list) > 0 and operator_list[-1] in "+-":
                        number1 = equation.pop(0)
                        number0 = number_list.pop()
                        answer = self.get_str_ans(number0, number1, data)
                        number_list.append(answer)
                    # Detect ^ before *,/ so powered from left until operator_list[0] == "+", "-", "*", "/"
                    elif len(operator_list) > 0 and operator_list[-1] == "^":
                        while len(operator_list) > 0 and operator_list[0] not in "+-*/":
                            number = number_list.pop(0)
                            expo = number_list.pop(0)
                            operator_list.pop(0)
                            answer = str(math.pow(float(number), float(expo)))
                            number_list.insert(0, answer)
                        operator_list.append(data)
                    else:
                        operator_list.append(data)
                elif data == "^":
                    # Detect +, -, *, / before "^" so power from behind first
                    if len(operator_list) > 0 and operator_list[-1] in "+-*/":
                        expo = equation.pop(0)
                        number = number_list.pop()
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
        # Clear all calculation to complete
        while len(operator_list) > 0:
            operator = operator_list.pop(0)
            if operator == "^":         # Power it
                number = number_list.pop(0)
                expo = number_list.pop(0)
                answer = str(math.pow(float(number), float(expo)))
                number_list.insert(0, answer)
            elif len(operator_list) == 0 and len(number_list) == 1:     # number is positive or negative
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
        return str(float(number_list.pop()))

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

equation = raw_input("Enter equation : ")   # Set equation
cal = Calculator(equation)                  # Use calculator
cal.show_answer()                           # Calculate answer and show it
