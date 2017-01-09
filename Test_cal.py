class Calculator :
    
    def __init__(self, eq):
        self.eq = eq
        self.number = []
        self.operator = []
        self.x = 0
        self.y = 0
        self.op = ""
        self.ans = 0
        print(self.eq)
    
    def calculate(self):
        # infix
        list_eq = self.eq.split(" ")
        while(len(list_eq) != 0):
            self.debug()
            data = list_eq.pop(0)
            if data == ")" :
                self.op = self.operator.pop()
                while(self.op != "("):
                    self.y = self.number.pop()
                    self.x = self.number.pop()
                    self.number.append(str(self.push_data(self.x, self.y, self.op)))
                    self.op = self.operator.pop()
            elif (data == "*" or data == "/") :
                self.y = list_eq.pop(0)
                if self.y == "+" or self.y == "-" or self.y == "(" :
                    self.operator.append(data)
                    self.operator.append(self.y)
                else :
                    self.x = self.number.pop()
                    self.op = data
                    self.number.append(str(self.push_data(self.x, self.y, self.op)))
            elif (data == "+" or data == "-" or data == "(") :
                self.operator.append(data)
            else :
                self.number.append(data)
        
        # postfix
        while(len(self.operator) != 0):
            self.op = self.operator.pop()
            self.y = self.number.pop()
            self.x = self.number.pop()
            self.number.append(str(self.push_data(self.x, self.y, self.op)))
        self.ans = float(self.number.pop())
        
    def debug(self):
        print(self.number, self.operator)
                
    def push_data(self, x, y, op):
        if op == "+":
            return float(x) + float(y)
        elif op == "-":
            return float(x) - float(y)
        elif op == "*":
            return float(x) * float(y)
        elif op == "/":
            return float(x) / float(y)
    
    def get_ans(self):
        print(self.ans)
        
cal = Calculator("2 * ( ( 3 + 8 ) / 4 )")
cal.calculate()
cal.get_ans()
        