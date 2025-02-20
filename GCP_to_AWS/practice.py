class Restaurant:
    def __init__(self,restaurant_name,location):
        self.restaurant_name=restaurant_name
        self.location = location
        self.menu=[]

        def add_menu_item(self,item):
            self.menu.append(item)

class MenuItem:
    def __init__(self,name,price,prep_time):
        self.name = name
        self.price = price
        self.prep_time = prep_time

class Customer:
    def __init__(self,name,email):
        self.name=name
        self.email=email


class Order:
    def __init__(self,order_id,restaurant,customer):
        self.order_id=order_id
        self.restaurant = restaurant
        self.customer = customer
        self.items = []
        self.status='pending'
    def add_item(self,item):
        self.items.append(item)
    def calculate_total(self):
        subtotal = sum(item.price for item in self.items)
        tax=subtotal*0.10
        delivery_fee = 5
        return subtotal+tax+delivery_fee
        




class DeliveryAgent:
    def __init__(self,agent_id,name):
        self.agent_id = agent_id
        self.name= name
        self.is_available = True

        
