import random
import string
import datetime
import prod_cart_mod


class Person(object):
    """ Represents a person """
    __nbPerson = 0


    def __init__(self, userid, pwd):
        """ Initialized the instance variables userid and pwd and set pwd as private intsance variable with
         the supplied arguments userid and __pwd. Increments person count.  """
        self.userid = userid
        self.__pwd = pwd
        Person.__nbPerson += 1

    def __str__(self):
        """ Returns a string concatenating the user ID and pwd """
        return self.userid + ", " + self.__pwd

    def get_num_persons(self):
        """  Returns the person count """
        return "nb person: " + str(Person.__nbPerson)

    def get_pwd(self):
        """ Returns a person's pwd to be used to call the private method """
        return self.__pwd

    def change_pwd(self, oldpwd, newpwd):
        """ Checks if the supplied old password matches the private variable pwd and resets it when there
        is a match """
        if self.__pwd == oldpwd:
            self.__pwd = newpwd

    def reset_pwd(self):
        """ Resets the private instance variable pwd with a randomly generated sequence of characters and digits"""
        self.__pwd = ''.join(random.choice(string.ascii_letters + string.digits) for self.__pwd in range(10))
        return self.__pwd


class Customer(Person):
    """ Represents a customer """
    __nbCustomer = 0
    cart = {}

    def __init__(self, userid, pwd, joined_since=datetime.datetime.now()):
        """ Initialized the instance variables userid and pwd and set pwd as private intsance by inheriting from
        parent class. Adds a joined_since instance variable with the supplied arguments userid and __pwd, and
        joined.since. Increments customer count. """
        super().__init__(userid, pwd)
        self.joined_since = joined_since
        Customer.__nbCustomer += 1

    def __str__(self):
        """ Returns a string concatenating the user ID and pwd by inheriting the parent class str method.
        Add joined_since instance variable and customer count to the string"""
        return "Customer profile: " + super(Customer, self).__str__() + ", " + "Joined since: " + \
               str(self.joined_since) + " " + str(self.get_num_customers())

    def get_num_customers(self):
        """ Returns customer count """
        return "nb customer: " + str(Customer.__nbCustomer)

    def addProduct(self, product, qty):
        """ adds product & quantity to cart dictionary. """
        self.cart[product] = prod_cart_mod.CartLine(product, qty)

    def removeProduct(self, product):
        """ removes user defined product from dictionary. """
        self.cart.pop(product)

    def viewCart(self):
        """ display/ print elements in self.cart dictionary. Calculates item total
        including qty and discount price. """
        for (x) in self.cart.values():
            print(x)
        total = 0
        for item in self.cart.keys():
            cart_items = self.cart[item]
            disc_price = item.getprice()*(1-item.getdiscount()/100)
            price = disc_price*cart_items.qty
            total += price
        print("Total= $" + "%2d" % total)








