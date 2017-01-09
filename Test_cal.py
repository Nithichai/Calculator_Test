class Calculator :
    
    def __init__(self, eq):
        self.eq = eq            # Set equation
        self.number = []        # Number stack
        self.operator = []      # Operator stack
        self.ans = 0            # Answer of equation
    
    def calculate(self):        # Calculate answer
        self.infix()            # Infix step
        self.postfix()          # Postfix step
        
    # Infix step
    def infix(self):            
        list_eq = self.eq.split(" ")    # Split string to list
        while(len(list_eq) != 0):       # No value in list_eq
            data = list_eq.pop(0)       # Pop data from left
            if data == ")" :            # Find ")"
                op = self.operator.pop()    # Pop value from opertor stack
                while(op != "("):           # op is not "("
                    y = self.number.pop()   # set x
                    x = self.number.pop()   # Set y
                    str_ans = self.get_str_ans(x, y, op)    # Calculate 2 variable and get to string
                    self.number.append(str_ans)     # Push to number stack
                    op = self.operator.pop()        # Pop operator stack
            elif (data == "*" or data == "/") :     # Find "*" or "/"
                y = list_eq.pop(0)                  # Pop value from left
                if y == "+" or y == "-" or y == "(" :   # Find "+" or "-" or "("
                    self.operator.append(data)      # Push data to operator stack
                    self.operator.append(y)         # Push data to operator stack
                else :                              # Otherwise
                    x = self.number.pop()           # Set x
                    op = data                       # Set op
                    str_ans = self.get_str_ans(x, y, op)    # Calculate 2 variable and get to string 
                    self.number.append(str_ans)     # Push answer to number stack
            elif (data == "+" or data == "-" or data == "(") :  # Find "+" or "-" or "("
                self.operator.append(data)          # Push data to operator stack
            else :                                  # Otherwise
                self.number.append(data)            # Push data to number stack
    
    # Postfix step
    def postfix(self):
        while(len(self.operator) != 0):     # length of operator list is not null
            op = self.operator.pop()        # Pop operator stack
            y = self.number.pop()           # Pop number to y
            x = self.number.pop()           # Pop number to x
            str_ans = self.get_str_ans(x, y, op)    # Get answer
            self.number.append(str_ans)     # Push answer to number stack
        self.ans = float(self.number.pop()) # Set answer
        print(self.ans)                     # Print answer
    
    # Calculate answer            
    def get_str_ans(self, x, y, op):
        if op == "+":           # op is plus
            return str(float(x) + float(y)) # X + Y
        elif op == "-":         # op is minus
            return str(float(x) - float(y)) # X - Y
        elif op == "*":         # op is multiply
            return str(float(x) * float(y)) # X * Y
        elif op == "/":         # op is divine
            return str(float(x) / float(y)) # X / Y
        
equation = raw_input("Enter equation : ")       # Set equation
cal = Calculator(equation)                      # Use calculator
cal.calculate()                                 # Calculate answer
        