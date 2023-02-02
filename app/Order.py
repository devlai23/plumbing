class Order:
    def __init__(self, invoiceID, date, item):
        self.invoiceID = invoiceID
        self.date = date
        self.item = item
        self.customerID = -1

    def setCustomerID(self, customerID):
        self.customerID = customerID

    def getInvoice(self):
        return self.invoiceID

    def getDate(self):
        return self.date
    
    def __str__(self):
     return str(self.invoiceID) + "\n" + str(self.date) + "\n" + str(self.item) + "\n" + str(self.customerID) + "\n"

    def insertQuery(self):
        formatted = "INSERT INTO Purchases(Invoice_ID, Item, Customer_ID, Date) VALUES (" + str(self.invoiceID) + ", \"" + str(self.item) + "\", " + str(self.customerID) + ", \"" + str(self.date) + "\")"
        return formatted
