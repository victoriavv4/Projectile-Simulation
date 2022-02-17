"""
BDP200-
Name: Victoria Villani
Student id: 124307208
"""

import prod_cart_mod
import user


# import pyodbc


class ACS(object):
    """This class represents terminal-based customer service events."""
    SECRET_CODE = "bye"

    ################ Constructor #####################
    def __init__(self):
        self._customer = None
        self._products = {}  # list of products available to display to the user
        self._methods = {}  # Jump table for commands
        self._methods["1"] = self._viewProducts
        self._methods["2"] = self._addProduct
        self._methods["3"] = self._removeProduct
        self._methods["4"] = self._viewCart
        self._methods["5"] = self._quit
        self.__loadProducts()

    def __loadProducts(self):
        """ creates a set of 4 products added to _products dictionary.
        the Product class in the prod_cart_mod module should be defined.
        """
        p1 = prod_cart_mod.Product('11QER/31', 'Power painter, 15 psi., 3-nozzle', 120, 8, 20)
        p2 = prod_cart_mod.Product('13-Q2/P2', '7.25-in. pwr. saw blade', 80, 32)
        p3 = prod_cart_mod.Product('14-Q1/L3', '9.00-in. pwr. saw blade', 70, 18)
        p4 = prod_cart_mod.Product('1546-QQ2', 'Hrd. cloth, 1/4-in., 2x50', 100, 15)
        self._products[p1.getcode()] = p1
        self._products[p2.getcode()] = p2
        self._products[p3.getcode()] = p3
        self._products[p4.getcode()] = p4

        ################ run main menu #####################

    def run(self):
        """Logs in customers and processes their accounts."""
        while True:
            userid = input("Enter your user id: ")
            if userid == ACS.SECRET_CODE:
                break
            pwd = input("Enter your PASSWORD: ")
            self._customer = self._authenticateUser(userid, pwd)
            if self._customer == None:
                print("Error, incorrect userid or password")
            else:
                print(self._customer)
                self._processCustomerAccount()

    ################ view all products #####################
    def _viewProducts(self):
        """print the list of all products on the screen. Use the print function """
        for value in self._products.values():
            print(value)

        ################ authenticate user in DB  #####################

    def _authenticateUser(self, userid, pwd):
        """ this method will authenticate the user and returns the customer object.
        You may consider to read from a text file and search for the given userid and password
        If found, create a new customer object."""
        info_dict = {}
        with open("test_text") as f:
            for line in f:
                (key, val) = line.split()
                info_dict[key] = val
            f.close()
        try:
            if info_dict[userid]:
                pass
        except KeyError as err:
            print(err, "Invalid. Please try again.")
        x = info_dict.get(userid)
        if x == pwd:
            return user.Customer(userid, pwd)
        else:
            print("Password invalid or does not match username. Please try again")

    ################ process customer account #####################
    def _processCustomerAccount(self):
        """A menu-driven command showing the options to view all products,
        add a product in the cart, remove a product from the cart, view the cart.
        or quit. Given the user-entered option, the corresponding method should be
        called from self._methods.
        if the option is not recognized, print a message with the text:' unrecognized number.
        Refer to the sample execution output for more about functionalities.
        """

        while True:
            print("Main menu: ")
            print("1   View all products" + "\n" + "2   Add a product in the cart" + "\n" + "3   Remove a product from"
                    " the cart" + "\n" + "4   View your cart" + "\n" + "5   Quit")
            user_input = (input("Enter a number: "))
            if user_input == "1":
                self._viewProducts()
            elif user_input == "2":
                self._addProduct()
            elif user_input == "3":
                self._removeProduct()
            elif user_input == "4":
                self._viewCart()
            elif user_input == "5":
                self._quit()
                break
            else:
                print("Unrecognized number")

    ################ add product #####################
    def _addProduct(self):
        """ prompt the user for a product code to add to the cart and the quantity.
        print a message on the screen, that the product was added to the cart,
        out of stock or invalid.
        """
        pcode_input = input("Enter the product code to add to the cart: ")
        qty_input = int(input("Enter the quantity you would like to order: "))

        if pcode_input in self._products.keys():
            product = self._products[pcode_input]
            self._customer.addProduct(product, qty_input)
            print("Product added to the cart")
        else:
            print("Product invalid")

    ################ _viewCart #####################
    def _viewCart(self):
        """ prints what is in the users' cart on screen for user.  Calls viewCart() method from user module.   """
        print(self._customer)
        self._customer.viewCart()

    ################ _removeProduct #####################
    def _removeProduct(self):
        """ prompt the user for the product code that needs to be removed from the cart.
        print a message whether the product was removed from the card or the product code is invalid.
        """
        code_input = input("Enter the product code to remove from the cart:  ")

        if code_input in self._products.keys():
            product = self._products[code_input]
            if product in self._customer.cart.keys():
                self._customer.removeProduct(product)
                print("Product removed from cart. ")
        else:
            print("Invalid product code. ")

    ################ quit #####################
    def _quit(self):
        """ Assigns none to the current customer object, and print a message saying ' Have a nice day!"""
        self._customer = None
        print("Have a nice day!")


################ TESTING #####################
def main():
    acs = ACS()
    acs.run()


main()
