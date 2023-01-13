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
    
    def __str__(self):
     return str(self.invoiceID) + "\n" + str(self.date) + "\n" + str(self.item)
