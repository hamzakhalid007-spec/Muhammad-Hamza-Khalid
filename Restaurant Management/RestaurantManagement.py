# Define menu
menu = {
    'Pizza': 500,
    'Pasta': 400,
    'Burger': 350,
    'Salad': 250,
    'Coffee': 150,
}

# Greet
print("Welcome to PYTHON Restaurant")
print("Pizza: 500\nPasta: 400\nBurger: 350\nSalad: 250\nCoffee: 150")
order_total = 0

while True:
    item = input("Enter the name of the item you want to order: ")
    
    if item in menu:
        order_total += menu[item]
        print(f"Your item {item} has been added to your order.")
    else:
        print(f"Ordered item {item} is not available yet.")
    
    another_order = input("Do you want to order something else? (Yes/No) ")
    
    if another_order.lower() != 'yes':
        break

print(f"The total amount to pay is {order_total}.")