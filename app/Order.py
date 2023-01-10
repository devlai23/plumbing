class Order:
    def __init__(self, invoiceID, date, item):
        self.invoiceID = invoiceID
        self.date = date
        self.item = item
        self.customerID = -1

    def setCustomerID(self, customerID):
        self.customerID = customerID
