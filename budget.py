class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.cash = 0.00
    def __repr__(self):
        title = self.name.center(30,"*")+"\n"
        bill=""
        for item in self.ledger:
            line =""
            desc = item["description"]
            desc = desc[0:23]

            amt = "{:.2f}".format(item["amount"])
            amt = str(amt)
            amt = amt[0:7]
            line = "{:<23}{:>7}".format(desc, amt)
            line = line + "\n"
            bill = bill+line
        Tot = "{:.2f}".format(self.cash)
        Tot = "Total: "+str(Tot)
        return title+bill+Tot
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.cash = self.cash + amount
        return True
    def withdraw(self, amount, description=""):
        if self.cash - amount>=0:
            self.ledger.append({"amount": -amount, "description": description})
            self.cash = self.cash - amount
            return True
        else:
            return False
    def get_balance(self):
        return self.cash
    def transfer(self, amount, budget):
        if self.withdraw(amount, "Transfer to "+budget.name):
            budget.deposit(amount, "Transfer from "+self.name)
            return True
        else:
            return False
    def check_funds(self,amount):
        if self.cash>=amount:
            return True
        else:
            return False




def create_spend_chart(categories):
    title = "Percentage spent by category\n"
    raw_spends = []
    for category in categories:
        cash = 0
        for item in category.ledger:
            if item["amount"]<0:
                spend = item["amount"]*-1
                spend = round(spend,2)
                cash = cash + spend
                cash = round(cash,2)
        raw_spends.append({"category": category.name, "spends": cash})
        #Find total
        total = 0.0
        for spend in raw_spends:
            total = total + spend["spends"]
        #Calculate percentage
        perc_spends = []
        for spend in raw_spends:
            perc = spend["spends"]/total*100
            #perc = round(perc/10)*10
            perc = perc - (perc%10)
            perc_spends.append({"category": spend["category"], "perc": perc})
        #make graph
        graph = ""
        for i in reversed(range(0,109,10)):
            line = ""
            
            for per in perc_spends:
                if per["perc"]>=i:
                    line = line + " o "
                else:
                    line = line + "   "
            y_axis = "{:>4}".format(str(i)+"|")
            graph = graph + y_axis+line+" \n"
    graph = graph+"    "+"-"*((3*len(categories))+1)+"\n"
    #x-axis labels
    max_length = 0
    for category in categories:
        if len(category.name)>max_length:
            max_length = len(category.name)
    x_axis=""
    for i in range(0,max_length):
        line = "    "
        for category in categories:
            if i<len(category.name):
                line = line + " "+category.name[i]+" "
            else:
                line = line +"   "
        line = line +" \n"
        x_axis = x_axis+line
    x_axis = x_axis.rstrip('\n')
    return title+graph+x_axis