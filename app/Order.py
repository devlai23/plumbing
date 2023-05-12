class Order:
    def __init__(self, invoiceID, date, item):
        self.invoiceID = invoiceID
        self.date = date
        self.item = item
        self.customerID = -1

    def isSanatized(strArg):
        acceptableCharacters = {' ': 's', '@': 'a', '-': 'd', '/': 'l', '.': 'p', ':': 'c'}
        for x,y in acceptableCharacters.items():
            strArg = strArg.replace(x, y)
        if strArg == "":
            return True
        print(strArg)
        if strArg.isalnum() == True:
            return True
        return False

    def setCustomerID(self, customerID):
        self.customerID = customerID

    def getInvoice(self):
        return self.invoiceID

    def getDate(self):
        return self.date
    
    def __str__(self):
     return str(self.invoiceID) + "\n" + str(self.date) + "\n" + str(self.item) + "\n" + str(self.customerID) + "\n"

    def insertQuery(self):
        formatted = ""
        if(self.isSanatized(str(self.invoiceID)) and self.isSanatized(str(self.item)) and self.isSanatized(str(self.customerID)) and self.isSanatized(str(self.date))):
            formatted = "INSERT INTO Purchases(Invoice_ID, Item, Customer_ID, Date) VALUES (" + str(self.invoiceID) + ", \"" + str(self.item) + "\", " + str(self.customerID) + ", \"" + str(self.date) + "\")"
        return formatted
