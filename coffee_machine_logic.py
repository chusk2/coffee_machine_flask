class Coffee:

    def __init__(self, name: str, price: float, recipe: dict,
                 default_sugar: int = 1):
        self.name = name
        self.price = price
        self.recipe = recipe
        self.default_sugar = default_sugar

class Espresso(Coffee):
        
        def __init__(self):
            super().__init__(name = 'Espresso', price = 1.8,
                  recipe = {'water': 50, 'beans': 18, 'milk': 0},
                  default_sugar = 0)

class Latte(Coffee):
    def __init__(self):
        super().__init__(name = "Latte", price = 2.50,
               recipe = {'water': 40, 'beans': 18, 'milk': 150},
               default_sugar = 1)

class Cappuccino(Coffee):
    def __init__(self):
        super().__init__(name = "Cappuccino", price = 2.60,
                    recipe = {'water': 50, 'beans': 18, 'milk': 100},
                    default_sugar = 1)

class CoffeeMachine:

    def __init__(self, menu: dict, max_resources: dict, machine_credit:float = 0):
        """
        menu (dictionary): A dictionary containing instances of the available
        Coffee objects. Keys are coffeee names and
         values are the object instances. (e.g., an Espresso object, a Latte object).

        max_resources (dictionary): The current amount of ingredients
        available in the machine.
        Example: {'water': 1000, 'beans': 500, 'milk': 750}.

        money_credit (float): The amount of money the user has inserted.
        Initially 0.
        """

        self.menu = menu
        self.max_resources = max_resources
        # create a copy of the max_resources to track current resources
        self.resources = self.max_resources.copy()
        self.machine_credit = machine_credit
        # attribute to store the current transaction balance
        self.user_credit = 0
   
    ## Public methods
  
    def insert_money(self, amount: float):
        self.user_credit += amount

    # Maintenance
    def report_status(self):
        
        message = 'The available resources and their quantities are:\n'
        
        for resource, amount in self.resources.items():
            message += f'{resource}: {amount}\n'
        
        message += f'\n\nCurrent money in the machine is ${self.machine_credit}'

        return message

    ## Private methods
    def _coffee_not_available(self, coffee):
              
        message = f'''The selected coffee ({coffee.name}) is\
                currently not available!

                Sorry for the inconvenience.

                Here is the money you entered: ${self.user_credit:.2f}'''
        
        return message        
    
    def _check_resources(self, coffee : str):

        recipe = coffee.recipe

        for resource, amount in recipe.items():
            if self.resources[resource] >= amount:
                pass
            else:
                self._coffee_not_available(coffee)
                return False
        
        return True

    def _payment_ok(self, coffee) -> bool:

        price = coffee.price

        if self.user_credit < coffee.price:
            return False
        else:
            return True
    
    def _brew_drink(self, coffee):

        recipe = coffee.recipe

        for resource, amount in recipe.items():
            self.resources[resource] -= amount
    
    def return_change(self, coffee):

        change = self.user_credit - coffee.price
        self.user_credit = 0

        return change
    
    def order_coffee(self, selected_coffee):
        
        ## SHOW SELECTION AND PRICE
        coffee = self.menu[selected_coffee]
        
        ## CHECK THE PAYMENT
        if not self._payment_ok(coffee):
            message = f'''Your introduced money is insufficient for your current coffee selection.
            {coffee.name} price is ${coffee.price:.2f}.
            You have to introduce ${coffee.price - self.user_credit:.2f} more to get your {coffee.name}, please.')
            '''
            return message
        
        ## CHECK RESOURCES
        if not self._check_resources(coffee):
            self.user_credit = 0

            messsage = f'''We are sorry for the inconvenience.
            Currently the machine has insufficient resources to brew your coffee.
            Transaction canceled.

            Here you have your money: ${self.user_credit:.2f}'''
            
            return message
        
        ## THE COFFEE CAN BE BREWED
        # add the current transaction money to the machine credit
        self.machine_credit += coffee.price

        ## BREW THE COFFEE
        self._brew_drink(coffee)

        ## RETURN CHANGE, IF ANY
        change = self.return_change(coffee)

        message = f'\n\nEnjoy your {coffee.name}!\nHave a nice day and hope to see you soon!'
        
        if change > 0:
            message = f'\nHere is your change: ${change:.2f}' + message
        
        return message
    
    def refill_resources(self):
        """Refill the machine's resources to the specified amounts."""
        for k,v in self.max_resources.items():
            self.resources[k] = v

        return "Machine resources have been refilled."
