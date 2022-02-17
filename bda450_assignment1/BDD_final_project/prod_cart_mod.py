class Product(object):
    """ Represents a product """

    def __init__(self, pcode, pdesc, price, qoh=0, discount=0):
        """ Initialized intstance variables: pcode, pdesc, price, qoh, and discount with the supplied arguments pcode,
           pdesc, price, qoh, and discount"""
        self.pcode = pcode
        self.pdesc = pdesc
        self.price = price
        self.qoh = qoh
        self.discount = discount

    def getcode(self):
        """ returns the product code. """
        return self.pcode

    def getdesc(self):
        """ returns the product description. """
        return self.pdesc

    def getprice(self):
        """ returns the product price. """
        return self.price

    def getQOH(self):
        """ returns the product quantity. """
        return self.qoh

    def getdiscount(self):
        """ Returns the product discount. """
        return self.discount

    def updateQOH(self, qty):
        """ updates the product quantity. """
        self.qoh = qty
        return self.qoh

    def updaterprice(self, newprice):
        """ updated the product price. """
        self.price = newprice
        return self.price

    def updateddiscount(self, newdiscount):
        """ updates the product discount. """
        self.discount = newdiscount
        return self.discount

    def __str__(self):
        """ returns a formatted string containing product code, description, price and discount. """
        return "{}|{:36}|${:>6.2f}|{}%".format(self.pcode, self.pdesc, self.price, self.discount)


class CartLine(object):
    """ Represents a cart line containing a product and quantity ordered.   """

    def __init__(self, product, qty):
        """ Initialized instance variables: product, qty with the supplied arguments product and qty """
        self.product = product
        self.qty = qty

    def updateQty(self, newqty):
        """ updates the quantity of an item"""
        self.qty = newqty
        return self.qty

    def __str__(self):
        """returns a formatted string containing product code, description, price, quantity, discount
        and total price. """
        return "{:<14}{:<36}{:<6.2f}  {:<4}{}%\n${:.2f}".format(self.product.getcode(), self.product.getdesc(),
        self.product.getprice(), self.qty, self.product.getdiscount(),
        self.qty * (self.product.getprice()))
